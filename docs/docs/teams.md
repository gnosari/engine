---
sidebar_position: 4
---

# Teams

Teams are collections of agents that work together to accomplish complex tasks. A well-designed team leverages the strengths of different agents through coordination, specialization, and collaboration.

## What are Teams?

Teams in Gnosari AI Teams are:
- **Collections of agents** working toward common goals
- **Coordinated workflows** managed by orchestrator agents
- **Tool and knowledge sharing** among team members
- **Structured collaboration** through task delegation
- **Configurable entities** defined in YAML

:::info Team vs Individual Agents
While individual agents can handle simple tasks, teams excel at complex, multi-step workflows that require different types of expertise and coordination.
:::

## Team Structure

A team configuration consists of several key sections:

```yaml
name: Team Name
description: "Optional team description"

# Knowledge bases (optional)
knowledge:
  - id: "knowledge_base_id"  # Unique identifier for referencing
    name: "knowledge_base_name"
    type: "website"
    data: ["https://example.com"]

# Tools (optional)
tools:
  - name: tool_name
    id: tool_id  # Unique identifier for referencing
    module: gnosari.tools.tool_module
    class: ToolClassName
    args:
      # Tool configuration

# Agents (required)
agents:
  - name: AgentName
    instructions: "Agent behavior and responsibilities"
    model: gpt-4o
    orchestrator: true  # Optional
    tools: ["tool_id1", "tool_id2"]  # Optional - references tool IDs
    knowledge: ["kb_id1", "kb_id2"]  # Optional - references knowledge base IDs
```

:::info Environment Variables
Team configurations support environment variable substitution using `${VAR_NAME}` or `${VAR_NAME:default_value}` syntax. This works throughout the entire configuration - in team names, agent instructions, tool configurations, and more. See [Environment Variables](#environment-variables) section below.
:::

## Team Configuration

### Basic Team Structure

```yaml
name: Content Creation Team

agents:
  - name: ContentManager
    instructions: "Coordinate content creation workflows"
    orchestrator: true
    model: gpt-4o
    delegation:
      - agent: Researcher
        instructions: "Use for research and information gathering"
      - agent: Writer
        instructions: "Use for content writing tasks"

  - name: Researcher
    instructions: "Research topics and gather information"
    model: gpt-4o

  - name: Writer
    instructions: "Create engaging, well-structured content"
    model: gpt-4o
```

:::tip Team Naming
Use descriptive names that clearly indicate the team's purpose (e.g., `Customer Support Team`, `Data Analysis Team`, `Content Creation Team`).
:::

### Advanced Team Configuration

```yaml
name: "Advanced Analytics Team"
description: "Comprehensive data analytics team with full coordination capabilities"

# Team configuration settings
config:
  max_turns: 100  # Maximum conversation turns per execution
  timeout: 300    # Team execution timeout in seconds

# Knowledge bases for the team (with custom Embedchain configuration)
knowledge:
  - id: "company_data"
    name: "Company Data Sources"
    description: "Internal company data and metrics"
    type: "website"
    config:
      # Custom Embedchain configuration for websites
      llm:
        provider: "openai"
        config:
          model: "${KNOWLEDGE_LLM_MODEL:gpt-4o}"
          temperature: ${KNOWLEDGE_LLM_TEMP:0.1}
          max_tokens: 1000
      embedder:
        provider: "openai"
        config:
          model: "${EMBEDDING_MODEL:text-embedding-3-small}"
      chunker:
        chunk_size: ${WEB_CHUNK_SIZE:1200}
        chunk_overlap: ${WEB_CHUNK_OVERLAP:200}
        length_function: "len"
    data: ["https://data.company.com", "https://metrics.company.com"]
  
  - id: "industry_reports"
    name: "Industry Research"
    description: "External industry reports and benchmarks"
    type: "pdf"
    config:
      # Custom configuration optimized for PDF documents
      llm:
        provider: "openai"
        config:
          model: "${PDF_LLM_MODEL:gpt-4o}"
          temperature: ${PDF_LLM_TEMP:0.2}
          max_tokens: 1500
      embedder:
        provider: "openai"
        config:
          model: "${EMBEDDING_MODEL:text-embedding-3-small}"
      chunker:
        chunk_size: ${PDF_CHUNK_SIZE:1000}
        chunk_overlap: ${PDF_CHUNK_OVERLAP:150}
        length_function: "len"
    data: ["/data/reports/industry-2024.pdf", "/data/benchmarks/market-analysis.pdf"]
  
  - id: "technical_docs"
    name: "Technical Documentation"
    description: "API documentation and technical specifications"
    type: "website"
    config:
      # Optimized for technical documentation
      llm:
        provider: "openai"
        config:
          model: "${TECH_LLM_MODEL:gpt-4o}"
          temperature: 0.1
      embedder:
        provider: "openai"
        config:
          model: "text-embedding-3-small"
      chunker:
        chunk_size: 800  # Smaller chunks for technical content
        chunk_overlap: 100
        length_function: "len"
    data: ["https://docs.company.com"]
  
  - id: "custom_procedures"
    name: "Company Procedures"
    description: "Internal procedures and guidelines"
    type: "text"
    config:
      # Minimal configuration for text content
      chunker:
        chunk_size: ${TEXT_CHUNK_SIZE:600}
        chunk_overlap: ${TEXT_CHUNK_OVERLAP:80}
        length_function: "len"
    data:
      - |
        Analytics Team Procedures:
        
        Data Collection Guidelines:
        - Always validate data sources before processing
        - Document data lineage and transformation steps
        - Implement data quality checks at each stage
        - Maintain backup copies of raw data
        
        Analysis Standards:
        - Use statistical significance testing
        - Provide confidence intervals for estimates
        - Document assumptions and limitations
        - Peer review all analysis before publication
        
        Reporting Requirements:
        - Include executive summary for all reports
        - Provide detailed methodology section
        - Present findings with clear visualizations
        - Include recommendations and next steps

# Tools for the team (built-in + MCP servers)
tools:
  # Built-in API tool
  - name: data_api
    module: gnosari.tools.api_request
    class: APIRequestTool
    args:
      base_url: "${API_BASE_URL:https://api.analytics.com}"
      base_headers:
        Authorization: "Bearer ${API_TOKEN}"
        Content-Type: "application/json"
        User-Agent: "Analytics-Team/1.0"
      timeout: ${API_TIMEOUT:30}
      verify_ssl: true
      max_retries: 3

  # Built-in database tool
  - name: database
    module: gnosari.tools.mysql_query
    class: MySQLQueryTool
    args:
      host: "${DB_HOST:localhost}"
      port: ${DB_PORT:3306}
      database: "${DB_NAME:analytics}"
      username: "${DB_USER:analyst}"
      password: "${DB_PASSWORD}"
      pool_size: ${DB_POOL_SIZE:10}
      max_overflow: 20
      query_timeout: ${DB_TIMEOUT:60}
      charset: "utf8mb4"

  # Built-in file operations tool
  - name: file_ops
    module: gnosari.tools.file_operations
    class: FileOperationsTool
    args:
      base_directory: "${WORKSPACE_DIR:./workspace}"
      allowed_extensions: [".csv", ".json", ".md", ".xlsx", ".pdf"]
      max_file_size: ${MAX_FILE_SIZE:10485760}  # 10MB
      create_directories: true

  # Built-in website content tool
  - name: web_content
    module: gnosari.tools.website_content
    class: WebsiteContentTool
    args:
      timeout: 30
      max_content_length: 50000
      user_agent: "Analytics-Bot/1.0"

  # MCP Server - Slack integration
  - name: Slack Integration
    id: slack_mcp
    url: "${SLACK_MCP_URL:https://slack-mcp.company.com}"
    connection_type: streamable_http
    headers:
      Authorization: "Bearer ${SLACK_BOT_TOKEN}"
      X-Team-ID: "${SLACK_TEAM_ID}"
    timeout: ${SLACK_TIMEOUT:45}
    sse_read_timeout: 60
    terminate_on_close: true

  # MCP Server - Jira integration
  - name: Jira Integration
    id: jira_mcp
    url: "${JIRA_MCP_URL:https://jira-mcp.company.com}"
    connection_type: streamable_http
    headers:
      Authorization: "Basic ${JIRA_AUTH_TOKEN}"
      X-Atlassian-Token: "no-check"
    timeout: 30

  # MCP Server - Local file system
  - name: File System Access
    id: filesystem_mcp
    command: "${MCP_FS_PATH:/usr/local/bin/filesystem-mcp-server}"
    connection_type: stdio
    args:
      - "--root-path"
      - "${FS_ROOT:/data/analytics}"
      - "--allowed-extensions"
      - ".csv,.json,.xlsx,.pdf"
      - "--max-file-size"
      - "${FS_MAX_SIZE:52428800}"  # 50MB
    client_session_timeout_seconds: 120

# Team agents with full configuration options
agents:
  - name: "AnalyticsManager"
    instructions: >
      You are the analytics manager responsible for coordinating data analysis projects.
      
      Key responsibilities:
      - Coordinate analytics projects and delegate tasks to specialists
      - Ensure all analysis is accurate and insights are actionable
      - Manage project timelines and quality standards
      - Communicate results to stakeholders
      
      When coordinating:
      - Break down complex analysis requests into specific tasks
      - Delegate data collection to DataCollector
      - Assign analysis work to DataAnalyst
      - Have ReportWriter create final documentation
      - Use Slack for team communication and Jira for project tracking
    orchestrator: true
    model: "${MANAGER_MODEL:gpt-4o}"
    temperature: ${MANAGER_TEMP:0.2}
    reasoning_effort: "${MANAGER_REASONING:medium}"
    tools:
      - knowledge_query
      - file_ops
      - slack_mcp
      - jira_mcp
    knowledge: ["company_data", "industry_reports", "technical_docs"]
    can_transfer_to:
      - agent: SeniorAnalyst
        instructions: "Transfer complex technical analysis that requires senior expertise"
    delegation:
      - agent: DataCollector
        instructions: "Use for data collection and preparation tasks"
      - agent: DataAnalyst
        instructions: "Use for data analysis and statistical work"
      - agent: ReportWriter
        instructions: "Use for creating reports and documentation"

  - name: "DataCollector"
    instructions: >
      You are a data collector responsible for gathering and preparing data from various sources.
      
      Responsibilities:
      - Collect data from APIs, databases, and file systems
      - Ensure data quality and completeness
      - Clean and preprocess data for analysis
      - Document data sources and collection methods
      
      Always validate data integrity and report any quality issues.
    model: "${COLLECTOR_MODEL:gpt-4o}"
    temperature: ${COLLECTOR_TEMP:0.1}
    tools:
      - data_api
      - database
      - file_ops
      - web_content
      - filesystem_mcp
    knowledge: ["technical_docs"]
    delegation:
      - agent: DataValidator
        instructions: "Use for data quality validation and verification"

  - name: "DataAnalyst"
    instructions: >
      You are a data analyst who analyzes data and identifies patterns, trends, and insights.
      
      Responsibilities:
      - Perform statistical analysis and data mining
      - Identify patterns, trends, and anomalies
      - Create visualizations and charts
      - Provide clear, actionable recommendations
      
      Focus on accuracy and provide confidence intervals for your findings.
    model: "${ANALYST_MODEL:claude-3-5-sonnet-20241022}"
    temperature: ${ANALYST_TEMP:0.3}
    reasoning_effort: "high"
    tools:
      - database
      - knowledge_query
      - file_ops
      - filesystem_mcp
    knowledge: ["company_data", "industry_reports"]
    delegation:
      - agent: StatisticalExpert
        instructions: "Use for advanced statistical modeling and analysis"

  - name: "ReportWriter"
    instructions: >
      You are a report writer who creates comprehensive reports and documentation.
      
      Responsibilities:
      - Create detailed analysis reports
      - Present findings in clear, professional format
      - Generate executive summaries
      - Ensure reports meet company standards
      
      Always include methodology, limitations, and recommendations.
    model: "${WRITER_MODEL:gpt-4o}"
    temperature: ${WRITER_TEMP:0.4}
    tools:
      - knowledge_query
      - file_ops
      - web_content
    knowledge: ["industry_reports", "technical_docs"]

  - name: "DataValidator"
    instructions: >
      You are a data validator who ensures data quality and accuracy.
      Validate data integrity, check for anomalies, and verify data sources.
    model: "gpt-4o"
    temperature: 0.1
    tools:
      - database
      - file_ops

  - name: "StatisticalExpert"
    instructions: >
      You are a statistical expert who handles advanced statistical modeling and analysis.
      Provide expert-level statistical insights and validate analytical approaches.
    model: "claude-3-5-sonnet-20241022"
    temperature: 0.2
    reasoning_effort: "high"
    tools:
      - database
      - knowledge_query
    knowledge: ["industry_reports"]

  - name: "SeniorAnalyst"
    instructions: >
      You are a senior analyst who handles complex technical analysis requiring deep expertise.
      Review and validate complex analytical work and provide strategic insights.
    model: "gpt-4o"
    temperature: 0.2
    reasoning_effort: "high"
    tools:
      - database
      - knowledge_query
      - file_ops
      - slack_mcp
    knowledge: ["company_data", "industry_reports", "technical_docs"]
```

## Team Roles and Responsibilities

### Orchestrator Agents
Coordination agents that manage team workflows:

```yaml
agents:
  - name: ProjectManager
    instructions: >
      You are a project manager who coordinates team activities.
      Break down complex tasks, delegate to appropriate specialists,
      and ensure all work is completed to quality standards.
    orchestrator: true
    model: gpt-4o
```

:::info Orchestrator as Entry Point
When running a team without specifying a particular agent, **orchestrator agents are the first to receive user requests**. If your team has multiple orchestrator agents, the first one defined in the configuration will handle the initial user input.
:::

:::info Orchestrator Requirements
Orchestrator agents must have `orchestrator: true` - delegation capabilities are automatically enabled.
:::

### Specialist Agents
Focused agents that handle specific types of tasks:

```yaml
agents:
  - name: TechnicalWriter
    instructions: >
      You are a technical writer who creates clear, accurate documentation.
      Focus on explaining complex concepts in simple terms.
    model: gpt-4o
    tools:
      - knowledge_query
    knowledge: ["technical_docs"]
```

### Generalist Agents
Versatile agents that can handle multiple types of tasks:

```yaml
agents:
  - name: GeneralAssistant
    instructions: >
      You are a general assistant who can help with various tasks.
      Adapt your approach based on the specific request.
    model: gpt-4o
    tools:
      - api_request
      - knowledge_query
```

## Team Workflow Patterns

### 1. **Sequential Workflow**
Tasks flow from one agent to the next in sequence:

```yaml
agents:
  - name: Coordinator
    instructions: "Coordinate sequential tasks"
    orchestrator: true
    model: gpt-4o

  - name: Researcher
    instructions: "Research and gather information"
    model: gpt-4o

  - name: Analyst
    instructions: "Analyze research findings"
    model: gpt-4o

  - name: Writer
    instructions: "Write based on analysis"
    model: gpt-4o
```

### 2. **Parallel Workflow**
Multiple agents work on different aspects simultaneously:

```yaml
agents:
  - name: ProjectManager
    instructions: "Coordinate parallel work streams"
    orchestrator: true
    tools:
      - delegate_agent

  - name: DataAnalyst
    instructions: "Analyze data and metrics"
    model: gpt-4o

  - name: ContentCreator
    instructions: "Create content and materials"
    model: gpt-4o

  - name: QualityReviewer
    instructions: "Review and ensure quality"
    model: gpt-4o
```

### 3. **Hierarchical Workflow**
Agents have different levels of authority and responsibility:

```yaml
agents:
  - name: Director
    instructions: "Set strategy and high-level direction"
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent

  - name: Manager
    instructions: "Manage specific projects and teams"
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent

  - name: Specialist
    instructions: "Execute specific tasks"
    model: gpt-4o
```

## Team Design Principles

### 1. **Clear Role Definition**
Each agent should have a well-defined role:

```yaml
agents:
  - name: CustomerSupportAgent
    instructions: >
      You are a customer support agent responsible for:
      - Resolving customer issues
      - Providing product information
      - Escalating complex problems
      - Maintaining customer satisfaction
```

### 2. **Appropriate Tool Assignment**
Assign tools based on agent responsibilities:

```yaml
agents:
  - name: DataScientist
    instructions: "Analyze data and provide insights"
    tools:
      - mysql_query      # For database access
      - api_request      # For external data
      - knowledge_query  # For reference information
```

### 3. **Knowledge Base Access**
Provide relevant knowledge to agents:

```yaml
agents:
  - name: TechnicalSupport
    instructions: "Provide technical support"
    tools:
      - knowledge_query
    knowledge: ["technical_docs", "troubleshooting_guides"]
```

### 4. **Model Selection**
Choose appropriate models for different roles:

```yaml
agents:
  - name: CreativeWriter
    model: gpt-4o  # Good for creative tasks
    
  - name: DataAnalyst
    model: claude-3-5-sonnet-20241022  # Good for analysis
    
  - name: CodeReviewer
    model: deepseek-chat  # Good for technical tasks
```

## Team Communication

### Internal Communication
Agents communicate through:
- **Task delegation** via the `delegate_agent` tool
- **Shared context** through conversation history
- **Knowledge bases** for information sharing
- **Tool results** passed between agents

### External Communication
Teams interact with users through:
- **Orchestrator responses** that coordinate team output
- **Specialist responses** for specific expertise
- **Structured workflows** that provide comprehensive results

:::tip Communication Flow
Design clear communication patterns in your team to ensure effective collaboration and user interaction.
:::

## Team Performance

### Coordination Efficiency
- **Clear delegation patterns** reduce confusion
- **Appropriate specialization** improves quality
- **Effective tool usage** enhances capabilities
- **Knowledge sharing** improves consistency

### Quality Assurance
- **Review processes** ensure output quality
- **Specialist expertise** provides accuracy
- **Knowledge validation** maintains consistency
- **Error handling** manages failures gracefully

### Scalability
- **Modular design** allows easy expansion
- **Clear interfaces** enable agent replacement
- **Standardized patterns** support replication
- **Tool abstraction** simplifies maintenance

:::info Team Optimization
Monitor team performance and adjust agent roles, tools, and workflows based on results and user feedback.
:::

## Common Team Patterns

### 1. **Customer Support Team**
```yaml
name: Customer Support Team
agents:
  - name: SupportManager
    instructions: "Coordinate support requests and delegate to specialists"
    orchestrator: true
    tools:
      - delegate_agent
      - knowledge_query
    knowledge: ["support_docs", "faq"]

  - name: TechnicalSupport
    instructions: "Handle technical issues and troubleshooting"
    tools:
      - knowledge_query
    knowledge: ["technical_docs"]

  - name: BillingSupport
    instructions: "Handle billing and account questions"
    tools:
      - api_request
```

### 2. **Content Creation Team**
```yaml
name: Content Creation Team
agents:
  - name: ContentManager
    instructions: "Coordinate content creation from research to publication"
    orchestrator: true
    tools:
      - delegate_agent
      - knowledge_query
    knowledge: ["brand_guidelines", "content_standards"]

  - name: Researcher
    instructions: "Research topics and gather information"
    tools:
      - api_request
      - knowledge_query
    knowledge: ["research_sources"]

  - name: Writer
    instructions: "Create engaging, well-structured content"
    tools:
      - knowledge_query
    knowledge: ["writing_guidelines"]

  - name: Editor
    instructions: "Review and improve content quality"
    tools:
      - knowledge_query
    knowledge: ["style_guide"]
```

### 3. **Data Analysis Team**
```yaml
name: Data Analysis Team
agents:
  - name: AnalyticsManager
    instructions: "Coordinate data analysis projects and ensure quality"
    orchestrator: true
    tools:
      - delegate_agent
      - knowledge_query
    knowledge: ["business_context"]

  - name: DataCollector
    instructions: "Collect and prepare data from various sources"
    tools:
      - mysql_query
      - api_request

  - name: DataAnalyst
    instructions: "Analyze data and identify insights"
    tools:
      - mysql_query
      - knowledge_query
    knowledge: ["analytics_methods"]

  - name: ReportGenerator
    instructions: "Create reports and visualizations"
    tools:
      - knowledge_query
    knowledge: ["reporting_standards"]
```

## Team Limitations

### Coordination Complexity
- **More agents** increase coordination overhead
- **Complex workflows** can be difficult to manage
- **Tool dependencies** may create bottlenecks
- **Knowledge conflicts** can cause inconsistencies

### Resource Requirements
- **Multiple models** increase API costs
- **Tool usage** may have rate limits
- **Knowledge bases** require storage and processing
- **Complex teams** need more computational resources

### Maintenance Overhead
- **Agent updates** require coordination
- **Tool changes** affect multiple agents
- **Knowledge updates** need distribution
- **Workflow changes** impact team dynamics

:::warning Team Complexity
Balance team complexity with maintainability. Start simple and add complexity as needed.
:::

## Environment Variables

Team configurations support environment variable substitution throughout the entire YAML file using `${VAR_NAME}` or `${VAR_NAME:default_value}` syntax.

### Basic Environment Variable Usage

```yaml
name: "${TEAM_NAME:My AI Team}"
description: "${TEAM_DESC:A configurable AI team}"

knowledge:
  - name: "${KB_NAME:docs}"
    type: "website"
    data: ["${DOCS_URL:https://docs.example.com}"]

tools:
  - name: api_tool
    module: gnosari.tools.api_request
    class: APIRequestTool
    args:
      base_url: "${API_BASE_URL:https://api.example.com}"
      timeout: ${API_TIMEOUT:30}

agents:
  - name: "${AGENT_NAME:Assistant}"
    instructions: "${AGENT_INSTRUCTIONS:You are a helpful AI assistant}"
    model: "${MODEL:gpt-4o}"
    temperature: ${TEMPERATURE:0.7}
    tools: ["api_tool"]
    knowledge: ["${KB_NAME:docs}"]
```

### Environment Variables in Agent Instructions

You can use environment variables in agent instructions for dynamic behavior:

```yaml
agents:
  - name: CustomerSupport
    instructions: >
      You are a customer support agent for ${COMPANY_NAME:Our Company}.
      
      Company policies:
      - Support hours: ${SUPPORT_HOURS:9 AM - 5 PM EST}
      - Escalation contact: ${ESCALATION_EMAIL:support@company.com}
      - Knowledge base: ${KB_URL:https://help.company.com}
      
      Always maintain a ${TONE:professional and helpful} tone.
    model: "${SUPPORT_MODEL:gpt-4o}"
    temperature: ${SUPPORT_TEMPERATURE:0.3}
```

### Setting Environment Variables

Set environment variables before running your team:

```bash
export TEAM_NAME="Production Support Team"
export COMPANY_NAME="Acme Corp"
export SUPPORT_HOURS="24/7"
export API_BASE_URL="https://api.acme.com"
export MODEL="gpt-4o"
```

:::tip Security Best Practice
Use environment variables for sensitive information like API keys, database passwords, and company-specific data instead of hardcoding them in YAML files.
:::

## Related Topics

- [Agents](agents) - Learn about individual agent configuration
- [Orchestration](coordination/orchestration) - Understand agent coordination and workflow management
- [Handoffs](coordination/handoffs) - Learn about control transfer mechanisms
- [Delegation](coordination/delegation) - Understand task assignment and response handling
- [Tools](tools/intro) - Explore tools for team capabilities
- [Knowledge Bases](knowledge-bases/intro) - Understand knowledge base integration
- [MCP Servers](mcp-servers) - Connect to external APIs and services
- [Quickstart](quickstart) - Create your first team

## Next Steps

Now that you understand teams, learn how to:
- [Configure individual agents](agents) with proper instructions
- [Set up orchestration](coordination/orchestration) for team coordination
- [Use handoffs](coordination/handoffs) for control transfer
- [Implement delegation](coordination/delegation) for task assignment
- [Add tools](tools/intro) to enhance team capabilities
- [Set up knowledge bases](knowledge-bases/intro) for information access
- [Create your first team](quickstart) with the quickstart guide