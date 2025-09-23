---
sidebar_position: 1
---

# Queues & Async Processing

Gnosari AI Teams supports asynchronous job processing through a powerful queue system built on **Celery** with **Redis** as the message broker. This enables agents to execute tools and delegate tasks asynchronously, allowing for better scalability and non-blocking operations.

## Overview

The queue system provides several key capabilities:

- 🔄 **Async Tool Execution**: Any built-in tool can be executed asynchronously
- 🤝 **Async Delegation**: Agents can delegate tasks to other agents without blocking
- ⚡ **Scalable Processing**: Multiple workers can process jobs concurrently
- 📊 **Monitoring**: Built-in monitoring with Flower UI
- 🛠️ **Worker Management**: Start, stop, and monitor workers via CLI

## Architecture

```mermaid
graph TB
    A[Agent] -->|Creates Message| B[Redis Queue]
    B --> C[Celery Worker 1]
    B --> D[Celery Worker 2]
    B --> E[Celery Worker N]
    C --> F[Tool Execution]
    D --> G[Delegation]
    E --> H[Other Tasks]
    I[Flower UI] -->|Monitors| B
```

## Key Components

### Messages
- **BaseMessage**: Foundation for all queue messages with validation
- **ToolExecutionMessage**: Executes any built-in tool asynchronously
- **Custom Messages**: Extend BaseMessage for specific use cases

### Consumers
- **BaseConsumer**: Abstract base for all message processors
- **ToolExecutionConsumer**: Generic consumer for tool execution
- **Custom Consumers**: Process specific message types

### Configuration
- **CeleryConfig**: Centralized Celery configuration with best practices
- **Environment Variables**: Redis broker and result backend configuration
- **Queue Names**: Configurable queue routing for different task types

## Getting Started

1. **Start Redis** (via docker-compose):
   ```bash
   docker-compose up redis -d
   ```

2. **Start Workers**:
   ```bash
   poetry run gnosari worker start
   ```

3. **Monitor with Flower**:
   ```bash
   poetry run gnosari flower
   # Visit http://localhost:5555
   ```

4. **Configure Async Tools** in your team YAML:
   ```yaml
   tools:
     - name: "file_ops"
       module: "gnosari.tools.builtin.file_operations"
       class: "FileOperationsTool"
       mode: async  # Enable async execution
   ```

## Next Steps

- [Async Configuration](./async-configuration): Learn how to configure async mode for tools and delegation
- [CLI Commands](./cli-commands): Master the worker management commands
- [Worker Management](./worker-management): Advanced worker configuration and monitoring