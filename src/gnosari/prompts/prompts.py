"""Core prompt building functions and constants for the Gnosari framework."""

from typing import Dict, List, Any
from .tool_prompts import get_tools_definition


def build_agent_system_prompt(name: str, instructions: str, agent_tools: List[str] = None, tool_manager = None, agent_config: Dict[str, Any] = None, knowledge_descriptions: Dict[str, str] = None, team_config: Dict[str, Any] = None, real_tool_info: List[Dict] = None) -> Dict[str, List[str]]:
    """Build system prompt components for any agent (orchestrator or specialized).
    
    Args:
        name: Agent name
        instructions: Agent instructions  
        agent_tools: List of tool names for this agent
        tool_manager: Tool manager instance for getting tool descriptions
        agent_config: Agent configuration dictionary
        knowledge_descriptions: Dictionary mapping knowledge base names to descriptions
        team_config: Team configuration dictionary (for orchestrators)
        
    Returns:
        Dictionary with 'background', 'steps', and 'output_instructions' lists
    """
    # Load tool definitions if tool_manager is provided
    if tool_manager and team_config and 'tools' in team_config:
        tool_manager.load_tools_from_config(team_config)
    
    background = [
        f"# {name}",
        "",
        instructions,
        "",
    ]
    
    # Add collaboration mechanisms if configured
    has_delegation = agent_config and 'delegation' in agent_config and agent_config['delegation']
    has_handoffs = agent_config and 'can_transfer_to' in agent_config and agent_config['can_transfer_to']
    
    if has_delegation or has_handoffs:
        background.append("## Team Collaboration")
        mechanisms = []
        if has_delegation:
            mechanisms.append("**delegate_agent tool** for task delegation")
        if has_handoffs:
            mechanisms.append("**handoffs** to transfer conversation control")
        background.append(f"Use {' and '.join(mechanisms)}.")
        background.append("")
        
        # Add specific delegation instructions
        if has_delegation:
            delegation_config = agent_config['delegation']
            background.append("### Delegation Instructions")
            for del_config in delegation_config:
                if isinstance(del_config, dict) and del_config.get('agent') and del_config.get('instructions'):
                    background.append(f"- **{del_config['agent']}**: {del_config['instructions']}")
            background.append("")
        
        # Add specific handoff instructions  
        if has_handoffs:
            can_transfer_to = agent_config['can_transfer_to']
            background.append("### Handoff Instructions")
            for transfer_config in can_transfer_to:
                if isinstance(transfer_config, dict) and transfer_config.get('agent') and transfer_config.get('instructions'):
                    background.append(f"- **{transfer_config['agent']}**: {transfer_config['instructions']}")
            background.append("")

    # Add knowledge base access if configured
    if agent_config and 'knowledge' in agent_config and agent_config['knowledge']:
        knowledge_names = agent_config['knowledge']
        background.append("## Available Knowledge Bases")
        for kb_name in knowledge_names:
            description = knowledge_descriptions.get(kb_name, "") if knowledge_descriptions else ""
            kb_info = f"- **{kb_name}**"
            if description:
                kb_info += f": {description}"
            background.append(kb_info)
        background.append("")
        background.append("**Important**: Use the `knowledge_query` tool with exact knowledge base names. Always search knowledge before responding.")
        background.append("")
    
    # Add tool information using real tool info if available
    tool_sections = get_tools_definition(agent_tools, tool_manager, real_tool_info)
    if tool_sections:
        background.extend(tool_sections)
    
    return {
        "background": background,
        "steps": [],
        "output_instructions": ["Use available tools as needed to fulfill requests."]
    }


