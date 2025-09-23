# Authentication

The Gnosari Registry uses API key authentication to secure access to team configurations. This guide covers how to set up and manage authentication for the registry.

## API Key Setup

### Environment Variable (Recommended)

Set your API key as an environment variable:

```bash
# Linux/macOS
export GNOSARI_API_KEY="your-api-key-here"

# Windows (Command Prompt)
set GNOSARI_API_KEY=your-api-key-here

# Windows (PowerShell)
$env:GNOSARI_API_KEY="your-api-key-here"
```

### .env File

Create a `.env` file in your project directory:

```bash
# .env file
GNOSARI_API_KEY=your-api-key-here
GNOSARI_API_URL=https://api.gnosari.com
```

The CLI automatically loads environment variables from `.env` files.

### Command Line (Not Recommended)

You can also pass the API key directly, but this is less secure:

```bash
# Not recommended - API key visible in command history
GNOSARI_API_KEY="your-key" gnosari push "team.yaml"
```

## API Key Types

### Personal API Keys

Personal API keys provide access to:
- Your own team configurations
- Public team configurations
- Teams shared with you

### Organization API Keys

Organization API keys provide access to:
- All team configurations within your organization
- Organization-wide team sharing
- Team management capabilities

## Authentication Headers

The Gnosari CLI automatically adds authentication headers to API requests:

```http
X-Auth-Token: your-api-key-here
Content-Type: application/json
Accept: application/json
```

## Custom API URLs

### Default API URL

By default, the CLI uses:
```
https://api.gnosari.com
```

### Custom API URL

Set a custom API URL for:
- Self-hosted Gnosari instances
- Development environments
- Corporate deployments

```bash
# Environment variable
export GNOSARI_API_URL="https://my-gnosari-instance.com"

# Command line option
gnosari push "team.yaml" --api-url "https://my-gnosari-instance.com"
```

## Security Best Practices

### 1. Never Commit API Keys

Add `.env` to your `.gitignore`:

```gitignore
# Environment variables
.env
.env.local
.env.*.local
```

### 2. Use Environment Variables

Prefer environment variables over hardcoded keys:

```bash
# ✅ Good
export GNOSARI_API_KEY="your-key"
gnosari push "team.yaml"

# ❌ Bad
gnosari push "team.yaml" --api-key "your-key"
```

### 3. Rotate Keys Regularly

- Generate new API keys periodically
- Revoke old keys when no longer needed
- Monitor key usage for suspicious activity

### 4. Use Least Privilege

- Use personal keys for individual projects
- Use organization keys only when necessary
- Limit key permissions to required operations

## Troubleshooting

### Missing API Key

```
Warning: GNOSARI_API_KEY not found in environment variables
```

**Solutions:**
1. Set the environment variable: `export GNOSARI_API_KEY="your-key"`
2. Create a `.env` file with your API key
3. Check for typos in the variable name

### Invalid API Key

```
Error: Unauthorized. Check your GNOSARI_API_KEY
```

**Solutions:**
1. Verify the API key is correct
2. Check if the key has expired
3. Ensure the key has the required permissions
4. Contact support if the key appears valid

### Network Issues

```
Error connecting to API: Connection refused
```

**Solutions:**
1. Check your internet connection
2. Verify the API URL is correct
3. Check if your firewall blocks the connection
4. Try using a different network

### SSL/TLS Issues

```
Error: SSL certificate verification failed
```

**Solutions:**
1. Update your system's certificate store
2. Check if your system clock is correct
3. Verify the API URL uses HTTPS
4. Contact support if using a custom certificate

## API Key Management

### Generating New Keys

1. Log into your Gnosari account
2. Navigate to API Keys section
3. Click "Generate New Key"
4. Copy the key immediately (it won't be shown again)
5. Set the key in your environment

### Revoking Keys

1. Log into your Gnosari account
2. Navigate to API Keys section
3. Find the key you want to revoke
4. Click "Revoke" or "Delete"
5. Update your environment to remove the old key

### Key Permissions

API keys can have different permission levels:

- **Read**: Can pull team configurations
- **Write**: Can push team configurations
- **Admin**: Can manage team configurations and permissions

## Environment Setup Examples

### Development Environment

```bash
# .env.development
GNOSARI_API_KEY=dev-key-here
GNOSARI_API_URL=https://dev-api.gnosari.com
LOG_LEVEL=debug
```

### Production Environment

```bash
# .env.production
GNOSARI_API_KEY=prod-key-here
GNOSARI_API_URL=https://api.gnosari.com
LOG_LEVEL=info
```

### CI/CD Pipeline

```yaml
# GitHub Actions example
env:
  GNOSARI_API_KEY: ${{ secrets.GNOSARI_API_KEY }}
  GNOSARI_API_URL: https://api.gnosari.com
```

## Multiple Environments

You can manage multiple environments by using different `.env` files:

```bash
# Load development environment
cp .env.development .env
gnosari push "team.yaml"

# Load production environment
cp .env.production .env
gnosari push "team.yaml"
```

Or use environment-specific commands:

```bash
# Development
GNOSARI_API_URL="https://dev-api.gnosari.com" gnosari push "team.yaml"

# Production
GNOSARI_API_URL="https://api.gnosari.com" gnosari push "team.yaml"
```