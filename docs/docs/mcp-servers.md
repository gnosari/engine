---
sidebar_position: 6
---

# MCP Servers

MCP (Model Context Protocol) servers provide dynamic tool discovery and external integrations for your AI agents. They enable agents to access external APIs, databases, and services through a standardized protocol.

## What are MCP Servers?

MCP Servers are external services that implement the Model Context Protocol, allowing agents to:
- **Discover tools dynamically** at runtime
- **Access external APIs** and services
- **Interact with databases** and data sources
- **Extend agent capabilities** beyond built-in tools
- **Share tools** across multiple agents

:::info MCP vs Built-in Tools
While built-in tools are statically configured, MCP servers provide dynamic tool discovery and can offer complex, stateful integrations with external services.
:::

## Connection Types

Gnosari supports three types of MCP server connections:

### 1. **Streamable HTTP** (Recommended)
Best for web-based MCP servers with real-time communication:

```yaml
tools:
  - name: Slack Integration
    id: slack_mcp
    url: https://api.example.com/mcp
    connection_type: streamable_http
```

### 2. **Server-Sent Events (SSE)**
For traditional SSE-based MCP servers:

```yaml
tools:
  - name: SSE Integration
    id: sse_mcp
    url: https://api.example.com/mcp
    connection_type: sse
```

### 3. **Standard Input/Output (STDIO)**
For local MCP server processes:

```yaml
tools:
  - name: Local MCP Server
    id: local_mcp
    command: "/usr/local/bin/mcp-server"
    connection_type: stdio
```

## Basic Configuration

### Simple MCP Server

```yaml
name: Basic MCP Team

tools:
  - name: My MCP Server
    id: my_mcp_server
    url: https://api.example.com/mcp
    connection_type: streamable_http

agents:
  - name: Agent
    instructions: "Use MCP tools to help users"
    orchestrator: true
    model: gpt-4o
    tools:
      - my_mcp_server
```

:::tip Connection Testing
MCP servers are tested during team building. Only successfully connected servers are added to agents, with clear warnings for failed connections.
:::

## Advanced Configuration

### HTTP/HTTPS MCP Server with Authentication

```yaml
tools:
  - name: Authenticated API
    id: authenticated_api
    url: https://api.example.com/mcp
    connection_type: streamable_http
    
    # Authentication headers
    headers:
      Authorization: "Bearer your-api-token"
      X-API-Key: "your-api-key"
      User-Agent: "Gnosari-Agent/1.0"
      Content-Type: "application/json"
    
    # Timeout configurations
    timeout: 45                              # Connection timeout (seconds)
    sse_read_timeout: 60                     # SSE read timeout (seconds)  
    client_session_timeout_seconds: 300     # Client session timeout (seconds)
    terminate_on_close: true                 # Terminate on connection close

agents:
  - name: APIAgent
    instructions: "Use authenticated API to retrieve data"
    orchestrator: true
    model: gpt-4o
    tools:
      - authenticated_api
```

### Local STDIO MCP Server

```yaml
tools:
  - name: Local Database MCP
    id: local_database_mcp
    command: "/usr/local/bin/database-mcp-server"
    connection_type: stdio
    
    # Command line arguments
    args: 
      - "--config"
      - "/path/to/config.json"
      - "--verbose"
      - "--port"
      - "5432"
    
    # Session timeout
    client_session_timeout_seconds: 120

agents:
  - name: DatabaseAgent
    instructions: "Query local database through MCP"
    orchestrator: true
    model: gpt-4o
    tools:
      - local_database_mcp
```

### Multiple MCP Servers

```yaml
tools:
  # Slack integration
  - name: Slack Integration
    id: slack_mcp
    url: https://slack-mcp.example.com/
    connection_type: streamable_http
    headers:
      Authorization: "Bearer slack-token"
    timeout: 30
  
  # Jira integration  
  - name: Jira Integration
    id: jira_mcp
    url: https://jira-mcp.example.com/
    connection_type: streamable_http
    headers:
      Authorization: "Basic base64-credentials"
    timeout: 45
  
  # Local file system
  - name: File System Access
    id: filesystem_mcp
    command: "/usr/local/bin/fs-mcp-server"
    connection_type: stdio
    args: ["--root", "/workspace"]

agents:
  - name: ProjectManager
    instructions: >
      Coordinate projects using Slack for communication,
      Jira for task management, and local files for documentation.
    orchestrator: true
    model: gpt-4o
    tools:
      - slack_mcp
      - jira_mcp
      - filesystem_mcp
  
  - name: CommunicationAgent
    instructions: "Handle team communication through Slack"
    model: gpt-4o
    tools:
      - slack_mcp
  
  - name: TaskAgent
    instructions: "Manage tasks and issues in Jira"
    model: gpt-4o
    tools:
      - jira_mcp
```

## Configuration Options

### HTTP/HTTPS Server Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `url` | string | required | MCP server endpoint URL |
| `connection_type` | string | `"sse"` | Connection type: `"streamable_http"`, `"sse"` |
| `headers` | object | `{}` | HTTP headers (including authentication) |
| `timeout` | number | `30` | Connection timeout in seconds |
| `sse_read_timeout` | number | `30` | SSE read timeout in seconds |
| `client_session_timeout_seconds` | number | `30` | Client session timeout in seconds |
| `terminate_on_close` | boolean | `true` | Terminate connection on close (streamable_http only) |

### STDIO Server Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `command` | string | required | Path to MCP server executable |
| `connection_type` | string | required | Must be `"stdio"` |
| `args` | array | `[]` | Command line arguments |
| `client_session_timeout_seconds` | number | `30` | Client session timeout in seconds |

## Authentication Methods

### Bearer Token Authentication

```yaml
tools:
  - name: API with Bearer Token
    id: api_with_bearer
    url: https://api.example.com/mcp
    connection_type: streamable_http
    headers:
      Authorization: "Bearer your-jwt-token"
```

### API Key Authentication

```yaml
tools:
  - name: API with Key
    id: api_with_key
    url: https://api.example.com/mcp
    connection_type: streamable_http
    headers:
      X-API-Key: "your-api-key"
      X-Client-ID: "your-client-id"
```

### Basic Authentication

```yaml
tools:
  - name: API with Basic Auth
    id: api_with_basic
    url: https://api.example.com/mcp
    connection_type: streamable_http
    headers:
      Authorization: "Basic base64-encoded-credentials"
```

### Custom Headers

```yaml
tools:
  - name: API with Custom Headers
    id: api_with_custom
    url: https://api.example.com/mcp
    connection_type: streamable_http
    headers:
      Authorization: "Bearer token"
      X-Custom-Header: "custom-value"
      User-Agent: "MyApp/1.0"
      Accept: "application/json"
      Content-Type: "application/json"
```

:::warning Security Note
Store sensitive tokens and credentials in environment variables rather than hardcoding them in configuration files.
:::

## Environment Variables

Gnosari supports environment variable substitution in YAML configuration files using `${VAR_NAME}` or `${VAR_NAME:default_value}` syntax.

### Basic Environment Variable Usage

```yaml
tools:
  - name: Secure API
    id: secure_api
    url: https://api.example.com/mcp
    connection_type: streamable_http
    headers:
      Authorization: "Bearer ${API_TOKEN}"
      X-API-Key: "${API_KEY}"
```

Set environment variables:
```bash
export API_TOKEN="your-secret-token"
export API_KEY="your-secret-key"
```

### Environment Variables with Default Values

```yaml
tools:
  - name: Configurable API
    id: configurable_api
    url: "${API_URL:https://api.example.com/mcp}"
    connection_type: streamable_http
    headers:
      Authorization: "Bearer ${API_TOKEN}"
      User-Agent: "${USER_AGENT:Gnosari-Agent/1.0}"
    timeout: ${TIMEOUT:30}

agents:
  - name: Agent
    instructions: "Use configurable API"
    orchestrator: true
    model: "${MODEL:gpt-4o}"
    tools:
      - configurable_api
```

### Environment Variable Features

- **Recursive substitution**: Works in nested objects and arrays
- **Default values**: Use `${VAR:default}` syntax for fallback values
- **Type preservation**: Numeric values are preserved as numbers
- **Warning logging**: Missing variables without defaults are logged as warnings
- **Flexible placement**: Can be used anywhere in the YAML configuration

## Error Handling

### Connection Failures

When MCP servers fail to connect:
- **Build-time warnings** are displayed during team creation
- **Execution warnings** appear in the CLI summary
- **Agents continue** to function with available tools only
- **Failed servers** are not added to agents

Example warning output:
```
⚠️  Warning: 2 MCP server(s) failed to connect:
   - slack_mcp: Connection timeout
   - jira_mcp: Server unavailable (502 Bad Gateway)
```

### Troubleshooting Connection Issues

1. **Check server availability**:
   ```bash
   curl -X POST https://your-mcp-server.com/
   ```

2. **Verify authentication**:
   ```bash
   curl -H "Authorization: Bearer token" https://your-mcp-server.com/
   ```

3. **Test with increased timeouts**:
   ```yaml
   timeout: 60
   sse_read_timeout: 120
   ```

4. **Check server logs** for detailed error information

## MCP Server Examples

### Slack Integration

```yaml
tools:
  - name: Slack Integration
    id: slack_mcp
    url: https://slack-integration.tools.mcp.example.com/
    connection_type: streamable_http
    headers:
      Authorization: "Bearer ${SLACK_BOT_TOKEN}"
    timeout: ${SLACK_TIMEOUT:30}

agents:
  - name: SlackBot
    instructions: >
      You can send messages, create channels, and manage Slack workspaces.
      Always be helpful and professional in communications.
    orchestrator: true
    model: gpt-4o
    tools:
      - slack_mcp
```

### Database Integration

```yaml
tools:
  - name: PostgreSQL Integration
    id: postgres_mcp
    command: "/usr/local/bin/postgres-mcp-server"
    connection_type: stdio
    args:
      - "--host"
      - "${DB_HOST:localhost}"
      - "--port" 
      - "${DB_PORT:5432}"
      - "--database"
      - "${DB_NAME:myapp}"
      - "--username"
      - "${DB_USER}"
      - "--password"
      - "${DB_PASSWORD}"

agents:
  - name: DataAnalyst
    instructions: >
      You can query the PostgreSQL database to analyze data and generate reports.
      Always ensure queries are safe and efficient.
    orchestrator: true
    model: gpt-4o
    tools:
      - postgres_mcp
```

### File System Integration

```yaml
tools:
  - name: File System Manager
    id: files_mcp
    command: "${MCP_SERVER_PATH:/usr/local/bin/filesystem-mcp-server}"
    connection_type: stdio
    args:
      - "--root-path"
      - "${WORKSPACE_PATH:/workspace}"
      - "--allowed-extensions"
      - "${ALLOWED_EXTENSIONS:.txt,.md,.json,.py}"

agents:
  - name: FileManager
    instructions: >
      You can read, write, and manage files in the workspace directory.
      Always respect file permissions and security constraints.
    orchestrator: true
    model: gpt-4o
    tools:
      - files_mcp
```

## Best Practices

### 1. **Security**
- Use environment variables for credentials
- Implement proper authentication headers
- Limit server access through firewall rules
- Regular credential rotation

### 2. **Reliability**
- Set appropriate timeouts for your use case
- Implement retry logic in MCP servers
- Monitor server health and availability
- Have fallback tools for critical functionality

### 3. **Performance**
- Use connection pooling in MCP servers
- Implement caching where appropriate
- Set reasonable session timeouts
- Monitor API rate limits

### 4. **Maintainability**
- Document MCP server APIs and capabilities
- Version your MCP server implementations
- Use consistent naming conventions
- Implement proper logging and monitoring

## Integration Patterns

### 1. **Service-Specific Agents**
Dedicated agents for specific MCP servers:

```yaml
agents:
  - name: SlackAgent
    instructions: "Handle all Slack communications"
    tools: [slack_mcp]
  
  - name: DatabaseAgent  
    instructions: "Handle all database operations"
    tools: [postgres_mcp]
```

### 2. **Multi-Service Agents**
Agents that use multiple MCP servers:

```yaml
agents:
  - name: ProjectManager
    instructions: "Coordinate projects across multiple platforms"
    tools: [slack_mcp, jira_mcp, files_mcp]
```

### 3. **Hierarchical Access**
Different access levels for different agents:

```yaml
agents:
  - name: Manager
    instructions: "Full access to all systems"
    tools: [slack_mcp, jira_mcp, admin_mcp]
  
  - name: Developer
    instructions: "Development-focused access"
    tools: [jira_mcp, git_mcp]
```

## Limitations

### Current Limitations
- **No dedicated auth section**: Use headers for authentication
- **HTTP-based servers only** for remote connections
- **No dynamic server discovery**: Servers must be configured in YAML
- **Single authentication method** per server

### Resource Considerations
- **Connection overhead**: Each MCP server maintains a connection
- **Memory usage**: Tools are cached in agent memory
- **API rate limits**: Consider limits from external services
- **Network latency**: Remote servers add latency to tool calls

:::tip Planning MCP Integration
Consider your specific use case, security requirements, and performance needs when designing MCP server integration.
:::

## Related Topics

- [Tools](tools/intro) - Learn about built-in tools and tool development
- [Teams](teams) - Understand team configuration and structure
- [Agents](agents) - Learn about individual agent configuration
- [Quickstart](quickstart) - Create your first team with MCP servers

## Next Steps

Now that you understand MCP servers, learn how to:
- [Configure teams](teams) with MCP server integration
- [Set up agents](agents) to use MCP tools effectively
- [Use built-in tools](tools/intro) alongside MCP servers
- [Create your first team](quickstart) with external integrations