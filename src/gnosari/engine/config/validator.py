"""Configuration validation functionality."""

import logging
from typing import Dict, Any, List


class ConfigValidator:
    """Validates team configuration structure and content."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate_team_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate team configuration structure.
        
        Args:
            config: Team configuration dictionary
            
        Returns:
            True if valid, raises ValueError if invalid
        """
        if 'agents' not in config:
            raise ValueError("Team configuration must contain 'agents' section")
        
        agents = config['agents']
        if not isinstance(agents, list) or len(agents) == 0:
            raise ValueError("Team configuration must have at least one agent")
        
        # Validate each agent
        for i, agent in enumerate(agents):
            self._validate_agent_config(agent, i)
        
        # Validate handoff references
        self._validate_handoff_references(config)
        
        return True
    
    def _validate_agent_config(self, agent: Dict[str, Any], index: int) -> None:
        """Validate individual agent configuration."""
        if 'name' not in agent:
            raise ValueError(f"Agent at index {index} must have a 'name' field")
        
        if 'instructions' not in agent:
            raise ValueError(f"Agent '{agent.get('name', f'at index {index}')}' must have 'instructions' field")
        
        # Validate tools if present
        if 'tools' in agent and not isinstance(agent['tools'], list):
            raise ValueError(f"Agent '{agent['name']}' tools must be a list")
        
        # Validate knowledge if present
        if 'knowledge' in agent and not isinstance(agent['knowledge'], list):
            raise ValueError(f"Agent '{agent['name']}' knowledge must be a list")
    
    def _validate_handoff_references(self, config: Dict[str, Any]) -> None:
        """Validate that handoff references point to existing agents."""
        agent_names = {agent['name'] for agent in config['agents']}
        
        for agent in config['agents']:
            can_transfer_to = agent.get('can_transfer_to', [])
            for transfer_config in can_transfer_to:
                if isinstance(transfer_config, str):
                    target_name = transfer_config
                elif isinstance(transfer_config, dict):
                    target_name = transfer_config.get('agent')
                else:
                    continue
                
                if target_name and target_name not in agent_names:
                    self.logger.warning(
                        f"Agent '{agent['name']}' references non-existent agent '{target_name}' in can_transfer_to"
                    )