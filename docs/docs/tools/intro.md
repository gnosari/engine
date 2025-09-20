---
sidebar_position: 1
---

# Tools Overview

Tools are the building blocks that give your AI agents superpowers. In Gnosari AI Teams, tools enable agents to interact with external systems, query databases, make API calls, delegate tasks, and much more.

:::info MCP Servers
Looking for dynamic external integrations? Check out [MCP Servers](../mcp-servers) for connecting to external APIs and services through the Model Context Protocol.
:::

## What are Tools?

Tools are Python classes that implement specific functionality and can be called by AI agents during their execution. Each tool follows a consistent pattern and can be configured with custom parameters to suit your needs.

## Built-in Tools

Gnosari AI Teams comes with several powerful built-in tools:

| Tool | Description | Use Case |
|------|-------------|----------|
| **delegate_agent** | *Automatically added to agents with `delegation` property* | Multi-agent coordination |
| **api_request** | Make HTTP requests to external APIs | External service integration |
| **knowledge_query** | Query knowledge bases for information | RAG and information retrieval |
| **sql_query** | Execute SQL queries against any database via SQLAlchemy | Universal database operations |
| **mysql_query** | Execute SQL queries against MySQL databases | Database operations |
| **website_content** | Fetch content from websites via API | Web content retrieval |
| **web_search** | Real-time web search using OpenAI's search infrastructure | Current information gathering |
| **file_operations** | Read, write, and manage files in a sandboxed directory | Local file management |

## Adding Tools to Your Team

Tools are configured in the `tools` section of your team YAML file. Here's the basic structure:

```yaml
tools:
  - name: tool_name
    module: gnosari.tools.tool_module
    class: ToolClassName
    args:
      # Tool-specific configuration parameters
```

:::tip Tool Naming
Each tool must have a unique name within your team configuration. This name is used by agents to reference the tool.
:::

### Basic Tool Configuration

```yaml
name: My Team

tools:
  - name: api_request
    module: gnosari.tools.builtin.api_request
    class: APIRequestTool
    args:
      base_url: https://api.example.com
      timeout: 30

agents:
  - name: Coordinator
    instructions: "Coordinate team tasks and delegate when needed"
    orchestrator: true
    model: gpt-4o
    tools:
      - api_request

  - name: Specialist
    instructions: "Handle specific tasks assigned by the coordinator"
    model: gpt-4o
    tools:
      - api_request
```

### Advanced Tool Configuration

Some tools accept configuration parameters to customize their behavior:

```yaml
name: API Team

tools:
  - name: api_request
    module: gnosari.tools.builtin.api_request
    class: APIRequestTool
    args:
      base_url: https://api.example.com
      base_headers:
        Authorization: Bearer your-token
        Content-Type: application/json
      timeout: 30
      verify_ssl: true

  - name: mysql_query
    module: gnosari.tools.builtin.mysql_query
    class: MySQLQueryTool
    args:
      host: localhost
      port: 3306
      database: my_database
      username: my_user
      password: my_password
      pool_size: 10
      query_timeout: 60

agents:
  - name: Data Analyst
    instructions: "Analyze data from APIs and databases"
    model: gpt-4o
    tools:
      - api_request
      - mysql_query
```

## Tool Assignment to Agents

Once you've defined tools in the `tools` section, you can assign them to specific agents in the `agents` section:

```yaml
agents:
  - name: Coordinator
    instructions: "Coordinate team tasks"
    orchestrator: true
    model: gpt-4o
    tools:
      - api_request
      
  - name: Researcher
    instructions: "Research information from various sources"
    model: gpt-4o
    tools:
      - knowledge_query  # This agent can query knowledge bases
      - website_content  # This agent can fetch web content
      
  - name: Data Processor
    instructions: "Process data from APIs and databases"
    model: gpt-4o
    tools:
      - api_request      # This agent can make API calls
      - mysql_query      # This agent can query databases
```

## Tool Naming and References

- **Tool Name**: The `name` field in the tool definition creates a reference that agents use
- **Agent Tools**: The `tools` list in agent definitions references these names
- **Unique Names**: Each tool must have a unique name within your team configuration

## Best Practices

### 1. **Tool Organization**
Group related tools together and use descriptive names:

```yaml
tools:
  - name: external_api
    module: gnosari.tools.builtin.api_request
    class: APIRequestTool
    args:
      base_url: https://external-service.com
      
  - name: internal_api
    module: gnosari.tools.builtin.api_request
    class: APIRequestTool
    args:
      base_url: https://internal-service.com
```

:::info Multiple Tool Instances
You can create multiple instances of the same tool class with different configurations by giving them different names.
:::

### 2. **Security Considerations**
- Store sensitive credentials in environment variables
- Use appropriate timeouts for external services
- Enable SSL verification for production APIs

:::warning Security Best Practice
Never hardcode API keys, passwords, or other sensitive credentials in your YAML files. Use environment variables instead.
:::

### 3. **Error Handling**
All built-in tools include comprehensive error handling and logging. Check the logs for detailed error information when tools fail.

:::tip Debug Mode
Use `--debug` flag when running your team to see detailed tool execution logs and error information.
:::

### 4. **Performance**
- Use connection pooling for database tools
- Set appropriate timeouts for external services
- Consider tool execution time in your agent instructions

:::note Performance Optimization
Database tools like `mysql_query` use connection pooling by default. Configure `pool_size` and `max_overflow` based on your expected load.
:::

## Related Topics

- [Agents](../agents) - Learn how to configure agents with tools
- [Teams](../teams) - Understand team structure and tool assignment
- [Orchestration](../coordination/orchestration) - Learn about agent coordination with tools
- [Knowledge Bases](../knowledge) - Set up knowledge bases for agents
- [Quickstart](../quickstart) - Create your first team with tools

## Next Steps

Now that you understand how to add tools to your teams, explore the individual tool documentation:

- [Delegate Agent Tool](delegate-agent) - Automatic multi-agent coordination
- [API Request Tool](api-request) - External API integration
- [Knowledge Query Tool](knowledge-query) - Knowledge base queries
- [SQL Query Tool](sql-query) - Universal database operations
- [MySQL Query Tool](mysql-query) - Database operations
- [Website Content Tool](website-content) - Web content retrieval
- [Web Search Tool](web-search) - Real-time web search capabilities
- [File Operations Tool](file-operations) - Local file management

Ready to enhance your agents with powerful tools? Let's dive into each tool's capabilities!