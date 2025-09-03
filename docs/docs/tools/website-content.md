---
sidebar_position: 6
---

# Website Content Tool

The **website_content** tool enables agents to fetch content from websites by querying an API. This tool provides a simple way to retrieve web content for analysis, processing, or integration into agent workflows.

## Overview

The website content tool allows agents to:
- Fetch content from websites via API calls
- Retrieve text content from web pages
- Process web content for analysis or integration
- Handle various content types and encodings
- Manage API timeouts and error handling

## Capabilities

- ✅ **Web Content Retrieval**: Fetch content from websites via API
- ✅ **Text Processing**: Decode and process web content
- ✅ **Timeout Handling**: Configurable request timeouts
- ✅ **Error Handling**: Comprehensive error reporting
- ✅ **Content Validation**: Handle various content types
- ✅ **API Integration**: Simple API-based content fetching
- ✅ **Logging**: Detailed logging of content retrieval activities

## YAML Configuration

### Basic Configuration

```yaml
tools:
  - name: website_content
    module: gnosari.tools.website_content
    class: WebsiteContentTool
    args:
      base_url: https://r.ai.neomanex.com
      timeout: 30
```

:::info Default API
The tool defaults to using `https://r.ai.neomanex.com` as the base URL for content retrieval.
:::

### Advanced Configuration

```yaml
tools:
  - name: content_fetcher
    module: gnosari.tools.website_content
    class: WebsiteContentTool
    args:
      base_url: https://api.content-service.com
      timeout: 60
      tool_name: "content_fetcher"
      tool_description: "Fetch website content for analysis and processing"
```

### Multiple Content Sources

```yaml
tools:
  - name: news_fetcher
    module: gnosari.tools.website_content
    class: WebsiteContentTool
    args:
      base_url: https://news-api.example.com
      timeout: 30

  - name: blog_fetcher
    module: gnosari.tools.website_content
    class: WebsiteContentTool
    args:
      base_url: https://blog-api.example.com
      timeout: 45
```

## Agent Assignment

Assign the website content tool to agents that need to retrieve web content:

```yaml
agents:
  - name: Content Analyst
    instructions: >
      You are a content analyst who retrieves and analyzes web content. Use the website_content tool to:
      
      1. **Fetch Content**: Retrieve content from websites via API
      2. **Process Information**: Analyze and extract relevant information
      3. **Handle Errors**: Manage API failures and timeouts gracefully
      4. **Provide Insights**: Offer analysis and insights based on retrieved content
      
      Always handle content retrieval errors appropriately and provide meaningful responses.
    model: gpt-4o
    tools:
      - website_content
```

## Usage Examples

### Example 1: News Monitoring Team

```yaml
name: News Monitoring Team

tools:
  - name: news_fetcher
    module: gnosari.tools.website_content
    class: WebsiteContentTool
    args:
      base_url: https://news-api.example.com
      timeout: 30

agents:
  - name: News Monitor
    instructions: >
      Monitor news sources and provide updates. Use the news_fetcher tool to:
      - Get latest news: /latest-news
      - Fetch specific articles: /articles/{id}
      - Retrieve news by category: /news/category/{category}
    model: gpt-4o
    tools:
      - news_fetcher

  - name: News Analyst
    instructions: "Analyze news content and provide insights"
    model: gpt-4o
    tools:
      - news_fetcher
```

### Example 2: Content Research Team

```yaml
name: Content Research Team

tools:
  - name: research_fetcher
    module: gnosari.tools.website_content
    class: WebsiteContentTool
    args:
      base_url: https://research-api.example.com
      timeout: 60

agents:
  - name: Research Assistant
    instructions: >
      Research topics and gather information from various sources. Use the research_fetcher tool to:
      - Get research papers: /papers/{topic}
      - Fetch documentation: /docs/{section}
      - Retrieve case studies: /cases/{industry}
    model: gpt-4o
    tools:
      - research_fetcher

  - name: Content Summarizer
    instructions: >
      Summarize and analyze research content. Use the research_fetcher tool to:
      - Get detailed content for analysis
      - Provide comprehensive summaries
      - Extract key insights and findings
    model: gpt-4o
    tools:
      - research_fetcher
```

### Example 3: Documentation Team

```yaml
name: Documentation Team

tools:
  - name: docs_fetcher
    module: gnosari.tools.website_content
    class: WebsiteContentTool
    args:
      base_url: https://docs-api.example.com
      timeout: 45

agents:
  - name: Documentation Assistant
    instructions: >
      Help users find and understand documentation. Use the docs_fetcher tool to:
      - Get API documentation: /api/{endpoint}
      - Fetch user guides: /guides/{topic}
      - Retrieve troubleshooting info: /troubleshooting/{issue}
    model: gpt-4o
    tools:
      - docs_fetcher

  - name: Technical Writer
    instructions: >
      Create and update technical documentation. Use the docs_fetcher tool to:
      - Retrieve existing documentation for updates
      - Get reference materials for writing
      - Access examples and code snippets
    model: gpt-4o
    tools:
      - docs_fetcher
```

## Tool Parameters

The website content tool accepts the following configuration parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_url` | string | "https://r.ai.neomanex.com" | Base URL for the content API |
| `timeout` | int | 30 | Request timeout in seconds |
| `tool_name` | string | "website_content" | Custom name for the tool |
| `tool_description` | string | "Fetch the content of a given URL by querying an API" | Custom description |

## Per-Call Parameters

When agents use the tool, they specify the URL to fetch:

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | string | The URL to fetch content from (appended to base_url) |

## Agent Instructions

Provide clear instructions for content retrieval:

```yaml
agents:
  - name: Content Specialist
    instructions: >
      You are a content specialist who retrieves and processes web content. When using the website_content tool:
      
      **Content Retrieval:**
      - Specify the URL path to fetch content from
      - Handle different content types appropriately
      - Process and analyze retrieved content
      
      **Error Handling:**
      - Handle API failures gracefully
      - Provide meaningful error messages
      - Suggest alternative approaches when content isn't available
      
      **Content Processing:**
      - Extract relevant information from content
      - Provide summaries and insights
      - Format content appropriately for users
    model: gpt-4o
    tools:
      - website_content
```

## Best Practices

### 1. **URL Management**
Use descriptive and organized URL patterns:

```yaml
instructions: >
  When fetching content, use clear URL patterns:
  - /articles/{id} for specific articles
  - /category/{name} for category content
  - /search?q={query} for search results
```

### 2. **Timeout Configuration**
Set appropriate timeouts for different content types:

```yaml
tools:
  - name: fast_content
    module: gnosari.tools.website_content
    class: WebsiteContentTool
    args:
      timeout: 15  # For simple content
      
  - name: complex_content
    module: gnosari.tools.website_content
    class: WebsiteContentTool
    args:
      timeout: 60  # For complex or large content
```

:::tip Timeout Best Practices
Set shorter timeouts for simple content and longer timeouts for complex or large content that may take more time to process.
:::

### 3. **Error Handling**
Provide clear error handling instructions:

```yaml
instructions: >
  When content retrieval fails:
  - Explain what went wrong in user-friendly terms
  - Suggest alternative approaches
  - Offer to try different URLs or parameters
```

## Error Handling

The website content tool provides comprehensive error handling:

- **API Errors**: HTTP error responses and status codes
- **Timeout Errors**: Request timeout handling
- **Connection Errors**: Network connectivity issues
- **Content Errors**: Invalid or unprocessable content
- **Authentication Errors**: API authentication failures

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Verify the base URL is correct and accessible
   - Check network connectivity
   - Ensure the API service is running

2. **Timeout Errors**
   - Increase timeout for slow APIs
   - Check if the API is experiencing issues
   - Verify the requested content is available

3. **Content Processing Errors**
   - Check if the API returns valid content
   - Verify content encoding and format
   - Handle different content types appropriately

4. **Authentication Errors**
   - Verify API credentials if required
   - Check API key validity
   - Ensure proper authentication headers

### Debug Mode

Use debug mode to see detailed content retrieval logs:

```bash
poetry run gnosari --config "team.yaml" --message "Your message" --debug
```

:::tip Content Retrieval Debugging
Debug mode shows detailed information about content retrieval requests, including the full URL, response status, and content processing details.
:::

## Related Tools

- [API Request Tool](/docs/tools/api-request) - For general HTTP API integration
- [Knowledge Query Tool](/docs/tools/knowledge-query) - For knowledge base queries
- [Delegate Agent Tool](/docs/tools/delegate-agent) - For multi-agent coordination

The website content tool is useful for creating agents that need to retrieve and process web content. Use it to build agents that can fetch information from web APIs and provide content-based services to users.