# Gnosari Queue System

The Gnosari Queue System provides a robust, Celery-based asynchronous job processing framework. It follows best practices with clean separation of concerns, type safety through Pydantic models, and easy extensibility.

## Architecture Overview

The queue system is built on:
- **Celery**: Distributed task queue
- **Redis**: Message broker and result backend
- **Pydantic**: Message validation and serialization
- **Base Classes**: Consistent patterns for messages and consumers

### Key Components

1. **BaseMessage**: Abstract base class for all queue messages
2. **BaseConsumer**: Abstract base class for all message consumers  
3. **CeleryConfig**: Centralized configuration following best practices
4. **Celery App**: Pre-configured application instance

## Getting Started

### 1. Setup Redis

Redis is included in the docker-compose.yml:

```bash
# Start Redis service
docker-compose up redis -d
```

### 2. Install Dependencies

Dependencies are already added to pyproject.toml:
- `celery[redis]` - Celery with Redis support
- `redis` - Redis Python client

```bash
poetry install
```

### 3. Start Worker

```bash
# Start a Celery worker
poetry run gnosari worker

# With custom options
poetry run gnosari worker --concurrency 4 --queue custom_queue --loglevel debug
```

## Creating Messages

### Step 1: Define Your Message Class

Create a new message class inheriting from `BaseMessage`:

```python
# src/gnosari/queue/consumers/my_feature.py
from typing import Dict, Any
from pydantic import Field
from ..base import BaseMessage
import uuid

class MyFeatureMessage(BaseMessage):
    \"\"\"Message for my feature processing.\"\"\"
    
    user_id: str = Field(description="User ID who triggered this task")
    task_type: str = Field(description="Type of task to perform")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Task parameters")
    
    @classmethod
    def create(cls, user_id: str, task_type: str, parameters: Dict[str, Any] = None) -> "MyFeatureMessage":
        \"\"\"Create a new message instance.\"\"\"
        return cls(
            message_id=str(uuid.uuid4()),
            user_id=user_id,
            task_type=task_type,
            parameters=parameters or {}
        )
```

### Step 2: Define Message Validation

Use Pydantic validators for complex validation:

```python
from pydantic import validator

class MyFeatureMessage(BaseMessage):
    # ... fields ...
    
    @validator('task_type')
    def validate_task_type(cls, v):
        allowed_types = ['process', 'analyze', 'generate']
        if v not in allowed_types:
            raise ValueError(f'task_type must be one of {allowed_types}')
        return v
    
    @validator('parameters')
    def validate_parameters(cls, v, values):
        task_type = values.get('task_type')
        if task_type == 'process' and 'input_data' not in v:
            raise ValueError('input_data required for process tasks')
        return v
```

## Creating Consumers

### Step 1: Define Your Consumer Class

Create a consumer class inheriting from `BaseConsumer`:

```python
# src/gnosari/queue/consumers/my_feature.py
import asyncio
from typing import Dict, Any
from ..base import BaseConsumer

class MyFeatureConsumer(BaseConsumer):
    \"\"\"Consumer for processing my feature messages.\"\"\"
    
    async def process(self, message: MyFeatureMessage) -> Dict[str, Any]:
        \"\"\"Process the message.\"\"\"
        print(f"Processing {message.task_type} for user {message.user_id}")
        
        # Simulate async work
        await asyncio.sleep(2)
        
        # Perform actual processing based on task_type
        if message.task_type == "process":
            result = self._process_data(message.parameters.get("input_data"))
        elif message.task_type == "analyze":
            result = self._analyze_data(message.parameters)
        else:
            result = {"status": "unknown_task"}
        
        return {
            "message_id": message.message_id,
            "user_id": message.user_id,
            "result": result,
            "processed_at": message.created_at.isoformat()
        }
    
    def _process_data(self, input_data: Any) -> Dict[str, Any]:
        \"\"\"Process input data.\"\"\"
        # Your processing logic here
        return {"processed": True, "data": input_data}
    
    def _analyze_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        \"\"\"Analyze data based on parameters.\"\"\"
        # Your analysis logic here
        return {"analysis": "completed", "parameters": parameters}
    
    def on_success(self, result: Dict[str, Any], message: MyFeatureMessage) -> None:
        \"\"\"Called when processing succeeds.\"\"\"
        print(f"✅ Successfully processed {message.task_type} task {message.message_id}")
    
    def on_failure(self, exc: Exception, message: MyFeatureMessage) -> None:
        \"\"\"Called when processing fails.\"\"\"
        print(f"❌ Failed to process {message.task_type} task {message.message_id}: {exc}")
    
    def should_retry(self, exc: Exception, message: MyFeatureMessage) -> bool:
        \"\"\"Determine if message should be retried.\"\"\"
        # Custom retry logic
        if isinstance(exc, ValueError):
            return False  # Don't retry validation errors
        return message.retry_count < message.max_retries
```

### Step 2: Create the Celery Task

Create a Celery task that uses your consumer:

```python
# src/gnosari/queue/consumers/my_feature.py
from ..app import celery_app
import asyncio

@celery_app.task(bind=True)
def process_my_feature_task(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
    \"\"\"Celery task for processing my feature messages.\"\"\"
    consumer = MyFeatureConsumer()
    message = MyFeatureMessage.from_dict(message_data)
    
    try:
        # Run async process method
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(consumer.process(message))
        loop.close()
        
        consumer.on_success(result, message)
        return result
    except Exception as exc:
        consumer.on_failure(exc, message)
        
        if consumer.should_retry(exc, message):
            message.retry_count += 1
            # Retry with exponential backoff
            raise self.retry(
                countdown=2 ** message.retry_count,
                max_retries=message.max_retries
            )
        raise
```

### Step 3: Create Helper Functions

Add helper functions for sending messages:

```python
# src/gnosari/queue/consumers/my_feature.py
def send_my_feature_message(user_id: str, task_type: str, parameters: Dict[str, Any] = None) -> str:
    \"\"\"Send a my feature message to the queue.\"\"\"
    message = MyFeatureMessage.create(user_id, task_type, parameters)
    process_my_feature_task.delay(message.to_dict())
    return message.message_id

def send_my_feature_message_priority(user_id: str, task_type: str, parameters: Dict[str, Any] = None, priority: int = 5) -> str:
    \"\"\"Send a priority my feature message to the queue.\"\"\"
    message = MyFeatureMessage.create(user_id, task_type, parameters)
    message.priority = priority
    process_my_feature_task.apply_async(
        args=[message.to_dict()],
        priority=priority
    )
    return message.message_id
```

### Step 4: Register Your Consumer

Update the consumers `__init__.py`:

```python
# src/gnosari/queue/consumers/__init__.py
from .example import ExampleMessage, ExampleConsumer, process_example_task
from .my_feature import MyFeatureMessage, MyFeatureConsumer, process_my_feature_task

__all__ = [
    "ExampleMessage", "ExampleConsumer", "process_example_task",
    "MyFeatureMessage", "MyFeatureConsumer", "process_my_feature_task"
]
```

## Usage Examples

### Sending Messages

```python
from gnosari.queue.consumers.my_feature import send_my_feature_message

# Send a simple message
message_id = send_my_feature_message(
    user_id="user123",
    task_type="process",
    parameters={"input_data": "some data to process"}
)

print(f"Sent message: {message_id}")
```

### Working with Message Results

```python
from gnosari.queue.consumers.my_feature import process_my_feature_task

# Send message and get result
result = process_my_feature_task.delay({
    "message_id": "test-123",
    "user_id": "user123", 
    "task_type": "analyze",
    "parameters": {"data": "test"},
    "created_at": "2024-01-01T00:00:00Z",
    "priority": 5,
    "retry_count": 0,
    "max_retries": 3
})

# Get result (blocking)
final_result = result.get(timeout=60)
print(final_result)
```

### Error Handling

```python
from celery.exceptions import Retry

try:
    result = process_my_feature_task.delay(message_data)
    final_result = result.get(timeout=30)
except Retry:
    print("Task is being retried")
except Exception as e:
    print(f"Task failed: {e}")
```

## Best Practices

### 1. Message Design
- Keep messages immutable after creation
- Include all necessary data in the message
- Use descriptive field names and documentation
- Validate input data with Pydantic validators

### 2. Consumer Design
- Keep consumers stateless
- Use dependency injection for external services
- Implement proper error handling
- Log important events and errors

### 3. Error Handling
- Distinguish between retryable and non-retryable errors
- Use exponential backoff for retries
- Set reasonable retry limits
- Log failures for monitoring

### 4. Performance
- Use appropriate concurrency settings
- Monitor queue length and processing times
- Consider message batching for high-throughput scenarios
- Use message priorities for urgent tasks

### 5. Monitoring
- Log processing times
- Track success/failure rates
- Monitor queue depth
- Set up alerts for failed messages

## Configuration

### Environment Variables

```bash
# .env file
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Custom Configuration

Modify `src/gnosari/queue/config.py` for custom settings:

```python
class CeleryConfig:
    # Custom queue routing
    task_routes = {
        'gnosari.queue.consumers.my_feature.*': {'queue': 'my_feature_queue'},
        'gnosari.queue.consumers.urgent.*': {'queue': 'urgent_queue'}
    }
    
    # Custom retry settings
    task_retry_delay = 60  # 1 minute
    task_max_retries = 5
```

## Running Workers

### Basic Worker
```bash
poetry run gnosari worker
```

### Multiple Queues
```bash
poetry run gnosari worker --queue my_feature_queue,urgent_queue
```

### High Concurrency
```bash
poetry run gnosari worker --concurrency 8
```

### Docker Deployment
```bash
# In docker-compose.yml
services:
  gnosari-worker:
    build: .
    command: poetry run gnosari worker --concurrency 4
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
    depends_on:
      - redis
```

## Testing

### Unit Testing Consumers

```python
import pytest
from unittest.mock import AsyncMock
from gnosari.queue.consumers.my_feature import MyFeatureConsumer, MyFeatureMessage

@pytest.mark.asyncio
async def test_my_feature_consumer():
    consumer = MyFeatureConsumer()
    message = MyFeatureMessage.create(
        user_id="test_user",
        task_type="process",
        parameters={"input_data": "test"}
    )
    
    result = await consumer.process(message)
    
    assert result["user_id"] == "test_user"
    assert result["result"]["processed"] is True
```

### Integration Testing

```python
def test_message_processing_integration():
    from gnosari.queue.consumers.my_feature import process_my_feature_task
    
    message_data = {
        "message_id": "test-123",
        "user_id": "test_user",
        "task_type": "analyze", 
        "parameters": {"data": "test"},
        "created_at": "2024-01-01T00:00:00Z",
        "priority": 5,
        "retry_count": 0,
        "max_retries": 3
    }
    
    # Test synchronously
    result = process_my_feature_task.apply(args=[message_data])
    assert result.successful()
    assert result.result["user_id"] == "test_user"
```

## Async Tool Execution

The queue system provides seamless async execution for all builtin tools. Tools can be configured to execute either synchronously (immediate) or asynchronously (via queue) based on configuration.

### Tool Configuration for Async Execution

Add `mode: async` to any tool configuration in your team YAML:

```yaml
tools:
  - name: "File Manager"
    id: "file_tool_async"
    mode: "async"
    priority: 5
    description: "Manages files asynchronously via queue system"
    module: "gnosari.tools.builtin.file_operations"
    class: "FileOperationsTool"
    args:
      base_directory: "./workspace"
      allowed_extensions: [".txt", ".json", ".md", ".py"]
  
  - name: "API Request Tool"
    id: "api_tool_async"
    mode: "async" 
    priority: 2
    queue_name: "high_priority_queue"
    description: "Makes HTTP requests asynchronously"
    module: "gnosari.tools.builtin.api_request"
    class: "APIRequestTool"
```

### Async Tool Parameters

- **`mode`**: `"sync"` (default) or `"async"`
- **`priority`**: Integer 1-10 (lower numbers = higher priority, default: 5)
- **`queue_name`**: Queue name for async execution (default: "gnosari_queue")

### How Async Tools Work

1. **Sync Mode**: Tool executes immediately and returns results
2. **Async Mode**: Tool creates a queue message and returns task information

### Agent Usage

Agents can choose execution mode at runtime:

```yaml
# Agent can use both sync and async versions
agents:
  - name: "Task Manager"
    tools: 
      - "file_tool_async"    # Always async
      - "file_tool_sync"     # Always sync
```

Or agents can control execution mode dynamically:

```python
# Agent decides execution mode
{
  "operation": "write",
  "file_path": "report.txt", 
  "content": "data",
  "execution_mode": "async",    # Agent chooses async
  "async_priority": 3           # High priority
}
```

### Tool Execution Consumer

The generic `ToolExecutionConsumer` can execute any builtin tool asynchronously:

```python
# Message structure for any tool
{
  "task_id": "unique-task-id",
  "tool_name": "file_operations",
  "tool_module": "gnosari.tools.builtin.file_operations", 
  "tool_class": "FileOperationsTool",
  "tool_init_args": {"base_directory": "./workspace"},
  "tool_args": '{"operation": "write", "file_path": "test.txt"}',
  "priority": 5
}
```

### Example: File Operations Async

```yaml
# In team configuration
tools:
  - name: "Async File Manager"
    mode: "async"
    module: "gnosari.tools.builtin.file_operations"
    class: "FileOperationsTool"
    args:
      base_directory: "./data"
```

When an agent uses this tool:
1. Tool wrapper intercepts the call
2. Creates `ToolExecutionMessage` with tool configuration
3. Sends message to queue with priority
4. Returns task tracking information to agent
5. Worker processes task asynchronously
6. Results logged by worker

### Example: Delegation Async

```yaml
tools:
  - name: "Async Delegator"
    mode: "async"
    priority: 1  # Highest priority
    module: "gnosari.tools.builtin.delegation"
    class: "DelegateAgentTool"
```

Delegation tasks are queued and processed by workers, allowing for:
- Non-blocking delegation
- Priority-based agent scheduling
- Scalable agent coordination

### Benefits

1. **Non-blocking**: Long-running tools don't block agents
2. **Scalable**: Multiple workers process tools in parallel
3. **Prioritized**: Critical tasks processed first
4. **Reliable**: Failed tasks automatically retried
5. **Generic**: Works with any builtin tool without modification

### Running Workers

```bash
# Start worker to process async tools
poetry run gnosari worker

# High concurrency for async tools
poetry run gnosari worker --concurrency 8 --queue gnosari_queue
```

This queue system provides a solid foundation for building scalable, maintainable async job processing in Gnosari while following the Single Responsibility Principle and maintaining clean, type-safe code.