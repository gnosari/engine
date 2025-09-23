---
sidebar_position: 4
---

# Worker Management

Advanced worker configuration, monitoring, and scaling strategies for production deployments.

## Worker Architecture

### Process Model

Gnosari uses Celery's multiprocessing worker model:

```text
Master Process
├── Worker Process 1 (Queue: high_priority)
├── Worker Process 2 (Queue: normal)
├── Worker Process 3 (Queue: background)
└── Worker Process N
```

Each worker process can handle multiple concurrent tasks based on the tool type and system resources.

### Worker Types

#### Prefork Workers (Default)
- **Best for**: CPU-bound tasks, tool execution, file operations
- **Concurrency**: Process-based parallelism
- **Memory**: Higher per-worker overhead
- **Isolation**: Complete process isolation

```bash
# Start prefork workers (default)
poetry run gnosari worker start --concurrency 4
```

#### Thread Workers
- **Best for**: I/O-bound tasks, API calls, database queries
- **Concurrency**: Thread-based parallelism  
- **Memory**: Lower overhead
- **Isolation**: Shared memory space

```bash
# Note: Thread workers require additional Celery configuration
# Currently using prefork by default for better isolation
```

## Scaling Strategies

### Horizontal Scaling

Run multiple worker instances across different processes:

```bash
# Terminal 1: High-priority queue
poetry run gnosari worker start --queue critical --concurrency 2

# Terminal 2: Normal priority queue  
poetry run gnosari worker start --queue normal --concurrency 4

# Terminal 3: Background processing
poetry run gnosari worker start --queue background --concurrency 1
```

### Vertical Scaling

Increase concurrency within a single worker instance:

```bash
# Scale up for CPU-intensive workloads
poetry run gnosari worker start --concurrency 8

# Scale down for memory-constrained environments
poetry run gnosari worker start --concurrency 1
```

### Auto-scaling with Monitoring

Monitor queue depth and scale workers dynamically:

```python
# Example monitoring script (not included in core)
import redis
import subprocess

r = redis.Redis(host='localhost', port=6379, db=0)
queue_length = r.llen('gnosari_queue')

if queue_length > 100:
    # Scale up workers
    subprocess.run(['poetry', 'run', 'gnosari', 'worker', 'start', '--concurrency', '8'])
elif queue_length < 10:
    # Scale down workers
    subprocess.run(['poetry', 'run', 'gnosari', 'worker', 'restart', '--concurrency', '2'])
```

## Configuration Management

### Environment-based Configuration

Configure workers through environment variables:

```bash
# .env file
CELERY_WORKER_CONCURRENCY=4
CELERY_WORKER_LOGLEVEL=info
CELERY_WORKER_PREFETCH_MULTIPLIER=1
CELERY_WORKER_MAX_TASKS_PER_CHILD=1000
CELERY_WORKER_DISABLE_RATE_LIMITS=true

# Redis Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP=true
```

### Production Configuration

Recommended settings for production environments:

```bash
# Production .env
CELERY_WORKER_CONCURRENCY=8
CELERY_WORKER_LOGLEVEL=warning
CELERY_WORKER_PREFETCH_MULTIPLIER=1
CELERY_WORKER_MAX_TASKS_PER_CHILD=1000
CELERY_TASK_SOFT_TIME_LIMIT=300
CELERY_TASK_TIME_LIMIT=600
CELERY_WORKER_SEND_TASK_EVENTS=true
CELERY_TASK_SEND_SENT_EVENT=true
```

## Monitoring and Observability

### Real-time Monitoring

#### Flower Dashboard

Access comprehensive monitoring at http://localhost:5555:

- **Workers**: Active workers, their status, and processing capacity
- **Tasks**: Real-time task execution, success/failure rates
- **Queues**: Queue lengths, message flow, and bottlenecks
- **Performance**: Task execution times, throughput metrics

#### CLI Monitoring

```bash
# Quick status check
poetry run gnosari worker status

# Detailed Redis queue inspection
docker-compose exec redis redis-cli info

# Monitor worker resource usage
ps aux | grep celery
htop
```

### Logging Configuration

#### Structured Logging

```bash
# Enable detailed logging
poetry run gnosari worker start --loglevel debug

# Log to file
poetry run gnosari worker start --loglevel info > worker.log 2>&1
```

#### Log Analysis

Monitor worker logs for patterns:

```bash
# Search for errors
grep -i error worker.log

# Monitor task completion rates
grep -i "task.*succeeded" worker.log | wc -l

# Check for memory issues
grep -i "memory" worker.log
```

### Health Checks

#### Worker Health

```bash
# Check if workers are responsive
poetry run gnosari worker status

# Verify queue processing
docker-compose exec redis redis-cli llen gnosari_queue
```

#### Redis Health

```bash
# Test Redis connectivity
docker-compose exec redis redis-cli ping

# Check Redis memory usage
docker-compose exec redis redis-cli info memory

# Monitor Redis connections
docker-compose exec redis redis-cli info clients
```

## Performance Optimization

### Queue Configuration

#### Queue Routing

Route different task types to specialized queues:

```yaml
# Team configuration with queue routing
tools:
  - name: "fast_api_tool"
    module: "gnosari.tools.builtin.api_request"
    class: "APIRequestTool"
    mode: async
    queue: "fast_queue"
    
  - name: "slow_file_tool"
    module: "gnosari.tools.builtin.file_operations"
    class: "FileOperationsTool"
    mode: async
    queue: "slow_queue"
```

Start specialized workers:

```bash
# Fast queue workers (more concurrency)
poetry run gnosari worker start --queue fast_queue --concurrency 8

# Slow queue workers (less concurrency, more memory)
poetry run gnosari worker start --queue slow_queue --concurrency 2
```

#### Priority Queues

```yaml
# High-priority delegation
agents:
  - name: "Manager"
    delegation:
      - agent: "CriticalHandler"
        mode: async
        queue: "critical"
        priority: 9
      - agent: "BackgroundProcessor"
        mode: async
        queue: "background"
        priority: 1
```

### Memory Management

#### Worker Recycling

Prevent memory leaks by recycling workers:

```bash
# Set max tasks per worker before restart
CELERY_WORKER_MAX_TASKS_PER_CHILD=1000 poetry run gnosari worker start
```

#### Memory Monitoring

```bash
# Monitor worker memory usage
ps -o pid,ppid,cmd,%mem,%cpu -A | grep celery

# Check system memory
free -h
```

### Task Optimization

#### Batch Processing

Group related tasks to reduce overhead:

```python
# Example: Batch file operations
tasks = [
    {'operation': 'read', 'file': 'file1.txt'},
    {'operation': 'read', 'file': 'file2.txt'},
    {'operation': 'read', 'file': 'file3.txt'}
]
# Process as single batch rather than individual tasks
```

#### Result Storage

Configure result backend for optimal performance:

```bash
# Use Redis for fast results
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# Or disable results if not needed
CELERY_TASK_IGNORE_RESULT=true
```

## Troubleshooting

### Common Issues

#### Workers Not Starting

```bash
# Check Redis connectivity
docker-compose up redis -d
docker-compose logs redis

# Verify environment variables
echo $CELERY_BROKER_URL

# Test manual worker start
celery -A gnosari.queue.app.celery_app worker --loglevel debug
```

#### Tasks Not Processing

```bash
# Check queue contents
docker-compose exec redis redis-cli llen gnosari_queue

# Verify worker registration
poetry run gnosari flower
# Check "Workers" tab in browser
```

#### Memory Issues

```bash
# Check worker memory usage
ps aux | grep celery | awk '{print $4, $11}' | sort -nr

# Reduce worker concurrency
poetry run gnosari worker restart --concurrency 2

# Enable worker recycling
CELERY_WORKER_MAX_TASKS_PER_CHILD=500 poetry run gnosari worker start
```

#### Performance Issues

```bash
# Monitor queue backlog
watch -n 1 'docker-compose exec redis redis-cli llen gnosari_queue'

# Check task execution times in Flower
# Visit http://localhost:5555/tasks

# Profile worker resource usage
htop
iostat -x 1
```

### Debug Mode

Enable comprehensive debugging:

```bash
# Maximum debugging
CELERY_WORKER_LOGLEVEL=debug \
CELERY_WORKER_LOG_FORMAT="[%(asctime)s: %(levelname)s/%(processName)s] %(message)s" \
poetry run gnosari worker start --concurrency 1
```

### Recovery Procedures

#### Graceful Restart

```bash
# 1. Stop accepting new tasks
poetry run gnosari worker stop

# 2. Wait for current tasks to complete
sleep 30

# 3. Start fresh workers
poetry run gnosari worker start --concurrency 4
```

#### Emergency Reset

```bash
# 1. Stop all workers immediately
poetry run gnosari worker stop

# 2. Clear all queues (destructive!)
docker-compose exec redis redis-cli flushdb

# 3. Restart services
docker-compose restart redis
poetry run gnosari worker start
```

## Production Deployment

### Docker Deployment

```dockerfile
# Production Dockerfile for workers
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
ENV PYTHONPATH=/app

CMD ["celery", "-A", "gnosari.queue.app.celery_app", "worker", "--concurrency=4", "--loglevel=info"]
```

### Kubernetes Deployment

```yaml
# worker-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gnosari-worker
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gnosari-worker
  template:
    metadata:
      labels:
        app: gnosari-worker
    spec:
      containers:
      - name: worker
        image: gnosari-engine:latest
        command: ["poetry", "run", "gnosari", "worker", "start"]
        args: ["--concurrency", "4"]
        env:
        - name: CELERY_BROKER_URL
          value: "redis://redis-service:6379/0"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

### Process Management

Use process managers for production:

```ini
# supervisor.conf
[program:gnosari-worker]
command=poetry run gnosari worker start --concurrency 4
directory=/app
user=gnosari
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/gnosari-worker.log
```

### Monitoring Integration

```yaml
# Prometheus monitoring
apiVersion: v1
kind: Service
metadata:
  name: gnosari-worker-metrics
  labels:
    app: gnosari-worker
spec:
  ports:
  - port: 9540
    name: metrics
  selector:
    app: gnosari-worker
```