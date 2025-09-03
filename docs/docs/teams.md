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
  - name: "knowledge_base_name"
    type: "website"
    data: ["https://example.com"]

# Tools (optional)
tools:
  - name: tool_name
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
    tools: ["tool1", "tool2"]  # Optional
    knowledge: ["kb1", "kb2"]  # Optional
```

## Team Configuration

### Basic Team Structure

```yaml
name: Content Creation Team

agents:
  - name: ContentManager
    instructions: "Coordinate content creation workflows"
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent

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
name: Advanced Analytics Team

# Knowledge bases for the team
knowledge:
  - name: "company_data"
    type: "website"
    data: ["https://data.company.com"]
  - name: "industry_reports"
    type: "pdf"
    data: ["/data/reports/industry-2024.pdf"]

# Tools for the team
tools:
  - name: delegate_agent
    module: gnosari.tools.delegate_agent
    class: DelegateAgentTool
    args:
      pass

  - name: data_api
    module: gnosari.tools.api_request
    class: APIRequestTool
    args:
      base_url: https://api.analytics.com
      timeout: 30

  - name: database
    module: gnosari.tools.mysql_query
    class: MySQLQueryTool
    args:
      host: ${DB_HOST}
      database: ${DB_NAME}
      username: ${DB_USER}
      password: ${DB_PASSWORD}

# Team agents
agents:
  - name: AnalyticsManager
    instructions: >
      Coordinate analytics projects and delegate tasks to specialists.
      Ensure all analysis is accurate and insights are actionable.
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent
      - knowledge_query
    knowledge: ["company_data", "industry_reports"]

  - name: DataCollector
    instructions: >
      Collect data from various sources including APIs and databases.
      Ensure data quality and completeness.
    model: gpt-4o
    tools:
      - data_api
      - database

  - name: DataAnalyst
    instructions: >
      Analyze collected data and identify patterns, trends, and insights.
      Provide clear, actionable recommendations.
    model: gpt-4o
    tools:
      - database
      - knowledge_query
    knowledge: ["company_data"]

  - name: ReportWriter
    instructions: >
      Create comprehensive reports based on analysis results.
      Present findings in clear, professional format.
    model: gpt-4o
    tools:
      - knowledge_query
    knowledge: ["industry_reports"]
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
    tools:
      - delegate_agent
```

:::info Orchestrator Requirements
Orchestrator agents must have `orchestrator: true` and access to the `delegate_agent` tool.
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
    tools:
      - delegate_agent

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

## Related Topics

- [Agents](/docs/agents) - Learn about individual agent configuration
- [Orchestration](/docs/orchestration) - Understand agent coordination and workflow management
- [Handoffs](/docs/handoffs) - Learn about control transfer mechanisms
- [Delegation](/docs/delegation) - Understand task assignment and response handling
- [Tools](/docs/tools/intro) - Explore tools for team capabilities
- [Knowledge](/docs/knowledge) - Understand knowledge base integration
- [Quickstart](/docs/quickstart) - Create your first team

## Next Steps

Now that you understand teams, learn how to:
- [Configure individual agents](/docs/agents) with proper instructions
- [Set up orchestration](/docs/orchestration) for team coordination
- [Use handoffs](/docs/handoffs) for control transfer
- [Implement delegation](/docs/delegation) for task assignment
- [Add tools](/docs/tools/intro) to enhance team capabilities
- [Set up knowledge bases](/docs/knowledge) for information access
- [Create your first team](/docs/quickstart) with the quickstart guide