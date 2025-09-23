from __future__ import annotations

# Suppress warnings before any imports
import warnings
import os
warnings.filterwarnings("ignore", category=DeprecationWarning) 
warnings.filterwarnings("ignore", message=".*deprecated.*")
warnings.filterwarnings("ignore", message=".*Support for class-based.*")
os.environ["PYTHONWARNINGS"] = "ignore::DeprecationWarning"

import argparse
import asyncio
import json
import logging
import sys
from datetime import datetime
from typing import NoReturn
from pathlib import Path
import aiohttp
import yaml

from dotenv import load_dotenv
from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.syntax import Syntax

from .engine.builder import TeamBuilder
from .engine.runner import TeamRunner
from .prompts.prompts import build_orchestrator_system_prompt, build_specialized_agent_system_prompt


async def push_team_config(config_path: str, api_url: str = None):
    """Push a team configuration YAML file to the Gnosari API."""
    console = Console()
    logger = logging.getLogger(__name__)
    
    # Default API URL if not provided
    if not api_url:
        api_url = os.getenv("GNOSARI_API_URL", "https://api.gnosari.com")
    
    # Ensure the API URL ends with the correct endpoint
    if not api_url.endswith("/api/v1/teams/push"):
        # Only add endpoint if it's a base URL (no path after domain)
        from urllib.parse import urlparse
        parsed = urlparse(api_url)
        if parsed.path in ['', '/']:
            api_url = api_url.rstrip("/") + "/api/v1/teams/push"
    
    try:
        # Read and parse YAML file
        config_file = Path(config_path)
        if not config_file.exists():
            console.print(f"[red]Error: Configuration file '{config_path}' not found[/red]")
            return False
        
        with open(config_file, 'r', encoding='utf-8') as f:
            yaml_content = yaml.safe_load(f)
        
        # Validate required fields
        if not yaml_content.get('name'):
            console.print(f"[red]Error: 'name' field is required in the team configuration[/red]")
            return False
        
        if not yaml_content.get('id'):
            console.print(f"[red]Error: 'id' field is required in the team configuration[/red]")
            return False
        
        console.print(f"[blue]Loading team configuration from:[/blue] {config_path}")
        console.print(f"[blue]Team name:[/blue] {yaml_content.get('name')}")
        console.print(f"[blue]Team ID:[/blue] {yaml_content.get('id')}")
        console.print(f"[blue]Pushing to API:[/blue] {api_url}")
        
        # Convert YAML to JSON for API
        json_payload = json.dumps(yaml_content, indent=2)
        
        # Make HTTP request
        async with aiohttp.ClientSession() as session:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            # Add authentication header if API key is available
            api_key = os.getenv("GNOSARI_API_KEY")
            if api_key:
                headers['X-Auth-Token'] = api_key
            else:
                console.print("[yellow]Warning: GNOSARI_API_KEY not found in environment variables[/yellow]")
            
            console.print("🚀 [yellow]Pushing team configuration...[/yellow]")
            
            # Debug logging of the request
            logger.debug(f"Making HTTP POST request to: {api_url}")
            logger.debug(f"Request headers: {dict(headers)}")
            logger.debug(f"Request payload: {json_payload}")
            
            async with session.post(api_url, data=json_payload, headers=headers) as response:
                response_text = await response.text()
                
                # Debug logging of the response
                logger.debug(f"Response status: {response.status}")
                logger.debug(f"Response headers: {dict(response.headers)}")
                logger.debug(f"Response body: {response_text}")
                
                if response.status == 200 or response.status == 201:
                    console.print("✅ [green]Team configuration pushed successfully![/green]")
                    
                    # Try to parse response as JSON for additional info
                    try:
                        response_data = json.loads(response_text)
                        if isinstance(response_data, dict):
                            if 'id' in response_data:
                                console.print(f"[green]Team ID:[/green] {response_data['id']}")
                            if 'message' in response_data:
                                console.print(f"[green]Message:[/green] {response_data['message']}")
                    except json.JSONDecodeError:
                        pass
                    
                    return True
                else:
                    console.print(f"[red]Error: API returned status {response.status}[/red]")
                    console.print(f"[red]Response:[/red] {response_text}")
                    return False
                    
    except yaml.YAMLError as e:
        console.print(f"[red]Error parsing YAML file: {e}[/red]")
        return False
    except aiohttp.ClientError as e:
        console.print(f"[red]Error connecting to API: {e}[/red]")
        return False
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        return False


async def pull_team_config(team_identifier: str, api_url: str = None):
    """Pull a team configuration from the Gnosari API and save as YAML file."""
    console = Console()
    logger = logging.getLogger(__name__)
    
    # Default API URL if not provided
    if not api_url:
        api_url = os.getenv("GNOSARI_API_URL", "https://api.gnosari.com")
    
    # Build the pull endpoint URL
    from urllib.parse import urlparse
    parsed = urlparse(api_url)
    if parsed.path in ['', '/']:
        api_url = api_url.rstrip("/") + f"/api/v1/teams/{team_identifier}/pull"
    else:
        # If API URL already has a path, assume it's the base and append the endpoint
        if not api_url.endswith(f"/api/v1/teams/{team_identifier}/pull"):
            api_url = api_url.rstrip("/") + f"/api/v1/teams/{team_identifier}/pull"
    
    try:
        console.print(f"[blue]Pulling team configuration for:[/blue] {team_identifier}")
        console.print(f"[blue]From API:[/blue] {api_url}")
        
        # Make HTTP request
        async with aiohttp.ClientSession() as session:
            headers = {
                'Accept': 'application/json'
            }
            
            # Add authentication header if API key is available
            api_key = os.getenv("GNOSARI_API_KEY")
            if api_key:
                headers['X-Auth-Token'] = api_key
            else:
                console.print("[yellow]Warning: GNOSARI_API_KEY not found in environment variables[/yellow]")
            
            console.print("📥 [yellow]Pulling team configuration...[/yellow]")
            
            # Debug logging of the request
            logger.debug(f"Making HTTP GET request to: {api_url}")
            logger.debug(f"Request headers: {dict(headers)}")
            
            async with session.get(api_url, headers=headers) as response:
                response_text = await response.text()
                
                # Debug logging of the response
                logger.debug(f"Response status: {response.status}")
                logger.debug(f"Response headers: {dict(response.headers)}")
                logger.debug(f"Response body: {response_text}")
                
                if response.status == 200:
                    # Parse JSON response
                    try:
                        team_data = json.loads(response_text)
                        
                        # Transform JSON to proper YAML structure
                        yaml_config = _transform_json_to_yaml(team_data)
                        
                        # Create output filename
                        output_filename = f"{team_identifier}.yaml"
                        output_path = Path(output_filename)
                        
                        # Convert to YAML and save with proper formatting
                        with open(output_path, 'w', encoding='utf-8') as f:
                            yaml.dump(yaml_config, f, default_flow_style=False, sort_keys=False, indent=2, allow_unicode=True)
                        
                        console.print("✅ [green]Team configuration pulled successfully![/green]")
                        console.print(f"[green]Team name:[/green] {yaml_config.get('name', 'Unknown')}")
                        console.print(f"[green]Team ID:[/green] {yaml_config.get('id', team_identifier)}")
                        console.print(f"[green]Saved to:[/green] {output_path.absolute()}")
                        
                        return True
                        
                    except json.JSONDecodeError as e:
                        console.print(f"[red]Error parsing JSON response: {e}[/red]")
                        return False
                        
                elif response.status == 404:
                    console.print(f"[red]Error: Team '{team_identifier}' not found[/red]")
                    return False
                elif response.status == 401:
                    console.print("[red]Error: Unauthorized. Check your GNOSARI_API_KEY[/red]")
                    return False
                elif response.status == 403:
                    console.print("[red]Error: Forbidden. You don't have access to this team[/red]")
                    return False
                else:
                    console.print(f"[red]Error: API returned status {response.status}[/red]")
                    console.print(f"[red]Response:[/red] {response_text}")
                    return False
                    
    except aiohttp.ClientError as e:
        console.print(f"[red]Error connecting to API: {e}[/red]")
        return False
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        return False


def _transform_json_to_yaml(team_data: dict) -> dict:
    """Transform JSON team data to proper YAML structure."""
    yaml_config = {}
    
    # Basic team info
    if 'name' in team_data:
        yaml_config['name'] = team_data['name']
    if 'id' in team_data:
        yaml_config['id'] = team_data['id']
    if 'description' in team_data:
        yaml_config['description'] = team_data['description']
    
    # Team configuration settings
    if 'config' in team_data:
        yaml_config['config'] = team_data['config']
    
    # Knowledge bases
    if 'knowledge' in team_data and team_data['knowledge']:
        yaml_config['knowledge'] = []
        for kb in team_data['knowledge']:
            kb_config = {}
            if 'id' in kb:
                kb_config['id'] = kb['id']
            if 'name' in kb:
                kb_config['name'] = kb['name']
            if 'description' in kb:
                kb_config['description'] = kb['description']
            if 'type' in kb:
                kb_config['type'] = kb['type']
            if 'config' in kb:
                kb_config['config'] = kb['config']
            if 'data' in kb:
                kb_config['data'] = kb['data']
            yaml_config['knowledge'].append(kb_config)
    
    # Tools
    if 'tools' in team_data and team_data['tools']:
        yaml_config['tools'] = []
        for tool in team_data['tools']:
            tool_config = {}
            if 'name' in tool:
                tool_config['name'] = tool['name']
            if 'id' in tool:
                tool_config['id'] = tool['id']
            if 'description' in tool:
                tool_config['description'] = tool['description']
            if 'module' in tool:
                tool_config['module'] = tool['module']
            if 'class' in tool:
                tool_config['class'] = tool['class']
            if 'args' in tool:
                tool_config['args'] = tool['args']
            if 'url' in tool:  # MCP server tool
                tool_config['url'] = tool['url']
            if 'command' in tool:  # MCP server tool
                tool_config['command'] = tool['command']
            yaml_config['tools'].append(tool_config)
    
    # Agents
    if 'agents' in team_data and team_data['agents']:
        yaml_config['agents'] = []
        for agent in team_data['agents']:
            agent_config = {}
            if 'name' in agent:
                agent_config['name'] = agent['name']
            if 'id' in agent:
                agent_config['id'] = agent['id']
            if 'description' in agent:
                agent_config['description'] = agent['description']
            if 'instructions' in agent:
                agent_config['instructions'] = agent['instructions']
            if 'model' in agent:
                agent_config['model'] = agent['model']
            if 'temperature' in agent:
                agent_config['temperature'] = agent['temperature']
            if 'reasoning_effort' in agent:
                agent_config['reasoning_effort'] = agent['reasoning_effort']
            if 'orchestrator' in agent:
                agent_config['orchestrator'] = agent['orchestrator']
            if 'tools' in agent and agent['tools']:
                agent_config['tools'] = agent['tools']
            if 'knowledge' in agent and agent['knowledge']:
                agent_config['knowledge'] = agent['knowledge']
            if 'delegation' in agent and agent['delegation']:
                agent_config['delegation'] = agent['delegation']
            if 'can_transfer_to' in agent and agent['can_transfer_to']:
                agent_config['can_transfer_to'] = agent['can_transfer_to']
            if 'mcp_servers' in agent and agent['mcp_servers']:
                agent_config['mcp_servers'] = agent['mcp_servers']
            yaml_config['agents'].append(agent_config)
    
    return yaml_config


async def show_team_prompts(config_path: str, model: str = "gpt-4o", temperature: float = 1.0):
    """Display the generated system prompts for all agents in a team configuration."""
    console = Console()
    
    try:
        # Create team builder (no API key needed for prompt generation)
        builder = TeamBuilder(model=model, temperature=temperature)
        
        # Load team configuration
        config = builder.load_team_config(config_path)
        
        # Load knowledge bases if they exist
        if 'knowledge' in config:
            builder._load_knowledge_bases(config['knowledge'])
        
        # Load tools and register them
        builder._ensure_tool_manager()
        if 'tools' in config:
            builder.tool_manager.load_tools_from_config(config)
        
        console.print(f"\n[bold blue]Team Configuration:[/bold blue] {config_path}")
        console.print(f"[bold blue]Team Name:[/bold blue] {config.get('name', 'Unnamed Team')}")
        console.print(f"[bold blue]Description:[/bold blue] {config.get('description', 'No description')}\n")
        
        # Process each agent
        for agent_config in config['agents']:
            agent_name = agent_config['name']
            agent_instructions = agent_config['instructions']
            is_orchestrator = agent_config.get('orchestrator', False)
            agent_tools = agent_config.get('tools', [])
            
            # Generate system prompt
            if is_orchestrator:
                prompt_components = build_orchestrator_system_prompt(
                    agent_name, agent_instructions, config, agent_tools, 
                    builder.tool_manager, agent_config, builder.knowledge_descriptions
                )
                agent_type = "Orchestrator"
            else:
                prompt_components = build_specialized_agent_system_prompt(
                    agent_name, agent_instructions, agent_tools, 
                    builder.tool_manager, agent_config, builder.knowledge_descriptions
                )
                agent_type = "Specialized Agent"
            
            # Combine all prompt components
            full_prompt = f"{chr(10).join(prompt_components['background'])}\\n\\n{chr(10).join(prompt_components['steps'])}\\n\\n{chr(10).join(prompt_components['output_instructions'])}"
            
            # Display agent information
            console.print(f"[bold green]{'='*60}[/bold green]")
            console.print(f"[bold green]Agent:[/bold green] {agent_name} ({agent_type})")
            console.print(f"[bold green]Model:[/bold green] {agent_config.get('model', model)}")
            console.print(f"[bold green]Temperature:[/bold green] {agent_config.get('temperature', temperature)}")
            if agent_tools:
                console.print(f"[bold green]Tools:[/bold green] {', '.join(agent_tools)}")
            console.print(f"[bold green]{'='*60}[/bold green]")
            
            # Display the system prompt with syntax highlighting
            syntax = Syntax(full_prompt, "text", theme="monokai", line_numbers=False, word_wrap=True)
            console.print(syntax)
            console.print()
    
    except Exception as e:
        console.print(f"[red]Error displaying prompts: {e}[/red]")
        raise


async def run_single_agent_stream(executor: TeamRunner, agent_name: str, message: str, debug: bool = False, session_id: str = None, builder: 'TeamBuilder' = None):
    """Run single agent with streaming response using Rich console and provide execution summary."""
    console = Console()
    
    # Track execution steps for final summary
    execution_steps = []
    tools_used = set()
    final_response = ""
    current_agent_response = ""
    
    def add_step(step_type: str, details: str, timestamp: str = None):
        """Add a step to the execution tracking."""
        if timestamp is None:
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        execution_steps.append({
            "timestamp": timestamp,
            "type": step_type,
            "agent": agent_name,
            "details": details
        })
    
    # Clear screen and show header
    console.clear()
    console.print("🚀 [bold blue]GNOSARI SINGLE AGENT EXECUTION[/bold blue]", style="bold")
    console.print("=" * 80, style="dim")
    console.print(f"🤖 [blue]Agent:[/blue] {agent_name}")
    console.print(f"📝 [blue]Message:[/blue] {message}")
    console.print(f"🔗 [blue]Session:[/blue] {session_id}")
    console.print("=" * 80, style="dim")
    console.print()
    
    # Suppress ChromaDB warnings during execution
    import warnings
    warnings.filterwarnings("ignore", message=".*Add of existing embedding ID.*")
    warnings.filterwarnings("ignore", message=".*Accessing the 'model_fields' attribute.*")
    
    if debug:
        # For debug mode, print raw JSON output and formatted messages
        console.print("🐛 [bold red]DEBUG MODE[/bold red]", style="bold")
        console.print("─" * 80, style="dim")
        
        event_count = 0
        async for output in executor.run_single_agent_stream(agent_name, message, debug, session_id=session_id):
            event_count += 1
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            
            # Print event header
            console.print(f"\n📡 [bold cyan]EVENT #{event_count}[/bold cyan]", style="bold")
            console.print(f"⏰ [dim]{timestamp}[/dim]")
            
            # Print raw JSON for debugging
            json_output = json.dumps(output, indent=2, default=str)
            syntax = Syntax(json_output, "json", theme="monokai", line_numbers=False)
            console.print(syntax)
            
            # Show formatted output for readability
            event_type = output.get("type", "unknown")
            
            if event_type == "response":
                content = output.get('content', '')
                # Handle Rich Text objects
                if hasattr(content, 'plain'):
                    content_str = content.plain
                else:
                    content_str = str(content)
                console.print(f"💬 [bold green]RESPONSE[/bold green] from [bold]{agent_name}[/bold]: [green]{content_str}[/green]")
                current_agent_response += content_str
                if not hasattr(console, '_response_started'):
                    add_step("response", f"Started generating response", timestamp)
                    console._response_started = True
            elif event_type == "tool_call":
                tool_name = output.get("tool_name", output.get("name", "unknown"))
                tool_input = output.get("tool_input", output.get("input", {}))
                console.print(f"🔧 [bold yellow]TOOL CALL[/bold yellow] by [bold]{agent_name}[/bold]: [yellow]{tool_name}[/yellow]")
                console.print(f"📥 Input: [dim]{tool_input}[/dim]")
                add_step("tool_call", f"Called tool: {tool_name}", timestamp)
                tools_used.add(tool_name)
            elif event_type == "tool_result":
                content = output.get('content', '')
                preview = content[:200] + "..." if len(str(content)) > 200 else content
                console.print(f"🔨 [bold cyan]TOOL RESULT[/bold cyan] for [bold]{agent_name}[/bold]: [cyan]{preview}[/cyan]")
                add_step("tool_result", f"Tool result: {preview}", timestamp)
            elif event_type == "completion":
                content = output.get('content', '')
                console.print(f"✅ [bold green]COMPLETION[/bold green] from [bold]{agent_name}[/bold]: [green]{content}[/green]")
                add_step("completion", f"Completed execution", timestamp)
                final_response = current_agent_response
            elif event_type == "error":
                content = output.get('content', '')
                console.print(f"❌ [bold red]ERROR[/bold red]: [red]{content}[/red]")
                return
            elif output.get("is_done"):
                console.print(f"🎯 [bold green]DONE![/bold green] Agent execution completed.")
                break
            
            console.print("─" * 80, style="dim")
    else:
        # Use Live display for streaming response
        console.print("📡 [bold cyan]STREAMING RESPONSE[/bold cyan]", style="bold")
        console.print("─" * 80, style="dim")
        
        with Live("", refresh_per_second=10, auto_refresh=True) as live:
            live.update(Text.assemble(("⏳ Initializing...", "dim")))
            current_response = ""
            event_count = 0
            
            # Suppress logging during streaming
            import logging
            logging.getLogger().setLevel(logging.ERROR)
            
            async for output in executor.run_single_agent_stream(agent_name, message, debug, session_id=session_id):
                event_count += 1
                timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                event_type = output.get("type", "unknown")
                
                # Handle different output types
                if event_type == "response":
                    content = output.get("content", "")
                    # Handle Rich Text objects
                    if hasattr(content, 'plain'):
                        content_str = content.plain
                    else:
                        content_str = str(content)
                    current_response += content_str
                    current_agent_response += content_str
                    display_text = Text.assemble(
                        (f"[{agent_name}] ", "bold blue"), 
                        (current_response, "green")
                    )
                    live.update(display_text)
                    if not hasattr(live, '_response_started'):
                        add_step("response", f"Started generating response", timestamp)
                        live._response_started = True
                elif event_type == "tool_call":
                    tool_name = output.get("tool_name", output.get("name", "unknown"))
                    display_text = Text.assemble(
                        (f"[{agent_name}] ", "bold blue"),
                        (f"🔧 Calling {tool_name}...", "yellow")
                    )
                    live.update(display_text)
                    add_step("tool_call", f"Called tool: {tool_name}", timestamp)
                    tools_used.add(tool_name)
                elif event_type == "tool_result":
                    display_text = Text.assemble(
                        (f"[{agent_name}] ", "bold blue"),
                        ("🔨 Tool completed", "cyan")
                    )
                    live.update(display_text)
                    add_step("tool_result", "Tool execution completed", timestamp)
                elif event_type == "completion":
                    content = output.get("content", "")
                    # Handle Rich Text objects
                    if hasattr(content, 'plain'):
                        current_response = content.plain
                    else:
                        current_response = str(content)
                    display_text = Text.assemble(
                        (f"[{agent_name}] ", "bold blue"), 
                        (current_response, "green")
                    )
                    live.update(display_text)
                    add_step("completion", "Completed execution", timestamp)
                    final_response = current_agent_response
                elif event_type == "error":
                    content = output.get('content', '')
                    display_text = Text.assemble(
                        (f"[{agent_name}] ", "bold red"),
                        (f"❌ Error: {content}", "red")
                    )
                    live.update(display_text)
                    return
                elif output.get("is_done"):
                    break
    
    # Print final newline after streaming
    console.print()
    
    # Print execution summary
    console.print("\n" + "="*80)
    console.print("🎯 [bold cyan]EXECUTION SUMMARY[/bold cyan]")
    console.print("="*80)
    
    # Summary statistics
    console.print(f"📊 [bold]Statistics:[/bold]")
    console.print(f"   • Session ID: {session_id}")
    console.print(f"   • Total steps: {len(execution_steps)}")
    console.print(f"   • Agent: {agent_name}")
    console.print(f"   • Tools used: {len(tools_used)} ({', '.join(sorted(tools_used)) if tools_used else 'None'})")
    
    # Execution timeline
    console.print(f"\n⏱️  [bold]Execution Timeline:[/bold]")
    for i, step in enumerate(execution_steps, 1):
        step_type_emoji = {
            "response": "💬",
            "tool_call": "🔧", 
            "tool_result": "🔨",
            "completion": "✅"
        }.get(step["type"], "📝")
        
        console.print(f"   {i:2d}. [{step['timestamp']}] {step_type_emoji} {step['agent']}: {step['details']}")
    
    # Final response
    if final_response:
        console.print(f"\n💬 [bold]Final Response:[/bold]")
        console.print(f"   {final_response}")
    
    # MCP connection warnings
    if builder and hasattr(builder, 'failed_mcp_connections') and builder.failed_mcp_connections:
        console.print(f"\n⚠️  [bold yellow]MCP Connection Warnings:[/bold yellow]")
        for failed in builder.failed_mcp_connections:
            console.print(f"   • [yellow]{failed['name']}[/yellow]: {failed['error']}")
    
    console.print("="*80)


async def run_team_stream(executor: TeamRunner, message: str, debug: bool = False, session_id: str = None, builder: 'TeamBuilder' = None):
    """Run team with streaming response using Rich console and provide execution summary."""
    console = Console()
    
    # Track execution steps for final summary
    execution_steps = []
    agents_involved = set()
    tools_used = set()
    handoffs = []
    final_response = ""
    current_agent_response = ""
    
    def add_step(step_type: str, agent: str, details: str, timestamp: str = None):
        """Add a step to the execution tracking."""
        if timestamp is None:
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        execution_steps.append({
            "timestamp": timestamp,
            "type": step_type,
            "agent": agent,
            "details": details
        })
        agents_involved.add(agent)
    
    # Clear screen and show header
    console.clear()
    console.print("🚀 [bold blue]GNOSARI TEAM EXECUTION[/bold blue]", style="bold")
    console.print("=" * 80, style="dim")
    console.print(f"📝 [blue]Message:[/blue] {message}")
    console.print(f"🔗 [blue]Session:[/blue] {session_id}")
    console.print("=" * 80, style="dim")
    console.print()
    
    # Suppress ChromaDB warnings during execution
    import warnings
    warnings.filterwarnings("ignore", message=".*Add of existing embedding ID.*")
    warnings.filterwarnings("ignore", message=".*Accessing the 'model_fields' attribute.*")
    
    if debug:
        # For debug mode, print raw JSON output and formatted messages
        console.print("🐛 [bold red]DEBUG MODE[/bold red]", style="bold")
        console.print("─" * 80, style="dim")
        
        event_count = 0
        async for output in executor.run_team_stream(message, debug, session_id=session_id):
            event_count += 1
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            
            # Print event header
            console.print(f"\n📡 [bold cyan]EVENT #{event_count}[/bold cyan]", style="bold")
            console.print(f"⏰ [dim]{timestamp}[/dim]")
            
            # Print raw JSON for debugging (like WebSocket)
            json_output = json.dumps(output, indent=2, default=str)
            syntax = Syntax(json_output, "json", theme="monokai", line_numbers=False)
            console.print(syntax)
            
            # Show formatted output for readability
            event_type = output.get("type", "unknown")
            agent_name = output.get("agent_name", "Unknown Agent")
            
            if event_type == "response":
                content = output.get('content', '')
                # Handle Rich Text objects
                if hasattr(content, 'plain'):
                    content_str = content.plain
                else:
                    content_str = str(content)
                console.print(f"💬 [bold green]RESPONSE[/bold green] from [bold]{agent_name}[/bold]: [green]{content_str}[/green]")
                current_agent_response += content_str  # Track actual response content
                # Only add step for first response chunk to avoid spam
                if not hasattr(console, '_response_started'):
                    add_step("response", agent_name, f"Started generating response", timestamp)
                    console._response_started = True
            elif event_type == "tool_call":
                tool_name = output.get("tool_name", output.get("name", "unknown"))
                tool_input = output.get("tool_input", output.get("input", {}))
                console.print(f"🔧 [bold yellow]TOOL CALL[/bold yellow] by [bold]{agent_name}[/bold]: [yellow]{tool_name}[/yellow]")
                console.print(f"📥 Input: [dim]{tool_input}[/dim]")
                add_step("tool_call", agent_name, f"Called tool: {tool_name}", timestamp)
                tools_used.add(tool_name)
            elif event_type == "tool_result":
                content = output.get('content', '')
                preview = content[:200] + "..." if len(str(content)) > 200 else content
                console.print(f"🔨 [bold cyan]TOOL RESULT[/bold cyan] for [bold]{agent_name}[/bold]: [cyan]{preview}[/cyan]")
                add_step("tool_result", agent_name, f"Tool result: {preview}", timestamp)
            elif event_type == "completion":
                content = output.get('content', '')
                # Handle Rich Text objects
                if hasattr(content, 'plain'):
                    content_str = content.plain
                else:
                    content_str = str(content)
                console.print(f"✅ [bold green]COMPLETION[/bold green] from [bold]{agent_name}[/bold]: [green]{content_str}[/green]")
                add_step("completion", agent_name, f"Completed execution", timestamp)
                final_response = current_agent_response  # Use actual response content, not completion message
                # Reset response tracking for next agent
                if hasattr(console, '_response_started'):
                    delattr(console, '_response_started')
                current_agent_response = ""  # Reset for next agent
            elif event_type == "handoff":
                target_agent = output.get("agent_name", "Unknown")
                escalation_data = output.get("escalation")
                
                if escalation_data:
                    reason = escalation_data.get("reason", "Unknown")
                    from_agent = escalation_data.get("from_agent", "Unknown")
                    context = escalation_data.get("context")
                    
                    console.print(f"🤝 [bold magenta]HANDOFF ESCALATION[/bold magenta]")
                    console.print(f"   📤 From: [bold]{from_agent}[/bold]")
                    console.print(f"   📥 To: [bold]{target_agent}[/bold]")
                    console.print(f"   📋 Reason: [yellow]{reason}[/yellow]")
                    if context:
                        console.print(f"   📝 Context: [dim]{context}[/dim]")
                    
                    handoffs.append({
                        "from": from_agent,
                        "to": target_agent,
                        "reason": reason,
                        "context": context
                    })
                    add_step("handoff", from_agent, f"Handed off to {target_agent} (Reason: {reason})", timestamp)
                    # Reset response tracking for new agent
                    if hasattr(console, '_response_started'):
                        delattr(console, '_response_started')
                    current_agent_response = ""  # Reset for next agent
                else:
                    console.print(f"🤝 [bold magenta]HANDOFF[/bold magenta] to [bold]{target_agent}[/bold]")
                    add_step("handoff", agent_name, f"Handed off to {target_agent}", timestamp)
                    # Reset response tracking for new agent
                    if hasattr(console, '_response_started'):
                        delattr(console, '_response_started')
                    current_agent_response = ""  # Reset for next agent
            elif output.get("is_done"):
                console.print(f"🎯 [bold green]DONE![/bold green] Final response completed.")
                break
            
            console.print("─" * 80, style="dim")
    else:
        # Use Live display to show streaming response with better formatting
        console.print("📡 [bold cyan]STREAMING EVENTS[/bold cyan]", style="bold")
        console.print("─" * 80, style="dim")
        
        with Live("", refresh_per_second=10, auto_refresh=True) as live:
            # Show initial status
            live.update(Text.assemble(("⏳ Initializing...", "dim")))
            current_response = ""
            current_agent = "Team"
            event_count = 0
            
            # Suppress logging during streaming
            import logging
            logging.getLogger().setLevel(logging.ERROR)
            
            async for output in executor.run_team_stream(message, debug, session_id=session_id):
                event_count += 1
                timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                event_type = output.get("type", "unknown")
                agent_name = output.get("agent_name", current_agent)
                
                # Update current agent if it changed
                if agent_name != current_agent:
                    current_agent = agent_name
                
                # Handle different output types
                if event_type == "response":
                    content = output.get("content", "")
                    # Handle Rich Text objects
                    if hasattr(content, 'plain'):
                        content_str = content.plain
                    else:
                        content_str = str(content)
                    current_response += content_str
                    current_agent_response += content_str  # Track actual response content
                    display_text = Text.assemble(
                        (f"[{current_agent}] ", "bold blue"), 
                        (current_response, "green")
                    )
                    live.update(display_text)
                    # Only add step for first response chunk to avoid spam
                    if not hasattr(live, '_response_started'):
                        add_step("response", agent_name, f"Started generating response", timestamp)
                        live._response_started = True
                elif event_type == "tool_call":
                    tool_name = output.get("tool_name", output.get("name", "unknown"))
                    display_text = Text.assemble(
                        (f"[{current_agent}] ", "bold blue"),
                        (f"🔧 Calling {tool_name}...", "yellow")
                    )
                    live.update(display_text)
                    add_step("tool_call", agent_name, f"Called tool: {tool_name}", timestamp)
                    tools_used.add(tool_name)
                elif event_type == "tool_result":
                    display_text = Text.assemble(
                        (f"[{current_agent}] ", "bold blue"),
                        ("🔨 Tool completed", "cyan")
                    )
                    live.update(display_text)
                    add_step("tool_result", agent_name, "Tool execution completed", timestamp)
                elif event_type == "completion":
                    content = output.get("content", "")
                    # Handle Rich Text objects
                    if hasattr(content, 'plain'):
                        current_response = content.plain
                    else:
                        current_response = str(content)
                    display_text = Text.assemble(
                        (f"[{current_agent}] ", "bold blue"), 
                        (current_response, "green")
                    )
                    live.update(display_text)
                    add_step("completion", agent_name, "Completed execution", timestamp)
                    final_response = current_agent_response  # Use actual response content, not completion message
                    # Reset response tracking for next agent
                    if hasattr(live, '_response_started'):
                        delattr(live, '_response_started')
                    current_agent_response = ""  # Reset for next agent
                elif event_type == "handoff":
                    target_agent = output.get("agent_name", "Unknown")
                    escalation_data = output.get("escalation")
                    
                    if escalation_data:
                        reason = escalation_data.get("reason", "Unknown")
                        display_text = Text.assemble(
                            (f"[{current_agent}] ", "bold blue"),
                            (f"🤝 Escalating to {target_agent} ({reason})...", "magenta")
                        )
                        handoffs.append({
                            "from": escalation_data.get("from_agent", current_agent),
                            "to": target_agent,
                            "reason": reason,
                            "context": escalation_data.get("context")
                        })
                        add_step("handoff", current_agent, f"Handed off to {target_agent} (Reason: {reason})", timestamp)
                    else:
                        display_text = Text.assemble(
                            (f"[{current_agent}] ", "bold blue"),
                            (f"🤝 Handing off to {target_agent}...", "magenta")
                        )
                        add_step("handoff", current_agent, f"Handed off to {target_agent}", timestamp)
                    live.update(display_text)
                    # Reset response tracking for new agent
                    if hasattr(live, '_response_started'):
                        delattr(live, '_response_started')
                    current_agent_response = ""  # Reset for next agent
                elif output.get("is_done"):
                    break
    
    # Print final newline after streaming
    console.print()
    
    # Print execution summary
    console.print("\n" + "="*80)
    console.print("🎯 [bold cyan]EXECUTION SUMMARY[/bold cyan]")
    console.print("="*80)
    
    # Summary statistics
    console.print(f"📊 [bold]Statistics:[/bold]")
    console.print(f"   • Session ID: {session_id}")
    console.print(f"   • Total steps: {len(execution_steps)}")
    console.print(f"   • Agents involved: {len(agents_involved)} ({', '.join(sorted(agents_involved))})")
    console.print(f"   • Tools used: {len(tools_used)} ({', '.join(sorted(tools_used)) if tools_used else 'None'})")
    console.print(f"   • Handoffs: {len(handoffs)}")
    
    # Execution timeline
    console.print(f"\n⏱️  [bold]Execution Timeline:[/bold]")
    for i, step in enumerate(execution_steps, 1):
        step_type_emoji = {
            "response": "💬",
            "tool_call": "🔧", 
            "tool_result": "🔨",
            "completion": "✅",
            "handoff": "🤝"
        }.get(step["type"], "📝")
        
        console.print(f"   {i:2d}. [{step['timestamp']}] {step_type_emoji} {step['agent']}: {step['details']}")
    
    # Handoff details
    if handoffs:
        console.print(f"\n🤝 [bold]Handoff Details:[/bold]")
        for i, handoff in enumerate(handoffs, 1):
            console.print(f"   {i}. {handoff['from']} → {handoff['to']}")
            console.print(f"      Reason: {handoff['reason']}")
            if handoff.get('context'):
                console.print(f"      Context: {handoff['context'][:100]}...")
    
    # Final response
    if final_response:
        console.print(f"\n💬 [bold]Final Response:[/bold]")
        console.print(f"   {final_response}")
    
    # MCP connection warnings
    if builder and hasattr(builder, 'failed_mcp_connections') and builder.failed_mcp_connections:
        console.print(f"\n⚠️  [bold yellow]MCP Connection Warnings:[/bold yellow]")
        for failed in builder.failed_mcp_connections:
            console.print(f"   • [yellow]{failed['name']}[/yellow]: {failed['error']}")
    
    console.print("="*80)


def setup_logging():
    """Setup logging configuration based on environment variables."""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        force=True  # Force reconfiguration even if logging was already configured
    )
    
    # Also set the level for specific loggers that might be created before basicConfig
    logging.getLogger().setLevel(getattr(logging, log_level, logging.INFO))
    
    # Ensure gnosari loggers use the configured level
    for logger_name in ['gnosari', 'gnosari.agents', 'gnosari.tools', 'gnosari.engine', 'gnosari.knowledge']:
        logging.getLogger(logger_name).setLevel(getattr(logging, log_level, logging.INFO))


def load_environment():
    """Load environment variables from .env file if it exists."""
    # Look for .env file in current directory and parent directories
    current_dir = Path.cwd()
    env_file = None
    
    # Check current directory and up to 3 parent directories
    for i in range(4):
        check_dir = current_dir / ("../" * i) if i > 0 else current_dir
        potential_env = check_dir / ".env"
        if potential_env.exists():
            env_file = potential_env
            break
    
    if env_file:
        print(f"Loading environment from: {env_file}")
        load_dotenv(env_file)
    else:
        # Try to load from current directory anyway (python-dotenv will handle it gracefully)
        load_dotenv()


def main() -> NoReturn:
    """Entrypoint for the gnosari CLI."""
    # Load environment variables from .env file
    load_environment()
    
    # Setup logging
    setup_logging()
    
    parser = argparse.ArgumentParser(
        description="Gnosari Teams - Multi-Agent AI Team Runner",
        epilog="Use 'gnosari --help' for more information."
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Default behavior (backward compatibility) - if no subcommand is provided, treat as run
    parser.add_argument("--config", "-c", help="Path to team configuration YAML file")
    parser.add_argument("--message", "-m", help="Message to send to the team")
    parser.add_argument("--agent", "-a", help="Run only a specific agent from the team (by name)")
    parser.add_argument("--session-id", "-s", help="Session ID for conversation persistence (generates new if not provided)")
    parser.add_argument("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4o"), help="Model to use (default: gpt-4o)")
    parser.add_argument("--temperature", type=float, default=float(os.getenv("OPENAI_TEMPERATURE", "1")), help="Model temperature (default: 1.0)")
    parser.add_argument("--stream", action="store_true", help="Stream the response in real-time")
    parser.add_argument("--debug", action="store_true", help="Show debug information with raw JSON output")
    parser.add_argument("--show-prompts", action="store_true", help="Display the generated system prompts for all agents in the team")
    
    # Push subcommand
    push_parser = subparsers.add_parser('push', help='Push team configuration to Gnosari API')
    push_parser.add_argument('config_file', help='Path to team configuration YAML file')
    push_parser.add_argument('--api-url', help='Gnosari API URL (default: https://api.gnosari.com or GNOSARI_API_URL env var)')
    
    # Pull subcommand
    pull_parser = subparsers.add_parser('pull', help='Pull team configuration from Gnosari API')
    pull_parser.add_argument('team_identifier', help='Team identifier to pull from the API')
    pull_parser.add_argument('--api-url', help='Gnosari API URL (default: https://api.gnosari.com or GNOSARI_API_URL env var)')
    
    # Worker subcommand
    worker_parser = subparsers.add_parser('worker', help='Run Celery worker for queue processing')
    worker_parser.add_argument('action', nargs='?', default='start', choices=['start', 'stop', 'restart', 'status'], help='Worker action (default: start)')
    worker_parser.add_argument('--concurrency', '-c', type=int, default=1, help='Number of concurrent workers (default: 1)')
    worker_parser.add_argument('--queue', '-q', default='gnosari_queue', help='Queue name to process (default: gnosari_queue)')
    worker_parser.add_argument('--loglevel', '-l', default='info', choices=['debug', 'info', 'warning', 'error'], help='Log level (default: info)')
    
    # Flower subcommand  
    flower_parser = subparsers.add_parser('flower', help='Run Flower UI for monitoring Celery tasks')
    flower_parser.add_argument('--port', '-p', type=int, default=5555, help='Port to run Flower on (default: 5555)')
    flower_parser.add_argument('--auth', help='Basic auth in format user:password (default: admin:admin)')
    flower_parser.add_argument('--broker', help='Broker URL (default: redis://localhost:6379/0)')
    
    args = parser.parse_args()
    
    # Handle push command
    if args.command == 'push':
        async def push_async():
            success = await push_team_config(args.config_file, args.api_url)
            sys.exit(0 if success else 1)
        
        asyncio.run(push_async())
        return
    
    # Handle pull command
    if args.command == 'pull':
        async def pull_async():
            success = await pull_team_config(args.team_identifier, args.api_url)
            sys.exit(0 if success else 1)
        
        asyncio.run(pull_async())
        return
    
    # Handle worker command
    if args.command == 'worker':
        from .queue.app import celery_app
        import subprocess
        import shlex
        import signal
        import psutil
        
        def find_celery_workers():
            """Find running Celery worker processes."""
            workers = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['cmdline'] and 'celery' in ' '.join(proc.info['cmdline']) and 'worker' in ' '.join(proc.info['cmdline']):
                        workers.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            return workers
        
        if args.action == 'status':
            workers = find_celery_workers()
            if workers:
                print(f"Found {len(workers)} running Celery worker(s):")
                for worker in workers:
                    try:
                        print(f"  PID: {worker.pid}, Status: {worker.status()}, CMD: {' '.join(worker.cmdline()[:5])}")
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            else:
                print("No Celery workers are currently running.")
            return
        
        elif args.action == 'stop':
            workers = find_celery_workers()
            if workers:
                print(f"Stopping {len(workers)} Celery worker(s)...")
                for worker in workers:
                    try:
                        print(f"Stopping worker PID {worker.pid}...")
                        worker.terminate()
                        worker.wait(timeout=10)
                        print(f"Worker PID {worker.pid} stopped.")
                    except psutil.TimeoutExpired:
                        print(f"Worker PID {worker.pid} didn't stop gracefully, killing...")
                        worker.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        print(f"Worker PID {worker.pid} already stopped or access denied.")
                print("All workers stopped.")
            else:
                print("No Celery workers are currently running.")
            return
            
        elif args.action == 'restart':
            # Stop existing workers first
            workers = find_celery_workers()
            if workers:
                print("Stopping existing workers...")
                for worker in workers:
                    try:
                        worker.terminate()
                        worker.wait(timeout=10)
                    except psutil.TimeoutExpired:
                        worker.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
        
        # Start worker (for start, restart actions)
        if args.action in ['start', 'restart']:
            # Build celery worker command
            worker_cmd = [
                "celery", "-A", "gnosari.queue.app.celery_app", "worker",
                "--concurrency", str(args.concurrency),
                "--queues", args.queue,
                "--loglevel", args.loglevel
            ]
            
            print(f"Starting Celery worker with command: {' '.join(worker_cmd)}")
            try:
                subprocess.run(worker_cmd, check=True)
            except KeyboardInterrupt:
                print("\nWorker stopped.")
            except subprocess.CalledProcessError as e:
                print(f"Error running worker: {e}")
                sys.exit(1)
        return
    
    # Handle flower command
    if args.command == 'flower':
        import subprocess
        
        # Set environment variables for Flower
        env = os.environ.copy()
        if args.broker:
            env['CELERY_BROKER_URL'] = args.broker
        
        # Build flower command  
        flower_cmd = [
            "celery", "-A", "gnosari.queue.app.celery_app", "flower",
            "--port", str(args.port)
        ]
        
        # Add basic auth if specified
        auth = args.auth or "admin:admin"
        flower_cmd.extend(["--basic-auth", auth])
        
        print(f"Starting Flower UI on port {args.port}")
        print(f"Access at: http://localhost:{args.port}")
        print(f"Login with: {auth}")
        
        try:
            subprocess.run(flower_cmd, env=env, check=True)
        except KeyboardInterrupt:
            print("\nFlower stopped.")
        except subprocess.CalledProcessError as e:
            print(f"Error running Flower: {e}")
            sys.exit(1)
        return
    
    # Handle backward compatibility - if no subcommand but config is provided, treat as run
    if not args.command and not args.config:
        print("Error: --config is required")
        sys.exit(1)
    
    # Validate arguments for run command
    if not args.show_prompts and not args.message:
        print("Error: --message is required when not using --show-prompts")
        sys.exit(1)
    
    # Get API key from args or environment (only needed for non-prompt-only operations)
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not args.show_prompts and not api_key:
        print("Error: OpenAI API key is required. Set it with --api-key, OPENAI_API_KEY environment variable, or in .env file.")
        sys.exit(1)
    
    # Handle show-prompts command
    if args.show_prompts:
        # Just show prompts and exit
        async def show_prompts_async():
            await show_team_prompts(args.config, args.model, args.temperature)
        
        asyncio.run(show_prompts_async())
        sys.exit(0)
    
    # Generate session ID if not provided
    import uuid
    session_id = args.session_id or f"cli-session-{uuid.uuid4().hex[:8]}"
    print(f"Session ID: {session_id}")
    
    # Create OpenAI team orchestrator and run team
    async def run_team_async():
        try:
            builder = TeamBuilder(
                api_key=api_key,
                model=args.model,
                temperature=args.temperature,
                session_id=session_id
            )
            
            # Build the team
            print(f"Building team from configuration: {args.config}")
            team = await builder.build_team(args.config, debug=args.debug)
            print(f"Team built successfully with {len(team.all_agents)} agents:")
            for name in team.list_agents():
                agent = team.get_agent(name)
                if agent and hasattr(agent, 'model'):
                    model = agent.model
                    print(f"  - {name} (Model: {model})")
                else:
                    print(f"  - {name}")
            
            # Show MCP connection warnings if any
            if hasattr(builder, 'failed_mcp_connections') and builder.failed_mcp_connections:
                print(f"\n⚠️  Warning: {len(builder.failed_mcp_connections)} MCP server(s) failed to connect:")
                for failed in builder.failed_mcp_connections:
                    print(f"   - {failed['name']}: {failed['error']}")
            
            # Create executor and execute
            runner = TeamRunner(team)
            
            if args.agent:
                # Validate agent exists
                target_agent = team.get_agent(args.agent)
                if not target_agent:
                    available_agents = ", ".join(team.list_agents())
                    print(f"Error: Agent '{args.agent}' not found in team configuration.")
                    print(f"Available agents: {available_agents}")
                    sys.exit(1)
                
                # Run single agent
                if args.stream:
                    print(f"\nRunning agent '{args.agent}' with streaming...")
                    await run_single_agent_stream(runner, args.agent, args.message, args.debug, session_id, builder)
                else:
                    print(f"\nRunning agent '{args.agent}' with message: {args.message}")
                    result = await runner.run_agent_until_done_async(
                        target_agent, args.message, session_id=session_id
                    )
                    
                    # Extract and display response
                    if isinstance(result, dict) and "outputs" in result:
                        for output in result["outputs"]:
                            if output.get("type") == "completion":
                                print(f"\nAgent Response:")
                                print(output.get("content", ""))
                                break
                    else:
                        print(f"Unexpected result format: {type(result)}")
                        print(result)
            elif args.stream:
                # Run with streaming
                print(f"\nRunning team with streaming...")
                await run_team_stream(runner, args.message, args.debug, session_id, builder)
            else:
                # Run without streaming
                print(f"\nRunning team with message: {args.message}")
                result = await runner.run_team_async(args.message, args.debug, session_id=session_id)
                print(f"\nTeam Response:")
                
                # Extract response content from OpenAI Runner result
                if hasattr(result, 'final_output'):
                    print(result.final_output)
                elif isinstance(result, dict) and "outputs" in result:
                    response_content = ""
                    
                    for output in result["outputs"]:
                        if output.get("type") == "completion":
                            response_content = output.get("content", "")
                            break
                    
                    if response_content:
                        print(response_content)
                    else:
                        print("No response content found")
                else:
                    print(f"Unexpected result format: {type(result)}")
                    print(result)
                
        except Exception as e:
            print(f"Error running team: {e}")
            if args.debug:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    
    # Run the async function
    asyncio.run(run_team_async())
    
    raise SystemExit(0)