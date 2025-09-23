---
sidebar_position: 2
---

# Async Configuration

Learn how to configure asynchronous execution for tools and delegation in your Gnosari AI Teams.

## Async Tool Configuration

Any built-in tool can be configured to run asynchronously by adding the `mode: async` parameter to its configuration.

### Basic Async Tool Setup

```yaml
name: "My Team"
description: "Team with async tools"

tools:
  - name: "file_ops"
    module: "gnosari.tools.builtin.file_operations"
    class: "FileOperationsTool"
    mode: async  # Enable async execution
    args:
      base_directory: "./workspace"
      allowed_extensions: [".txt", ".json", ".md"]
  
  - name: "api_tool"
    module: "gnosari.tools.builtin.api_request"
    class: "APIRequestTool"
    mode: async  # This tool will also run async

agents:
  - name: "File Manager"
    instructions: "Manage files asynchronously"
    tools: ["file_ops", "api_tool"]
```

### How Async Tools Work

When a tool is configured with `mode: async`:

1. **Wrapper Creation**: The tool is automatically wrapped with `AsyncToolWrapper`
2. **Queue Submission**: Tool execution is submitted to the Celery queue
3. **Non-blocking**: The agent continues without waiting for completion
4. **Result Handling**: Results are processed when the task completes

### Supported Tools

All built-in tools support async mode:
- `FileOperationsTool`
- `APIRequestTool`
- `BashOperationsTool`
- `InteractiveBashOperationsTool`
- `KnowledgeQueryTool`
- `MySQLQueryTool`
- `WebsiteContentTool`

## Async Delegation Configuration

Delegation between agents can also be configured to run asynchronously, enabling non-blocking agent coordination.

### Basic Async Delegation

```yaml
name: "Documentation Team"
description: "Team with async delegation"

agents:
  - name: "Documentation Manager"
    instructions: "Coordinate documentation tasks"
    orchestrator: true
    delegation:
      - agent: "Content Writer"
        mode: async  # Enable async delegation
        instructions: "Write documentation content"
      - agent: "Code Reviewer"
        mode: async  # This delegation is also async
        instructions: "Review code for documentation"
  
  - name: "Content Writer"
    instructions: "Write high-quality documentation"
  
  - name: "Code Reviewer"
    instructions: "Review code and provide feedback"
```

### Delegation Modes

You can mix sync and async delegation in the same agent:

```yaml
agents:
  - name: "Manager"
    delegation:
      - agent: "Critical Task Handler"
        # No mode specified = sync (blocking)
        instructions: "Handle critical tasks immediately"
      
      - agent: "Background Processor"
        mode: async
        instructions: "Process this in the background"
      
      - agent: "Report Generator"
        mode: async
        instructions: "Generate reports asynchronously"
```

### How Async Delegation Works

When delegation is configured with `mode: async`:

1. **Detection**: The TeamBuilder detects async mode in delegation configuration
2. **Wrapper Creation**: Creates an async-wrapped delegation tool
3. **Queue Processing**: Delegation requests are submitted to the queue
4. **Parallel Execution**: Multiple delegations can run concurrently

## Environment Variables

Configure Redis connection for the queue system in your `.env` file:

```bash
# Queue System Configuration (Celery with Redis)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Optional: Worker Configuration
CELERY_WORKER_CONCURRENCY=4
CELERY_WORKER_QUEUE=gnosari_queue
```

## Advanced Configuration

### Custom Queue Names

Different tools can use different queues for priority-based processing:

```yaml
tools:
  - name: "high_priority_tool"
    module: "gnosari.tools.builtin.api_request"
    class: "APIRequestTool"
    mode: async
    queue: "high_priority"  # Custom queue name
  
  - name: "low_priority_tool"
    module: "gnosari.tools.builtin.file_operations"
    class: "FileOperationsTool"
    mode: async
    queue: "low_priority"   # Different queue
```

### Retry Configuration

Configure retry behavior for async operations:

```yaml
tools:
  - name: "retry_tool"
    module: "gnosari.tools.builtin.api_request"
    class: "APIRequestTool"
    mode: async
    retry_config:
      max_retries: 5
      retry_delay: 60  # seconds
      exponential_backoff: true
```

## Best Practices

### When to Use Async Mode

✅ **Good for async:**
- Long-running API calls
- File processing operations
- Database queries
- Background report generation
- Non-critical delegations

❌ **Keep sync for:**
- Quick operations (< 1 second)
- Critical path operations
- Operations requiring immediate results
- Simple text processing

### Performance Considerations

1. **Worker Scaling**: Start with 2-4 workers, scale based on queue length
2. **Queue Monitoring**: Use Flower UI to monitor queue depth
3. **Memory Usage**: Async operations use more memory per task
4. **Error Handling**: Implement proper retry logic for failed tasks

### Error Handling

```yaml
# Configure robust error handling
tools:
  - name: "robust_tool"
    module: "gnosari.tools.builtin.api_request"
    class: "APIRequestTool"
    mode: async
    error_handling:
      max_retries: 3
      retry_delay: 30
      dead_letter_queue: "failed_tasks"
```

## Troubleshooting

### Common Issues

1. **Tasks not processing**: Check if workers are running with `gnosari worker status`
2. **Redis connection errors**: Verify Redis is running and connection settings
3. **Memory issues**: Reduce worker concurrency or increase system memory
4. **Stale tasks**: Clear Redis queues or restart workers

### Debugging

Enable debug logging for queue operations:

```bash
# Set log level for detailed queue debugging
LOG_LEVEL=DEBUG gnosari worker start
```

Monitor task execution in real-time:

```bash
# Watch Flower UI for live task monitoring
gnosari flower
# Visit http://localhost:5555
```