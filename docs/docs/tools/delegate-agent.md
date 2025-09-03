---
sidebar_position: 2
---

# Delegate Agent Tool

The **delegate_agent** tool enables agents to delegate tasks to other agents within the same team. This is the core mechanism for multi-agent coordination and task distribution in Gnosari AI Teams.

## Overview

The delegate agent tool allows an orchestrator agent to:
- Send tasks to specific team members
- Receive responses from delegated agents
- Coordinate complex workflows across multiple agents
- Maintain conversation context across task delegations

:::info Task Delegation vs Handoffs
This tool is for **task delegation**, not handoffs. The delegate_agent tool sends a task to another agent and waits for a response, while handoffs transfer control to another agent without waiting for a response.
:::

## Capabilities

- ✅ **Task Delegation**: Send specific tasks to named agents
- ✅ **Response Handling**: Receive and process responses from delegated agents
- ✅ **Error Handling**: Graceful handling of delegation failures
- ✅ **Logging**: Comprehensive logging of delegation activities
- ✅ **Context Preservation**: Maintain conversation context across task delegations

## YAML Configuration

### Basic Configuration

```yaml
tools:
  - name: delegate_agent
    module: gnosari.tools.delegate_agent
    class: DelegateAgentTool
    args:
      pass
```

:::tip Simple Configuration
The delegate_agent tool requires minimal configuration - just the basic module and class references.
:::

### Advanced Configuration

```yaml
tools:
  - name: task_delegator
    module: gnosari.tools.delegate_agent
    class: DelegateAgentTool
    args:
      pass
```

## Agent Assignment

Assign the delegate agent tool to orchestrator agents:

```yaml
agents:
  - name: Coordinator
    instructions: >
      You are a coordinator who manages conversations with multiple agents. 
      When you delegate tasks to other agents using the delegate_agent tool, you should:
      1. Use the delegate_agent tool to ask other agents for help when needed
      2. If the user mentions multiple agents, delegate to each agent separately
      3. After receiving responses from delegated agents, provide a summary
      4. Always maintain the conversation flow and provide a complete response
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent
    can_delegate_to: [Alice, Bob]  # Optional: specify allowed delegation targets
```

:::note Orchestrator Requirement
Only agents with `orchestrator: true` should use the delegate_agent tool. Regular agents don't need this tool.
:::
```

## Usage Examples

### Example 1: Simple Task Delegation

```yaml
name: Research Team

tools:
  - name: delegate_agent
    module: gnosari.tools.delegate_agent
    class: DelegateAgentTool
    args:
      pass

agents:
  - name: Research Coordinator
    instructions: "Coordinate research tasks and delegate to specialists"
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent

  - name: Web Researcher
    instructions: "Research information from web sources"
    model: gpt-4o

  - name: Data Analyst
    instructions: "Analyze data and provide insights"
    model: gpt-4o
```

**Usage**: The Research Coordinator can delegate web research tasks to Web Researcher and data analysis to Data Analyst.

### Example 2: Multi-Agent Workflow

```yaml
name: Content Creation Team

tools:
  - name: delegate_agent
    module: gnosari.tools.delegate_agent
    class: DelegateAgentTool
    args:
      pass

agents:
  - name: Content Manager
    instructions: >
      Manage content creation workflow:
      1. Delegate research to Research Agent
      2. Delegate writing to Writer Agent
      3. Delegate review to Editor Agent
      4. Compile final content
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent

  - name: Research Agent
    instructions: "Research topics and gather information"
    model: gpt-4o

  - name: Writer Agent
    instructions: "Write content based on research"
    model: gpt-4o

  - name: Editor Agent
    instructions: "Review and edit content for quality"
    model: gpt-4o
```

## Tool Parameters

The delegate agent tool accepts the following parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `tool_name` | string | "delegate_agent" | Custom name for the tool |
| `tool_description` | string | "Delegate a task to another agent in the team" | Custom description |

## Agent Instructions

When using the delegate agent tool, provide clear instructions to your orchestrator:

```yaml
agents:
  - name: Project Manager
    instructions: >
      You are a project manager who coordinates team tasks. Use the delegate_agent tool to:
      
      1. **Identify Tasks**: Break down complex requests into specific tasks
      2. **Select Agents**: Choose the most appropriate agent for each task
      3. **Delegate Clearly**: Provide clear, actionable instructions to delegated agents
      4. **Monitor Progress**: Track task completion and handle any issues
      5. **Synthesize Results**: Combine responses from multiple agents into coherent output
      
      Always maintain context and ensure the user receives a complete response.
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent
```

## Error Handling

The delegate agent tool includes comprehensive error handling:

- **Agent Not Found**: Returns error if target agent doesn't exist
- **Delegation Failures**: Handles communication errors gracefully
- **Timeout Handling**: Manages long-running delegated tasks
- **Context Preservation**: Maintains conversation context across failures

## Best Practices

### 1. **Clear Delegation Instructions**
Provide specific, actionable tasks to delegated agents:

```yaml
instructions: >
  When delegating tasks, be specific about:
  - What needs to be done
  - Expected output format
  - Any constraints or requirements
  - Deadline or priority level
```

:::tip Effective Delegation
The more specific your delegation instructions, the better the results. Include context, expected format, and any constraints.
:::

### 2. **Agent Role Definition**
Define clear roles and responsibilities for each agent:

```yaml
agents:
  - name: Technical Writer
    instructions: >
      You are a technical writer specializing in:
      - API documentation
      - Code examples
      - Clear, concise explanations
      
      Always provide practical examples and use proper formatting.
    model: gpt-4o
```

### 3. **Workflow Design**
Design logical workflows that leverage agent strengths:

```yaml
agents:
  - name: Workflow Coordinator
    instructions: >
      Coordinate this workflow:
      1. Research → Research Agent
      2. Analysis → Data Analyst  
      3. Writing → Technical Writer
      4. Review → Quality Reviewer
      5. Finalize → Content Manager
    orchestrator: true
    tools:
      - delegate_agent
```

## Troubleshooting

### Common Issues

1. **Agent Not Found Error**
   - Ensure agent names match exactly
   - Check that agents are defined in the team configuration

2. **Delegation Timeout**
   - Increase timeout settings if needed
   - Break down complex tasks into smaller pieces

3. **Context Loss**
   - Provide clear context in delegation messages
   - Use orchestrator instructions to maintain conversation flow

### Debug Mode

Use debug mode to see detailed delegation logs:

```bash
poetry run gnosari --config "team.yaml" --message "Your message" --debug
```

:::tip Debugging Delegation Issues
Debug mode shows detailed logs of delegation activities, including which agent was contacted, the message sent, and the response received.
:::

## Related Tools

- [API Request Tool](/docs/tools/api-request) - For external service integration
- [Knowledge Query Tool](/docs/tools/knowledge-query) - For information retrieval
- [MySQL Query Tool](/docs/tools/mysql-query) - For database operations

The delegate agent tool is the foundation of multi-agent coordination in Gnosari AI Teams. Use it to create sophisticated workflows that leverage the strengths of multiple specialized agents.