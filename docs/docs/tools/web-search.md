---
sidebar_position: 9
---

# Web Search Tool

The Web Search Tool provides real-time web search capabilities using OpenAI's native web search functionality. This tool allows agents to find current information from across the internet, making it perfect for research tasks, news gathering, and accessing up-to-date information.

:::info OpenAI SDK Tool
This tool is part of the OpenAI Agents SDK and provides native web search capabilities through OpenAI's search infrastructure.
:::

## Features

- **Real-time Search**: Access current information from across the web
- **Intelligent Results**: OpenAI's search system provides relevant, high-quality results
- **Source Citations**: Results include proper source attribution and URLs
- **Context Awareness**: Search results are optimized for AI agent consumption
- **Geographic Filtering**: Optional location-based search results

## Configuration

### Basic Configuration

```yaml
tools:
  - name: web_search
    module: agents
    class: WebSearchTool
```

### Advanced Configuration

```yaml
tools:
  - name: web_search
    module: agents
    class: WebSearchTool
    args:
      search_context_size: large  # Options: small, medium, large
      user_location: US           # Geographic location for localized results
      filters:                    # Optional search filters
        - recent                  # Prioritize recent content
        - authoritative          # Prioritize authoritative sources
```

## Usage in Teams

### Basic Web Search Team

```yaml
name: Web Research Team
description: Team with web search capabilities

tools:
  - name: web_search
    module: agents
    class: WebSearchTool

agents:
  - name: Web Researcher
    instructions: >
      You are a web researcher. Use the web search tool to find current 
      information on any topic. Always cite your sources and provide 
      comprehensive, up-to-date information.
    orchestrator: true
    model: gpt-4o
    tools:
      - web_search
```

### Combined Research Team

```yaml
name: Advanced Research Team
description: Team with multiple research capabilities

tools:
  - name: web_search
    module: agents
    class: WebSearchTool
    args:
      search_context_size: large
      
  - name: website_content
    module: gnosari.tools.builtin.website_content
    class: WebsiteContentTool
    args:
      base_url: https://r.ai.neomanex.com
      timeout: 30

agents:
  - name: Research Coordinator
    instructions: >
      Coordinate research tasks. Use web search for general information 
      gathering and website content tool for specific page analysis.
    orchestrator: true
    model: gpt-4o
    tools:
      - web_search
      - website_content
```

## Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `search_context_size` | string | `medium` | Search result context size: `small`, `medium`, or `large` |
| `user_location` | string | `US` | Geographic location for localized search results |
| `filters` | array | `[]` | Optional search filters to apply |

### Search Context Sizes

- **small**: Concise results, faster processing
- **medium**: Balanced results with good detail (recommended)
- **large**: Comprehensive results with maximum context

### Available Filters

- **recent**: Prioritize recently published content
- **authoritative**: Focus on authoritative and trusted sources
- **news**: Emphasize news sources and current events
- **academic**: Prioritize academic and research sources

## Agent Instructions Best Practices

### Effective Search Instructions

```yaml
agents:
  - name: News Researcher
    instructions: >
      You are a news researcher specializing in current events. When searching:
      
      1. Use specific, targeted search queries
      2. Always verify information from multiple sources
      3. Include publication dates when citing sources
      4. Provide direct quotes when relevant
      5. Summarize key findings clearly
      
      Focus on recent developments and breaking news.
    model: gpt-4o
    tools:
      - web_search
```

### Research Workflow Instructions

```yaml
agents:
  - name: Research Analyst
    instructions: >
      You are a research analyst. Follow this workflow:
      
      1. **Initial Search**: Start with broad queries to understand the topic
      2. **Focused Research**: Drill down into specific aspects
      3. **Source Verification**: Cross-reference information across sources
      4. **Analysis**: Synthesize findings into actionable insights
      5. **Citation**: Always provide proper source attribution
      
      Use web search to gather comprehensive, current information.
    model: gpt-4o
    tools:
      - web_search
```

## Example Queries and Use Cases

### News and Current Events

```yaml
# Example: Getting latest AI news
agents:
  - name: AI News Tracker
    instructions: >
      Search for and summarize the latest developments in artificial 
      intelligence. Focus on:
      - New model releases
      - Industry partnerships
      - Regulatory developments
      - Breakthrough research
      
      Always include publication dates and source credibility.
    tools:
      - web_search
```

### Market Research

```yaml
# Example: Market analysis
agents:
  - name: Market Analyst
    instructions: >
      Conduct market research using web search. For each topic:
      - Search for market size and growth data
      - Identify key players and competitors
      - Find recent trends and developments
      - Locate authoritative industry reports
      
      Prioritize recent data and credible sources.
    tools:
      - web_search
```

### Technical Documentation

```yaml
# Example: Technical research
agents:
  - name: Tech Researcher
    instructions: >
      Research technical topics and best practices. When searching:
      - Look for official documentation
      - Find recent tutorials and guides
      - Search for common issues and solutions
      - Identify expert opinions and recommendations
      
      Focus on authoritative technical sources.
    tools:
      - web_search
```

## Error Handling

The Web Search Tool includes comprehensive error handling:

- **Network Issues**: Automatic retry with exponential backoff
- **Rate Limiting**: Graceful handling of API rate limits
- **Invalid Queries**: Clear error messages for malformed searches
- **No Results**: Informative responses when searches return no results

## Limitations

:::warning Usage Limits
The Web Search Tool is subject to OpenAI's usage limits and rate limiting. Monitor your usage to avoid hitting limits during high-volume operations.
:::

- **Rate Limits**: Subject to OpenAI's rate limiting policies
- **Geographic Restrictions**: Some content may be geo-restricted
- **Real-time Data**: Results are current but not necessarily real-time
- **Content Filtering**: Some content may be filtered by OpenAI's safety systems

## Integration with Other Tools

### With Knowledge Query Tool

```yaml
tools:
  - name: web_search
    module: agents
    class: WebSearchTool
    
  - name: knowledge_query
    module: gnosari.tools.builtin.knowledge
    class: KnowledgeQueryTool

agents:
  - name: Hybrid Researcher
    instructions: >
      Use both web search for current information and knowledge query 
      for internal documentation. Always compare and contrast findings 
      from both sources.
    tools:
      - web_search
      - knowledge_query
```

### With API Request Tool

```yaml
tools:
  - name: web_search
    module: agents
    class: WebSearchTool
    
  - name: api_request
    module: gnosari.tools.builtin.api_request
    class: APIRequestTool

agents:
  - name: Data Enricher
    instructions: >
      Use web search to gather context, then use API requests to fetch 
      structured data. Combine both sources for comprehensive analysis.
    tools:
      - web_search
      - api_request
```

## Troubleshooting

### Common Issues

1. **Tool Not Loading**
   ```bash
   # Check if OpenAI agents module is available
   python -c "from agents import WebSearchTool; print('Available')"
   ```

2. **Search Not Working**
   - Verify OpenAI API key is configured
   - Check network connectivity
   - Review search query formatting

3. **Limited Results**
   - Try different search queries
   - Adjust `search_context_size` parameter
   - Remove or modify search filters

### Debug Mode

Enable debug logging to troubleshoot issues:

```bash
LOG_LEVEL=debug poetry run gnosari --config "your-team.yaml" --message "your message" --debug
```

## Best Practices

### 1. **Query Optimization**
- Use specific, targeted search terms
- Include relevant context in queries
- Avoid overly broad or vague searches

### 2. **Source Verification**
- Always cross-reference important information
- Check publication dates for currency
- Verify source credibility and authority

### 3. **Result Processing**
- Summarize key findings clearly
- Extract actionable insights
- Maintain proper source attribution

### 4. **Performance Considerations**
- Use appropriate `search_context_size` for your needs
- Be mindful of rate limits and usage quotas
- Cache results when appropriate to reduce API calls

## Security Considerations

:::warning API Security
Ensure your OpenAI API key is properly secured and not exposed in configuration files or logs.
:::

- **API Key Protection**: Store API keys in environment variables
- **Content Filtering**: Be aware that results may be filtered by OpenAI's safety systems
- **Data Privacy**: Consider data privacy implications when searching sensitive topics

## Related Tools

- [Website Content Tool](website-content) - Fetch specific website content
- [Knowledge Query Tool](knowledge-query) - Query internal knowledge bases
- [API Request Tool](api-request) - Make structured API calls

## Next Steps

1. **Configure the Tool**: Add web search to your team configuration
2. **Test Searches**: Try different query types and configurations
3. **Optimize Performance**: Adjust parameters based on your use case
4. **Combine Tools**: Integrate with other research tools for comprehensive workflows

Ready to give your agents powerful web search capabilities? Add the Web Search Tool to your team and start exploring the web!