# CLI Commands

Complete reference for all Gnosari CLI commands and operations.

## Execution Commands

### Team and Agent Execution
```bash
# Execute team with message
gnosari --config <config.yaml> --message <message>

# Execute single agent
gnosari --config <config.yaml> --message <message> --agent <name>

# Streaming execution
gnosari --config <config.yaml> --message <message> --stream

# Debug execution with raw JSON events
gnosari --config <config.yaml> --message <message> --debug

# Custom model and temperature
gnosari --config <config.yaml> --message <message> --model <model> --temperature <float>

# Session-based execution
gnosari --config <config.yaml> --message <message> --session-id <id>
```

### System Prompt Inspection
```bash
# View generated system prompts
gnosari --config <config.yaml> --show-prompts

# View prompts with custom settings
gnosari --config <config.yaml> --show-prompts --model <model> --temperature <float>
```

## API Registry Commands

### Configuration Push
```bash
# Push team configuration to API
gnosari push <config.yaml>

# Push with custom API URL
gnosari push <config.yaml> --api-url <url>
```
Requires `GNOSARI_API_KEY` environment variable.

### Configuration Pull
```bash
# Pull team configuration from API
gnosari pull <team_identifier>

# Pull to custom directory
gnosari pull <team_identifier> <output_directory>

# Pull with custom API URL
gnosari pull <team_identifier> --api-url <url>
```
Creates `<output_directory>/<team_identifier>/team.yaml` and `.env.example`.

## Template Management Commands

### Template Operations
```bash
# List all available templates
gnosari prompts list

# View template with rich formatting
gnosari prompts view <name>

# View template as markdown
gnosari prompts view <name> --format markdown

# View template variables only
gnosari prompts view <name> variables

# Process template with variables
gnosari prompts use <name> "message" --var1 "value" --var2 "value"

# Create file from template
gnosari prompts create <name> <filepath> "message" --var1 "value"
```

## Background Processing Commands

### Worker Management
```bash
# Start Celery worker
gnosari worker start

# Stop all workers
gnosari worker stop

# Restart workers
gnosari worker restart

# Check worker status
gnosari worker status

# Start with custom settings
gnosari worker start --concurrency <n> --queue <name> --loglevel <level>
```

### Process Monitoring
```bash
# Start Flower monitoring UI
gnosari flower

# Start with custom configuration
gnosari flower --port <port> --auth <user:pass> --broker <url>
```
Default: Port 5555, auth `admin:admin`.

## Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `--config`, `-c` | Team configuration YAML file | Required |
| `--message`, `-m` | Message to send to team | Required |
| `--agent`, `-a` | Execute specific agent only | All agents |
| `--session-id`, `-s` | Session ID for persistence | Auto-generated |
| `--api-key` | OpenAI API key override | `OPENAI_API_KEY` |
| `--model` | LLM model selection | `gpt-4o` |
| `--temperature` | Model temperature (0.0-2.0) | `1.0` |
| `--stream` | Enable streaming output | Disabled |
| `--debug` | Show debug information | Disabled |
| `--show-prompts` | Display system prompts | Disabled |

## Environment Configuration

### Required Variables
```bash
OPENAI_API_KEY=<key>                    # OpenAI API access
```

### Model Configuration
```bash
OPENAI_MODEL=gpt-4o                     # Default model
OPENAI_TEMPERATURE=1.0                  # Default temperature
```

### Multi-Provider Support
```bash
ANTHROPIC_API_KEY=<key>                 # Claude models
DEEPSEEK_API_KEY=<key>                  # DeepSeek models  
GOOGLE_API_KEY=<key>                    # Gemini models
```

### Registry Configuration
```bash
GNOSARI_API_KEY=<key>                   # Registry authentication
GNOSARI_API_URL=https://api.gnosari.com # Registry endpoint
```

### Session Storage
```bash
SESSION_PROVIDER=file                   # file|database|gnosari_api
SESSION_DATABASE_URL=<url>              # Database connection
GNOSARI_API_BASE_URL=<url>             # API session storage
```

### Background Processing
```bash
CELERY_BROKER_URL=redis://localhost:6379/0    # Message broker
CELERY_RESULT_BACKEND=redis://localhost:6379/0 # Result storage
```

### System Configuration
```bash
LOG_LEVEL=INFO                          # DEBUG|INFO|WARNING|ERROR
```

## Usage Examples

### Team Execution
```bash
# Basic execution
gnosari --config "team.yaml" --message "Hello world"

# Streaming with session
gnosari --config "team.yaml" --message "Analyze data" --stream --session-id "user-123"

# Single agent execution
gnosari --config "team.yaml" --message "Research topic" --agent "Researcher"
```

### Template Processing
```bash
# List and inspect templates
gnosari prompts list
gnosari prompts view planning variables

# Create document from template
gnosari prompts create planning "./docs/plan.md" "New feature" --feature_name "search"
```

### Registry Operations
```bash
# Push and pull configurations
gnosari push "./my-team.yaml"
gnosari pull "my-team" "./projects/"
```

### Background Processing
```bash
# Worker management
gnosari worker start --concurrency 4
gnosari flower --port 8080
gnosari worker status
```

## Exit Codes
- `0` - Success
- `1` - Error (configuration, API, runtime)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Missing API Key | Set environment variables or `.env` file |
| Configuration Error | Validate YAML syntax and required fields |
| Agent Not Found | Verify agent names in configuration |
| Template Not Found | Check `prompts/` directory exists |
| Registry Errors | Verify API key and network connectivity |
| Worker Errors | Check Redis connection and queue configuration |