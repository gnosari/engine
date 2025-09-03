---
sidebar_position: 3
---

# Agents

Agents are the core building blocks of Gnosari AI Teams. Each agent is an intelligent entity that can process information, make decisions, and execute tasks using various tools and capabilities.

## What are Agents?

Agents in Gnosari AI Teams are AI-powered entities that can:
- **Process natural language** instructions and requests
- **Execute tasks** using assigned tools
- **Make decisions** based on context and instructions
- **Collaborate** with other agents through delegation
- **Access knowledge** from configured knowledge bases
- **Use different LLM models** from various providers

:::info Agent vs LLM
An agent is more than just an LLM - it's a complete entity with instructions, tools, knowledge access, and the ability to collaborate with other agents.
:::

## Agent Configuration

Agents are defined in the `agents` section of your team YAML configuration:

```yaml
agents:
  - name: AgentName
    instructions: "What this agent does and how it behaves"
    model: gpt-4o
    orchestrator: true  # Optional: for coordination agents
    tools: ["tool1", "tool2"]  # Optional: tools this agent can use
    knowledge: ["kb1", "kb2"]  # Optional: knowledge bases this agent can access
```

## Core Agent Properties

### Name
The unique identifier for the agent within the team:

```yaml
agents:
  - name: ResearchSpecialist
    # ... other properties
```

:::tip Naming Conventions
Use descriptive names that clearly indicate the agent's role or specialization (e.g., `DataAnalyst`, `ContentWriter`, `ProjectManager`).
:::

### Instructions
The core behavior definition for the agent. This is where you define:
- **Role and responsibilities**
- **How to approach tasks**
- **Communication style**
- **Decision-making criteria**
- **Quality standards**

```yaml
agents:
  - name: TechnicalWriter
    instructions: >
      You are a technical writer who specializes in creating clear, accurate documentation.
      
      Your responsibilities include:
      - Writing technical documentation and guides
      - Explaining complex concepts in simple terms
      - Ensuring accuracy and completeness
      - Following documentation best practices
      
      When writing:
      - Use clear, concise language
      - Include practical examples
      - Structure content logically
      - Always verify technical accuracy
      
      If you need clarification on technical details, ask for more information
      rather than making assumptions.
```

:::tip Effective Instructions
Good instructions are:
- **Specific**: Clear about what the agent should do
- **Comprehensive**: Cover the agent's role and responsibilities
- **Actionable**: Provide clear guidance on how to behave
- **Context-aware**: Include relevant constraints and considerations
:::

### Model
The LLM model that powers the agent's intelligence:

```yaml
agents:
  - name: CreativeWriter
    model: gpt-4o  # OpenAI GPT-4o
    instructions: "Create engaging, creative content"
    
  - name: DataAnalyst
    model: claude-3-5-sonnet-20241022  # Anthropic Claude
    instructions: "Analyze data and provide insights"
    
  - name: CodeReviewer
    model: deepseek-chat  # DeepSeek model
    instructions: "Review code for quality and security"
```

:::info Multi-Provider Support
Each agent can use a different model from different providers, allowing you to leverage the strengths of various LLMs in your team.
:::

### Orchestrator
Marks an agent as a coordinator that can delegate tasks to other agents:

```yaml
agents:
  - name: ProjectManager
    instructions: "Coordinate team tasks and delegate work"
    orchestrator: true  # This agent can delegate to others
    model: gpt-4o
    tools:
      - delegate_agent  # Required for delegation
    
  - name: Specialist
    instructions: "Handle specific tasks"
    model: gpt-4o
    # No orchestrator: true - this agent cannot delegate
```

:::warning Orchestrator Requirements
Only agents with `orchestrator: true` can use the `delegate_agent` tool to coordinate with other agents.
:::

## Agent Types and Patterns

### 1. Orchestrator Agents
Coordination agents that manage workflows and delegate tasks:

```yaml
agents:
  - name: WorkflowManager
    instructions: >
      You are a workflow manager who coordinates complex tasks.
      Break down large requests into smaller tasks and delegate
      to appropriate specialists. Always provide a summary of
      completed work.
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent
```

### 2. Specialist Agents
Focused agents that handle specific types of tasks:

```yaml
agents:
  - name: DataScientist
    instructions: >
      You are a data scientist who analyzes data and provides insights.
      Focus on statistical analysis, pattern recognition, and
      data-driven recommendations.
    model: gpt-4o
    tools:
      - mysql_query
      - api_request
```

### 3. Generalist Agents
Versatile agents that can handle multiple types of tasks:

```yaml
agents:
  - name: GeneralAssistant
    instructions: >
      You are a general assistant who can help with various tasks.
      Adapt your approach based on the specific request and
      use available tools as needed.
    model: gpt-4o
    tools:
      - api_request
      - knowledge_query
```

## Agent Instructions Best Practices

### 1. **Clear Role Definition**
Define the agent's primary role and responsibilities:

```yaml
instructions: >
  You are a customer support specialist who helps users resolve issues.
  Your primary responsibilities are:
  - Understanding user problems
  - Providing accurate solutions
  - Escalating complex issues when needed
  - Maintaining a helpful, professional tone
```

### 2. **Behavioral Guidelines**
Specify how the agent should behave:

```yaml
instructions: >
  When responding to users:
  - Always be polite and professional
  - Ask clarifying questions if needed
  - Provide step-by-step solutions
  - Confirm understanding before proceeding
  - Escalate if you cannot resolve the issue
```

### 3. **Quality Standards**
Set expectations for output quality:

```yaml
instructions: >
  When creating content:
  - Ensure accuracy and fact-check information
  - Use clear, engaging language
  - Structure content logically
  - Include relevant examples
  - Proofread for grammar and clarity
```

### 4. **Context Awareness**
Help the agent understand its environment:

```yaml
instructions: >
  You are part of a content creation team. You work with:
  - Researchers who provide information
  - Editors who review your work
  - Designers who create visuals
  
  Always consider how your work fits into the larger content strategy.
```

## Agent Communication

### Internal Communication
Agents communicate through:
- **Task delegation** via the `delegate_agent` tool
- **Shared context** through conversation history
- **Knowledge bases** for information sharing

### External Communication
Agents interact with users through:
- **Direct responses** to user messages
- **Structured outputs** based on instructions
- **Tool results** and processed information

:::tip Communication Style
Define the agent's communication style in the instructions to ensure consistent, appropriate responses.
:::

## Agent Performance

### Model Selection
Choose models based on the agent's needs:

```yaml
# For creative tasks
model: gpt-4o

# For analytical tasks  
model: claude-3-5-sonnet-20241022

# For cost-effective general tasks
model: gpt-3.5-turbo
```

### Temperature Settings
Control creativity and randomness:

```yaml
agents:
  - name: CreativeWriter
    model: gpt-4o
    temperature: 0.8  # More creative
    
  - name: TechnicalWriter
    model: gpt-4o
    temperature: 0.1  # More focused and consistent
```

:::info Temperature Guidelines
- **Low (0.1-0.3)**: Factual, consistent responses
- **Medium (0.4-0.6)**: Balanced creativity and consistency
- **High (0.7-1.0)**: Creative, varied responses
:::

## Common Agent Patterns

### 1. **Research → Analysis → Writing**
```yaml
agents:
  - name: Researcher
    instructions: "Gather and organize information"
    
  - name: Analyst
    instructions: "Analyze information and identify insights"
    
  - name: Writer
    instructions: "Create content based on research and analysis"
```

### 2. **Coordination → Specialization**
```yaml
agents:
  - name: Coordinator
    instructions: "Break down tasks and delegate to specialists"
    orchestrator: true
    tools:
      - delegate_agent
      
  - name: TechnicalSpecialist
    instructions: "Handle technical tasks and analysis"
    
  - name: CreativeSpecialist
    instructions: "Handle creative and design tasks"
```

### 3. **Quality Assurance**
```yaml
agents:
  - name: Creator
    instructions: "Create initial content or solutions"
    
  - name: Reviewer
    instructions: "Review and improve created content"
    
  - name: Finalizer
    instructions: "Finalize and polish the final output"
```

## Agent Limitations

### Context Window
Agents are limited by their model's context window:
- **Input context**: Previous conversation and instructions
- **Output context**: Generated responses and tool usage
- **Tool context**: Results from tool executions

### Tool Dependencies
Agents can only use tools that are:
- **Defined in the team configuration**
- **Assigned to the agent**
- **Properly configured and available**

### Knowledge Access
Agents can only access knowledge bases that are:
- **Defined in the team configuration**
- **Assigned to the agent**
- **Properly configured and available**

:::warning Agent Limitations
Be aware of model limitations, tool availability, and knowledge base access when designing your agents.
:::

## Related Topics

- [Teams](/docs/teams) - Learn how to configure and structure teams
- [Orchestration](/docs/orchestration) - Understand agent coordination and workflow management
- [Handoffs](/docs/handoffs) - Learn about control transfer mechanisms
- [Delegation](/docs/delegation) - Understand task assignment and response handling
- [Tools](/docs/tools/intro) - Explore available tools for agents
- [Knowledge](/docs/knowledge) - Understand knowledge base integration
- [Quickstart](/docs/quickstart) - Get started with your first team

## Next Steps

Now that you understand agents, learn how to:
- [Configure teams](/docs/teams) with multiple agents
- [Set up orchestration](/docs/orchestration) for agent coordination
- [Use handoffs](/docs/handoffs) for control transfer
- [Implement delegation](/docs/delegation) for task assignment
- [Add tools](/docs/tools/intro) to enhance agent capabilities
- [Set up knowledge bases](/docs/knowledge) for information access
- [Create your first team](/docs/quickstart) with the quickstart guide