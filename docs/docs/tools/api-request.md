---
sidebar_position: 3
---

# API Request Tool

The **api_request** tool enables agents to make HTTP requests to external APIs and services. This tool provides a flexible way to integrate with REST APIs, webhooks, and other HTTP-based services.

## Overview

The API request tool allows agents to:
- Make HTTP requests (GET, POST, PUT, DELETE, PATCH, etc.)
- Send JSON payloads and custom headers
- Handle authentication and SSL verification
- Configure timeouts and connection settings
- Process JSON and text responses

## Capabilities

- ✅ **HTTP Methods**: Support for all standard HTTP methods
- ✅ **Authentication**: Bearer tokens, API keys, custom headers
- ✅ **JSON Payloads**: Send structured data in request bodies
- ✅ **Custom Headers**: Configure request headers per call
- ✅ **SSL Verification**: Configurable SSL certificate validation
- ✅ **Timeout Handling**: Configurable request timeouts
- ✅ **Error Handling**: Comprehensive error reporting
- ✅ **Response Processing**: Automatic JSON parsing with text fallback

## YAML Configuration

### Basic Configuration

```yaml
tools:
  - name: api_request
    module: gnosari.tools.builtin.api_request
    class: APIRequestTool
    args:
      base_url: https://api.example.com
      timeout: 30
      verify_ssl: true
```

:::tip SSL Verification
Always enable `verify_ssl: true` in production environments to ensure secure connections.
:::

### Advanced Configuration

```yaml
tools:
  - name: external_api
    module: gnosari.tools.builtin.api_request
    class: APIRequestTool
    args:
      base_url: https://api.external-service.com
      base_headers:
        Authorization: Bearer your-api-token
        User-Agent: GnosariAgent/1.0
        Accept: application/json
        Content-Type: application/json
      timeout: 60
      verify_ssl: true
```

### Multiple API Configurations

```yaml
tools:
  - name: github_api
    module: gnosari.tools.builtin.api_request
    class: APIRequestTool
    args:
      base_url: https://api.github.com
      base_headers:
        Authorization: token your-github-token
        Accept: application/vnd.github.v3+json
      timeout: 30
      verify_ssl: true

  - name: slack_api
    module: gnosari.tools.builtin.api_request
    class: APIRequestTool
    args:
      base_url: https://slack.com/api
      base_headers:
        Authorization: Bearer xoxb-your-slack-token
        Content-Type: application/json
      timeout: 15
      verify_ssl: true
```

## Agent Assignment

Assign the API request tool to agents that need to interact with external services:

```yaml
agents:
  - name: API Integrator
    instructions: >
      You are responsible for integrating with external APIs. Use the api_request tool to:
      
      1. **Make API Calls**: Use appropriate HTTP methods for different operations
      2. **Handle Authentication**: Include proper headers and tokens
      3. **Process Responses**: Parse JSON responses and handle errors
      4. **Retry Logic**: Implement appropriate retry strategies for failed requests
      
      Always check response status codes and handle errors gracefully.
    model: gpt-4o
    tools:
      - api_request
```

## Usage Examples

### Example 1: GitHub API Integration

```yaml
name: GitHub Integration Team

tools:
  - name: github_api
    module: gnosari.tools.builtin.api_request
    class: APIRequestTool
    args:
      base_url: https://api.github.com
      base_headers:
        Authorization: token your-github-token
        Accept: application/vnd.github.v3+json
      timeout: 30
      verify_ssl: true

agents:
  - name: GitHub Manager
    instructions: >
      Manage GitHub repositories and issues. Use the github_api tool to:
      - Get repository information: GET /repos/{owner}/{repo}
      - Create issues: POST /repos/{owner}/{repo}/issues
      - List pull requests: GET /repos/{owner}/{repo}/pulls
      - Get user information: GET /users/{username}
    model: gpt-4o
    tools:
      - github_api
```

### Example 2: Slack Integration

```yaml
name: Slack Notification Team

tools:
  - name: slack_api
    module: gnosari.tools.builtin.api_request
    class: APIRequestTool
    args:
      base_url: https://slack.com/api
      base_headers:
        Authorization: Bearer xoxb-your-slack-token
        Content-Type: application/json
      timeout: 15
      verify_ssl: true

agents:
  - name: Slack Notifier
    instructions: >
      Send notifications to Slack channels. Use the slack_api tool to:
      - Send messages: POST /chat.postMessage
      - Upload files: POST /files.upload
      - Get channel info: GET /conversations.info
    model: gpt-4o
    tools:
      - slack_api
```

### Example 3: Custom API Integration

```yaml
name: Custom API Team

tools:
  - name: custom_api
    module: gnosari.tools.builtin.api_request
    class: APIRequestTool
    args:
      base_url: https://api.custom-service.com
      base_headers:
        X-API-Key: your-api-key
        Accept: application/json
        Content-Type: application/json
      timeout: 45
      verify_ssl: true

agents:
  - name: Data Processor
    instructions: >
      Process data through custom API endpoints. Use the custom_api tool to:
      - Retrieve data: GET /data/{id}
      - Create records: POST /data
      - Update records: PUT /data/{id}
      - Delete records: DELETE /data/{id}
    model: gpt-4o
    tools:
      - custom_api
```

## Tool Parameters

The API request tool accepts the following configuration parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_url` | string | "https://api.example.com" | Base URL for all API requests |
| `base_headers` | dict | `{}` | Default headers for all requests |
| `timeout` | int | 30 | Request timeout in seconds |
| `verify_ssl` | bool | true | Whether to verify SSL certificates |

:::info Tool Identity
Use the YAML `name` and `description` fields to customize how the tool appears in the UI and agent prompts. The `name` becomes the tool's display name, while `description` explains its purpose to agents.
:::

## Per-Call Parameters

When agents use the tool, they can override configuration parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `endpoint` | string | API endpoint path (e.g., "/users", "/posts/123") |
| `method` | string | HTTP method (GET, POST, PUT, DELETE, PATCH, etc.) |
| `body_params` | string | JSON body parameters for POST/PUT/PATCH requests |
| `headers` | string | Custom headers as JSON string |
| `base_url` | string | Override configured base URL |
| `timeout` | int | Override configured timeout |
| `verify_ssl` | bool | Override SSL verification setting |

## Agent Instructions

Provide clear instructions for API usage:

```yaml
agents:
  - name: API Specialist
    instructions: >
      You are an API integration specialist. When using the api_request tool:
      
      **Request Format:**
      - Use appropriate HTTP methods (GET for retrieval, POST for creation, etc.)
      - Include proper endpoint paths (e.g., "/users/123" not "users/123")
      - Send JSON payloads for POST/PUT requests
      - Include authentication headers when required
      
      **Error Handling:**
      - Check response status codes
      - Handle 4xx and 5xx errors appropriately
      - Provide meaningful error messages to users
      
      **Response Processing:**
      - Parse JSON responses when possible
      - Handle both success and error responses
      - Extract relevant information from responses
    model: gpt-4o
    tools:
      - api_request
```

## Security Best Practices

### 1. **Environment Variables**
Store sensitive credentials in environment variables:

```yaml
tools:
  - name: secure_api
    module: gnosari.tools.builtin.api_request
    class: APIRequestTool
    args:
      base_url: https://api.secure-service.com
      base_headers:
        Authorization: Bearer ${API_TOKEN}
        X-API-Key: ${API_KEY}
```

:::warning Security Best Practice
Never hardcode API keys or tokens in your YAML files. Use environment variables or secure credential management systems.
:::

### 2. **SSL Verification**
Always enable SSL verification in production:

```yaml
args:
  verify_ssl: true  # Never disable in production
```

### 3. **Timeout Configuration**
Set appropriate timeouts for different services:

```yaml
args:
  timeout: 30  # 30 seconds for most APIs
  # timeout: 60  # Longer for complex operations
```

## Error Handling

The API request tool provides comprehensive error handling:

- **HTTP Errors**: Detailed error messages for 4xx and 5xx responses
- **Network Errors**: Timeout and connection error handling
- **JSON Parsing**: Graceful handling of malformed JSON responses
- **SSL Errors**: Clear SSL certificate validation errors

## Troubleshooting

### Common Issues

1. **Authentication Errors (401/403)**
   - Check API tokens and keys
   - Verify header format and values
   - Ensure tokens haven't expired

2. **Timeout Errors**
   - Increase timeout value for slow APIs
   - Check network connectivity
   - Verify API endpoint availability

3. **SSL Certificate Errors**
   - Verify SSL certificates are valid
   - Check if `verify_ssl` should be disabled for development
   - Ensure proper certificate chain

4. **JSON Parsing Errors**
   - Check if API returns valid JSON
   - Handle non-JSON responses appropriately
   - Verify Content-Type headers

### Debug Mode

Use debug mode to see detailed API request logs:

```bash
gnosari --config "team.yaml" --message "Your message" --debug
```

:::tip API Debugging
Debug mode shows detailed HTTP request/response information including headers, body content, and status codes.
:::

## Related Tools

- [Delegate Agent Tool](delegate-agent) - For multi-agent coordination
- [MySQL Query Tool](mysql-query) - For database operations
- [Website Content Tool](website-content) - For web content retrieval

The API request tool is essential for integrating your AI agents with external services and APIs. Use it to create powerful integrations that extend your agents' capabilities beyond the local environment.