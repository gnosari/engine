# LLM.md - Complete Team YAML Configuration Guide

## Complete YAML Structure

```yaml
# MANDATORY: Team identification
name: "Team Name"                    # MANDATORY
description: "Team description"       # OPTIONAL

# OPTIONAL: Team configuration settings
config:
  max_turns: 100                    # Max conversation turns (default: 100)
  timeout: 300                       # Execution timeout in seconds (default: 300)

# OPTIONAL: Knowledge bases (auto-adds knowledge_query tool to agents)
knowledge:
  - id: "kb_unique_id"              # MANDATORY: Unique identifier for referencing
    name: "Knowledge Base Name"      # MANDATORY: Display name
    type: "website"                  # MANDATORY: website|youtube|pdf|text|csv|json|directory
    data: ["source1", "source2"]    # MANDATORY: Data sources array
    config:                          # OPTIONAL: Embedchain configuration
      llm:                           # LLM provider settings
        provider: "openai"           # openai|anthropic|google|deepseek|azure_openai
        config:
          model: "gpt-4o"
          temperature: 0.1
          max_tokens: 1000
      embedder:                      # Embedding model settings
        provider: "openai"           # openai|huggingface|cohere|google
        config:
          model: "text-embedding-3-small"
          dimensions: 1536
      chunker:                       # Document chunking settings
        chunk_size: 1000
        chunk_overlap: 200
        length_function: "len"
      db:                            # Vector database settings
        provider: "chroma"           # chroma|pinecone|weaviate|qdrant
        config:
          collection_name: "kb_name"
          persist_directory: "./data"

# OPTIONAL: Tools (built-in + MCP servers)
tools:
  # Built-in tool example
  - name: "tool_name"               # MANDATORY: Tool reference name
    id: "tool_id"                   # OPTIONAL: Unique identifier
    module: "gnosari.tools.builtin.api_request"  # MANDATORY: Module path
    class: "APIRequestTool"         # MANDATORY: Class name
    args:                           # OPTIONAL: Tool-specific args
      base_url: "${API_URL:https://api.example.com}"
      timeout: ${TIMEOUT:30}
  
  # MCP server examples
  - name: "MCP Server Name"         # MANDATORY: Display name
    id: "mcp_server_id"             # OPTIONAL: Unique identifier
    url: "${MCP_URL}"               # MANDATORY for HTTP/SSE
    command: "/path/to/server"      # MANDATORY for STDIO
    connection_type: "streamable_http"  # streamable_http|sse|stdio
    headers:                        # OPTIONAL: For HTTP/SSE
      Authorization: "Bearer ${TOKEN}"
    args: ["--arg1", "--arg2"]     # OPTIONAL: For STDIO
    timeout: 30                     # OPTIONAL: Connection timeout

# MANDATORY: Agents array (at least one agent required)
agents:
  - name: "AgentName"               # MANDATORY: Agent name
    instructions: "Agent behavior"   # MANDATORY: Agent instructions/prompt
    model: "gpt-4o"                 # OPTIONAL: gpt-5|gpt-4o|gpt-4o-mini (default: gpt-4o)
    temperature: 0.7                # OPTIONAL: 0.0-1.0 (default: 0.7)
    reasoning_effort: "medium"       # OPTIONAL: low|medium|high (default: medium)
    orchestrator: true              # OPTIONAL: Makes agent the entry point
    tools: ["tool_id1", "tool_id2"] # OPTIONAL: Tool references by name/id
    knowledge: ["kb_id1", "kb_id2"] # OPTIONAL: Knowledge base references by id
    delegation:                     # OPTIONAL: Task delegation configuration
      - agent: "OtherAgentName"     # Target agent name
        instructions: "When/how to use this agent"
```

## Core Concepts

### Models & Settings
- **model**: gpt-5, gpt-4o, gpt-4o-mini
- **temperature**: 0.0-1.0 (creativity level)
- **reasoning_effort**: low/medium/high (thinking depth)

### Agent Roles
- **orchestrator: true**: Entry point, receives initial user request
- **delegation**: Two-way task assignment (gets response back)
- **tools**: Array of tool names/ids the agent can use
- **knowledge**: Array of knowledge base ids the agent can access

### Tool Types & Parameters

**Built-in Tools:**

#### api_request - HTTP API calls
```yaml
module: gnosari.tools.builtin.api_request
class: APIRequestTool
args:
  base_url: "https://api.example.com"  # Base URL for requests
  base_headers: {}                      # Default headers (dict)
  timeout: 30                           # Request timeout (seconds)
  verify_ssl: true                      # SSL verification
  tool_name: "api_request"              # Custom tool name
  tool_description: "Make HTTP requests" # Custom description
```

#### sql_query - Universal SQL via SQLAlchemy  
```yaml
module: gnosari.tools.builtin.sql_query
class: SQLQueryTool
args:
  database_url: "postgresql://user:pass@host:port/db"  # Required
  pool_size: 5                          # Connection pool size
  max_overflow: 10                      # Max overflow connections
  pool_timeout: 30                      # Pool timeout (seconds)
  pool_recycle: 3600                    # Connection recycle (seconds)
  query_timeout: 30                     # Query timeout (seconds)
  echo: false                           # Echo SQL statements
  enable_unsafe_operations: false       # Allow DROP/TRUNCATE
  allowed_schemas: null                 # List of allowed schemas
  blocked_keywords: []                  # Additional blocked keywords
  tool_name: "sql_query"                # Custom tool name
  tool_description: "Execute SQL queries" # Custom description
```

#### mysql_query - MySQL specific
```yaml
module: gnosari.tools.builtin.mysql_query
class: MySQLQueryTool
args:
  host: "localhost"                     # MySQL server host
  port: 3306                           # MySQL server port
  database: ""                         # Database name
  username: ""                         # Database username
  password: ""                         # Database password
  charset: "utf8mb4"                   # Character set
  pool_size: 5                         # Connection pool size
  max_overflow: 10                     # Max overflow connections
  pool_timeout: 30                     # Pool timeout (seconds)
  pool_recycle: 3600                   # Connection recycle (seconds)
  query_timeout: 30                    # Query timeout (seconds)
  echo: false                          # Echo SQL statements
```

#### website_content - Web content fetch
```yaml
module: gnosari.tools.builtin.website_content
class: WebsiteContentTool
args:
  base_url: "https://r.ai.neomanex.com" # API base URL
  timeout: 30                           # Request timeout (seconds)
  tool_name: "website_content"          # Custom tool name
  tool_description: "Fetch URL content"  # Custom description
```

#### web_search - Real-time web search
```yaml
module: agents
class: WebSearchTool
args:
  search_context_size: "medium"         # small|medium|large
  user_location: "US"                   # Geographic location
  filters: []                           # recent|authoritative|news|academic
```

#### file_operations - File management
```yaml
module: gnosari.tools.builtin.file_operations
class: FileOperationsTool
args:
  base_directory: "./workspace"         # Base directory path
  allowed_extensions: null              # List of allowed extensions
  max_file_size: 10485760               # Max file size (bytes)
  tool_name: "file_operations"          # Custom tool name
  tool_description: "Manage files"       # Custom description
```

#### bash_operations - Secure bash execution
```yaml
module: gnosari.tools.builtin.bash_operations
class: BashOperationsTool
args:
  base_directory: "./workspace"         # Base directory for command execution
  allowed_commands: null                # List of allowed command prefixes (e.g., ['git', 'npm'])
  blocked_commands: null                # List of blocked command prefixes (e.g., ['rm', 'sudo'])
  max_output_size: 1048576              # Maximum output size in bytes (1MB)
  unsafe_mode: false                    # Disable all safety mechanisms (dangerous)
  tool_name: "bash_operations"          # Custom tool name
  tool_description: "Execute bash commands in a secure environment"
```

#### interactive_bash - Interactive process handling
```yaml
module: gnosari.tools.builtin.interactive_bash_operations
class: InteractiveBashOperationsTool
args:
  base_directory: "./workspace"         # Base directory for command execution
  allowed_commands: null                # List of allowed command prefixes
  blocked_commands: null                # List of blocked command prefixes
  max_output_size: 5242880              # Maximum output size in bytes (5MB)
  unsafe_mode: false                    # Disable all safety mechanisms (dangerous)
  session_timeout: 3600                 # Session timeout in seconds (1 hour)
  tool_name: "interactive_bash"         # Custom tool name
  tool_description: "Execute interactive bash commands and respond to prompts"
```

#### bash - Enhanced bash with multiple commands
```yaml
module: gnosari.tools.builtin.bash
class: BashTool
args:
  base_directory: "./workspace"         # Base directory for command execution
  allowed_commands: null                # List of allowed command prefixes
  blocked_commands: null                # List of blocked command prefixes
  max_output_size: 1048576              # Maximum output size in bytes (1MB)
  unsafe_mode: false                    # Disable all safety mechanisms (dangerous)
  commands: null                        # Pre-configured list of commands
  timeout: 30                           # Default timeout for commands (seconds)
  env_vars: {}                          # Default environment variables
  tool_name: "bash"                     # Custom tool name
  tool_description: "Execute bash commands with support for multiple commands, environment variables, and command chaining"
```

**MCP Servers:**
```yaml
# HTTP/SSE Server
url: "https://api.example.com/mcp"      # Required for HTTP/SSE
connection_type: "streamable_http"      # streamable_http|sse|stdio
headers: {}                             # HTTP headers
timeout: 30                             # Connection timeout
sse_read_timeout: 30                    # SSE read timeout
client_session_timeout_seconds: 30      # Session timeout
terminate_on_close: true                # Terminate on close

# STDIO Server
command: "/path/to/server"              # Required for STDIO
connection_type: "stdio"                # Must be stdio
args: []                                # Command arguments
client_session_timeout_seconds: 30      # Session timeout
```

### Knowledge Base Types
- **website**: Web crawling and indexing
- **youtube**: Video transcript extraction
- **pdf**: Document processing
- **text**: Direct text content
- **csv/json**: Structured data
- **directory**: Local file processing

## Minimal Valid Configuration

```yaml
name: "Minimal Team"
agents:
  - name: "Assistant"
    instructions: "Help users with their requests"
```

## Common Patterns

### Multi-Agent with Orchestration
```yaml
name: "Support Team"
agents:
  - name: "Manager"
    instructions: "Coordinate support requests"
    orchestrator: true
    delegation:
      - agent: "Technical"
        instructions: "Use for technical issues"
      - agent: "Billing"
        instructions: "Use for billing questions"
  
  - name: "Technical"
    instructions: "Resolve technical problems"
  
  - name: "Billing"
    instructions: "Handle billing inquiries"
```

### Agent with Tools & Knowledge
```yaml
name: "Research Team"
knowledge:
  - id: "docs"
    name: "Documentation"
    type: "website"
    data: ["https://docs.example.com"]

tools:
  - name: "api"
    module: "gnosari.tools.builtin.api_request"
    class: "APIRequestTool"

agents:
  - name: "Researcher"
    instructions: "Research and analyze information"
    tools: ["api", "knowledge_query"]
    knowledge: ["docs"]
```

### Environment Variables
Use `${VAR_NAME}` or `${VAR_NAME:default}` anywhere in YAML:

```yaml
name: "${TEAM_NAME:My Team}"
agents:
  - name: "${AGENT_NAME:Assistant}"
    model: "${MODEL:gpt-4o}"
    temperature: ${TEMP:0.7}
    instructions: "Work for ${COMPANY:our company}"
```

## Validation Rules

### Required Fields
- Team must have `name`
- Must have at least one agent
- Each agent must have `name` and `instructions`
- Knowledge bases need `id`, `name`, `type`, `data`
- Tools need `name` and either:
  - `module` + `class` (built-in)
  - `url` + `connection_type` (MCP HTTP/SSE)
  - `command` + `connection_type: stdio` (MCP STDIO)

### Constraints
- Agent/tool/knowledge names must be unique within team
- Avoid circular delegation (A→B→A)
- Knowledge bases auto-add `knowledge_query` tool
- First orchestrator agent receives user requests
- Without orchestrator, first agent is entry point

## Quick Reference

**Model Selection**:
- gpt-5: Latest, most capable
- gpt-4o: High quality, complex tasks
- gpt-4o-mini: Cost-effective, simpler tasks

**Temperature Guide**:
- 0.1-0.3: Factual, consistent (technical, data)
- 0.4-0.6: Balanced (general assistance)
- 0.7-1.0: Creative, varied (writing, brainstorming)

**Reasoning Effort**:
- low: Fast responses, simple analysis
- medium: Balanced speed/thoroughness
- high: Deep analysis, complex problems

**Connection Types**:
- streamable_http: Modern HTTP MCP servers
- sse: Server-sent events MCP servers
- stdio: Local process MCP servers