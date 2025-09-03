---
sidebar_position: 7
---

# File Operations Tool

The **file_operations** tool enables agents to read, write, and manage files within a secure, sandboxed directory. This tool provides safe file system access with built-in security measures and configurable restrictions.

## Overview

The file operations tool allows agents to:
- **Read files** and retrieve their content
- **Write files** with automatic directory creation
- **List directory contents** to explore file structures
- **Check file existence** and get file information
- **Delete files** and empty directories safely
- **Work within a sandboxed directory** for security

## Capabilities

- ✅ **File Reading**: Read text files with configurable encoding
- ✅ **File Writing**: Write content with automatic directory creation
- ✅ **Directory Listing**: Explore file and directory structures
- ✅ **Existence Checking**: Verify file and directory existence
- ✅ **Safe Deletion**: Delete files and empty directories
- ✅ **Security Sandbox**: Restricted to configured base directory
- ✅ **Extension Filtering**: Optional file extension restrictions
- ✅ **Size Limits**: Configurable maximum file size limits
- ✅ **Path Validation**: Protection against directory traversal attacks

## YAML Configuration

### Basic Configuration

```yaml
tools:
  - name: file_operations
    module: gnosari.tools.file_operations
    class: FileOperationsTool
    args:
      base_directory: "./workspace"
      max_file_size: 10485760  # 10MB
```

### Advanced Configuration

```yaml
tools:
  - name: secure_file_ops
    module: gnosari.tools.file_operations
    class: FileOperationsTool
    args:
      base_directory: "./secure_workspace"
      allowed_extensions: [".txt", ".json", ".md", ".py", ".yaml"]
      max_file_size: 5242880  # 5MB
      tool_name: "secure_file_operations"
      tool_description: "Secure file operations with restricted extensions"
```

### Multiple File Operation Tools

```yaml
tools:
  - name: docs_file_ops
    module: gnosari.tools.file_operations
    class: FileOperationsTool
    args:
      base_directory: "./documents"
      allowed_extensions: [".md", ".txt", ".json"]
      max_file_size: 2097152  # 2MB

  - name: code_file_ops
    module: gnosari.tools.file_operations
    class: FileOperationsTool
    args:
      base_directory: "./code"
      allowed_extensions: [".py", ".js", ".yaml", ".json"]
      max_file_size: 1048576  # 1MB
```

## Agent Assignment

Assign the file operations tool to agents that need to work with files:

```yaml
agents:
  - name: FileManager
    instructions: >
      You are a file manager who can read, write, and organize files. Use the file_operations tool to:
      
      1. **Read Files**: Retrieve content from existing files
      2. **Write Files**: Create new files with specified content
      3. **List Directories**: Explore file structures and contents
      4. **Check Existence**: Verify if files or directories exist
      5. **Delete Files**: Remove files and empty directories safely
      
      Always provide clear feedback about file operations performed.
    model: gpt-4o
    tools:
      - file_operations
```

## Usage Examples

### Example 1: Document Management Team

```yaml
name: Document Management Team

tools:
  - name: doc_file_ops
    module: gnosari.tools.file_operations
    class: FileOperationsTool
    args:
      base_directory: "./documents"
      allowed_extensions: [".md", ".txt", ".json"]
      max_file_size: 5242880  # 5MB

agents:
  - name: DocumentWriter
    instructions: >
      Create and manage documents. Use the doc_file_ops tool to:
      - Write new documents: operation="write", file_path="documents/new-doc.md"
      - Read existing documents: operation="read", file_path="documents/existing.md"
      - List document directory: operation="list", file_path="documents"
    model: gpt-4o
    tools:
      - doc_file_ops

  - name: DocumentOrganizer
    instructions: >
      Organize and manage document structure. Use the doc_file_ops tool to:
      - Check if files exist: operation="exists", file_path="documents/file.md"
      - List directory contents: operation="list", file_path="documents"
      - Delete old files: operation="delete", file_path="documents/old-file.md"
    model: gpt-4o
    tools:
      - doc_file_ops
```

### Example 2: Code Management Team

```yaml
name: Code Management Team

tools:
  - name: code_file_ops
    module: gnosari.tools.file_operations
    class: FileOperationsTool
    args:
      base_directory: "./code"
      allowed_extensions: [".py", ".js", ".yaml", ".json", ".md"]
      max_file_size: 2097152  # 2MB

agents:
  - name: CodeWriter
    instructions: >
      Write and manage code files. Use the code_file_ops tool to:
      - Create Python scripts: operation="write", file_path="scripts/script.py"
      - Read configuration files: operation="read", file_path="config/settings.json"
      - List project structure: operation="list", file_path="."
    model: gpt-4o
    tools:
      - code_file_ops

  - name: CodeReviewer
    instructions: >
      Review and analyze code files. Use the code_file_ops tool to:
      - Read code files for review: operation="read", file_path="src/main.py"
      - Check if files exist: operation="exists", file_path="tests/test_main.py"
      - List test directory: operation="list", file_path="tests"
    model: gpt-4o
    tools:
      - code_file_ops
```

### Example 3: Data Processing Team

```yaml
name: Data Processing Team

tools:
  - name: data_file_ops
    module: gnosari.tools.file_operations
    class: FileOperationsTool
    args:
      base_directory: "./data"
      allowed_extensions: [".json", ".csv", ".txt", ".md"]
      max_file_size: 10485760  # 10MB

agents:
  - name: DataProcessor
    instructions: >
      Process and manage data files. Use the data_file_ops tool to:
      - Read data files: operation="read", file_path="input/data.json"
      - Write processed data: operation="write", file_path="output/processed.json"
      - List data directories: operation="list", file_path="input"
    model: gpt-4o
    tools:
      - data_file_ops

  - name: DataAnalyst
    instructions: >
      Analyze data files and create reports. Use the data_file_ops tool to:
      - Read analysis results: operation="read", file_path="analysis/results.json"
      - Write analysis reports: operation="write", file_path="reports/analysis.md"
      - Check file existence: operation="exists", file_path="data/raw.csv"
    model: gpt-4o
    tools:
      - data_file_ops
```

## Tool Parameters

The file operations tool accepts the following configuration parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_directory` | string | "./workspace" | Base directory for file operations |
| `allowed_extensions` | list | None | List of allowed file extensions (e.g., [".txt", ".json"]) |
| `max_file_size` | int | 10485760 | Maximum file size in bytes (10MB default) |
| `tool_name` | string | "file_operations" | Custom name for the tool |
| `tool_description` | string | "Read, write, and manage files..." | Custom description |

## Per-Call Parameters

When agents use the tool, they specify operation details:

| Parameter | Type | Description |
|-----------|------|-------------|
| `operation` | string | Operation to perform: "read", "write", "list", "exists", "delete" |
| `file_path` | string | Path to the file relative to base directory |
| `content` | string | Content to write (required for write operation) |
| `encoding` | string | File encoding (default: "utf-8") |
| `create_dirs` | bool | Create parent directories if they don't exist (default: true) |

## File Operations

### Read Files
Read the content of existing files:

```yaml
# Agent instructions for reading files
instructions: >
  To read a file, use:
  - operation: "read"
  - file_path: "path/to/file.txt"
  - encoding: "utf-8" (optional)
```

### Write Files
Create new files or overwrite existing ones:

```yaml
# Agent instructions for writing files
instructions: >
  To write a file, use:
  - operation: "write"
  - file_path: "path/to/file.txt"
  - content: "File content here"
  - encoding: "utf-8" (optional)
  - create_dirs: true (optional, creates directories if needed)
```

### List Directories
Explore directory contents:

```yaml
# Agent instructions for listing directories
instructions: >
  To list directory contents, use:
  - operation: "list"
  - file_path: "directory/path" or "." for base directory
```

### Check Existence
Verify if files or directories exist:

```yaml
# Agent instructions for checking existence
instructions: >
  To check if a file exists, use:
  - operation: "exists"
  - file_path: "path/to/file.txt"
```

### Delete Files
Remove files and empty directories:

```yaml
# Agent instructions for deleting files
instructions: >
  To delete a file, use:
  - operation: "delete"
  - file_path: "path/to/file.txt"
```

:::warning Safe Deletion
The tool only deletes empty directories for safety. Files are deleted immediately, so use with caution.
:::

## Security Features

### Directory Sandboxing
All file operations are restricted to the configured base directory:

```yaml
tools:
  - name: secure_file_ops
    module: gnosari.tools.file_operations
    class: FileOperationsTool
    args:
      base_directory: "./secure_workspace"  # All operations limited to this directory
```

:::info Security Sandbox
The tool prevents directory traversal attacks by validating all file paths and ensuring they stay within the base directory.
:::

### Extension Filtering
Restrict file operations to specific file types:

```yaml
tools:
  - name: text_only_ops
    module: gnosari.tools.file_operations
    class: FileOperationsTool
    args:
      allowed_extensions: [".txt", ".md", ".json"]  # Only these file types allowed
```

### Size Limits
Prevent large file operations:

```yaml
tools:
  - name: small_file_ops
    module: gnosari.tools.file_operations
    class: FileOperationsTool
    args:
      max_file_size: 1048576  # 1MB limit
```

## Agent Instructions

Provide clear instructions for file operations:

```yaml
agents:
  - name: FileSpecialist
    instructions: >
      You are a file specialist who manages files safely and efficiently. When using the file_operations tool:
      
      **File Operations:**
      - Use "read" to retrieve file content
      - Use "write" to create or update files
      - Use "list" to explore directories
      - Use "exists" to check file presence
      - Use "delete" to remove files (use carefully)
      
      **Best Practices:**
      - Always provide clear feedback about operations
      - Use descriptive file paths and names
      - Check file existence before reading
      - Create organized directory structures
      - Handle errors gracefully
      
      **Security:**
      - Only work within the configured directory
      - Respect file extension restrictions
      - Be mindful of file size limits
    model: gpt-4o
    tools:
      - file_operations
```

## Best Practices

### 1. **Organized Directory Structure**
Create logical directory hierarchies:

```yaml
instructions: >
  Organize files in logical directories:
  - documents/ for text files
  - data/ for JSON and CSV files
  - scripts/ for code files
  - reports/ for generated content
```

### 2. **File Naming Conventions**
Use consistent, descriptive file names:

```yaml
instructions: >
  Use clear, descriptive file names:
  - Use lowercase with hyphens: "user-guide.md"
  - Include dates when relevant: "report-2024-01-15.json"
  - Use meaningful extensions: ".config.json", ".data.csv"
```

### 3. **Error Handling**
Handle file operation errors gracefully:

```yaml
instructions: >
  When file operations fail:
  - Check if the file exists before reading
  - Verify directory permissions
  - Handle encoding errors appropriately
  - Provide helpful error messages to users
```

### 4. **Content Validation**
Validate file content before writing:

```yaml
instructions: >
  Before writing files:
  - Validate JSON content format
  - Check text encoding compatibility
  - Ensure content fits within size limits
  - Verify file extension matches content type
```

## Error Handling

The file operations tool provides comprehensive error handling:

- **Path Validation**: Prevents directory traversal attacks
- **Extension Checking**: Validates allowed file types
- **Size Limits**: Enforces maximum file sizes
- **Encoding Errors**: Handles text encoding issues
- **Permission Errors**: Manages file system permissions
- **Existence Checks**: Validates file and directory existence

## Troubleshooting

### Common Issues

1. **File Not Found**
   - Check if the file path is correct
   - Verify the file exists in the base directory
   - Ensure the file path is relative to the base directory

2. **Permission Denied**
   - Check file system permissions
   - Ensure the base directory is writable
   - Verify the agent has necessary permissions

3. **File Too Large**
   - Check file size against configured limits
   - Increase `max_file_size` if needed
   - Consider splitting large files

4. **Extension Not Allowed**
   - Verify file extension is in `allowed_extensions`
   - Add the extension to the configuration
   - Use a different file extension

5. **Directory Traversal**
   - Ensure file paths don't contain ".."
   - Use relative paths within the base directory
   - Check path validation settings

### Debug Mode

Use debug mode to see detailed file operation logs:

```bash
poetry run gnosari --config "team.yaml" --message "Your message" --debug
```

:::tip File Operations Debugging
Debug mode shows detailed information about file operations, including path validation, size checks, and operation results.
:::

## Related Tools

- [API Request Tool](/docs/tools/api-request) - For external file operations
- [MySQL Query Tool](/docs/tools/mysql-query) - For database file operations
- [Website Content Tool](/docs/tools/website-content) - For web content retrieval
- [Delegate Agent Tool](/docs/tools/delegate-agent) - For multi-agent coordination

The file operations tool is essential for creating agents that can manage local files safely and efficiently. Use it to build agents that can read, write, and organize files within a secure, sandboxed environment.