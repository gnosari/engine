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
    tools: ["tool_id1", "tool_id2"]  # Optional: tools this agent can use (references tool IDs)
    knowledge: ["kb_id1", "kb_id2"]  # Optional: knowledge bases this agent can access (references knowledge base IDs)
```

:::info Environment Variables
Agent configurations support environment variable substitution using `${VAR_NAME}` or `${VAR_NAME:default_value}` syntax. This works for all agent properties including names, instructions, models, and more. See [Environment Variables](#environment-variables) section below.
:::

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
    
  - name: Specialist
    instructions: "Handle specific tasks"
    model: gpt-4o
    # No orchestrator: true - this agent cannot delegate
```

:::info Orchestrator as Entry Point
When running a team without specifying a particular agent, **orchestrator agents are the first to receive user requests**. If your team has multiple orchestrator agents, the first one defined in the configuration will handle the initial user input.
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
- **Task delegation** via delegation configuration (see [Delegation](coordination/delegation))
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

## Environment Variables

Agent configurations support environment variable substitution throughout all agent properties using `${VAR_NAME}` or `${VAR_NAME:default_value}` syntax.

### Dynamic Agent Configuration

```yaml
agents:
  - name: "${AGENT_NAME:DataAnalyst}"
    instructions: >
      You are a ${ROLE:data analyst} working for ${COMPANY:our company}.
      
      Your responsibilities include:
      - ${RESPONSIBILITY_1:Analyzing business data}
      - ${RESPONSIBILITY_2:Creating reports and insights}
      - ${RESPONSIBILITY_3:Supporting data-driven decisions}
      
      Use ${ANALYSIS_STYLE:statistical methods} and always ${QUALITY_STANDARD:double-check your work}.
    model: "${AGENT_MODEL:gpt-4o}"
    temperature: ${AGENT_TEMPERATURE:0.3}
    tools: ["${PRIMARY_TOOL:mysql_query}", "${SECONDARY_TOOL:api_request}"]
```

### Environment-Specific Agent Behavior

```yaml
agents:
  - name: "${ENV}_Support_Agent"
    instructions: >
      You are a customer support agent for the ${ENV:production} environment.
      
      Environment-specific guidelines:
      - Database: ${DB_NAME:prod_db}
      - Support level: ${SUPPORT_LEVEL:L1}
      - Escalation contact: ${ESCALATION_EMAIL:support@company.com}
      - Debug mode: ${DEBUG_MODE:false}
      
      ${ENV_SPECIFIC_INSTRUCTIONS:Follow standard production protocols.}
    model: "${ENV_MODEL:gpt-4o}"
    temperature: ${ENV_TEMPERATURE:0.2}
```

### Multi-Environment Agent Setup

```yaml
agents:
  - name: "${ROLE_PREFIX:Production}_Manager"
    instructions: >
      You are a ${ROLE_TYPE:production} manager responsible for ${DOMAIN:system operations}.
      
      Configuration:
      - Environment: ${ENVIRONMENT:production}
      - Region: ${REGION:us-east-1}
      - Alert threshold: ${ALERT_THRESHOLD:95%}
      - On-call contact: ${ONCALL_CONTACT:ops@company.com}
    model: "${MANAGER_MODEL:gpt-4o}"
    orchestrator: ${IS_ORCHESTRATOR:true}
    tools: ["${MONITORING_TOOL:api_request}"]
```

### Setting Environment Variables for Agents

Set environment variables to customize agent behavior:

```bash
# Agent configuration
export AGENT_NAME="ProductionAnalyst"
export ROLE="senior data analyst"
export COMPANY="Acme Corporation"
export AGENT_MODEL="gpt-4o"
export AGENT_TEMPERATURE="0.2"

# Environment-specific settings
export ENV="production"
export DB_NAME="acme_prod"
export SUPPORT_LEVEL="L2"
export DEBUG_MODE="false"

# Role-specific settings
export ROLE_PREFIX="Senior"
export ROLE_TYPE="production"
export DOMAIN="data analytics"
export ENVIRONMENT="production"
export REGION="us-west-2"
```

### Agent Instructions with Dynamic Content

Environment variables are particularly useful for agent instructions:

```yaml
agents:
  - name: CustomSupport
    instructions: >
      You are a customer support representative for ${COMPANY_NAME}.
      
      Company Information:
      - Website: ${COMPANY_WEBSITE:https://company.com}
      - Support email: ${SUPPORT_EMAIL:support@company.com}
      - Phone: ${SUPPORT_PHONE:1-800-SUPPORT}
      - Hours: ${SUPPORT_HOURS:9 AM - 6 PM EST, Monday-Friday}
      
      Product Information:
      - Main product: ${PRODUCT_NAME:Our Product}
      - Version: ${PRODUCT_VERSION:2.0}
      - Documentation: ${DOCS_URL:https://docs.company.com}
      
      Policies:
      - Refund period: ${REFUND_PERIOD:30 days}
      - Escalation process: ${ESCALATION_PROCESS:Contact supervisor after 3 attempts}
      
      Always maintain a ${COMMUNICATION_TONE:professional and empathetic} tone.
      ${ADDITIONAL_GUIDELINES:Follow company guidelines at all times.}
```

:::tip Agent Customization
Use environment variables to create reusable agent configurations that can be customized for different environments, companies, or use cases without modifying the YAML files.
:::

## Related Topics

- [Teams](teams) - Learn how to configure and structure teams
- [Orchestration](coordination/orchestration) - Understand agent coordination and workflow management
- [Handoffs](coordination/handoffs) - Learn about control transfer mechanisms
- [Delegation](coordination/delegation) - Understand task assignment and response handling with delegation configuration
- [Tools](tools/intro) - Explore available tools for agents
- [Knowledge](knowledge) - Understand knowledge base integration
- [Quickstart](quickstart) - Get started with your first team

## Next Steps

Now that you understand agents, learn how to:
- [Configure teams](teams) with multiple agents
- [Set up orchestration](coordination/orchestration) for agent coordination
- [Use handoffs](coordination/handoffs) for control transfer
- [Implement delegation](coordination/delegation) for task assignment
- [Add tools](tools/intro) to enhance agent capabilities
- [Set up knowledge bases](knowledge) for information access
- [Create your first team](quickstart) with the quickstart guide