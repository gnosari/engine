---
sidebar_position: 4
---

# Knowledge Query Tool

The **knowledge_query** tool enables agents to query knowledge bases for relevant information. This tool integrates with Embedchain to provide RAG (Retrieval-Augmented Generation) capabilities, allowing agents to access and search through various types of knowledge sources.

## Overview

The knowledge query tool allows agents to:
- Search through knowledge bases using natural language queries
- Retrieve relevant information from various data sources
- Access context-aware information for better responses
- Integrate with multiple knowledge base types (websites, documents, videos, etc.)

## Capabilities

- ✅ **Natural Language Queries**: Search using human-readable questions
- ✅ **Multiple Data Sources**: Support for websites, documents, videos, and more
- ✅ **Semantic Search**: Find relevant information based on meaning, not just keywords
- ✅ **Context Retrieval**: Get relevant context for better AI responses
- ✅ **Knowledge Base Management**: Support for multiple named knowledge bases
- ✅ **Error Handling**: Graceful handling of query failures and missing knowledge bases

## YAML Configuration

### Basic Configuration

The knowledge query tool is automatically available when you define knowledge bases in your team configuration:

```yaml
name: Knowledge Team

# Knowledge bases (automatically adds knowledge_query tool)
knowledge:
  - id: "docs"
    name: "Documentation"
    type: "website"
    data: ["https://docs.example.com"]
  - id: "research"
    name: "Research Materials"
    type: "website" 
    data: ["https://research.example.com"]
```

:::info Automatic Tool Addition
When you define knowledge bases in your team configuration, the `knowledge_query` tool is automatically added and available to agents.
:::

agents:
  - name: Research Assistant
    instructions: "Answer questions using knowledge from our documentation and research"
    model: gpt-4o
    tools:
      - knowledge_query
    knowledge: ["docs", "research"]
```

### Advanced Configuration

```yaml
name: Advanced Knowledge Team

knowledge:
  - id: "product_docs"
    name: "Product Documentation"
    type: "website"
    data: 
      - "https://docs.product.com"
      - "https://api.product.com/docs"
  - id: "training_videos"
    name: "Training Videos"
    type: "youtube"
    data: ["https://youtube.com/playlist?list=your-playlist-id"]
  - id: "company_docs"
    name: "Company Documentation"
    type: "pdf"
    data: ["/path/to/company-handbook.pdf"]

agents:
  - name: Knowledge Expert
    instructions: >
      You are a knowledge expert who can answer questions using multiple knowledge sources.
      Use the knowledge_query tool to search through:
      - Product documentation for technical questions
      - Training videos for learning content
      - Company documents for policy information
    model: gpt-4o
    tools:
      - knowledge_query
    knowledge: ["product_docs", "training_videos", "company_docs"]
```

## Knowledge Base Types

Gnosari AI Teams supports various knowledge base types through Embedchain:

### Website Knowledge Bases

```yaml
knowledge:
  - id: "web_docs"
    name: "Web Documentation"
    type: "website"
    data: 
      - "https://docs.example.com"
      - "https://api.example.com/docs"
      - "https://blog.example.com"
```

:::tip Website Crawling
Website knowledge bases will crawl and index the content from the specified URLs for semantic search.
:::

### YouTube Knowledge Bases

```yaml
knowledge:
  - id: "tutorials"
    name: "Tutorial Videos"
    type: "youtube"
    data:
      - "https://youtube.com/watch?v=video-id"
      - "https://youtube.com/playlist?list=playlist-id"
      - "https://youtube.com/channel/channel-id"
```

:::note YouTube Processing
YouTube knowledge bases extract and index transcript content from videos for search and retrieval.
:::

### Document Knowledge Bases

```yaml
knowledge:
  - id: "manuals"
    name: "User Manuals"
    type: "pdf"
    data:
      - "/path/to/user-manual.pdf"
      - "/path/to/technical-spec.pdf"
```

### Text Knowledge Bases

```yaml
knowledge:
  - id: "faq"
    name: "Frequently Asked Questions"
    type: "text"
    data:
      - "Question: How do I reset my password? Answer: Click the forgot password link..."
      - "Question: What are the system requirements? Answer: Windows 10 or later..."
```

## Agent Assignment

Assign the knowledge query tool to agents that need to access knowledge bases:

```yaml
agents:
  - name: Documentation Expert
    instructions: >
      You are a documentation expert who helps users find information. Use the knowledge_query tool to:
      
      1. **Search Knowledge Bases**: Query relevant knowledge bases for information
      2. **Provide Context**: Use retrieved information to give accurate, helpful answers
      3. **Cite Sources**: Reference the knowledge base when providing information
      4. **Handle Queries**: Answer both specific and general questions
      
      Always search knowledge bases before providing answers to ensure accuracy.
    model: gpt-4o
    tools:
      - knowledge_query
    knowledge: ["docs", "faq", "tutorials"]
```

## Usage Examples

### Example 1: Customer Support Team

```yaml
name: Customer Support Team

knowledge:
  - id: "product_docs"
    name: "Product Documentation"
    type: "website"
    data: ["https://docs.product.com"]
  - id: "faq"
    name: "Frequently Asked Questions"
    type: "text"
    data:
      - "Question: How do I install the software? Answer: Download from our website..."
      - "Question: What are the system requirements? Answer: Windows 10 or macOS 10.15..."

agents:
  - name: Support Agent
    instructions: >
      Help customers with their questions using our knowledge base. Search through:
      - Product documentation for technical questions
      - FAQ for common questions
      
      Provide accurate, helpful answers and cite your sources.
    model: gpt-4o
    tools:
      - knowledge_query
    knowledge: ["product_docs", "faq"]

  - name: Support Manager
    instructions: "Coordinate support tasks and delegate to specialists"
    orchestrator: true
    model: gpt-4o
    delegation:
      - agent: OtherAgent
        instructions: "Use for coordination tasks"
```

### Example 2: Research Team

```yaml
name: Research Team

knowledge:
  - id: "research_papers"
    name: "Research Papers"
    type: "website"
    data: ["https://arxiv.org", "https://scholar.google.com"]
  - id: "industry_reports"
    name: "Industry Reports"
    type: "pdf"
    data: ["/data/industry-report-2024.pdf"]
  - id: "training_videos"
    name: "Training Videos"
    type: "youtube"
    data: ["https://youtube.com/playlist?list=research-methods"]

agents:
  - name: Research Analyst
    instructions: >
      Conduct research using multiple knowledge sources. Search through:
      - Research papers for academic information
      - Industry reports for market data
      - Training videos for methodology
      
      Provide comprehensive, well-sourced research findings.
    model: gpt-4o
    tools:
      - knowledge_query
    knowledge: ["research_papers", "industry_reports", "training_videos"]

  - name: Research Coordinator
    instructions: "Coordinate research projects and delegate tasks"
    orchestrator: true
    model: gpt-4o
    delegation:
      - agent: OtherAgent
        instructions: "Use for coordination tasks"
```

## Tool Parameters

The knowledge query tool accepts the following parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | The search query to find relevant information |
| `knowledge_name` | string | The name of the knowledge base to query |

## Agent Instructions

Provide clear instructions for knowledge query usage:

```yaml
agents:
  - name: Knowledge Assistant
    instructions: >
      You are a knowledge assistant who helps users find information. When using the knowledge_query tool:
      
      **Query Strategy:**
      - Use natural language questions
      - Be specific about what information you're looking for
      - Try different phrasings if initial queries don't return results
      
      **Response Format:**
      - Provide accurate information based on knowledge base content
      - Cite the knowledge base when providing information
      - If information isn't found, suggest alternative approaches
      
      **Knowledge Base Selection:**
      - Choose the most appropriate knowledge base for the query
      - Use multiple knowledge bases for comprehensive answers
      - Combine information from different sources when relevant
    model: gpt-4o
    tools:
      - knowledge_query
    knowledge: ["docs", "faq", "tutorials"]
```

## Best Practices

### 1. **Knowledge Base Organization**
Organize knowledge bases by topic or use case:

```yaml
knowledge:
  - id: "technical_docs"
    name: "Technical Documentation"
    type: "website"
    data: ["https://docs.technical.com"]
  - id: "user_guides"
    name: "User Guides"
    type: "website"
    data: ["https://guides.user.com"]
  - id: "troubleshooting"
    name: "Troubleshooting Guide"
    type: "text"
    data: ["Common issues and solutions..."]
```

### 2. **Query Optimization**
Help agents write effective queries:

```yaml
instructions: >
  When querying knowledge bases:
  - Use specific, descriptive terms
  - Include context about what you're trying to accomplish
  - Try different keywords if initial searches don't work
  - Break complex questions into simpler parts
```

### 3. **Source Citation**
Always cite knowledge sources:

```yaml
instructions: >
  When providing information from knowledge bases:
  - Always mention which knowledge base provided the information
  - Quote relevant sections when appropriate
  - Indicate if information comes from multiple sources
```

## Error Handling

The knowledge query tool includes comprehensive error handling:

- **Knowledge Base Not Found**: Clear error when specified knowledge base doesn't exist
- **Query Failures**: Graceful handling of search errors
- **Empty Results**: Appropriate responses when no relevant information is found
- **Connection Issues**: Handling of network and service connectivity problems

## Troubleshooting

### Common Issues

1. **Knowledge Base Not Found**
   - Verify knowledge base names match exactly
   - Check that knowledge bases are defined in the team configuration
   - Ensure knowledge bases are assigned to the agent

2. **No Results Found**
   - Try different query phrasings
   - Use more specific or general terms
   - Check if the knowledge base contains relevant information

3. **Slow Query Performance**
   - Optimize knowledge base size and content
   - Use more specific queries
   - Consider breaking large knowledge bases into smaller ones

### Debug Mode

Use debug mode to see detailed knowledge query logs:

```bash
gnosari --config "team.yaml" --message "Your message" --debug
```

:::tip Knowledge Query Debugging
Debug mode shows detailed information about knowledge base queries, including which knowledge base was searched and what results were found.
:::

## Related Tools

- [Delegate Agent Tool](delegate-agent) - For multi-agent coordination
- [API Request Tool](api-request) - For external service integration
- [Website Content Tool](website-content) - For web content retrieval

The knowledge query tool is essential for creating intelligent agents that can access and utilize organizational knowledge. Use it to build agents that provide accurate, well-sourced information to users.