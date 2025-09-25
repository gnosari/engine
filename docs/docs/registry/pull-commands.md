# Pull Commands

The `gnosari pull` command allows you to download team configurations from the Gnosari Registry. This is useful for accessing shared team configurations or restoring configurations from the cloud.

## Basic Usage

```bash
# Pull to default teams directory
gnosari pull "team-identifier"

# Pull to custom directory
gnosari pull "team-identifier" ./my-project
```

## Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `team_identifier` | Unique identifier of the team to pull | Required |
| `output_directory` | Directory where team will be created | `./teams` |
| `--api-url` | Custom Gnosari API URL | `https://api.gnosari.com` |

## Prerequisites

Before pulling a team configuration, ensure:

1. **API Key**: Set the `GNOSARI_API_KEY` environment variable (optional for public teams)
2. **Team Identifier**: Know the exact team ID you want to pull
3. **Access Rights**: Have permission to access the team configuration

## Examples

### Basic Pull

```bash
# Pull to default teams directory
gnosari pull "customer-support-team"
# Creates: ./teams/customer-support-team/team.yaml
#          ./teams/customer-support-team/.env.example
```

### Custom Directory

```bash
# Pull to custom directory
gnosari pull "customer-support-team" ./my-projects
# Creates: ./my-projects/customer-support-team/team.yaml
#          ./my-projects/customer-support-team/.env.example
```

### Custom API URL

```bash
# Pull from a custom API endpoint
gnosari pull "my-team-id" --api-url "https://my-gnosari-instance.com"
```

### Using Environment Variables

```bash
# Set API key in environment
export GNOSARI_API_KEY="your-api-key-here"

# Set custom API URL
export GNOSARI_API_URL="https://my-gnosari-instance.com"

# Pull configuration
gnosari pull "team-identifier"
```

## Output

The pull command creates a structured project directory with team configuration and environment template:

```
✅ Team configuration pulled successfully!
Team name: Customer Support Team
Team ID: customer-support-team
Team directory: /absolute/path/to/teams/customer-support-team
Team config: team.yaml
Environment template: .env.example
Environment variables detected: OPENAI_API_KEY, DATABASE_URL
```

## Directory Structure

The pull command creates a structured directory for each team:

```
teams/                          # Default output directory
└── customer-support-team/      # Team identifier directory
    ├── team.yaml              # Team configuration
    └── .env.example           # Environment variables template
```

With custom directory:
```
my-projects/                    # Custom output directory
└── customer-support-team/      # Team identifier directory
    ├── team.yaml              # Team configuration
    └── .env.example           # Environment variables template
```

## Environment Variables

The pull command automatically detects environment variables in your team configuration and creates a `.env.example` file:

### Detection

Environment variables are detected using the `${VAR_NAME}` or `${VAR_NAME:default}` syntax:

```yaml
# In team.yaml
agents:
  - name: "Assistant"
    model: "${OPENAI_MODEL:gpt-4o}"
    tools:
      - name: "database"
        args:
          connection_url: "${DATABASE_URL}"
```

### Generated .env.example

The command creates a `.env.example` file with all detected variables:

```bash
# Environment variables for this team configuration
# Copy this file to .env and fill in the values

DATABASE_URL=
OPENAI_MODEL=
```

### Setup Process

1. Copy `.env.example` to `.env`
2. Fill in your actual values
3. Run the team configuration

## Error Handling

Common errors and solutions:

### Team Not Found
```
Error: Team 'team-identifier' not found
```
**Solution**: Verify the team identifier is correct and the team exists

### Unauthorized Access
```
Error: Unauthorized. Check your GNOSARI_API_KEY
```
**Solution**: Set a valid API key or check if the team requires authentication

### Forbidden Access
```
Error: Forbidden. You don't have access to this team
```
**Solution**: Contact the team owner for access permissions

### Missing API Key
```
Warning: GNOSARI_API_KEY not found in environment variables
```
**Solution**: Set the `GNOSARI_API_KEY` environment variable if required

### API Connection Error
```
Error connecting to API: Connection refused
```
**Solution**: Check your internet connection and API URL

## Authentication

The pull command uses HTTP authentication with your API key:

- **Header**: `X-Auth-Token: your-api-key`
- **Accept**: `application/json`

## API Endpoint

The pull command sends a GET request to:
```
https://api.gnosari.com/api/v1/teams/{team-identifier}/pull
```

Or your custom API URL:
```
{your-api-url}/api/v1/teams/{team-identifier}/pull
```

## Data Transformation

The pull command automatically transforms the API response into a complete project structure:

### Team Configuration (team.yaml)
- **Team Information**: name, id, description
- **Configuration**: team settings and parameters
- **Knowledge Bases**: knowledge base configurations
- **Tools**: tool definitions and configurations
- **Agents**: agent definitions with all properties

### Environment Template (.env.example)
- **Variable Detection**: Scans YAML for `${VAR_NAME}` patterns
- **Template Generation**: Creates ready-to-use environment file
- **Setup Instructions**: Includes helpful comments

## Best Practices

1. **Verify Team ID**: Double-check the team identifier before pulling
2. **Choose Directory**: Use meaningful directory names for organization
3. **Environment Setup**: Always copy `.env.example` to `.env` and configure
4. **Check Permissions**: Ensure you have access to the team configuration
5. **Review Configuration**: Examine both `team.yaml` and `.env.example` before using
6. **Version Control**: Track the entire team directory in your repository
7. **Security**: Never commit `.env` files with actual secrets

## Use Cases

- **Team Sharing**: Download complete team projects shared by colleagues
- **Quick Setup**: Get started with pre-configured teams including environment templates
- **Template Usage**: Use community templates as starting points for new projects
- **Configuration Backup**: Restore team configurations with proper project structure
- **Development Workflow**: Organize multiple teams in structured directories
- **Environment Management**: Easily manage different environments with separate .env files