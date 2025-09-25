---
sidebar_position: 4
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

:::tip Team Configuration
For team orchestration, delegation patterns, and workflow management, see the [Teams](teams) documentation.
:::

## Advanced Agent Configuration

Agents support extensive configuration options for fine-tuning behavior and performance:

```yaml
agents:
  - name: AgentName
    instructions: "What this agent does and how it behaves"
    model: gpt-4o                    # LLM model
    temperature: 0.7                  # Creativity level (0.0-1.0)
    reasoning_effort: "medium"        # Reasoning depth (low/medium/high)
    orchestrator: true               # Optional: for coordination agents
    tools: ["tool_id1", "tool_id2"] # Optional: tools this agent can use
    knowledge: ["kb_id1", "kb_id2"]  # Optional: knowledge bases this agent can access
```

:::info Environment Variables
Agent configurations support environment variable substitution using `${VAR_NAME}` or `${VAR_NAME:default_value}` syntax. This works for all agent properties including names, instructions, models, and more. See [Environment Variables](#environment-variables) section below.
:::

## Model Configuration

### Model Selection
Choose the GPT model that best fits the agent's role:

```yaml
agents:
  - name: CreativeWriter
    model: gpt-5  # GPT-5 - latest model for creative tasks
    instructions: "Create engaging, creative content"
    
  - name: DataAnalyst
    model: gpt-4o  # GPT-4o - strong analytical capabilities
    instructions: "Analyze data and provide insights"
    
  - name: CodeReviewer
    model: gpt-4o-mini  # GPT-4o Mini - cost-effective for technical tasks
    instructions: "Review code for quality and security"
```

:::info GPT Model Options
Choose from various GPT models based on your needs:
- **gpt-5**: Latest model with advanced capabilities
- **gpt-4o**: High quality for complex tasks
- **gpt-4o-mini**: Cost-effective for simpler tasks
:::

### Temperature Settings
Control creativity and randomness in agent responses:

```yaml
agents:
  - name: CreativeWriter
    model: gpt-4o
    temperature: 0.8  # High creativity for creative writing
    
  - name: TechnicalWriter
    model: gpt-4o
    temperature: 0.1  # Low creativity for consistent technical content
    
  - name: GeneralAssistant
    model: gpt-4o
    temperature: 0.5  # Balanced creativity and consistency
```

:::info Temperature Guidelines
- **Low (0.1-0.3)**: Factual, consistent responses
- **Medium (0.4-0.6)**: Balanced creativity and consistency
- **High (0.7-1.0)**: Creative, varied responses
:::

### Reasoning Effort
Control the depth of reasoning for GPT models:

```yaml
agents:
  - name: ComplexAnalyst
    model: gpt-4o
    reasoning_effort: "high"  # Deep reasoning for complex analysis
    
  - name: QuickResponder
    model: gpt-4o-mini
    reasoning_effort: "low"   # Fast responses for simple tasks
    
  - name: BalancedAgent
    model: gpt-4o
    reasoning_effort: "medium" # Balanced reasoning depth
```

:::info Reasoning Effort
- **Low**: Faster responses, less thorough analysis
- **Medium**: Balanced speed and thoroughness
- **High**: Slower responses, more thorough analysis
:::


## Advanced Agent Features

### Orchestrator Configuration
Configure agents to coordinate team workflows:

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
    temperature: 0.2  # Low temperature for consistent coordination
    reasoning_effort: "medium"
```

:::info Orchestrator as Entry Point
When running a team without specifying a particular agent, **orchestrator agents are the first to receive user requests**. If your team has multiple orchestrator agents, the first one defined in the configuration will handle the initial user input.
:::

### Tool Assignment
Assign specific tools to agents based on their role:

```yaml
agents:
  - name: DataScientist
    instructions: >
      You are a data scientist who analyzes data and provides insights.
      Focus on statistical analysis, pattern recognition, and
      data-driven recommendations.
    model: gpt-4o
    temperature: 0.3
    reasoning_effort: "high"
    tools:
      - mysql_query
      - api_request
      - knowledge_query
```

### Knowledge Base Access
Provide agents with relevant knowledge bases:

```yaml
agents:
  - name: TechnicalSupport
    instructions: >
      You are a technical support agent who helps users with
      technical issues and provides accurate solutions.
    model: gpt-4o
    temperature: 0.1  # Low temperature for consistent technical responses
    tools:
      - knowledge_query
    knowledge: ["technical_docs", "troubleshooting_guides"]
```

## Performance Optimization

### Model Selection Strategy
Choose GPT models based on specific requirements:

```yaml
# For creative tasks requiring high quality
agents:
  - name: CreativeWriter
    model: gpt-4o
    temperature: 0.8
    reasoning_effort: "medium"

# For analytical tasks requiring deep reasoning
agents:
  - name: DataAnalyst
    model: gpt-4o
    temperature: 0.2
    reasoning_effort: "high"

# For cost-effective general tasks
agents:
  - name: GeneralAssistant
    model: gpt-4o-mini
    temperature: 0.5
```

### Temperature Optimization
Fine-tune creativity based on task requirements:

```yaml
# High creativity for brainstorming
agents:
  - name: Brainstormer
    temperature: 0.9

# Balanced for general assistance
agents:
  - name: Assistant
    temperature: 0.5

# Low creativity for factual tasks
agents:
  - name: FactChecker
    temperature: 0.1
```

### Reasoning Effort Tuning
Balance speed vs. thoroughness:

```yaml
# Deep analysis for complex problems
agents:
  - name: ComplexAnalyst
    reasoning_effort: "high"

# Balanced for most tasks
agents:
  - name: GeneralAgent
    reasoning_effort: "medium"

# Fast responses for simple tasks
agents:
  - name: QuickResponder
    reasoning_effort: "low"
```

## Advanced Configuration Patterns

### Multi-Model Teams
Use different GPT models for different agent roles:

```yaml
agents:
  - name: CreativeDirector
    model: gpt-5
    temperature: 0.8
    reasoning_effort: "medium"
    instructions: "Lead creative projects and provide artistic direction"
    
  - name: TechnicalLead
    model: gpt-4o
    temperature: 0.2
    reasoning_effort: "high"
    instructions: "Handle technical architecture and complex problem solving"
    
  - name: ProjectCoordinator
    model: gpt-4o-mini
    temperature: 0.3
    instructions: "Coordinate tasks and manage timelines"
```

### Environment-Specific Configuration
Configure agents for different environments:

```yaml
agents:
  - name: "${ENV}_Support_Agent"
    model: "${SUPPORT_MODEL:gpt-4o}"
    temperature: ${SUPPORT_TEMP:0.2}
    reasoning_effort: "${SUPPORT_REASONING:medium}"
    instructions: >
      You are a customer support agent for the ${ENV:production} environment.
      Support level: ${SUPPORT_LEVEL:L1}
      Escalation contact: ${ESCALATION_EMAIL:support@company.com}
```

### Cost Optimization
Balance performance with cost using different GPT models:

```yaml
agents:
  - name: PremiumAnalyst
    model: gpt-4o
    temperature: 0.2
    reasoning_effort: "high"
    instructions: "Handle complex analysis requiring premium capabilities"
    
  - name: StandardAssistant
    model: gpt-4o-mini
    temperature: 0.5
    instructions: "Handle standard assistance tasks efficiently"
    
  - name: BudgetReviewer
    model: gpt-4o-mini
    temperature: 0.1
    instructions: "Review content for quality and accuracy"
```

## Agent Limitations

### Context Window Constraints
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
    reasoning_effort: "${AGENT_REASONING:medium}"
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
    reasoning_effort: "${ENV_REASONING:medium}"
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
    temperature: ${MANAGER_TEMP:0.2}
    reasoning_effort: "${MANAGER_REASONING:high}"
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
export AGENT_REASONING="high"

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

:::tip Agent Customization
Use environment variables to create reusable agent configurations that can be customized for different environments, companies, or use cases without modifying the YAML files.
:::

## Related Topics

- [Teams](teams) - Learn about team orchestration, delegation patterns, and workflow management
- [Orchestration](coordination/orchestration) - Understand agent coordination and workflow management
- [Handoffs](coordination/handoffs) - Learn about control transfer mechanisms
- [Delegation](coordination/delegation) - Understand task assignment and response handling with delegation configuration
- [Tools](tools/intro) - Explore available tools for agents
- [Knowledge Bases](knowledge-bases/intro) - Understand knowledge base integration
- [Quickstart](quickstart) - Get started with your first team

## Next Steps

Now that you understand advanced agent configuration, learn how to:
- [Configure teams](teams) with orchestration and delegation patterns
- [Set up orchestration](coordination/orchestration) for agent coordination
- [Use handoffs](coordination/handoffs) for control transfer
- [Implement delegation](coordination/delegation) for task assignment
- [Add tools](tools/intro) to enhance agent capabilities
- [Set up knowledge bases](knowledge-bases/intro) for information access
- [Create your first team](quickstart) with the quickstart guide