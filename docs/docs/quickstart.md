---
sidebar_position: 2
---

# Quickstart Guide

Get up and running with Gnosari AI Teams in minutes! This guide will walk you through creating your first multi-agent team, configuring it with YAML, and running it with the CLI.

## Prerequisites

Before you begin, make sure you have:

- **Python 3.12+** installed on your system
- **Poetry** for dependency management
- **API Keys** for the LLM providers you want to use

:::tip Python Version
Gnosari AI Teams requires Python 3.12 or higher. Check your version with `python --version`.
:::

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/neomanex/gnosari-engine.git
cd gnosari-engine
```

### 2. Install Dependencies

```bash
poetry install
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root with your API keys:

```bash
# OpenAI (required for most examples)
OPENAI_API_KEY=your-openai-api-key

# Optional: Other providers
ANTHROPIC_API_KEY=your-anthropic-key
DEEPSEEK_API_KEY=your-deepseek-key
```

:::warning API Keys
Never commit your `.env` file to version control. Add it to your `.gitignore` file.
:::

## Your First Team

Let's create a simple team with two agents that can work together.

### 1. Create a Team Configuration

Create a file called `my-first-team.yaml`:

```yaml
name: My First Team

# Define tools for the team
tools:
  - name: delegate_agent
    module: gnosari.tools.delegate_agent
    class: DelegateAgentTool
    args:
      pass

# Define agents
agents:
  - name: Coordinator
    instructions: >
      You are a helpful coordinator who manages tasks and delegates work to specialists.
      When you receive a request, analyze it and delegate to the appropriate specialist.
      Always provide a summary of the work completed.
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent

  - name: Writer
    instructions: >
      You are a professional writer who creates clear, engaging content.
      When given a writing task, focus on clarity, structure, and engaging the reader.
      Always ask for clarification if the requirements are unclear.
    model: gpt-4o

  - name: Researcher
    instructions: >
      You are a thorough researcher who gathers and analyzes information.
      When given a research task, provide comprehensive, well-sourced information.
      Always cite your sources and note any limitations in the information.
    model: gpt-4o
```

:::info Team Structure
This team has:
- **1 Orchestrator**: The Coordinator who manages tasks
- **2 Specialists**: Writer and Researcher who handle specific tasks
- **1 Tool**: delegate_agent for task delegation
:::

### 2. Run Your Team

Now let's run the team with a message:

```bash
poetry run gnosari --config "my-first-team.yaml" --message "Write a blog post about the benefits of renewable energy"
```

You can also run a specific agent from the team:

```bash
poetry run gnosari --config "my-first-team.yaml" --message "Research renewable energy trends" --agent "Researcher"
```

:::tip CLI Command Structure
The basic command structure is:
```bash
# Run entire team
poetry run gnosari --config "team.yaml" --message "your message"

# Run specific agent
poetry run gnosari --config "team.yaml" --message "your message" --agent "AgentName"
```
:::

### 3. Watch the Magic Happen

You'll see output like this:

```
🤖 Gnosari AI Teams - Multi-Agent Orchestration
📋 Team: My First Team
🎯 Message: Write a blog post about the benefits of renewable energy

[Coordinator] Analyzing the request and delegating to specialists...

[Coordinator] Delegating research task to Researcher...
[Researcher] Gathering comprehensive information about renewable energy benefits...

[Coordinator] Delegating writing task to Writer...
[Writer] Creating engaging blog post content...

[Coordinator] Compiling final blog post with research insights...
```

## Advanced Team Configuration

Let's create a more sophisticated team with multiple tools and capabilities.

### 1. Create an Advanced Team

Create `advanced-team.yaml`:

```yaml
name: Advanced Content Team

# Knowledge bases (automatically adds knowledge_query tool)
knowledge:
  - name: "company_docs"
    type: "website"
    data: ["https://docs.yourcompany.com"]

# Tools configuration
tools:
  - name: delegate_agent
    module: gnosari.tools.delegate_agent
    class: DelegateAgentTool
    args:
      pass

  - name: api_request
    module: gnosari.tools.api_request
    class: APIRequestTool
    args:
      base_url: https://api.example.com
      base_headers:
        Authorization: Bearer ${API_TOKEN}
        Content-Type: application/json
      timeout: 30
      verify_ssl: true

  - name: mysql_query
    module: gnosari.tools.mysql_query
    class: MySQLQueryTool
    args:
      host: ${DB_HOST}
      port: 3306
      database: ${DB_NAME}
      username: ${DB_USER}
      password: ${DB_PASSWORD}
      pool_size: 5
      query_timeout: 30

# Agents configuration
agents:
  - name: Content Manager
    instructions: >
      You are a content manager who coordinates content creation workflows.
      You can delegate tasks to specialists and use various tools to gather information.
      Always ensure content is accurate, engaging, and meets quality standards.
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent
      - knowledge_query
    knowledge: ["company_docs"]

  - name: Data Analyst
    instructions: >
      You are a data analyst who works with databases and APIs to gather insights.
      Use the mysql_query tool to analyze data and the api_request tool to fetch external data.
      Always provide clear, actionable insights based on the data.
    model: gpt-4o
    tools:
      - mysql_query
      - api_request

  - name: Content Writer
    instructions: >
      You are a professional content writer who creates engaging, well-researched content.
      Use the knowledge_query tool to access company documentation and ensure accuracy.
      Focus on creating content that resonates with the target audience.
    model: gpt-4o
    tools:
      - knowledge_query
    knowledge: ["company_docs"]

  - name: Research Specialist
    instructions: >
      You are a research specialist who gathers and analyzes information from multiple sources.
      Use the api_request tool to fetch data from external APIs and services.
      Always verify information and provide comprehensive analysis.
    model: gpt-4o
    tools:
      - api_request
```

:::info Advanced Features
This team includes:
- **Knowledge Base**: Company documentation for context
- **Multiple Tools**: Database queries, API requests, knowledge queries
- **Specialized Agents**: Each with specific tools and capabilities
- **Environment Variables**: Secure credential management
:::

### 2. Run with Streaming

Use the `--stream` flag to see real-time output:

```bash
poetry run gnosari --config "advanced-team.yaml" --message "Create a market analysis report for Q4" --stream
```

:::tip Streaming Output
The `--stream` flag shows real-time agent activity, making it easier to follow the workflow and debug issues.
:::

### 3. Debug Mode

Use `--debug` to see detailed logs:

```bash
poetry run gnosari --config "advanced-team.yaml" --message "Create a market analysis report for Q4" --debug
```

:::tip Debug Mode
Debug mode shows detailed JSON events and tool execution logs, perfect for troubleshooting and understanding agent behavior.
:::

## CLI Options

The Gnosari CLI supports various options for different use cases:

### Basic Usage

```bash
# Basic team execution
poetry run gnosari --config "team.yaml" --message "Your message"

# Run specific agent from team
poetry run gnosari --config "team.yaml" --message "Your message" --agent "AgentName"

# With streaming output
poetry run gnosari --config "team.yaml" --message "Your message" --stream

# With debug mode
poetry run gnosari --config "team.yaml" --message "Your message" --debug

# With custom model and temperature
poetry run gnosari --config "team.yaml" --message "Your message" --model "gpt-4o" --temperature 0.7
```

### Advanced Options

```bash
# All options combined
poetry run gnosari \
  --config "team.yaml" \
  --message "Your message" \
  --stream \
  --debug \
  --model "gpt-4o" \
  --temperature 0.5
```

:::info CLI Options
- `--config`: Path to team YAML configuration file
- `--message`: Message to send to the team
- `--agent`: Run only a specific agent from the team (by name)
- `--stream`: Enable real-time streaming output
- `--debug`: Enable debug mode with detailed logs
- `--model`: Override the model for all agents
- `--temperature`: Override the temperature for all agents
:::

## Environment Variables

Set up your environment variables for different providers:

```bash
# .env file
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
DEEPSEEK_API_KEY=your-deepseek-key
GOOGLE_API_KEY=your-google-key

# Database credentials
DB_HOST=localhost
DB_PORT=3306
DB_NAME=my_database
DB_USER=my_user
DB_PASSWORD=my_password

# API credentials
API_TOKEN=your-api-token
```

:::warning Environment Security
- Never commit `.env` files to version control
- Use different API keys for development and production
- Rotate API keys regularly
- Use environment-specific configurations
:::

## Common Patterns

### 1. Simple Coordination Team

```yaml
name: Simple Team
tools:
  - name: delegate_agent
    module: gnosari.tools.delegate_agent
    class: DelegateAgentTool
    args:
      pass

agents:
  - name: Manager
    instructions: "Coordinate tasks and delegate to specialists"
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent

  - name: Specialist
    instructions: "Handle specific tasks assigned by the manager"
    model: gpt-4o
```

### 2. Research and Writing Team

```yaml
name: Research Team
knowledge:
  - name: "research_docs"
    type: "website"
    data: ["https://research.example.com"]

tools:
  - name: delegate_agent
    module: gnosari.tools.delegate_agent
    class: DelegateAgentTool
    args:
      pass

agents:
  - name: Research Coordinator
    instructions: "Coordinate research and writing tasks"
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent
      - knowledge_query
    knowledge: ["research_docs"]

  - name: Researcher
    instructions: "Research topics using knowledge bases"
    model: gpt-4o
    tools:
      - knowledge_query
    knowledge: ["research_docs"]

  - name: Writer
    instructions: "Write content based on research"
    model: gpt-4o
```

### 3. Data Analysis Team

```yaml
name: Data Team
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
  - name: Data Manager
    instructions: "Coordinate data analysis tasks"
    orchestrator: true
    model: gpt-4o
    tools:
      - delegate_agent

  - name: Data Analyst
    instructions: "Analyze data using SQL queries"
    model: gpt-4o
    tools:
      - mysql_query
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Make sure you're in the project directory
   cd gnosari-engine
   
   # Reinstall dependencies
   poetry install
   ```

2. **API Key Errors**
   ```bash
   # Check your .env file
   cat .env
   
   # Verify API keys are set
   echo $OPENAI_API_KEY
   ```

3. **Configuration Errors**
   ```bash
   # Validate YAML syntax
   poetry run gnosari --config "team.yaml" --message "test" --debug
   ```

:::tip Troubleshooting Steps
1. Check your Python version (3.12+)
2. Verify all dependencies are installed
3. Ensure API keys are properly set
4. Validate YAML configuration syntax
5. Use debug mode to see detailed error information
:::

## Next Steps

Now that you've created your first team, explore more advanced features:

- 🤖 [Agents](/docs/agents) - Learn about agent configuration and instructions
- 👥 [Teams](/docs/teams) - Understand team structure and coordination patterns
- 🎭 [Orchestration](/docs/orchestration) - Learn about agent coordination and workflow management
- 📚 [Knowledge Bases](/docs/knowledge) - Set up knowledge bases for RAG capabilities
- 🛠️ [Tools Overview](/docs/tools/intro) - Learn about all available tools
- 📝 [Examples](/docs/examples) - Real-world use cases
- 🔧 [API Reference](/docs/api) - Complete API documentation

:::tip Ready to Build
You're now ready to create sophisticated multi-agent teams! Start with simple configurations and gradually add more tools and capabilities as you become familiar with the framework.
:::

Happy building with Gnosari AI Teams! 🚀