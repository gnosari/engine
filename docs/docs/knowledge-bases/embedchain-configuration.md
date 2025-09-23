---
sidebar_position: 2
---

# Embedchain Configuration

Gnosari AI Teams uses Embedchain as the underlying knowledge base engine, providing powerful RAG (Retrieval-Augmented Generation) capabilities. This page covers all available configuration options for customizing Embedchain behavior in your knowledge bases.

## Overview

Embedchain configuration allows you to customize:
- **LLM Models**: Choose different language models for generation
- **Embedding Models**: Select embedding providers and models
- **Chunking Strategy**: Configure how documents are split and processed
- **Database Settings**: Customize vector database configuration
- **Loader Settings**: Configure data source processing

## Configuration Structure

Embedchain configuration is added to the `config` section of your knowledge base:

```yaml
knowledge:
  - id: "custom_knowledge_base"
    name: "Custom Knowledge Base"
    type: "website"
    config:
      # Embedchain configuration goes here
      llm:
        provider: "openai"
        config:
          model: "gpt-4o"
          temperature: 0.1
          max_tokens: 1000
      embedder:
        provider: "openai"
        config:
          model: "text-embedding-3-small"
      chunker:
        chunk_size: 1000
        chunk_overlap: 200
        length_function: "len"
    data:
      - "https://example.com"
```

## LLM Configuration

Configure the language model used for generating responses from your knowledge base.

### OpenAI Configuration

```yaml
config:
  llm:
    provider: "openai"
    config:
      model: "gpt-4o"                    # Model name
      temperature: 0.1                   # Creativity level (0.0-2.0)
      max_tokens: 1000                  # Maximum response length
      top_p: 1.0                        # Nucleus sampling parameter
      frequency_penalty: 0.0             # Frequency penalty (-2.0 to 2.0)
      presence_penalty: 0.0              # Presence penalty (-2.0 to 2.0)
      stop: ["\n\n"]                    # Stop sequences
      api_key: "your-api-key"           # Optional: override default API key
      base_url: "https://api.openai.com/v1"  # Optional: custom base URL
```

### Anthropic Configuration

```yaml
config:
  llm:
    provider: "anthropic"
    config:
      model: "claude-3-sonnet-20240229"  # Claude model
      temperature: 0.1                   # Creativity level (0.0-1.0)
      max_tokens: 1000                  # Maximum response length
      top_p: 1.0                        # Nucleus sampling parameter
      top_k: 40                         # Top-k sampling
      stop_sequences: ["\n\n"]           # Stop sequences
      api_key: "your-api-key"           # Optional: override default API key
      base_url: "https://api.anthropic.com"  # Optional: custom base URL
```

### Google Configuration

```yaml
config:
  llm:
    provider: "google"
    config:
      model: "gemini-pro"               # Gemini model
      temperature: 0.1                  # Creativity level (0.0-2.0)
      max_tokens: 1000                 # Maximum response length
      top_p: 1.0                       # Nucleus sampling parameter
      top_k: 40                        # Top-k sampling
      api_key: "your-api-key"          # Optional: override default API key
      base_url: "https://generativelanguage.googleapis.com/v1"  # Optional: custom base URL
```

### DeepSeek Configuration

```yaml
config:
  llm:
    provider: "deepseek"
    config:
      model: "deepseek-chat"           # DeepSeek model
      temperature: 0.1                 # Creativity level (0.0-2.0)
      max_tokens: 1000                # Maximum response length
      top_p: 1.0                      # Nucleus sampling parameter
      frequency_penalty: 0.0           # Frequency penalty (-2.0 to 2.0)
      presence_penalty: 0.0           # Presence penalty (-2.0 to 2.0)
      api_key: "your-api-key"         # Optional: override default API key
      base_url: "https://api.deepseek.com/v1"  # Optional: custom base URL
```

### Azure OpenAI Configuration

```yaml
config:
  llm:
    provider: "azure_openai"
    config:
      model: "gpt-4o"                  # Model name
      temperature: 0.1                 # Creativity level (0.0-2.0)
      max_tokens: 1000                 # Maximum response length
      api_key: "your-api-key"          # Azure OpenAI API key
      base_url: "https://your-resource.openai.azure.com/"  # Azure endpoint
      api_version: "2024-02-15-preview"  # API version
      deployment_name: "gpt-4o"        # Deployment name
```

## Embedder Configuration

Configure the embedding model used to create vector representations of your content.

### OpenAI Embeddings

```yaml
config:
  embedder:
    provider: "openai"
    config:
      model: "text-embedding-3-small"  # Embedding model
      dimensions: 1536                 # Optional: reduce dimensions
      api_key: "your-api-key"          # Optional: override default API key
      base_url: "https://api.openai.com/v1"  # Optional: custom base URL
```

### OpenAI Embeddings (Large)

```yaml
config:
  embedder:
    provider: "openai"
    config:
      model: "text-embedding-3-large"  # Larger embedding model
      dimensions: 3072                 # Optional: reduce dimensions
      api_key: "your-api-key"          # Optional: override default API key
```

### Hugging Face Embeddings

```yaml
config:
  embedder:
    provider: "huggingface"
    config:
      model: "sentence-transformers/all-MiniLM-L6-v2"  # HF model
      api_key: "your-hf-token"         # Optional: Hugging Face token
      cache_folder: "./cache"         # Optional: cache directory
```

### Cohere Embeddings

```yaml
config:
  embedder:
    provider: "cohere"
    config:
      model: "embed-english-v3.0"     # Cohere model
      api_key: "your-api-key"          # Cohere API key
      base_url: "https://api.cohere.ai/v1"  # Optional: custom base URL
```

### Google Embeddings

```yaml
config:
  embedder:
    provider: "google"
    config:
      model: "textembedding-gecko"    # Google embedding model
      api_key: "your-api-key"         # Google API key
      base_url: "https://generativelanguage.googleapis.com/v1"  # Optional: custom base URL
```

## Chunker Configuration

Configure how documents are split into chunks for processing.

### Basic Chunking

```yaml
config:
  chunker:
    chunk_size: 1000                  # Maximum characters per chunk
    chunk_overlap: 200                 # Overlap between chunks
    length_function: "len"             # Function to measure length
```

### Advanced Chunking

```yaml
config:
  chunker:
    chunk_size: 1000                  # Maximum characters per chunk
    chunk_overlap: 200                 # Overlap between chunks
    length_function: "len"             # Function to measure length
    separators: ["\n\n", "\n", " ", ""]  # Custom separators
    keep_separator: true               # Keep separators in chunks
    add_start_index: false             # Add start index to chunks
```

### Semantic Chunking

```yaml
config:
  chunker:
    chunk_size: 1000                  # Maximum characters per chunk
    chunk_overlap: 200                 # Overlap between chunks
    length_function: "len"             # Function to measure length
    separators: ["\n\n", "\n", ". ", "! ", "? ", " ", ""]  # Sentence-aware separators
    keep_separator: true               # Keep separators in chunks
```

## Database Configuration

Configure the vector database used to store embeddings.

### ChromaDB Configuration

```yaml
config:
  db:
    provider: "chroma"
    config:
      collection_name: "knowledge_base"  # Collection name
      persist_directory: "./chroma_db"   # Persistence directory
      host: "localhost"                 # Database host
      port: 8000                        # Database port
      settings:
        anonymized_telemetry: false     # Disable telemetry
        allow_reset: true               # Allow collection reset
```

### Pinecone Configuration

```yaml
config:
  db:
    provider: "pinecone"
    config:
      index_name: "knowledge-base"      # Pinecone index name
      api_key: "your-api-key"          # Pinecone API key
      environment: "us-west1-gcp"      # Pinecone environment
      dimension: 1536                   # Vector dimension
      metric: "cosine"                  # Distance metric
      pod_type: "p1.x1"                # Pod type
      replicas: 1                      # Number of replicas
```

### Weaviate Configuration

```yaml
config:
  db:
    provider: "weaviate"
    config:
      url: "http://localhost:8080"     # Weaviate URL
      api_key: "your-api-key"          # Optional: API key
      class_name: "KnowledgeBase"      # Class name
      vectorizer: "text2vec-openai"    # Vectorizer
      module_config:
        "text2vec-openai":
          model: "text-embedding-3-small"
          modelVersion: "latest"
          type: "text"
          vectorizeClassName: false
```

### Qdrant Configuration

```yaml
config:
  db:
    provider: "qdrant"
    config:
      url: "http://localhost:6333"     # Qdrant URL
      api_key: "your-api-key"          # Optional: API key
      collection_name: "knowledge_base" # Collection name
      vector_size: 1536                # Vector size
      distance: "Cosine"                # Distance metric
      on_disk_payload: true            # Store payload on disk
```

## Loader Configuration

Configure how different data sources are processed.

### Directory Loader Configuration

```yaml
knowledge:
  - name: "documentation"
    type: "directory"
    config:
      loader_config:
        recursive: true                 # Recursively scan subdirectories
        extensions: [".txt", ".md", ".py", ".yaml", ".yml", ".json"]  # Allowed extensions
        exclude_patterns: ["*.log", "*.tmp"]  # Exclude patterns
        include_patterns: ["*.md", "*.txt"]   # Include patterns
        max_file_size: 10485760        # Max file size (10MB)
        encoding: "utf-8"               # File encoding
```

### Website Loader Configuration

```yaml
knowledge:
  - name: "website_content"
    type: "website"
    config:
      loader_config:
        max_depth: 3                   # Maximum crawl depth
        max_pages: 100                 # Maximum pages to crawl
        delay: 1                       # Delay between requests (seconds)
        timeout: 30                    # Request timeout (seconds)
        user_agent: "Mozilla/5.0..."  # Custom user agent
        allowed_domains: ["example.com"]  # Allowed domains
        denied_domains: ["admin.example.com"]  # Denied domains
        follow_robots_txt: true        # Follow robots.txt
```

### PDF Loader Configuration

```yaml
knowledge:
  - name: "pdf_documents"
    type: "pdf"
    config:
      loader_config:
        extract_images: false           # Extract images from PDF
        extract_tables: true            # Extract tables from PDF
        language: "eng"                 # OCR language
        page_numbers: true              # Include page numbers
        max_pages: 100                 # Maximum pages to process
```

### YouTube Loader Configuration

```yaml
knowledge:
  - name: "youtube_content"
    type: "youtube_video"
    config:
      loader_config:
        language: "en"                  # Video language
        include_auto_generated: false   # Include auto-generated captions
        include_manual: true           # Include manual captions
        max_duration: 3600             # Max video duration (seconds)
        quality: "highest"              # Video quality preference
```

## Complete Configuration Examples

### Production-Ready Configuration

```yaml
knowledge:
  - id: "production_kb"
    name: "Production Knowledge Base"
    type: "website"
    config:
      llm:
        provider: "openai"
        config:
          model: "gpt-4o"
          temperature: 0.1
          max_tokens: 2000
          top_p: 0.9
      embedder:
        provider: "openai"
        config:
          model: "text-embedding-3-large"
          dimensions: 3072
      chunker:
        chunk_size: 1500
        chunk_overlap: 300
        length_function: "len"
        separators: ["\n\n", "\n", ". ", "! ", "? ", " ", ""]
        keep_separator: true
      db:
        provider: "chroma"
        config:
          collection_name: "production_kb"
          persist_directory: "./data/chroma_db"
          settings:
            anonymized_telemetry: false
            allow_reset: true
      loader_config:
        max_depth: 2
        max_pages: 50
        delay: 2
        timeout: 30
        follow_robots_txt: true
    data:
      - "https://docs.company.com"
      - "https://api.company.com/docs"
```

### Multi-Model Configuration

```yaml
knowledge:
  - id: "research_kb"
    name: "Research Knowledge Base"
    type: "website"
    config:
      llm:
        provider: "anthropic"
        config:
          model: "claude-3-sonnet-20240229"
          temperature: 0.2
          max_tokens: 3000
          top_p: 0.9
      embedder:
        provider: "cohere"
        config:
          model: "embed-english-v3.0"
      chunker:
        chunk_size: 2000
        chunk_overlap: 400
        length_function: "len"
      db:
        provider: "pinecone"
        config:
          index_name: "research-kb"
          dimension: 1024
          metric: "cosine"
          pod_type: "p1.x1"
    data:
      - "https://research.example.com"
```

### Cost-Optimized Configuration

```yaml
knowledge:
  - id: "cost_optimized_kb"
    name: "Cost-Optimized Knowledge Base"
    type: "website"
    config:
      llm:
        provider: "openai"
        config:
          model: "gpt-3.5-turbo"        # Cheaper model
          temperature: 0.1
          max_tokens: 1000
      embedder:
        provider: "openai"
        config:
          model: "text-embedding-3-small"  # Smaller embedding model
          dimensions: 512                 # Reduced dimensions
      chunker:
        chunk_size: 800                  # Smaller chunks
        chunk_overlap: 100
        length_function: "len"
      db:
        provider: "chroma"
        config:
          collection_name: "cost_optimized_kb"
          persist_directory: "./data/chroma_db"
    data:
      - "https://docs.example.com"
```

## Environment Variables

You can use environment variables in your configuration:

```yaml
config:
  llm:
    provider: "openai"
    config:
      model: "gpt-4o"
      api_key: "${OPENAI_API_KEY}"      # Use environment variable
      base_url: "${OPENAI_BASE_URL}"    # Optional custom base URL
  embedder:
    provider: "openai"
    config:
      model: "text-embedding-3-small"
      api_key: "${OPENAI_API_KEY}"      # Same API key
```

## Configuration Validation

Gnosari validates your Embedchain configuration and will show errors for:
- Invalid provider names
- Missing required configuration parameters
- Invalid parameter values
- Unsupported model combinations

## Performance Optimization

### Chunk Size Optimization
- **Small chunks (500-800)**: Better for specific questions, faster retrieval
- **Medium chunks (1000-1500)**: Balanced performance and context
- **Large chunks (2000+)**: Better for complex, multi-part questions

### Embedding Model Selection
- **text-embedding-3-small**: Fast, cost-effective, good for most use cases
- **text-embedding-3-large**: Higher quality, better for complex queries
- **Custom models**: Specialized for specific domains

### Database Selection
- **ChromaDB**: Good for development and small-scale production
- **Pinecone**: Scalable, managed service for production
- **Weaviate**: Advanced features, good for complex queries
- **Qdrant**: High performance, good for large-scale applications

## Troubleshooting Configuration

### Common Issues

1. **Invalid Provider**
   ```
   Error: Provider 'invalid_provider' not supported
   ```
   Solution: Use supported providers: `openai`, `anthropic`, `google`, `deepseek`, `azure_openai`

2. **Missing API Key**
   ```
   Error: API key required for provider 'openai'
   ```
   Solution: Set environment variable or provide in config

3. **Invalid Model**
   ```
   Error: Model 'invalid-model' not available for provider 'openai'
   ```
   Solution: Use valid model names for the provider

4. **Dimension Mismatch**
   ```
   Error: Embedding dimension mismatch with database
   ```
   Solution: Ensure embedding model dimensions match database configuration

### Debug Configuration

Enable debug mode to see detailed configuration information:

```bash
gnosari --config "team.yaml" --message "test" --debug
```

This will show:
- Configuration validation results
- Model initialization details
- Database connection status
- Embedding model information

## Related Topics

- [Knowledge Bases Introduction](intro) - Learn the basics of knowledge bases
- [Knowledge Query Tool](/tools/knowledge-query) - How to query knowledge bases
- [Agent Configuration](/agents) - Configure agents with knowledge access
- [Team Configuration](/teams) - Set up teams with knowledge bases

## Next Steps

Now that you understand Embedchain configuration:
- [Configure your first knowledge base](intro) with custom settings
- [Set up agents](/agents) to use your configured knowledge bases
- [Learn about the knowledge query tool](/tools/knowledge-query) for detailed usage
- [Explore team patterns](/teams) for knowledge-based workflows