# Sessions

Sessions enable persistent conversation memory in Gnosari, allowing agents to maintain context across multiple interactions. This is essential for building conversational AI systems that can remember previous exchanges and provide continuity in user experiences.

## Overview

Gnosari sessions use a custom `GnosariContextSession` implementation that extends the OpenAI Agents SDK session functionality. This custom implementation supports multiple storage backends, from simple SQLite files for development to production-grade PostgreSQL databases, as well as API-based distributed storage. Sessions automatically store conversation history and make it available to agents across interactions.

## Configuration

Sessions are configured using environment variables, providing flexibility for different deployment scenarios.

### Environment Variables

- **`SESSION_PROVIDER`**: Session storage provider (default: `file`)
  - `file`: SQLite file-based storage
  - `database`: External database storage  
  - `gnosari_api`: API-based distributed storage
- **`SESSION_DATABASE_URL`**: Database connection URL
- **`GNOSARI_API_BASE_URL`**: Base URL for API provider (required for `gnosari_api`)
- **`GNOSARI_API_KEY`**: Authentication key for API provider (required for `gnosari_api`)

## Session Providers

Gnosari automatically uses the custom `GnosariContextSession` for all session management. This session provider intelligently handles different storage backends based on your configuration.

### File Provider (Default)

The file provider uses SQLite for local session storage, making it perfect for development and single-instance deployments.

```bash
# Default configuration (uses conversations.db in current directory)
export SESSION_PROVIDER=file

# Custom SQLite file location
export SESSION_PROVIDER=file
export SESSION_DATABASE_URL=sqlite+aiosqlite:///my_conversations.db
```

**Supported SQLite URL formats:**
- `sqlite+aiosqlite:///conversations.db` - Relative path
- `sqlite+aiosqlite:////absolute/path/to/conversations.db` - Absolute path
- `sqlite+aiosqlite:///:memory:` - In-memory database (not persistent)

**Key characteristics:**
- ✅ Automatic table creation
- ✅ Zero configuration required
- ✅ Perfect for development
- ✅ Suitable for single-instance deployments
- ❌ Limited scalability for multi-instance deployments

### Database Provider

The database provider connects to external databases, making it suitable for production deployments with multiple instances.

```bash
export SESSION_PROVIDER=database
export SESSION_DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/gnosari_sessions
```

**Key characteristics:**
- ✅ Production-ready scaling
- ✅ Multi-instance support
- ✅ Full ACID compliance
- ✅ Advanced database features
- ❌ Requires manual table setup
- ❌ More complex configuration

### API Provider

The API provider stores sessions via the Gnosari API backend, making it perfect for distributed deployments where multiple engine instances need to share session storage.

```bash
export SESSION_PROVIDER=gnosari_api
export GNOSARI_API_BASE_URL=http://localhost:8001
export GNOSARI_API_KEY=your-api-key-here
```

**Key characteristics:**
- ✅ Distributed storage across multiple instances
- ✅ Context-aware (stores account_id, team_id, agent_id)
- ✅ REST API integration
- ✅ Secure authentication with API keys
- ✅ Automatic session creation
- ✅ Fallback to local storage if API unavailable
- ❌ Requires running Gnosari API backend
- ❌ Network dependency for session operations

## Supported Databases

| Database | URL Format | Async Driver | Notes |
|----------|------------|--------------|-------|
| **PostgreSQL** | `postgresql+asyncpg://user:pass@host:port/db` | asyncpg | Recommended for production |
| **MySQL** | `mysql+aiomysql://user:pass@host:port/db` | aiomysql | Good alternative for production |
| **SQLite** | `sqlite+aiosqlite:///path/to/file.db` | aiosqlite | Development and single-instance |

## Database Setup

When using the database provider, you must create the required tables before running Gnosari.

### Automatic Setup (Python API)

If you're using the Gnosari Python API, you can use Alembic migrations:

```bash
# Apply migrations to create session tables
alembic upgrade head
```

### Manual Setup (SQL)

For standalone deployments, create the tables manually:

```sql
-- PostgreSQL/MySQL (matches python-api models)
CREATE TABLE sessions (
    session_id VARCHAR(255) PRIMARY KEY,
    account_id INTEGER NULL,  -- Nullable to support engine-only usage
    team_id INTEGER NULL,
    agent_id INTEGER NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (account_id) REFERENCES account(id),
    FOREIGN KEY (team_id) REFERENCES teams(id),
    FOREIGN KEY (agent_id) REFERENCES agent(id)
);

CREATE TABLE session_messages (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    message_data TEXT NOT NULL,
    account_id INTEGER NULL,  -- Nullable to support engine-only usage
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES account(id)
);

CREATE INDEX idx_session_messages_session_time ON session_messages(session_id, created_at);
```

```sql
-- SQLite (handled automatically by file provider)
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    account_id INTEGER NULL,  -- Nullable to support engine-only usage
    team_id INTEGER NULL,
    agent_id INTEGER NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (account_id) REFERENCES account(id),
    FOREIGN KEY (team_id) REFERENCES teams(id),
    FOREIGN KEY (agent_id) REFERENCES agent(id)
);

CREATE TABLE session_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    message_data TEXT NOT NULL,
    account_id INTEGER NULL,  -- Nullable to support engine-only usage
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES account(id)
);

CREATE INDEX idx_session_messages_session_time ON session_messages(session_id, created_at);
```

## Usage

### Basic Usage

Use sessions by providing a `--session-id` parameter when running teams:

```bash
# Start a new conversation
gnosari --config "team.yaml" --message "Hello, my name is Alice" --session-id "user-123"

# Continue the conversation (agent remembers Alice)
gnosari --config "team.yaml" --message "What's my name?" --session-id "user-123"

# Different session (fresh context)
gnosari --config "team.yaml" --message "What's my name?" --session-id "user-456"
```

### Session Management

Sessions are managed automatically, but you can work with them programmatically:

```python
from gnosari.engine.team_runner import TeamRunner
from gnosari.engine.team_builder import TeamBuilder

# Load team configuration
team = TeamBuilder.from_yaml("team.yaml")
runner = TeamRunner(team)

# Run with session
result = await runner.run_team_async(
    message="Hello, I'm working on a project",
    session_id="project-session-1"
)

# Continue conversation
result = await runner.run_team_async(
    message="Can you help me with the next steps?",
    session_id="project-session-1"  # Same session
)
```

### Session IDs

Session IDs should be:
- **Unique per user/conversation**
- **Persistent across interactions**
- **Meaningful for your application**

Common patterns:
- `user-{user_id}` - One session per user
- `user-{user_id}-{conversation_id}` - Multiple conversations per user
- `project-{project_id}` - Project-based sessions
- `{uuid4()}` - Random unique sessions

## Best Practices

### Development

```bash
# Simple setup for development
export SESSION_PROVIDER=file
export SESSION_DATABASE_URL=sqlite+aiosqlite:///dev_conversations.db
```

### Production

```bash
# Scalable setup for production
export SESSION_PROVIDER=database
export SESSION_DATABASE_URL=postgresql+asyncpg://gnosari_user:secure_password@db.example.com:5432/gnosari_sessions
```

### Distributed (API-Based)

```bash
# Distributed setup with API backend
export SESSION_PROVIDER=gnosari_api
export GNOSARI_API_BASE_URL=https://api.yourcompany.com
export GNOSARI_API_KEY=sk-your-secure-api-key
```

### Security Considerations

1. **Database Credentials**: Store database URLs securely using secret management
2. **Session IDs**: Avoid exposing sensitive information in session IDs
3. **Data Retention**: Implement policies for cleaning up old sessions
4. **Access Control**: Ensure proper database access controls

### Performance Tips

1. **Connection Pooling**: Use connection pooling for database providers
2. **Indexing**: The default index on `(session_id, created_at)` optimizes message retrieval
3. **Cleanup**: Regularly clean up old sessions to maintain performance
4. **Monitoring**: Monitor database performance and connection usage

## Troubleshooting

### Common Issues

**Session not persisting:**
- Verify `SESSION_PROVIDER` is set correctly
- Check `SESSION_DATABASE_URL` format
- Ensure database is accessible

**Database connection errors:**
- Verify database credentials
- Check network connectivity
- Ensure database server is running

**Table not found errors:**
- Run database migrations or create tables manually
- Verify table names match schema
- Check database permissions

### Debug Mode

Enable debug logging to troubleshoot session issues:

```bash
export LOG_LEVEL=DEBUG
gnosari --config "team.yaml" --message "Test message" --session-id "debug-session" --debug
```

## Examples

### Multi-User Application

```bash
# User 1 conversation
gnosari --config "support.yaml" --message "I need help with billing" --session-id "user-1001"

# User 2 conversation (separate context)
gnosari --config "support.yaml" --message "I need help with billing" --session-id "user-1002"

# User 1 continues (remembers previous context)
gnosari --config "support.yaml" --message "Can you check my account balance?" --session-id "user-1001"
```

### Project-Based Sessions

```bash
# Project Alpha discussion
gnosari --config "project-team.yaml" --message "Let's plan the architecture" --session-id "project-alpha"

# Project Beta discussion (different context)
gnosari --config "project-team.yaml" --message "Let's plan the architecture" --session-id "project-beta"

# Continue Project Alpha
gnosari --config "project-team.yaml" --message "What were our main components?" --session-id "project-alpha"
```

### API-Based Sessions

```bash
# Configure API session provider
export SESSION_PROVIDER=gnosari_api
export GNOSARI_API_BASE_URL=http://localhost:8001
export GNOSARI_API_KEY=your-api-key

# Multiple engine instances can now share sessions
# Instance 1
gnosari --config "team.yaml" --message "Start working on feature X" --session-id "feature-x"

# Instance 2 (different server, same session)
gnosari --config "team.yaml" --message "What's the status?" --session-id "feature-x"
```

## Implementation Details

### Custom Session Provider

Gnosari uses a custom `GnosariContextSession` implementation instead of the default OpenAI Agents SDK `SQLAlchemySession`. This custom implementation provides:

- **Enhanced Context Storage**: Automatically stores account_id, team_id, and agent_id when available
- **Multi-Backend Support**: Seamlessly handles file, database, and API storage providers
- **API Integration**: Built-in support for distributed storage via Gnosari API backend
- **Intelligent Fallback**: Automatically falls back to SQLAlchemy when API provider is unavailable
- **Security**: Path validation and proper database connection handling

### Migration from SQLAlchemy

If you were previously using the default OpenAI Agents SDK session storage, your existing session data remains compatible. The `GnosariContextSession` uses the same underlying table structure for file and database providers, ensuring seamless migration.

Sessions provide the foundation for building sophisticated conversational AI systems with Gnosari, enabling agents to maintain context and provide personalized, continuous experiences across interactions.