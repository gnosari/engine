---
sidebar_position: 6
---

# Orchestration

Orchestration in Gnosari AI Teams refers to the coordination and management of multi-agent workflows. It encompasses how agents work together, transfer control, delegate tasks, and maintain conversation flow across complex, multi-step processes.

## What is Orchestration?

Orchestration in Gnosari AI Teams includes:
- **Agent Coordination**: How agents work together to accomplish goals
- **Control Transfer**: Moving responsibility between agents
- **Task Delegation**: Assigning specific tasks to specialized agents
- **Workflow Management**: Managing complex, multi-step processes
- **Context Preservation**: Maintaining conversation context across agents

:::info Orchestration vs Individual Agents
While individual agents can handle simple tasks, orchestration enables complex workflows that require coordination, specialization, and dynamic task distribution.
:::

## Types of Agent Coordination

Gnosari AI Teams supports two main types of agent coordination:

### 1. **Handoffs** (Control Transfer)
Handoffs transfer complete control from one agent to another. The receiving agent takes over the conversation and doesn't return control to the original agent.

### 2. **Delegation** (Task Assignment)
Delegation assigns specific tasks to other agents while maintaining control. The delegating agent receives a response and continues the conversation.

:::tip Coordination Patterns
- **Handoffs**: Use for escalation, specialization, or when an agent can't handle a request
- **Delegation**: Use for task distribution, parallel work, or when you need results from multiple agents
:::

## Orchestration Patterns

### 1. **Centralized Orchestration**
A single orchestrator agent coordinates all team activities:

```yaml
agents:
  - name: ProjectManager
    instructions: "Coordinate all project activities and delegate tasks"
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent
    can_transfer_to: ["TechnicalLead", "Designer"]  # Handoff targets

  - name: TechnicalLead
    instructions: "Handle technical decisions and implementation"
    model: gpt-4o

  - name: Designer
    instructions: "Handle design and user experience"
    model: gpt-4o
```

### 2. **Distributed Orchestration**
Multiple agents can coordinate and transfer control:

```yaml
agents:
  - name: CustomerService
    instructions: "Handle customer inquiries and escalate when needed"
    model: gpt-4o
    can_transfer_to: ["TechnicalSupport", "BillingSupport"]  # Handoff targets

  - name: TechnicalSupport
    instructions: "Handle technical support issues"
    model: gpt-4o
    can_transfer_to: ["SeniorEngineer"]  # Can escalate further

  - name: BillingSupport
    instructions: "Handle billing and account issues"
    model: gpt-4o
```

### 3. **Hybrid Orchestration**
Combines centralized coordination with distributed handoffs:

```yaml
agents:
  - name: MainCoordinator
    instructions: "Coordinate main workflow and delegate tasks"
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent
    can_transfer_to: ["EmergencyHandler"]  # Emergency handoff

  - name: TaskSpecialist
    instructions: "Handle specialized tasks"
    model: gpt-4o
    can_transfer_to: ["ExpertConsultant"]  # Can escalate to expert

  - name: EmergencyHandler
    instructions: "Handle emergency situations"
    model: gpt-4o
```

## Orchestrator Agents

Orchestrator agents are special agents that coordinate team activities:

### Orchestrator Characteristics
- **`orchestrator: true`** in configuration
- **Access to `delegate_agent` tool** for task delegation
- **Team context awareness** of all available agents
- **Workflow management** capabilities

### Orchestrator Responsibilities
- **Task Analysis**: Break down complex requests
- **Agent Selection**: Choose appropriate agents for tasks
- **Workflow Coordination**: Manage multi-step processes
- **Result Synthesis**: Combine outputs from multiple agents
- **Quality Assurance**: Ensure task completion and quality

:::info Orchestrator vs Regular Agents
Orchestrator agents have special capabilities for team coordination, while regular agents focus on specific tasks and can use handoffs for escalation.
:::

## Related Topics

- [Handoffs](/docs/handoffs) - Learn about control transfer mechanisms
- [Delegation](/docs/delegation) - Understand task assignment and response handling
- [Agents](/docs/agents) - Learn about individual agent configuration
- [Teams](/docs/teams) - Understand team structure and coordination
- [Quickstart](/docs/quickstart) - Create your first orchestrated team

## Next Steps

Now that you understand orchestration concepts, learn about the specific mechanisms:

- [Handoffs](/docs/handoffs) - Control transfer between agents
- [Delegation](/docs/delegation) - Task assignment and response handling
- [Agents](/docs/agents) - Configure individual agents
- [Teams](/docs/teams) - Set up coordinated teams
- [Quickstart](/docs/quickstart) - Build your first orchestrated team