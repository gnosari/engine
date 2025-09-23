# Introduction

The Gnosari Registry is a cloud-based service that allows you to share, discover, and manage team configurations. It provides a centralized repository where you can store your team configurations and access configurations created by others.

## Key Features

- **Team Sharing**: Upload your team configurations to share with others
- **Team Discovery**: Download and use team configurations from the community
- **Version Management**: Keep track of different versions of your team configurations
- **Access Control**: Secure access to your configurations with API keys

## Getting Started

To use the Gnosari Registry, you'll need:

1. A Gnosari API key (set as `GNOSARI_API_KEY` environment variable)
2. The Gnosari CLI installed
3. A team configuration YAML file

## Quick Commands

```bash
# Push a team configuration to the registry
gnosari push "examples/my-team.yaml"

# Pull a team configuration from the registry
gnosari pull "team-identifier"

# Use custom API URL
gnosari push "examples/my-team.yaml" --api-url "https://your-api.com"
```

## What's Next?

- [Push Commands](./push-commands.md) - Learn how to upload team configurations
- [Pull Commands](./pull-commands.md) - Learn how to download team configurations
- [Authentication](./authentication.md) - Set up API keys and authentication