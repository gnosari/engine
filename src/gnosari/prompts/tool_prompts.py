"""Tool prompt generation for agent system prompts."""

from typing import List, Dict, Any


def get_tools_definition(agent_tools: List[str], tool_manager) -> List[str]:
    """Generate tool definitions for system prompt injection.
    
    Args:
        agent_tools: List of tool names for the agent
        tool_manager: Tool manager instance for getting tool information
        
    Returns:
        List of strings containing tool definitions and usage instructions
    """
    if not agent_tools or not tool_manager:
        return []
    
    tool_sections = []
    tool_descriptions = []
    
    # Add tool descriptions
    for tool_name in agent_tools:
        try:
            # Get tool instance and config from registry
            tool_instance = tool_manager.get_tool(tool_name)
            tool_config = tool_manager.registry.get_config(tool_name)
            
            if tool_instance and tool_config:
                # Get tool information from config and instance
                tool_id = tool_config.get('id', tool_name)
                tool_display_name = tool_config.get('name', tool_name)
                tool_description = tool_config.get('description', tool_instance.description)
                
                # Format as markdown list item
                tool_info = f"- **{tool_display_name}** (`{tool_id}`): {tool_description}"
                tool_descriptions.append(tool_info)
            else:
                # Fallback if tool not found in registry
                tool_descriptions.append(f"- **{tool_name}**: Tool information unavailable")
                
        except Exception as e:
            # If tool loading fails, add a placeholder
            tool_descriptions.append(f"- **{tool_name}**: Tool information unavailable")

    if tool_descriptions:
        tool_sections.append("## Available Tools")
        tool_sections.extend(tool_descriptions)
        tool_sections.append("")

    return tool_sections



