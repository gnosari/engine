# API Reference

This section provides comprehensive documentation for the Gnosari AI Teams API and CLI interfaces.

## CLI Commands

### Core Commands

#### `gnosari team run`
Execute a team configuration with a message.

```bash
gnosari team run --config "path/to/team.yaml" --message "Your message"
```

**Options:**
- `--config, -c`: Path to team configuration file (required)
- `--message, -m`: Message to send to the team (required)
- `--stream`: Enable streaming output for real-time responses
- `--agent`: Run specific agent from the team
- `--model`: Override the default model for all agents
- `--temperature`: Override the default temperature for all agents
- `--debug`: Enable debug mode with raw JSON events

**Examples:**
```bash
# Basic team execution
gnosari team run --config "examples/database_admin_team.yaml" --message "Analyze the database schema"

# With streaming output
gnosari team run --config "examples/team_designer.yaml" --message "Design a web scraping team" --stream

# Run specific agent
gnosari team run --config "examples/universal_database_team.yaml" --message "Optimize this query" --agent "QueryOptimizer"

# Custom model settings
gnosari team run --config "examples/neomanex_demo.yaml" --message "Generate a report" --model "gpt-4o" --temperature 0.3
```

#### `gnosari team push`
Push team configuration to the Gnosari API.

```bash
gnosari team push "path/to/team.yaml"
```

**Options:**
- `--api-url`: Custom API URL (defaults to environment variable)
- `--api-key`: API key (defaults to environment variable)

**Environment Variables:**
- `GNOSARI_API_KEY`: Your Gnosari API key
- `GNOSARI_API_URL`: Custom API URL (optional)

### Legacy Commands

For backward compatibility, the following commands are also supported:

```bash
# Legacy format (still works)
gnosari --config "team.yaml" --message "message"
gnosari push "team.yaml"
```

## Python API

### Team Builder

The `TeamBuilder` class creates teams from YAML configurations.

```python
from gnosari.engine.team_builder import TeamBuilder

# Create a team builder
builder = TeamBuilder()

# Build team from configuration
team = await builder.build_team("path/to/team.yaml")
```

### Team Runner

The `TeamRunner` class executes team workflows.

```python
from gnosari.engine.team_runner import TeamRunner

# Create a team runner
runner = TeamRunner()

# Run team with message
result = await runner.run_team(team, "Your message", stream=True)
```

### Agent Management

```python
from gnosari.agents.gnosari_agent import GnosariAgent

# Create a custom agent
agent = GnosariAgent(
    name="CustomAgent",
    instructions="You are a helpful assistant",
    model="gpt-4o",
    temperature=0.7
)

# Add tools to agent
agent.add_tool("api_request")
agent.add_tool("file_operations")
```

## Configuration Schema

### Team Configuration

```yaml
name: "Team Name"
description: "Team description"

# Optional knowledge bases
knowledge:
  - name: "docs"
    type: "website"
    data: ["https://example.com"]

# Tools configuration
tools:
  - name: "api_tool"
    module: "gnosari.tools.api_request"
    class: "APIRequestTool"
  - name: "mcp_server"
    url: "http://localhost:8080"

# Agents configuration
agents:
  - name: "Manager"
    instructions: "Coordinate team tasks"
    orchestrator: true
    model: "gpt-4o"
    temperature: 0.1
    tools: ["delegate_agent", "api_tool"]
    knowledge: ["docs"]
```

### Agent Configuration

```yaml
agents:
  - name: "AgentName"           # Required: Unique agent identifier
    instructions: "..."         # Required: Agent behavior instructions
    orchestrator: true          # Optional: Whether agent can coordinate others
    model: "gpt-4o"            # Optional: LLM model to use
    temperature: 0.7            # Optional: Model temperature (0.0-2.0)
    reasoning_effort: "high"    # Optional: Reasoning effort level
    tools: ["tool1", "tool2"]   # Optional: List of tool names
    knowledge: ["kb1"]          # Optional: List of knowledge base names
    can_transfer_to: ["Agent2"] # Optional: Agents this can handoff to
```

### Tool Configuration

```yaml
tools:
  - name: "tool_name"                    # Required: Tool identifier
    module: "gnosari.tools.module"       # Required: Python module path
    class: "ToolClass"                   # Required: Tool class name
    args:                               # Optional: Tool-specific arguments
      param1: "value1"
      param2: "value2"
  - name: "mcp_tool"
    url: "http://localhost:8080"         # MCP server URL
```

## Built-in Tools

### API Request Tool
Make HTTP requests to external APIs.

**Module:** `gnosari.tools.api_request`

**Parameters:**
- `url`: Target URL
- `method`: HTTP method (GET, POST, PUT, DELETE)
- `headers`: Request headers
- `data`: Request body data

### File Operations Tool
Read, write, and manage files.

**Module:** `gnosari.tools.file_operations`

**Parameters:**
- `base_directory`: Base directory for operations
- `allowed_extensions`: Permitted file extensions
- `max_file_size`: Maximum file size limit

### Knowledge Query Tool
Query knowledge bases for information.

**Module:** `gnosari.tools.knowledge_query`

**Parameters:**
- `query`: Search query
- `knowledge_base`: Knowledge base name
- `max_results`: Maximum number of results

### Delegate Agent Tool
Delegate tasks to other agents in the team.

**Module:** `gnosari.tools.delegate_agent`

**Parameters:**
- `agent_name`: Target agent name
- `task`: Task description
- `context`: Additional context

## Error Handling

### Common Error Codes

- `CONFIG_ERROR`: Invalid team configuration
- `AGENT_ERROR`: Agent execution failed
- `TOOL_ERROR`: Tool execution failed
- `NETWORK_ERROR`: Network connectivity issues
- `AUTH_ERROR`: Authentication/authorization failed

### Debugging

Enable debug mode for detailed error information:

```bash
gnosari team run --config "team.yaml" --message "message" --debug
```

This will output raw JSON events and detailed error information.

## Rate Limits

- **OpenAI API**: Follows OpenAI's rate limits
- **Anthropic API**: Follows Anthropic's rate limits
- **Custom APIs**: Depends on provider-specific limits

## Authentication

### API Keys

Set environment variables for API keys:

```bash
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export DEEPSEEK_API_KEY="your-deepseek-key"
export GNOSARI_API_KEY="your-gnosari-key"
```

### Custom Providers

For custom LLM providers, configure the client in your team configuration:

```yaml
agents:
  - name: "CustomAgent"
    model: "custom-model"
    provider: "custom-provider"
    api_key: "your-custom-key"
```

## Best Practices

1. **Use environment variables** for API keys
2. **Test configurations** before production use
3. **Monitor usage** to avoid rate limits
4. **Handle errors gracefully** in your applications
5. **Use streaming** for long-running tasks
6. **Optimize prompts** for better performance
7. **Cache results** when appropriate