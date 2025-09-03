---
sidebar_position: 8
---

# Delegation

Delegation in Gnosari AI Teams is the mechanism for assigning specific tasks to other agents while maintaining control of the conversation. When an agent delegates a task, it receives a response back and can continue the conversation.

## What is Delegation?

Delegation is:
- **Task Assignment**: Assigning specific tasks to other agents
- **Response Handling**: Receiving responses back from delegated agents
- **Control Retention**: The delegating agent maintains conversation control
- **Two-Way Communication**: Request and response between agents
- **Workflow Coordination**: Managing multi-agent task execution

:::info Delegation vs Handoffs
Delegation assigns tasks and receives responses back, while handoffs transfer complete control without returning responses.
:::

## Delegation Configuration

Delegation is configured using the `delegate_agent` tool in agent configurations:

```yaml
tools:
  - name: delegate_agent
    module: gnosari.tools.delegate_agent
    class: DelegateAgentTool
    args:
      pass

agents:
  - name: ProjectManager
    instructions: "Coordinate project tasks and delegate to specialists"
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent  # Required for delegation

  - name: TechnicalWriter
    instructions: "Create technical documentation"
    model: gpt-4o

  - name: Designer
    instructions: "Create designs and visual content"
    model: gpt-4o
```

:::tip Delegation Requirements
Only agents with `orchestrator: true` and the `delegate_agent` tool can delegate tasks to other agents.
:::

## When to Use Delegation

### 1. **Task Distribution**
When you need to assign specific tasks to specialists:

```yaml
agents:
  - name: ContentManager
    instructions: >
      Coordinate content creation. Delegate writing tasks to ContentWriter,
      design tasks to Designer, and research tasks to Researcher.
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent

  - name: ContentWriter
    instructions: "Write engaging content based on requirements"
    model: gpt-4o

  - name: Designer
    instructions: "Create visual designs and layouts"
    model: gpt-4o

  - name: Researcher
    instructions: "Research topics and gather information"
    model: gpt-4o
```

### 2. **Parallel Work**
When you need multiple agents working on different aspects:

```yaml
agents:
  - name: ProjectCoordinator
    instructions: >
      Coordinate project execution. Delegate technical tasks to TechnicalTeam,
      business tasks to BusinessTeam, and quality tasks to QualityTeam.
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent

  - name: TechnicalTeam
    instructions: "Handle technical implementation and development"
    model: gpt-4o

  - name: BusinessTeam
    instructions: "Handle business requirements and stakeholder communication"
    model: gpt-4o

  - name: QualityTeam
    instructions: "Handle quality assurance and testing"
    model: gpt-4o
```

### 3. **Workflow Coordination**
When managing complex, multi-step processes:

```yaml
agents:
  - name: WorkflowManager
    instructions: >
      Manage complex workflows. Delegate research to Researcher,
      analysis to Analyst, and reporting to Reporter.
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent

  - name: Researcher
    instructions: "Research topics and gather data"
    model: gpt-4o

  - name: Analyst
    instructions: "Analyze data and provide insights"
    model: gpt-4o

  - name: Reporter
    instructions: "Create reports and documentation"
    model: gpt-4o
```

## Delegation Examples

### Example 1: Content Creation Workflow

```yaml
name: Content Creation Team

tools:
  - name: delegate_agent
    module: gnosari.tools.delegate_agent
    class: DelegateAgentTool
    args:
      pass

agents:
  - name: ContentManager
    instructions: >
      Coordinate content creation workflows:
      1. Delegate research to Researcher
      2. Delegate writing to Writer
      3. Delegate editing to Editor
      4. Compile final content
      
      Always provide clear, specific tasks to delegated agents.
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent

  - name: Researcher
    instructions: >
      Research topics and gather information. Provide comprehensive,
      well-sourced information for content creation.
    model: gpt-4o

  - name: Writer
    instructions: >
      Write engaging, well-structured content based on research.
      Focus on clarity, engagement, and audience needs.
    model: gpt-4o

  - name: Editor
    instructions: >
      Review and edit content for quality, accuracy, and style.
      Ensure content meets standards and is ready for publication.
    model: gpt-4o
```

### Example 2: Data Analysis Workflow

```yaml
name: Data Analysis Team

tools:
  - name: delegate_agent
    module: gnosari.tools.delegate_agent
    class: DelegateAgentTool
    args:
      pass

  - name: mysql_query
    module: gnosari.tools.mysql_query
    class: MySQLQueryTool
    args:
      host: ${DB_HOST}
      database: ${DB_NAME}
      username: ${DB_USER}
      password: ${DB_PASSWORD}

agents:
  - name: AnalysisManager
    instructions: >
      Coordinate data analysis projects:
      1. Delegate data collection to DataCollector
      2. Delegate analysis to DataAnalyst
      3. Delegate reporting to ReportGenerator
      4. Compile final analysis
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent

  - name: DataCollector
    instructions: >
      Collect and prepare data from various sources.
      Use the mysql_query tool to gather data from databases.
    model: gpt-4o
    tools:
      - mysql_query

  - name: DataAnalyst
    instructions: >
      Analyze collected data and identify patterns, trends, and insights.
      Provide clear, actionable analysis results.
    model: gpt-4o

  - name: ReportGenerator
    instructions: >
      Create comprehensive reports based on analysis results.
      Present findings in clear, professional format.
    model: gpt-4o
```

### Example 3: Customer Support Workflow

```yaml
name: Customer Support Team

tools:
  - name: delegate_agent
    module: gnosari.tools.delegate_agent
    class: DelegateAgentTool
    args:
      pass

  - name: knowledge_query
    # Automatically added when knowledge bases are defined

knowledge:
  - name: "support_docs"
    type: "website"
    data: ["https://support.company.com"]
  - name: "faq"
    type: "text"
    data: ["Q: How do I reset my password? A: Click forgot password..."]

agents:
  - name: SupportCoordinator
    instructions: >
      Coordinate customer support requests:
      1. Delegate technical issues to TechnicalSupport
      2. Delegate billing issues to BillingSupport
      3. Delegate general questions to GeneralSupport
      4. Compile final response
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent
      - knowledge_query
    knowledge: ["support_docs", "faq"]

  - name: TechnicalSupport
    instructions: >
      Handle technical support issues using knowledge bases.
      Provide step-by-step solutions and troubleshooting guidance.
    model: gpt-4o
    tools:
      - knowledge_query
    knowledge: ["support_docs"]

  - name: BillingSupport
    instructions: >
      Handle billing and account issues.
      Provide clear information about charges, payments, and account status.
    model: gpt-4o

  - name: GeneralSupport
    instructions: >
      Handle general customer questions and provide information.
      Use knowledge bases to provide accurate, helpful responses.
    model: gpt-4o
    tools:
      - knowledge_query
    knowledge: ["faq"]
```

## Delegation Best Practices

### 1. **Clear Task Instructions**
Provide specific, actionable tasks to delegated agents:

```yaml
agents:
  - name: TaskManager
    instructions: >
      When delegating tasks, be specific about:
      - What needs to be done
      - Expected output format
      - Any constraints or requirements
      - Deadline or priority level
      
      Example: "Research renewable energy trends for 2024 and provide
      a summary with key statistics and market insights."
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent
```

### 2. **Appropriate Agent Selection**
Choose the right agent for each task:

```yaml
agents:
  - name: WorkflowCoordinator
    instructions: >
      Delegate tasks to appropriate specialists:
      - Technical questions → TechnicalExpert
      - Creative tasks → CreativeSpecialist
      - Data analysis → DataAnalyst
      - Writing tasks → ContentWriter
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent
```

### 3. **Response Integration**
Effectively integrate responses from delegated agents:

```yaml
agents:
  - name: ProjectManager
    instructions: >
      When receiving responses from delegated agents:
      - Review the quality and completeness
      - Integrate multiple responses coherently
      - Provide feedback if needed
      - Compile final deliverables
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent
```

### 4. **Error Handling**
Handle delegation failures gracefully:

```yaml
agents:
  - name: TaskCoordinator
    instructions: >
      Handle delegation errors appropriately:
      - If an agent can't complete a task, try another agent
      - Provide clearer instructions if needed
      - Escalate to handoffs if delegation isn't working
      - Always provide feedback to users about progress
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent
```

## Delegation Monitoring

### Debug Mode
Use debug mode to see detailed delegation information:

```bash
poetry run gnosari --config "team.yaml" --message "Your message" --debug
```

:::tip Delegation Debugging
Debug mode shows detailed delegation information including:
- Which agent was contacted
- The message sent to the delegated agent
- The response received from the delegated agent
- Any errors or issues during delegation
:::

### Delegation Logging
The system automatically logs delegation activities:

```
🤝 DELEGATION STARTED - Target Agent: 'TechnicalWriter' | Message: 'Create technical documentation for API endpoints'
[TechnicalWriter] Response: I'll create comprehensive API documentation...
✅ DELEGATION SUCCESSFUL - Agent 'TechnicalWriter' responded with 1,234 characters
```

## Delegation Limitations

### 1. **Orchestrator Requirement**
Only agents with `orchestrator: true` can use the `delegate_agent` tool.

### 2. **Tool Dependency**
Delegation requires the `delegate_agent` tool to be properly configured.

### 3. **Response Handling**
Delegated agents must provide responses for the delegation to be successful.

### 4. **Context Preservation**
While context is maintained, complex multi-step delegations can become complex.

:::warning Delegation Considerations
- Delegation requires proper tool configuration
- Only orchestrator agents can delegate tasks
- Ensure delegated agents can handle the assigned tasks
- Consider response quality and integration
:::

## Related Topics

- [Handoffs](/docs/handoffs) - Learn about control transfer mechanisms
- [Orchestration](/docs/orchestration) - Understand overall coordination patterns
- [Agents](/docs/agents) - Learn about individual agent configuration
- [Teams](/docs/teams) - Understand team structure and coordination
- [Tools](/docs/tools/delegate-agent) - Detailed delegate agent tool documentation
- [Quickstart](/docs/quickstart) - Create your first team with delegation

## Next Steps

Now that you understand delegation, learn about the complementary mechanism:

- [Handoffs](/docs/handoffs) - Control transfer without response handling
- [Orchestration](/docs/orchestration) - Overall coordination strategies
- [Delegate Agent Tool](/docs/tools/delegate-agent) - Detailed tool documentation
- [Agents](/docs/agents) - Configure orchestrator agents
- [Teams](/docs/teams) - Set up teams with delegation capabilities
- [Quickstart](/docs/quickstart) - Build your first team with delegation