---
sidebar_position: 5
---

# Knowledge Bases

Knowledge bases enable your agents to access and search through large amounts of information. Gnosari AI Teams integrates with Embedchain to provide powerful RAG (Retrieval-Augmented Generation) capabilities, allowing agents to query various types of data sources.

## What are Knowledge Bases?

Knowledge bases in Gnosari AI Teams are:
- **Information repositories** that agents can search and query
- **RAG-enabled systems** that provide context-aware responses
- **Multi-source data** from websites, documents, videos, and more
- **Semantic search** capabilities for finding relevant information
- **Automatically integrated** with the `knowledge_query` tool

:::info Automatic Tool Integration
When you define knowledge bases in your team configuration, the `knowledge_query` tool is automatically added and available to agents.
:::

## Knowledge Base Configuration

Knowledge bases are defined in the `knowledge` section of your team YAML:

```yaml
name: Knowledge Team

# Knowledge bases configuration
knowledge:
  - id: "knowledge_base_id"  # Unique identifier for referencing
    name: "knowledge_base_name"
    type: "data_source_type"
    data: ["source1", "source2", "source3"]

# The knowledge_query tool is automatically added
agents:
  - name: ResearchAgent
    instructions: "Research topics using available knowledge"
    model: gpt-4o
    tools:
      - knowledge_query  # Automatically available
    knowledge: ["knowledge_base_id"]  # Assign knowledge bases to agents by ID
```

## Supported Data Sources

Gnosari AI Teams supports various types of knowledge sources through Embedchain:

### Website Knowledge Bases

Crawl and index content from websites:

```yaml
knowledge:
  - name: "company_docs"
    type: "website"
    data: 
      - "https://docs.company.com"
      - "https://api.company.com/docs"
      - "https://blog.company.com"
```

:::tip Website Crawling
Website knowledge bases will crawl and index the content from the specified URLs for semantic search. This is great for documentation, blogs, and API references.
:::

### YouTube Knowledge Bases

Extract and index content from YouTube videos:

```yaml
knowledge:
  - name: "tutorials"
    type: "youtube"
    data:
      - "https://youtube.com/watch?v=video-id"
      - "https://youtube.com/playlist?list=playlist-id"
      - "https://youtube.com/channel/channel-id"
```

:::note YouTube Processing
YouTube knowledge bases extract and index transcript content from videos for search and retrieval. Perfect for educational content and tutorials.
:::

### Document Knowledge Bases

Process various document formats:

```yaml
knowledge:
  - name: "manuals"
    type: "pdf"
    data:
      - "/path/to/user-manual.pdf"
      - "/path/to/technical-spec.pdf"
      - "/path/to/procedure-guide.pdf"
```

### Text Knowledge Bases

Direct text content for FAQs and structured information:

```yaml
knowledge:
  - name: "faq"
    type: "text"
    data:
      - "Question: How do I reset my password? Answer: Click the forgot password link on the login page..."
      - "Question: What are the system requirements? Answer: Windows 10 or later, 8GB RAM minimum..."
      - "Question: How do I contact support? Answer: Email support@company.com or call 1-800-SUPPORT..."
```

### CSV Knowledge Bases

Process structured data from CSV files:

```yaml
knowledge:
  - name: "product_catalog"
    type: "csv"
    data:
      - "/path/to/products.csv"
      - "/path/to/inventory.csv"
```

### JSON Knowledge Bases

Process structured data from JSON files:

```yaml
knowledge:
  - name: "api_specs"
    type: "json"
    data:
      - "/path/to/api-specification.json"
      - "/path/to/schema-definitions.json"
```

## Agent Knowledge Assignment

Assign knowledge bases to specific agents:

```yaml
agents:
  - name: TechnicalSupport
    instructions: "Provide technical support using company documentation"
    model: gpt-4o
    tools:
      - knowledge_query
    knowledge: ["technical_docs", "troubleshooting_guides"]

  - name: SalesAgent
    instructions: "Help customers with product information and sales"
    model: gpt-4o
    tools:
      - knowledge_query
    knowledge: ["product_catalog", "pricing_info"]

  - name: GeneralAssistant
    instructions: "Help with general questions and information"
    model: gpt-4o
    tools:
      - knowledge_query
    knowledge: ["faq", "company_docs"]
```

:::info Knowledge Access Control
Agents can only access knowledge bases that are assigned to them in the `knowledge` list. This allows you to control which agents have access to which information.
:::

## Knowledge Base Best Practices

### 1. **Organize by Topic**
Group related information together:

```yaml
knowledge:
  - name: "technical_docs"
    type: "website"
    data: ["https://docs.technical.com"]
    
  - name: "user_guides"
    type: "website"
    data: ["https://guides.user.com"]
    
  - name: "troubleshooting"
    type: "text"
    data: ["Common issues and solutions..."]
```

### 2. **Use Descriptive Names**
Choose clear, descriptive names for knowledge bases:

```yaml
knowledge:
  - name: "product_documentation"  # Clear and specific
  - name: "customer_support_faq"   # Indicates purpose
  - name: "api_reference_guides"   # Describes content type
```

### 3. **Optimize Data Sources**
Choose the most appropriate data source type:

```yaml
# For structured data
knowledge:
  - name: "product_catalog"
    type: "csv"
    data: ["/data/products.csv"]

# For unstructured content
knowledge:
  - name: "blog_posts"
    type: "website"
    data: ["https://blog.company.com"]

# For direct Q&A content
knowledge:
  - name: "faq"
    type: "text"
    data: ["Q: How do I...? A: You can..."]
```

## Common Knowledge Base Patterns

### 1. **Customer Support Team**
```yaml
name: Customer Support Team

knowledge:
  - name: "support_docs"
    type: "website"
    data: ["https://support.company.com"]
  - name: "faq"
    type: "text"
    data: ["Q: How do I reset my password? A: Click forgot password..."]
  - name: "troubleshooting"
    type: "pdf"
    data: ["/troubleshooting-guide.pdf"]

agents:
  - name: SupportAgent
    instructions: "Help customers resolve issues using support documentation"
    model: gpt-4o
    tools:
      - knowledge_query
    knowledge: ["support_docs", "faq", "troubleshooting"]
```

### 2. **Research Team**
```yaml
name: Research Team

knowledge:
  - name: "research_papers"
    type: "website"
    data: ["https://arxiv.org", "https://scholar.google.com"]
  - name: "industry_reports"
    type: "pdf"
    data: ["/data/industry-report-2024.pdf"]
  - name: "training_videos"
    type: "youtube"
    data: ["https://youtube.com/playlist?list=research-methods"]

agents:
  - name: ResearchAnalyst
    instructions: "Conduct research using multiple knowledge sources"
    model: gpt-4o
    tools:
      - knowledge_query
    knowledge: ["research_papers", "industry_reports", "training_videos"]
```

### 3. **Content Creation Team**
```yaml
name: Content Creation Team

knowledge:
  - name: "brand_guidelines"
    type: "pdf"
    data: ["/brand-guidelines.pdf"]
  - name: "content_standards"
    type: "text"
    data: ["Content should be clear, engaging, and follow our style guide..."]
  - name: "reference_materials"
    type: "website"
    data: ["https://reference.company.com"]

agents:
  - name: ContentWriter
    instructions: "Create content following brand guidelines and standards"
    model: gpt-4o
    tools:
      - knowledge_query
    knowledge: ["brand_guidelines", "content_standards", "reference_materials"]
```

## Knowledge Query Usage

Agents use the `knowledge_query` tool to search knowledge bases:

### Query Parameters
- **`query`**: The search query in natural language
- **`knowledge_name`**: The name of the knowledge base to search

### Example Queries
```yaml
# Agent instructions for effective knowledge queries
instructions: >
  When using the knowledge_query tool:
  - Use natural language questions
  - Be specific about what information you need
  - Try different phrasings if initial queries don't work
  - Combine information from multiple knowledge bases when relevant
```

:::tip Effective Queries
Good knowledge queries are:
- **Specific**: Clear about what information is needed
- **Natural**: Use human-readable language
- **Contextual**: Include relevant context when helpful
- **Iterative**: Try different approaches if needed
:::

## Knowledge Base Management

### Adding New Content
To add new content to existing knowledge bases:

1. **Update the data sources** in your YAML configuration
2. **Restart your team** to rebuild the knowledge base
3. **Test queries** to ensure new content is accessible

### Updating Knowledge Bases
```yaml
# Add new sources to existing knowledge base
knowledge:
  - name: "company_docs"
    type: "website"
    data: 
      - "https://docs.company.com"      # Existing
      - "https://api.company.com/docs"  # Existing
      - "https://new-docs.company.com"  # New addition
```

### Performance Optimization
- **Limit data sources** to relevant content only
- **Use appropriate types** for different content formats
- **Organize by topic** to improve search relevance
- **Regular updates** to keep information current

:::warning Knowledge Base Size
Large knowledge bases may take longer to build and query. Consider breaking very large knowledge bases into smaller, topic-specific ones.
:::

## Troubleshooting Knowledge Bases

### Common Issues

1. **Knowledge Base Not Found**
   - Verify knowledge base names match exactly
   - Check that knowledge bases are defined in team configuration
   - Ensure knowledge bases are assigned to agents

2. **No Results Found**
   - Try different query phrasings
   - Use more specific or general terms
   - Check if the knowledge base contains relevant information
   - Verify data sources are accessible

3. **Slow Query Performance**
   - Optimize knowledge base size and content
   - Use more specific queries
   - Consider breaking large knowledge bases into smaller ones

### Debug Mode
Use debug mode to see detailed knowledge query information:

```bash
gnosari --config "team.yaml" --message "Your message" --debug
```

:::tip Knowledge Query Debugging
Debug mode shows detailed information about knowledge base queries, including which knowledge base was searched and what results were found.
:::

## Integration with Other Tools

Knowledge bases work seamlessly with other tools:

### With API Request Tool
```yaml
agents:
  - name: ResearchAgent
    instructions: "Research topics using knowledge bases and external APIs"
    tools:
      - knowledge_query  # Search internal knowledge
      - api_request      # Fetch external data
    knowledge: ["research_docs"]
```

### With Database Tools
```yaml
agents:
  - name: DataAnalyst
    instructions: "Analyze data using databases and knowledge bases"
    tools:
      - mysql_query      # Query structured data
      - knowledge_query  # Search documentation
    knowledge: ["analytics_docs"]
```

### With Delegation
```yaml
agents:
  - name: Coordinator
    instructions: "Coordinate research using knowledge bases and delegation"
    orchestrator: true
    tools:
      - delegate_agent   # Delegate to specialists
      - knowledge_query  # Search for context
    knowledge: ["project_docs"]
```

## Related Topics

- [Agents](agents) - Learn how to configure agents with knowledge access
- [Teams](teams) - Understand team structure and knowledge sharing
- [Orchestration](coordination/orchestration) - Learn about agent coordination with knowledge
- [Tools](tools/knowledge-query) - Detailed knowledge query tool documentation
- [Quickstart](quickstart) - Create your first team with knowledge bases

## Next Steps

Now that you understand knowledge bases, learn how to:
- [Configure agents](agents) to use knowledge bases effectively
- [Set up teams](teams) with knowledge sharing capabilities
- [Use orchestration](coordination/orchestration) to coordinate knowledge-based workflows
- [Use the knowledge query tool](tools/knowledge-query) for detailed information
- [Create your first team](quickstart) with knowledge integration