"""
Refactored Team Builder - Uses SOLID principles with specialized components.
"""

import logging
from typing import Dict, List, Optional, Any, Callable

from ..tools import KnowledgeQueryTool, ToolManager
from ..core.team import Team
from .runner import TeamRunner

# Import new specialized components
from .config import ConfigLoader, EnvironmentVariableSubstitutor, ConfigValidator
from .mcp import MCPServerFactory, MCPConnectionManager, MCPServerRegistry
from .knowledge import KnowledgeLoader, KnowledgeRegistry
from .agents import AgentFactory, ToolResolver, HandoffConfigurator


class TeamBuilder:
    """Refactored team builder following SOLID principles."""
    
    def __init__(
        self, 
        api_key: str = None, 
        model: str = "gpt-4o", 
        temperature: float = 1,
        session_id: str = None,
        progress_callback=None
    ):
        """
        Initialize the team builder with default configuration.
        
        Args:
            api_key: OpenAI API key (optional, will use environment variable if not provided)
            model: Default model to use for agents
            temperature: Default temperature for agents
            session_id: Session ID for context propagation to agents and tools
            progress_callback: Optional callback for progress updates during streaming
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.session_id = session_id
        self.progress_callback = progress_callback
        self.logger = logging.getLogger(__name__)
        
        # Initialize specialized components
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all specialized components following dependency injection."""
        # Configuration components
        self.env_substitutor = EnvironmentVariableSubstitutor()
        self.config_validator = ConfigValidator()
        self.config_loader = ConfigLoader(self.env_substitutor, self.config_validator)
        
        # MCP components
        self.server_factory = MCPServerFactory()
        self.connection_manager = MCPConnectionManager(self.server_factory)
        self.mcp_registry = MCPServerRegistry()
        
        # Knowledge components
        self.knowledge_registry = KnowledgeRegistry()
        self.knowledge_loader = KnowledgeLoader(self.knowledge_registry, self.progress_callback)
        
        # Tool management
        self.tool_manager = None
        
        # Agent building components (initialized after tool manager)
        self.tool_resolver = None
        self.agent_factory = None
        self.handoff_configurator = HandoffConfigurator()
        
        # Team state
        self.team_config: Dict[str, Any] = {}
    
    def _ensure_tool_manager(self):
        """Ensure tool manager is initialized."""
        if self.tool_manager is None:
            self.knowledge_loader.ensure_knowledge_manager()
            self.tool_manager = ToolManager()
    
    def _ensure_agent_components(self):
        """Ensure agent building components are initialized."""
        if self.tool_resolver is None:
            self._ensure_tool_manager()
            self.tool_resolver = ToolResolver(
                self.tool_manager, 
                self.knowledge_loader.knowledge_manager,
                self.session_id
            )
            
        if self.agent_factory is None:
            self.agent_factory = AgentFactory(
                self.tool_resolver,
                self.mcp_registry,
                self.model,
                self.temperature,
                self.session_id
            )
    
    def load_team_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load team configuration from YAML file.
        
        Args:
            config_path: Path to the YAML configuration file
            
        Returns:
            Team configuration dictionary
        """
        return self.config_loader.load_team_config(config_path)
    
    async def build_team(
        self, 
        config_path: str, 
        debug: bool = False, 
        token_callback: Optional[Callable] = None
    ) -> Team:
        """
        Build a complete team from YAML configuration.
        
        Args:
            config_path: Path to the YAML configuration file
            debug: Whether to show debug information
            token_callback: Optional callback function to report token usage
            
        Returns:
            Team object containing orchestrator and worker agents
        """
        # Load and validate configuration
        config = self.load_team_config(config_path)
        self.team_config = config
        
        if debug:
            self.logger.debug(f"Team config after env substitution: {config}")
        
        # Initialize components that depend on configuration
        self._ensure_agent_components()
        
        # Load knowledge bases
        await self._load_knowledge_bases(config)
        
        # Load and register tools
        await self._load_tools(config)
        
        # Create and connect MCP servers
        mcp_servers = await self._setup_mcp_servers(config)
        
        # Register knowledge query tool if needed
        self._register_knowledge_tool(config)
        
        # Build all agents
        all_agents = await self._build_all_agents(config, token_callback)
        
        # Configure handoffs between agents
        self.handoff_configurator.configure_handoffs(all_agents)
        
        # Create team object
        team = self._create_team(config, all_agents)
        
        # Set up team dependencies for delegation tools
        await self._setup_team_dependencies(team, all_agents)
        
        return team
    
    async def _load_knowledge_bases(self, config: Dict[str, Any]):
        """Load knowledge bases from configuration."""
        if 'knowledge' in config:
            await self.knowledge_loader.load_knowledge_bases(config['knowledge'])
    
    async def _load_tools(self, config: Dict[str, Any]):
        """Load and register tools from configuration."""
        self._ensure_tool_manager()
        if 'tools' in config:
            self.logger.debug(f"Loading tools from config: {[tool.get('name') for tool in config['tools']]}")
            self.tool_manager.load_tools_from_config(config, team_config=config)
            self.logger.debug(f"Available tools after loading: {list(self.tool_manager.list_available_tools().keys())}")
        else:
            self.logger.debug("No tools section found in config")
    
    async def _setup_mcp_servers(self, config: Dict[str, Any]) -> List[Any]:
        """Set up MCP servers from configuration."""
        mcp_servers = []
        if 'tools' in config:
            mcp_servers = await self.connection_manager.create_and_connect_servers(config['tools'])
            self.mcp_registry.register_servers(mcp_servers, config['tools'])
        return mcp_servers
    
    def _register_knowledge_tool(self, config: Dict[str, Any]):
        """Register knowledge query tool if knowledge bases are defined."""
        if ('knowledge' in config and 
            self.knowledge_loader.knowledge_manager is not None):
            
            knowledge_tool = KnowledgeQueryTool(
                knowledge_manager=self.knowledge_loader.knowledge_manager
            )
            self.tool_manager.registry.register(
                knowledge_tool, 
                {'name': 'knowledge_query'}
            )
            self.logger.debug("Registered OpenAI-compatible knowledge_query tool")
    
    async def _build_all_agents(
        self, 
        config: Dict[str, Any], 
        token_callback: Optional[Callable]
    ) -> Dict[str, Dict[str, Any]]:
        """Build all agents from configuration."""
        all_agents = {}
        agent_id_to_name = {}
        
        for agent_config in config['agents']:
            agent_info = self._build_single_agent(agent_config, config, token_callback)
            
            name = agent_config['name']
            agent_id = agent_config.get('id')
            
            all_agents[name] = agent_info
            
            # Store ID-to-name mapping if ID is present
            if agent_id:
                agent_id_to_name[agent_id] = name
                self.logger.debug(f"Mapped agent ID '{agent_id}' to name '{name}'")
        
        # Store for team creation
        self.agent_id_to_name = agent_id_to_name
        return all_agents
    
    def _build_single_agent(
        self, 
        agent_config: Dict[str, Any], 
        team_config: Dict[str, Any], 
        token_callback: Optional[Callable]
    ) -> Dict[str, Any]:
        """Build a single agent from configuration."""
        name = agent_config['name']
        instructions = agent_config['instructions']
        is_orchestrator = agent_config.get('orchestrator', False)
        
        self.logger.debug(f"Building agent '{name}'")
        
        # Create the agent using the factory
        agent = self.agent_factory.create_agent(
            name=name,
            instructions=instructions,
            is_orchestrator=is_orchestrator,
            team_config=team_config,
            agent_config=agent_config,
            token_callback=token_callback
        )
        
        return {
            'agent': agent,
            'config': agent_config,
            'is_orchestrator': is_orchestrator
        }
    
    def _create_team(
        self, 
        config: Dict[str, Any], 
        all_agents: Dict[str, Dict[str, Any]]
    ) -> Team:
        """Create team object from agents."""
        orchestrator = None
        workers = {}
        
        # Separate orchestrator from workers
        for name, agent_info in all_agents.items():
            if agent_info['is_orchestrator']:
                orchestrator = agent_info['agent']
            else:
                workers[name] = agent_info['agent']
        
        # Use first agent as orchestrator if none specified
        if orchestrator is None and workers:
            first_agent_name = list(workers.keys())[0]
            orchestrator = workers.pop(first_agent_name)
            self.logger.warning(f"No orchestrator found, using '{first_agent_name}' as orchestrator")
        
        if orchestrator is None:
            raise ValueError("No agents found in team configuration")
        
        # Create team
        max_turns = config.get('config', {}).get('max_turns')
        team = Team(
            orchestrator, 
            workers, 
            name=config.get('name'), 
            max_turns=max_turns, 
            agent_id_to_name=getattr(self, 'agent_id_to_name', {}),
            original_config=config
        )
        
        return team
    
    async def _setup_team_dependencies(
        self, 
        team: Team, 
        all_agents: Dict[str, Dict[str, Any]]
    ):
        """Set up team dependencies for delegate_agent tools."""
        # Check if any agent has delegation
        has_delegation = any(
            "delegate_agent" in agent_info['config'].get('tools', [])
            for agent_info in all_agents.values()
        )
        
        if has_delegation:
            team_runner = TeamRunner(team)
            
            # Set up individual delegate tool instances
            delegate_tools = self.agent_factory.get_delegate_tools()
            for agent_name, delegate_tool in delegate_tools.items():
                delegate_tool.set_team_dependencies(team, team_runner)
                self.logger.debug(f"Set up team dependencies for delegate tool in agent '{agent_name}'")
            
            # Legacy dependencies no longer needed - TeamContext provides access to original_config
    
    async def cleanup_mcp_servers(self):
        """Clean up MCP server connections."""
        if hasattr(self.mcp_registry, 'servers') and self.mcp_registry.servers:
            await self.connection_manager.cleanup_servers(self.mcp_registry.servers)