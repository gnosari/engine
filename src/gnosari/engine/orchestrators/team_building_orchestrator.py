"""
Team Building Orchestrator - Coordinates the entire team building process following SRP.
"""

import logging
from typing import Dict, List, Any, Optional, Callable

from ...core.team import Team
from ...tools import KnowledgeQueryTool
from ..config.team_configuration_manager import TeamConfigurationManager, TeamConfig
from ..factories.component_factory import ComponentRegistry
from ..factories.team_factory import TeamFactory
from ..runner import TeamRunner
from ..exceptions import (
    TeamBuildingError, 
    ComponentInitializationError, 
    KnowledgeLoadingError,
    ToolRegistrationError,
    MCPConnectionError
)


class TeamBuildingOrchestrator:
    """
    Orchestrates the complete team building process.
    Follows Single Responsibility Principle by coordinating without doing the work itself.
    """
    
    def __init__(
        self,
        config_manager: TeamConfigurationManager,
        component_registry: ComponentRegistry
    ):
        """
        Initialize orchestrator with required dependencies.
        
        Args:
            config_manager: Manages team configuration loading and validation
            component_registry: Registry for managing component instances
        """
        self.config_manager = config_manager
        self.component_registry = component_registry
        self.logger = logging.getLogger(__name__)
    
    async def build_team(
        self,
        config_path: str,
        api_key: Optional[str] = None,
        model: str = "gpt-4o",
        temperature: float = 1.0,
        session_id: Optional[str] = None,
        debug: bool = False,
        token_callback: Optional[Callable] = None
    ) -> Team:
        """
        Build a complete team from YAML configuration.
        
        Args:
            config_path: Path to the YAML configuration file
            api_key: OpenAI API key (optional)
            model: Default model for agents
            temperature: Default temperature for agents
            session_id: Session ID for context propagation
            debug: Whether to show debug information
            token_callback: Optional callback for token usage reporting
            
        Returns:
            Team: Fully configured team ready for execution
            
        Raises:
            ValueError: If team building fails
        """
        try:
            # Phase 1: Load and validate configuration
            config = await self._load_configuration(config_path, debug)
            
            # Phase 2: Initialize all components
            components = await self._initialize_components(config, model, temperature, session_id)
            
            # Phase 3: Set up knowledge and tools
            await self._setup_knowledge_and_tools(config, components)
            
            # Phase 4: Create team
            team = await self._create_team(config, components, token_callback)
            
            # Phase 5: Set up team dependencies
            await self._setup_team_dependencies(team, components)
            
            self.logger.info(f"Successfully built team '{team.name}' from {config_path}")
            return team
            
        except TeamBuildingError:
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            self.logger.error(f"Team building failed: {e}")
            raise TeamBuildingError(f"Failed to build team from {config_path}: {e}") from e
    
    async def _load_configuration(self, config_path: str, debug: bool) -> TeamConfig:
        """Load and validate team configuration."""
        config = self.config_manager.load_team_config(config_path)
        
        if debug:
            self.logger.debug(f"Team config after env substitution: {config.raw_config}")
        
        return config
    
    async def _initialize_components(
        self,
        config: TeamConfig,
        model: str,
        temperature: float,
        session_id: Optional[str]
    ) -> Dict[str, Any]:
        """Initialize all required components."""
        try:
            # Get component instances from registry
            mcp_components = self.component_registry.get_or_create_mcp_components()
            knowledge_components = self.component_registry.get_or_create_knowledge_components()
            tool_manager = self.component_registry.get_or_create_tool_manager()
            agent_components = self.component_registry.get_or_create_agent_components(
                model, temperature, session_id
            )
            
            # Unpack components
            server_factory, connection_manager, mcp_registry = mcp_components
            knowledge_registry, knowledge_loader = knowledge_components
            tool_resolver, agent_factory, handoff_configurator = agent_components
            
            self.logger.debug("Successfully initialized all components")
            
            return {
                'server_factory': server_factory,
                'connection_manager': connection_manager,
                'mcp_registry': mcp_registry,
                'knowledge_registry': knowledge_registry,
                'knowledge_loader': knowledge_loader,
                'tool_manager': tool_manager,
                'tool_resolver': tool_resolver,
                'agent_factory': agent_factory,
                'handoff_configurator': handoff_configurator
            }
        except Exception as e:
            self.logger.error(f"Component initialization failed: {e}")
            raise ComponentInitializationError(f"Failed to initialize components: {e}") from e
    
    async def _setup_knowledge_and_tools(self, config: TeamConfig, components: Dict[str, Any]):
        """Set up knowledge bases and tools."""
        try:
            # Load knowledge bases
            if self.config_manager.has_knowledge_bases(config):
                try:
                    await components['knowledge_loader'].load_knowledge_bases(config.knowledge)
                    self.logger.debug(f"Loaded {len(config.knowledge)} knowledge bases")
                except Exception as e:
                    raise KnowledgeLoadingError(f"Failed to load knowledge bases: {e}") from e
            
            # Load and register tools
            if self.config_manager.has_tools(config):
                try:
                    self.logger.debug(f"Loading tools from config: {[tool.get('name') for tool in config.tools]}")
                    components['tool_manager'].load_tools_from_config(config.raw_config, team_config=config.raw_config)
                    self.logger.debug(f"Available tools after loading: {list(components['tool_manager'].list_available_tools().keys())}")
                except Exception as e:
                    raise ToolRegistrationError(f"Failed to load tools: {e}") from e
            
            # Set up MCP servers
            mcp_servers = []
            if self.config_manager.has_tools(config):
                try:
                    mcp_servers = await components['connection_manager'].create_and_connect_servers(config.tools)
                    components['mcp_registry'].register_servers(mcp_servers, config.tools)
                    self.logger.debug(f"Connected to {len(mcp_servers)} MCP servers")
                except Exception as e:
                    raise MCPConnectionError(f"Failed to connect to MCP servers: {e}") from e
            
            # Register knowledge query tool if needed
            if (self.config_manager.has_knowledge_bases(config) and 
                components['knowledge_loader'].knowledge_manager is not None):
                try:
                    knowledge_tool = KnowledgeQueryTool(
                        knowledge_manager=components['knowledge_loader'].knowledge_manager
                    )
                    components['tool_manager'].registry.register(
                        knowledge_tool, 
                        {'name': 'knowledge_query'}
                    )
                    self.logger.debug("Registered OpenAI-compatible knowledge_query tool")
                except Exception as e:
                    raise ToolRegistrationError(f"Failed to register knowledge query tool: {e}") from e
                    
        except (KnowledgeLoadingError, ToolRegistrationError, MCPConnectionError):
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            self.logger.error(f"Failed to setup knowledge and tools: {e}")
            raise TeamBuildingError(f"Failed to setup knowledge and tools: {e}") from e
    
    async def _create_team(
        self,
        config: TeamConfig,
        components: Dict[str, Any],
        token_callback: Optional[Callable]
    ) -> Team:
        """Create team using TeamFactory."""
        team_factory = TeamFactory(
            components['agent_factory'],
            components['handoff_configurator']
        )
        
        return await team_factory.create_team(config, token_callback)
    
    async def _setup_team_dependencies(self, team: Team, components: Dict[str, Any]):
        """Set up team dependencies for delegate_agent tools."""
        # Check if any agent has delegation
        has_delegation = any(
            "delegate_agent" in agent_info['config'].get('tools', [])
            for agent_info in team.all_agents.values()
            if hasattr(agent_info, 'get')  # Safety check
        )
        
        if has_delegation:
            team_runner = TeamRunner(team)
            
            # Set up individual delegate tool instances
            delegate_tools = components['agent_factory'].get_delegate_tools()
            for agent_name, delegate_tool in delegate_tools.items():
                delegate_tool.set_team_dependencies(team, team_runner)
                self.logger.debug(f"Set up team dependencies for delegate tool in agent '{agent_name}'")
    
    async def cleanup(self):
        """Clean up resources used during team building."""
        try:
            # Clean up MCP server connections
            mcp_components = self.component_registry.get_or_create_mcp_components()
            _, connection_manager, mcp_registry = mcp_components
            
            if hasattr(mcp_registry, 'servers') and mcp_registry.servers:
                await connection_manager.cleanup_servers(mcp_registry.servers)
                self.logger.debug("Cleaned up MCP server connections")
            
            # Clear component registry
            self.component_registry.clear()
            self.logger.debug("Cleared component registry")
            
        except Exception as e:
            self.logger.warning(f"Error during cleanup: {e}")