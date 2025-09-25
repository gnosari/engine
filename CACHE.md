# Cache System Documentation

The Gnosari AI Teams framework includes a sophisticated, generic cache system designed to improve performance and reduce redundant operations across all components. This document provides comprehensive documentation on how the cache system works, how to use it, and how it stores information.

## Overview

The cache system is built following SOLID principles and provides:

- **Type Safety**: Generic implementation with type variables
- **Pluggable Architecture**: Extensible hash strategies, storage backends, and validation
- **Rich Metadata**: Comprehensive tracking of cache entries with timestamps and status
- **Automatic Cleanup**: Built-in expiration and validation mechanisms
- **JSON Storage**: Human-readable cache files for debugging and inspection

## Architecture

### Core Components

The cache system consists of several key components:

#### 1. Base Interfaces (`src/gnosari/core/cache/base.py`)

- **`Cacheable`**: Protocol for items that can be cached
- **`CacheableItem`**: Simple implementation for basic use cases
- **`HashStrategy`**: Abstract base for different hashing algorithms
- **`CacheStorage`**: Abstract base for storage backends
- **`CacheValidator`**: Abstract base for validation strategies

#### 2. Cache Entry System (`src/gnosari/core/cache/entry.py`)

- **`CacheEntry`**: Represents individual cached items with metadata
- **`CacheStatus`**: Enumeration of cache entry statuses (LOADING, LOADED, FAILED, EXPIRED, INVALID)

#### 3. Cache Manager (`src/gnosari/core/cache/manager.py`)

- **`CacheManager`**: Main orchestrator for all cache operations
- **`CacheConfig`**: Configuration for cache manager instances
- **`JSONCacheStorage`**: JSON file-based storage implementation
- **`HashCacheValidator`**: Hash-based validation strategy

#### 4. Hash Strategies (`src/gnosari/core/cache/hashers.py`)

- **`ConfigHasher`**: SHA256 hash for configuration objects
- **`ContentHasher`**: SHA256 hash for arbitrary content
- **`MD5Hasher`**: MD5 hash for faster but less secure scenarios
- **`CombinedHasher`**: Combines multiple hash strategies

## How It Works

### Cache Entry Lifecycle

1. **LOADING**: Item is marked as currently being processed
2. **LOADED**: Item has been successfully cached and is ready for use
3. **FAILED**: Item failed to load/process (with error message)
4. **EXPIRED**: Item has expired and needs refresh
5. **INVALID**: Item is invalid due to configuration changes

### Storage Format

The cache system stores data in JSON files with the following structure:

```json
{
  "knowledge_base_id_1": {
    "cache_key": "knowledge_base_id_1",
    "item_type": "knowledge_base",
    "content_hash": "sha256_hash_of_config",
    "data_sources": ["https://example.com", "file.txt"],
    "created_at": "2024-01-15T10:30:00.000000",
    "last_accessed": "2024-01-15T11:45:00.000000",
    "last_modified": "2024-01-15T10:30:00.000000",
    "status": "loaded",
    "metadata": {
      "name": "docs",
      "data_source": "https://example.com",
      "source": "website"
    },
    "expires_at": null
  }
}
```

### Cache File Location

By default, knowledge base caches are stored in:
- **Directory**: `{current_working_directory}/.cache/knowledge/`
- **File**: `knowledge_cache.json`

## Usage Examples

### Basic Cache Manager Setup

```python
from gnosari.core.cache import CacheManager, CacheConfig
from gnosari.core.cache.hashers import ConfigHasher

# Create cache configuration
config = CacheConfig(
    cache_dir="./cache",
    cache_name="my_cache",
    hash_strategy=ConfigHasher(),
    max_entries=100,
    default_ttl_hours=24,
    auto_cleanup=True
)

# Initialize cache manager
cache = CacheManager(config)
```

### Caching Knowledge Base Data

```python
# Mark knowledge base as loading
cache.mark_loading(
    cache_key="kb_website_docs",
    item_type="knowledge_base",
    data={"type": "website", "data": ["https://example.com"]},
    data_sources=["https://example.com"],
    metadata={"name": "docs", "source": "website"}
)

# Mark as successfully loaded
cache.mark_loaded("kb_website_docs", {"loaded_at": "2024-01-15"})

# Check if cached and valid
is_cached = cache.is_cached("kb_website_docs", {"type": "website", "data": ["https://example.com"]})
```

### Knowledge Manager Integration

The `KnowledgeManager` automatically uses the cache system:

```python
from gnosari.knowledge import KnowledgeManager

# Initialize with custom cache directory
km = KnowledgeManager(cache_dir="./my_cache")

# Create knowledge base (automatically cached)
kb = km.create_knowledge_base(
    name="docs",
    kb_type="website", 
    config={"data": ["https://example.com"]},
    knowledge_id="website_docs"
)

# Add data (cache prevents duplicate loading)
await km.add_data_to_knowledge_base("docs", "https://example.com")

# Query (uses cached knowledge base)
results = await km.query_knowledge_base("docs", "What is AI?")
```

## Cache Operations

### Checking Cache Status

```python
# Check if item is cached and valid
is_valid = cache.is_cached("cache_key", current_data)

# Get cache entry
entry = cache.get_entry("cache_key")

# List entries by status
loaded_entries = cache.list_by_status(CacheStatus.LOADED)
failed_entries = cache.list_by_status(CacheStatus.FAILED)

# List entries by type
kb_entries = cache.list_by_type("knowledge_base")
```

### Cache Management

```python
# Invalidate specific entry
cache.invalidate("cache_key")

# Clear all cache
cache.clear()

# Clean up failed entries
failed_count = cache.cleanup_failed()

# Get cache statistics
stats = cache.get_stats()
```

### Cache Statistics

The cache system provides detailed statistics:

```python
stats = cache.get_stats()
# Returns:
{
    'total_entries': 5,
    'by_status': {
        'loaded': 3,
        'loading': 1,
        'failed': 1
    },
    'by_type': {
        'knowledge_base': 4,
        'model_config': 1
    },
    'cache_dir': './cache',
    'cache_name': 'my_cache',
    'hash_strategy': 'SHA256-JSON',
    'validator_strategy': 'Hash-SHA256-JSON'
}
```

## Knowledge Base Caching

### How Knowledge Bases Are Cached

1. **Configuration Hashing**: The knowledge base configuration is hashed using `ConfigHasher`
2. **Unique Identification**: Each knowledge base gets a unique `knowledge_id` used as the cache key
3. **Status Tracking**: Loading, loaded, and failed states are tracked
4. **Metadata Storage**: Source information, timestamps, and error messages are stored
5. **Validation**: Cache validity is checked by comparing configuration hashes

### Cache File Structure for Knowledge Bases

```json
{
  "website_docs": {
    "cache_key": "website_docs",
    "item_type": "knowledge_base",
    "content_hash": "a1b2c3d4e5f6...",
    "data_sources": ["https://example.com"],
    "created_at": "2024-01-15T10:30:00.000000",
    "last_accessed": "2024-01-15T11:45:00.000000",
    "last_modified": "2024-01-15T10:30:00.000000",
    "status": "loaded",
    "metadata": {
      "name": "docs",
      "data_source": "https://example.com",
      "source": "website",
      "loaded_at": "2024-01-15T10:30:00.000000"
    },
    "expires_at": null
  }
}
```

### Preventing Duplicate Loading

The cache system prevents duplicate knowledge base loading by:

1. **Checking Cache First**: Before loading data, check if knowledge base is already cached
2. **Configuration Validation**: Compare current config hash with cached hash
3. **Status Verification**: Ensure cached entry is in LOADED status
4. **Skip Loading**: If valid cache exists, skip the expensive loading process

## Advanced Usage

### Custom Hash Strategies

```python
from gnosari.core.cache.hashers import CombinedHasher, ConfigHasher, ContentHasher

# Create combined hash strategy
combined_hasher = CombinedHasher(
    ConfigHasher(),
    ContentHasher()
)

config = CacheConfig(
    cache_dir="./cache",
    cache_name="robust_cache",
    hash_strategy=combined_hasher
)
```

### Custom Storage Backend

```python
from gnosari.core.cache.base import CacheStorage

class DatabaseCacheStorage(CacheStorage[CacheEntry]):
    def load(self) -> Dict[str, CacheEntry]:
        # Load from database
        pass
    
    def save(self, cache_data: Dict[str, CacheEntry]) -> None:
        # Save to database
        pass
    
    def exists(self) -> bool:
        # Check database connection
        pass
    
    def clear(self) -> None:
        # Clear database table
        pass

# Use custom storage
cache = CacheManager(config, storage=DatabaseCacheStorage())
```

### Cache Entry Metadata

```python
# Add custom metadata
entry = cache.put(
    cache_key="custom_item",
    item_type="custom",
    data={"key": "value"},
    metadata={
        "version": "1.0",
        "author": "user@example.com",
        "tags": ["important", "production"]
    }
)

# Retrieve metadata
version = entry.get_metadata("version")
author = entry.get_metadata("author", "unknown")
```

## Best Practices

### 1. Cache Key Design

- Use descriptive, unique keys
- Include version information for evolving data
- Consider hierarchical naming (e.g., `kb_website_docs_v1`)

### 2. Configuration Management

- Keep configurations stable for consistent hashing
- Include all relevant parameters in the config hash
- Document configuration changes that affect caching

### 3. Error Handling

- Always check cache status before using cached data
- Handle FAILED status appropriately
- Implement fallback mechanisms for cache misses

### 4. Performance Optimization

- Use appropriate hash strategies (MD5 for speed, SHA256 for security)
- Set reasonable TTL values
- Enable auto_cleanup for production environments
- Monitor cache hit rates and adjust max_entries accordingly

### 5. Debugging

- Enable debug logging to track cache operations
- Inspect JSON cache files for troubleshooting
- Use cache statistics to monitor system health

## Troubleshooting

### Common Issues

1. **Cache Not Working**: Check if cache directory is writable
2. **Stale Data**: Verify configuration hasn't changed
3. **Memory Usage**: Monitor cache size and adjust max_entries
4. **Performance**: Consider using faster hash strategies for large datasets

### Debug Commands

```python
# Get detailed cache information
stats = cache.get_stats()
print(f"Cache stats: {stats}")

# List all cached knowledge bases
cached_kbs = cache.list_by_type("knowledge_base")
for kb in cached_kbs:
    print(f"KB: {kb.cache_key}, Status: {kb.status}")

# Check specific entry
entry = cache.get_entry("knowledge_base_id")
if entry:
    print(f"Entry metadata: {entry.metadata}")
```

## Integration with Other Components

The cache system is designed to be used across all Gnosari components:

- **Knowledge Bases**: Automatic caching of loaded data
- **Model Configurations**: Caching of LLM model settings
- **Tool Configurations**: Caching of tool setups
- **Team Configurations**: Caching of team definitions

This generic approach ensures consistent caching behavior and performance improvements across the entire framework.