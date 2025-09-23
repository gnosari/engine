---
sidebar_position: 3
---

# CLI Commands

Master the Gnosari CLI commands for managing workers, monitoring queues, and running the async processing system.

## Worker Management

The `gnosari worker` command provides comprehensive worker lifecycle management.

### Start Workers

Start Celery workers to process async jobs:

```bash
# Start worker with default settings
poetry run gnosari worker start

# Start with custom concurrency
poetry run gnosari worker start --concurrency 4

# Start with specific queue
poetry run gnosari worker start --queue high_priority

# Start with debug logging
poetry run gnosari worker start --loglevel debug
```

#### Start Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--concurrency` | `-c` | `1` | Number of concurrent worker processes |
| `--queue` | `-q` | `gnosari_queue` | Queue name to process |
| `--loglevel` | `-l` | `info` | Log level: debug, info, warning, error |

### Stop Workers

Gracefully stop all running Celery workers:

```bash
# Stop all workers
poetry run gnosari worker stop
```

The stop command:
1. **Graceful termination**: Sends SIGTERM to allow current tasks to complete
2. **Timeout handling**: Waits 10 seconds for graceful shutdown
3. **Force kill**: Uses SIGKILL if workers don't stop gracefully
4. **Status reporting**: Shows which workers were stopped

### Restart Workers

Stop existing workers and start new ones:

```bash
# Restart all workers with default settings
poetry run gnosari worker restart

# Restart with new configuration
poetry run gnosari worker restart --concurrency 8 --loglevel debug
```

### Check Worker Status

View information about running workers:

```bash
# Check worker status
poetry run gnosari worker status
```

**Example output:**
```
Found 2 running Celery worker(s):
  PID: 12345, Status: running, CMD: celery -A gnosari.queue.app.celery_app worker
  PID: 12346, Status: running, CMD: celery -A gnosari.queue.app.celery_app worker
```

If no workers are running:
```
No Celery workers are currently running.
```

## Monitoring with Flower

Flower provides a web-based monitoring interface for Celery workers and tasks.

### Start Flower

```bash
# Start Flower with default settings
poetry run gnosari flower

# Start on custom port
poetry run gnosari flower --port 8080

# Start with custom authentication
poetry run gnosari flower --auth myuser:mypassword

# Start with custom broker URL
poetry run gnosari flower --broker redis://localhost:6379/1
```

#### Flower Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--port` | `-p` | `5555` | Port to run Flower web interface |
| `--auth` | | `admin:admin` | Basic auth (user:password) |
| `--broker` | | `redis://localhost:6379/0` | Redis broker URL |

### Access Flower Web UI

Once started, access the Flower interface at:
- **URL**: http://localhost:5555 (or your custom port)
- **Username**: admin (or your custom auth)
- **Password**: admin (or your custom auth)

### Flower Features

The Flower web interface provides:

- 📊 **Real-time monitoring**: Active workers, tasks, and queues
- 📈 **Task history**: Completed, failed, and retry statistics
- 🔍 **Task details**: Inspect task arguments, results, and stack traces
- 👥 **Worker management**: View worker status and statistics
- 📋 **Broker monitoring**: Queue lengths and message details

## Docker Services

If using Docker Compose, you can manage services directly:

### Start Redis

```bash
# Start Redis service
docker-compose up redis -d

# View Redis logs
docker-compose logs redis -f
```

### Start All Queue Services

```bash
# Start Redis and Flower together
docker-compose up redis flower -d

# View all service logs
docker-compose logs -f
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop specific service
docker-compose stop redis
```

## Complete Workflow Examples

### Development Setup

```bash
# 1. Start Redis
docker-compose up redis -d

# 2. Start workers in development mode
poetry run gnosari worker start --loglevel debug --concurrency 2

# 3. In another terminal, start Flower
poetry run gnosari flower

# 4. Run your team with async tools
poetry run gnosari --config examples/async_team.yaml --message "Process files"
```

### Production Setup

```bash
# 1. Start services with Docker Compose
docker-compose up redis flower -d

# 2. Start multiple workers for high throughput
poetry run gnosari worker start --concurrency 8 --queue high_priority &
poetry run gnosari worker start --concurrency 4 --queue low_priority &

# 3. Monitor via Flower at http://localhost:5555
```

### Maintenance

```bash
# Check system status
poetry run gnosari worker status
docker-compose ps

# Restart workers to apply configuration changes
poetry run gnosari worker restart --concurrency 4

# View worker logs
docker-compose logs flower -f

# Clean shutdown
poetry run gnosari worker stop
docker-compose down
```

## Environment Configuration

Configure worker behavior via environment variables in `.env`:

```bash
# Worker Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Flower Configuration
FLOWER_PORT=5555
FLOWER_BASIC_AUTH=admin:admin

# Optional: Default worker settings
CELERY_WORKER_CONCURRENCY=4
CELERY_WORKER_LOGLEVEL=info
```

## Troubleshooting Commands

### Check Redis Connection

```bash
# Test Redis connectivity
docker-compose exec redis redis-cli ping
# Should return: PONG
```

### Clear Queues

```bash
# Clear all queues (destructive!)
docker-compose exec redis redis-cli flushdb

# Clear specific queue
docker-compose exec redis redis-cli del gnosari_queue
```

### View Queue Contents

```bash
# Check queue length
docker-compose exec redis redis-cli llen gnosari_queue

# View queue contents (first 10 items)
docker-compose exec redis redis-cli lrange gnosari_queue 0 9
```

### Debug Worker Issues

```bash
# Start worker with maximum debugging
poetry run gnosari worker start --loglevel debug --concurrency 1

# Check worker process details
poetry run gnosari worker status

# Monitor real-time logs
docker-compose logs flower -f
```

## Performance Optimization

### Worker Scaling

```bash
# Scale workers based on load
poetry run gnosari worker start --concurrency 2   # Light load
poetry run gnosari worker start --concurrency 4   # Medium load
poetry run gnosari worker start --concurrency 8   # Heavy load
```

### Queue Separation

```bash
# Start workers for different priority queues
poetry run gnosari worker start --queue critical --concurrency 2
poetry run gnosari worker start --queue normal --concurrency 4
poetry run gnosari worker start --queue background --concurrency 1
```

### Resource Monitoring

```bash
# Monitor system resources
htop
docker stats

# Monitor Redis memory usage
docker-compose exec redis redis-cli info memory
```