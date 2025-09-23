# Push Commands

The `gnosari push` command allows you to upload team configurations to the Gnosari Registry. This is useful for sharing your team configurations with others or backing them up in the cloud.

## Basic Usage

```bash
gnosari push "path/to/team-config.yaml"
```

## Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `config_file` | Path to the team configuration YAML file | Required |
| `--api-url` | Custom Gnosari API URL | `https://api.gnosari.com` |

## Prerequisites

Before pushing a team configuration, ensure:

1. **API Key**: Set the `GNOSARI_API_KEY` environment variable
2. **Valid Configuration**: Your YAML file must have required fields:
   - `name`: Team name
   - `id`: Unique team identifier
3. **File Format**: The configuration must be valid YAML

## Examples

### Basic Push

```bash
# Push a team configuration
gnosari push "examples/customer-support-team.yaml"
```

### Custom API URL

```bash
# Push to a custom API endpoint
gnosari push "examples/my-team.yaml" --api-url "https://my-gnosari-instance.com"
```

### Using Environment Variables

```bash
# Set API key in environment
export GNOSARI_API_KEY="your-api-key-here"

# Set custom API URL
export GNOSARI_API_URL="https://my-gnosari-instance.com"

# Push configuration
gnosari push "examples/my-team.yaml"
```

## Required Configuration Fields

Your team configuration YAML file must include:

```yaml
name: "My Team Name"        # Required: Display name
id: "my-team-id"            # Required: Unique identifier
description: "Team description"  # Optional: Description
# ... rest of configuration
```

## Success Response

When successful, the push command will display:

```
✅ Team configuration pushed successfully!
Team ID: my-team-id
Message: Configuration uploaded successfully
```

## Error Handling

Common errors and solutions:

### Missing API Key
```
Warning: GNOSARI_API_KEY not found in environment variables
```
**Solution**: Set the `GNOSARI_API_KEY` environment variable

### Missing Required Fields
```
Error: 'name' field is required in the team configuration
Error: 'id' field is required in the team configuration
```
**Solution**: Add the required `name` and `id` fields to your YAML file

### File Not Found
```
Error: Configuration file 'path/to/file.yaml' not found
```
**Solution**: Check the file path and ensure the file exists

### API Connection Error
```
Error connecting to API: Connection refused
```
**Solution**: Check your internet connection and API URL

## Authentication

The push command uses HTTP authentication with your API key:

- **Header**: `X-Auth-Token: your-api-key`
- **Content-Type**: `application/json`
- **Accept**: `application/json`

## API Endpoint

The push command sends a POST request to:
```
https://api.gnosari.com/api/v1/teams/push
```

Or your custom API URL:
```
{your-api-url}/api/v1/teams/push
```

## Best Practices

1. **Use Descriptive IDs**: Choose meaningful team IDs that are easy to remember
2. **Include Descriptions**: Add descriptions to help others understand your team's purpose
3. **Version Control**: Consider using version numbers in your team IDs for updates
4. **Test First**: Validate your configuration locally before pushing
5. **Secure Keys**: Never commit API keys to version control