# Pull Commands

The `gnosari pull` command allows you to download team configurations from the Gnosari Registry. This is useful for accessing shared team configurations or restoring configurations from the cloud.

## Basic Usage

```bash
gnosari pull "team-identifier"
```

## Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `team_identifier` | Unique identifier of the team to pull | Required |
| `--api-url` | Custom Gnosari API URL | `https://api.gnosari.com` |

## Prerequisites

Before pulling a team configuration, ensure:

1. **API Key**: Set the `GNOSARI_API_KEY` environment variable (optional for public teams)
2. **Team Identifier**: Know the exact team ID you want to pull
3. **Access Rights**: Have permission to access the team configuration

## Examples

### Basic Pull

```bash
# Pull a team configuration
gnosari pull "customer-support-team"
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

The pull command downloads the team configuration and saves it as a YAML file in your current directory:

```
✅ Team configuration pulled successfully!
Team name: Customer Support Team
Team ID: customer-support-team
Saved to: /path/to/current/directory/customer-support-team.yaml
```

## File Naming

The downloaded file is automatically named based on the team identifier:
- Team ID: `customer-support-team` → File: `customer-support-team.yaml`
- Team ID: `my-team` → File: `my-team.yaml`

## Success Response

When successful, the pull command will display:

```
✅ Team configuration pulled successfully!
Team name: Customer Support Team
Team ID: customer-support-team
Saved to: /absolute/path/to/customer-support-team.yaml
```

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

The pull command automatically transforms the JSON response from the API into a properly formatted YAML file, including:

- **Team Information**: name, id, description
- **Configuration**: team settings and parameters
- **Knowledge Bases**: knowledge base configurations
- **Tools**: tool definitions and configurations
- **Agents**: agent definitions with all properties

## Best Practices

1. **Verify Team ID**: Double-check the team identifier before pulling
2. **Check Permissions**: Ensure you have access to the team configuration
3. **Review Configuration**: Examine the downloaded configuration before using
4. **Backup Local Changes**: Save any local modifications before pulling updates
5. **Use Version Control**: Track changes to pulled configurations in your repository

## Use Cases

- **Team Sharing**: Download configurations shared by colleagues
- **Configuration Backup**: Restore team configurations from the cloud
- **Template Usage**: Use community templates as starting points
- **Version Updates**: Pull updated versions of team configurations
- **Cross-Environment**: Use the same configuration across different environments