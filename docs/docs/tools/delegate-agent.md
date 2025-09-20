---
sidebar_position: 2
---

# Delegate Agent Tool

:::info Automatic Tool
This documentation is **purely informational**. The `delegate_agent` tool is **automatically added** to any agent with a `delegation` property configured. You can also explicitly add it to any agent's `tools` list.
:::

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

## Configuration

The `delegate_agent` tool is added to an agent in two ways:

### 1. Automatic Addition (via delegation property)
The tool is **automatically added** to any agent that has a `delegation` property configured:

```yaml
agents:
  - name: Coordinator
    instructions: "Coordinate tasks and delegate to team members"
    delegation:
      - agent: "Researcher"
        instructions: "Research topics and provide detailed information"
      - agent: "Writer"
        instructions: "Write content based on research findings"
    model: gpt-4o
```

The `delegation` property is an array of objects, where each object specifies:
- `agent`: The name of the agent that can be delegated to
- `instructions`: Specific instructions for how to delegate to that agent

:::warning Circular Delegation Prevention
**Avoid circular delegation references** that could lead to infinite loops. For example, if Agent A delegates to Agent B, Agent B should not delegate back to Agent A. Design your delegation hierarchy to be unidirectional or use clear termination conditions.
:::

### 2. Explicit Addition (via tools list)
You can also explicitly add the tool to any agent's `tools` list:

```yaml
agents:
  - name: Manager
    instructions: "Manage team tasks and delegate when needed"
    tools:
      - delegate_agent
    model: gpt-4o
```

## Agent Assignment

The `delegate_agent` tool is available to agents configured with delegation capabilities:

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
    delegation:
      - agent: "Researcher"
        instructions: "Research topics and provide detailed information"
      - agent: "Writer"
        instructions: "Write content based on research findings"
    model: gpt-4o
```

:::note Delegation Configuration
The `delegate_agent` tool is automatically added to agents with a `delegation` property, or can be explicitly added to any agent's `tools` list.
:::
```

## Usage Examples

### Example 1: Simple Task Delegation

```yaml
name: Research Team

agents:
  - name: Research Coordinator
    instructions: "Coordinate research tasks and delegate to specialists"
    delegation:
      - agent: "Web Researcher"
        instructions: "Research information from web sources"
      - agent: "Data Analyst"
        instructions: "Analyze data and provide insights"
    model: gpt-4o

  - name: Web Researcher
    instructions: "Research information from web sources"
    model: gpt-4o

  - name: Data Analyst
    instructions: "Analyze data and provide insights"
    model: gpt-4o
```

**Usage**: The Research Coordinator automatically has access to the `delegate_agent` tool and can delegate web research tasks to Web Researcher and data analysis to Data Analyst.

### Example 2: Multi-Agent Workflow

```yaml
name: Content Creation Team

agents:
  - name: Content Manager
    instructions: >
      Manage content creation workflow:
      1. Delegate research to Research Agent
      2. Delegate writing to Writer Agent
      3. Delegate review to Editor Agent
      4. Compile final content
    delegation:
      - agent: "Research Agent"
        instructions: "Research topics and gather information"
      - agent: "Writer Agent"
        instructions: "Write content based on research"
      - agent: "Editor Agent"
        instructions: "Review and edit content for quality"
    model: gpt-4o

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
    delegation:
      - agent: "Developer"
        instructions: "Handle technical implementation tasks"
      - agent: "Designer"
        instructions: "Create visual designs and user interfaces"
      - agent: "Tester"
        instructions: "Test functionality and report issues"
    model: gpt-4o
```

## Error Handling

The delegate agent tool includes comprehensive error handling:

- **Agent Not Found**: Returns error if target agent doesn't exist
- **Delegation Failures**: Handles communication errors gracefully
- **Timeout Handling**: Manages long-running delegated tasks
- **Context Preservation**: Maintains conversation context across failures

## Best Practices

### 1. **Avoid Circular Delegation**
Design your delegation hierarchy to prevent infinite loops:

**❌ Bad - Circular Delegation:**
```yaml
agents:
  - name: Manager
    delegation:
      - agent: "Assistant"
        instructions: "Help with tasks"
  
  - name: Assistant
    delegation:
      - agent: "Manager"  # ❌ This creates a circular reference!
        instructions: "Get approval for decisions"
```

**✅ Good - Unidirectional Hierarchy:**
```yaml
agents:
  - name: Manager
    delegation:
      - agent: "Assistant"
        instructions: "Help with tasks"
      - agent: "Specialist"
        instructions: "Handle specialized tasks"
  
  - name: Assistant
    # No delegation - terminates the chain
    instructions: "Help with tasks and provide direct responses"
  
  - name: Specialist
    # No delegation - terminates the chain
    instructions: "Handle specialized tasks and provide direct responses"
```

**✅ Good - Clear Termination Conditions:**
```yaml
agents:
  - name: Coordinator
    delegation:
      - agent: "Researcher"
        instructions: "Research topics and provide detailed information"
  
  - name: Researcher
    delegation:
      - agent: "Writer"
        instructions: "Write content based on research findings"
  
  - name: Writer
    # No delegation - terminates the chain
    instructions: "Write content and provide final output"
```

### 2. **Clear Delegation Instructions**
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

### 3. **Delegation Depth Management**
Implement strategies to prevent infinite delegation:

```yaml
agents:
  - name: Task Manager
    instructions: >
      You are a task manager. When delegating:
      1. Only delegate to agents listed in your delegation configuration
      2. If a delegated agent asks you to delegate back, provide direct assistance instead
      3. Limit delegation depth to maximum 2 levels
      4. Always provide final synthesis of delegated results
    delegation:
      - agent: "Specialist"
        instructions: "Handle specialized tasks and provide direct responses"
    model: gpt-4o

  - name: Specialist
    instructions: >
      You are a specialist. Handle tasks directly and provide complete responses.
      Do not delegate back to other agents - provide your expertise directly.
    model: gpt-4o
```

### 4. **Workflow Design**
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
    delegation:
      - agent: "Research Agent"
        instructions: "Research topics and gather information"
      - agent: "Data Analyst"
        instructions: "Analyze data and provide insights"
      - agent: "Technical Writer"
        instructions: "Write technical documentation"
      - agent: "Quality Reviewer"
        instructions: "Review content for quality and accuracy"
      - agent: "Content Manager"
        instructions: "Finalize and format content"
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

4. **Infinite Delegation Loops**
   - Check for circular delegation references in your configuration
   - Ensure delegation chains have clear termination points
   - Use debug mode to trace delegation flow and identify loops
   - Consider adding delegation depth limits in agent instructions

### Debug Mode

Use debug mode to see detailed delegation logs:

```bash
gnosari --config "team.yaml" --message "Your message" --debug
```

:::tip Debugging Delegation Issues
Debug mode shows detailed logs of delegation activities, including which agent was contacted, the message sent, and the response received. Use this to identify circular delegation patterns and infinite loops.
:::

## Delegation Patterns

### Recommended Patterns

**1. Hierarchical Delegation (Tree Structure)**
```yaml
agents:
  - name: CEO
    delegation:
      - agent: "Manager"
        instructions: "Handle management tasks"
  
  - name: Manager
    delegation:
      - agent: "Worker"
        instructions: "Execute specific tasks"
  
  - name: Worker
    # No delegation - leaf node
    instructions: "Execute tasks directly"
```

**2. Hub-and-Spoke Delegation**
```yaml
agents:
  - name: Coordinator
    delegation:
      - agent: "Researcher"
        instructions: "Research topics"
      - agent: "Writer"
        instructions: "Write content"
      - agent: "Reviewer"
        instructions: "Review content"
  
  - name: Researcher
    # No delegation - spoke
    instructions: "Research and provide information"
  
  - name: Writer
    # No delegation - spoke
    instructions: "Write content directly"
  
  - name: Reviewer
    # No delegation - spoke
    instructions: "Review content directly"
```

### Anti-Patterns to Avoid

**❌ Circular Delegation**
```yaml
agents:
  - name: Agent A
    delegation:
      - agent: "Agent B"
  
  - name: Agent B
    delegation:
      - agent: "Agent A"  # Creates infinite loop!
```

**❌ Mutual Delegation**
```yaml
agents:
  - name: Manager
    delegation:
      - agent: "Assistant"
  
  - name: Assistant
    delegation:
      - agent: "Manager"  # Creates infinite loop!
```

**❌ Complex Circular Networks**
```yaml
agents:
  - name: A
    delegation:
      - agent: "B"
  
  - name: B
    delegation:
      - agent: "C"
  
  - name: C
    delegation:
      - agent: "A"  # Creates infinite loop!
```

## Related Tools

- [API Request Tool](api-request) - For external service integration
- [Knowledge Query Tool](knowledge-query) - For information retrieval
- [MySQL Query Tool](mysql-query) - For database operations

The delegate agent tool is the foundation of multi-agent coordination in Gnosari AI Teams. Use it to create sophisticated workflows that leverage the strengths of multiple specialized agents.