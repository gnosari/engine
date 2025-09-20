---
sidebar_position: 3
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

Delegation is configured using the `delegation` field for any agent:

```yaml
agents:
  - name: ProjectManager
    instructions: "Coordinate project tasks and delegate to specialists"
    orchestrator: true
    model: gpt-4o
    delegation:
      - agent: TechnicalWriter
        instructions: "Use for creating technical documentation"
      - agent: Designer
        instructions: "Use for design and visual content creation"

  - name: TechnicalWriter
    instructions: "Create technical documentation and delegate reviews"
    model: gpt-4o
    delegation:
      - agent: TechnicalReviewer
        instructions: "Use for reviewing technical content"

  - name: Designer
    instructions: "Create designs and visual content"
    model: gpt-4o
    delegation:
      - agent: DesignReviewer
        instructions: "Use for design review and feedback"

  - name: TechnicalReviewer
    instructions: "Review technical documentation for accuracy"
    model: gpt-4o

  - name: DesignReviewer
    instructions: "Review designs for consistency and usability"
    model: gpt-4o
```

:::tip Delegation Configuration
Delegation can be configured for any agent using the `delegation` field in the agent configuration.
:::

:::warning Circular Delegation
Avoid circular delegation patterns where Agent A delegates to Agent B, and Agent B delegates back to Agent A. This can create infinite loops and cause the system to hang. Design clear delegation hierarchies with well-defined responsibilities.
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
    delegation:
      - agent: ContentWriter
        instructions: "Use for writing engaging content"
      - agent: Designer
        instructions: "Use for visual designs and layouts"
      - agent: Researcher
        instructions: "Use for research and information gathering"

  - name: ContentWriter
    instructions: "Write engaging content and delegate editing tasks"
    model: gpt-4o
    delegation:
      - agent: Editor
        instructions: "Use for content editing and proofreading"

  - name: Designer
    instructions: "Create visual designs and delegate asset creation"
    model: gpt-4o
    delegation:
      - agent: AssetCreator
        instructions: "Use for creating specific design assets"

  - name: Researcher
    instructions: "Research topics and delegate fact-checking"
    model: gpt-4o
    delegation:
      - agent: FactChecker
        instructions: "Use for verifying research accuracy"

  - name: Editor
    instructions: "Edit and proofread content for quality"
    model: gpt-4o

  - name: AssetCreator
    instructions: "Create specific design assets and graphics"
    model: gpt-4o

  - name: FactChecker
    instructions: "Verify accuracy of research information"
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
    delegation:
      - agent: TechnicalTeam
        instructions: "Use for technical implementation and development"
      - agent: BusinessTeam
        instructions: "Use for business requirements and stakeholder communication"
      - agent: QualityTeam
        instructions: "Use for quality assurance and testing"

  - name: TechnicalTeam
    instructions: "Handle technical implementation and delegate code reviews"
    model: gpt-4o
    delegation:
      - agent: CodeReviewer
        instructions: "Use for code review and technical validation"
      - agent: Architect
        instructions: "Use for architectural decisions"

  - name: BusinessTeam
    instructions: "Handle business requirements and delegate stakeholder tasks"
    model: gpt-4o
    delegation:
      - agent: StakeholderLiaison
        instructions: "Use for stakeholder communication"
      - agent: RequirementsAnalyst
        instructions: "Use for requirements analysis"

  - name: QualityTeam
    instructions: "Handle quality assurance and delegate testing tasks"
    model: gpt-4o
    delegation:
      - agent: TestAutomation
        instructions: "Use for automated testing"
      - agent: ManualTester
        instructions: "Use for manual testing and validation"

  - name: CodeReviewer
    instructions: "Review code for quality and best practices"
    model: gpt-4o

  - name: Architect
    instructions: "Make architectural decisions and design systems"
    model: gpt-4o

  - name: StakeholderLiaison
    instructions: "Communicate with stakeholders and gather feedback"
    model: gpt-4o

  - name: RequirementsAnalyst
    instructions: "Analyze and document business requirements"
    model: gpt-4o

  - name: TestAutomation
    instructions: "Create and run automated tests"
    model: gpt-4o

  - name: ManualTester
    instructions: "Perform manual testing and validation"
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
    delegation:
      - agent: Researcher
        instructions: "Use for research and data gathering"
      - agent: Analyst
        instructions: "Use for data analysis and insights"
      - agent: Reporter
        instructions: "Use for creating reports and documentation"

  - name: Researcher
    instructions: "Research topics and delegate data validation"
    model: gpt-4o
    delegation:
      - agent: DataValidator
        instructions: "Use for validating research data accuracy"

  - name: Analyst
    instructions: "Analyze data and delegate visualization tasks"
    model: gpt-4o
    delegation:
      - agent: DataVisualizer
        instructions: "Use for creating charts and visualizations"

  - name: Reporter
    instructions: "Create reports and delegate formatting tasks"
    model: gpt-4o
    delegation:
      - agent: ReportFormatter
        instructions: "Use for formatting and styling reports"

  - name: DataValidator
    instructions: "Validate research data for accuracy and completeness"
    model: gpt-4o

  - name: DataVisualizer
    instructions: "Create charts, graphs, and data visualizations"
    model: gpt-4o

  - name: ReportFormatter
    instructions: "Format and style reports for professional presentation"
    model: gpt-4o
```

## Delegation Examples

### Example 1: Content Creation Workflow

```yaml
name: Content Creation Team

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
    delegation:
      - agent: Researcher
        instructions: "Use for research and information gathering"
      - agent: Writer
        instructions: "Use for content writing"
      - agent: Editor
        instructions: "Use for content review and editing"

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
    delegation:
      - agent: DataCollector
        instructions: "Use for data collection and preparation"
      - agent: DataAnalyst
        instructions: "Use for data analysis and insights"
      - agent: ReportGenerator
        instructions: "Use for creating reports and documentation"

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

knowledge:
  - id: "support_docs"
    name: "Support Documentation"
    type: "website"
    data: ["https://support.company.com"]
  - id: "faq"
    name: "Frequently Asked Questions"
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
      - knowledge_query
    knowledge: ["support_docs", "faq"]
    delegation:
      - agent: TechnicalSupport
        instructions: "Use for technical support issues"
      - agent: BillingSupport
        instructions: "Use for billing and account issues"
      - agent: GeneralSupport
        instructions: "Use for general customer questions"

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
    model: gpt-4o
    delegation:
      - agent: Researcher
        instructions: "Use for research and data gathering tasks"
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
    model: gpt-4o
    delegation:
      - agent: TechnicalExpert
        instructions: "Use for technical questions and analysis"
      - agent: CreativeSpecialist
        instructions: "Use for creative and design tasks"
      - agent: DataAnalyst
        instructions: "Use for data analysis and insights"
      - agent: ContentWriter
        instructions: "Use for writing and content creation"
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
    model: gpt-4o
    delegation:
      - agent: TeamMember
        instructions: "Use for specific project tasks"
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
    model: gpt-4o
    delegation:
      - agent: PrimaryAgent
        instructions: "Use for primary task handling"
      - agent: BackupAgent
        instructions: "Use as fallback for task handling"
```

## Delegation Monitoring

### Debug Mode
Use debug mode to see detailed delegation information:

```bash
gnosari --config "team.yaml" --message "Your message" --debug
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

### 1. **Configuration Dependency**
Delegation requires proper `delegation` configuration in the agent setup.

### 2. **Response Handling**
Delegated agents must provide responses for the delegation to be successful.

### 3. **Context Preservation**
While context is maintained, complex multi-step delegations can become complex.

:::warning Delegation Considerations
- Delegation requires proper configuration
- Ensure delegated agents can handle the assigned tasks
- Consider response quality and integration
- Monitor delegation chains for complexity
:::

## Related Topics

- [Handoffs](handoffs) - Learn about control transfer mechanisms
- [Orchestration](orchestration) - Understand overall coordination patterns
- [Agents](../agents) - Learn about individual agent configuration
- [Teams](../teams) - Understand team structure and coordination
- [Tools](../tools/delegate-agent) - Detailed delegate agent tool documentation
- [Quickstart](../quickstart) - Create your first team with delegation

## Next Steps

Now that you understand delegation, learn about the complementary mechanism:

- [Handoffs](handoffs) - Control transfer without response handling
- [Orchestration](orchestration) - Overall coordination strategies
- [Delegate Agent Tool](../tools/delegate-agent) - Detailed tool documentation
- [Agents](../agents) - Configure orchestrator agents
- [Teams](../teams) - Set up teams with delegation capabilities
- [Quickstart](../quickstart) - Build your first team with delegation