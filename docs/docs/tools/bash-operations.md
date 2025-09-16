---
sidebar_position: 8
---

# Bash Operations Tool

The **bash_operations** tool enables agents to execute bash commands safely within a controlled environment. This tool provides secure command execution with built-in security measures, command validation, and configurable restrictions.

## Overview

The bash operations tool allows agents to:
- **Execute bash commands** safely within a sandboxed directory
- **Run system utilities** like git, npm, python, and more
- **Capture command output** and return results to the agent
- **Set working directories** for command execution
- **Configure timeouts** to prevent long-running processes
- **Apply security restrictions** to prevent dangerous operations

## Capabilities

- ✅ **Command Execution**: Run bash commands with output capture
- ✅ **Working Directory Control**: Set execution directory within sandbox
- ✅ **Timeout Management**: Configurable command timeouts (max 300s)
- ✅ **Output Capture**: Capture both stdout and stderr
- ✅ **Environment Variables**: Set custom environment variables
- ✅ **Security Sandbox**: Restricted to configured base directory
- ✅ **Command Filtering**: Allow/block specific commands
- ✅ **Dangerous Command Protection**: Built-in protection against harmful commands
- ✅ **Output Size Limits**: Configurable maximum output size

## YAML Configuration

### Basic Configuration

```yaml
tools:
  - name: bash_operations
    module: gnosari.tools.bash_operations
    class: BashOperationsTool
    args:
      base_directory: "./workspace"
      max_output_size: 1048576  # 1MB
```

### Advanced Configuration

```yaml
tools:
  - name: secure_bash_ops
    module: gnosari.tools.bash_operations
    class: BashOperationsTool
    args:
      base_directory: "./secure_workspace"
      allowed_commands: ["git", "npm", "python", "node", "ls", "pwd", "echo"]
      blocked_commands: ["rm", "sudo", "chmod", "chown"]
      max_output_size: 512000  # 512KB
      tool_name: "secure_bash_operations"
      tool_description: "Secure bash operations with command restrictions"
```

### Development Environment Setup

```yaml
tools:
  - name: dev_bash_ops
    module: gnosari.tools.bash_operations
    class: BashOperationsTool
    args:
      base_directory: "./project"
      allowed_commands: ["git", "npm", "yarn", "python", "pip", "poetry", "node", "ls", "cat", "grep", "find", "mkdir", "touch"]
      blocked_commands: ["rm -rf", "sudo", "dd", "mkfs", "fdisk"]
      max_output_size: 2097152  # 2MB
```

### Unsafe Mode Configuration (⚠️ DANGEROUS)

```yaml
tools:
  - name: unrestricted_bash
    module: gnosari.tools.bash_operations
    class: BashOperationsTool
    args:
      base_directory: "/tmp/unsafe_workspace"  # Can use absolute paths in unsafe mode
      unsafe_mode: true  # DISABLES ALL SAFETY MECHANISMS
      max_output_size: 10485760  # 10MB
      tool_name: "unrestricted_bash_operations"
      tool_description: "DANGEROUS: Execute ANY bash command with no restrictions"
```

:::danger Unsafe Mode Warning
Setting `unsafe_mode: true` **COMPLETELY DISABLES ALL SECURITY MECHANISMS**:
- ❌ **No dangerous pattern blocking** (allows `rm -rf /`, `sudo`, `dd`, etc.)
- ❌ **No command filtering** (ignores `allowed_commands` and `blocked_commands`)
- ❌ **No path validation** (allows directory traversal with `..` and absolute paths)
- ⚠️ **Full system access** - agents can execute ANY command with ANY privileges
- 🔥 **EXTREMELY DANGEROUS** - use only in isolated environments or containers

**Only use unsafe mode if you absolutely need unrestricted command execution and understand the risks.**
:::

## Agent Assignment

Assign the bash operations tool to agents that need to run system commands:

```yaml
agents:
  - name: DevOpsAgent
    instructions: >
      You are a DevOps agent who can execute system commands safely. Use the bash_operations tool to:
      
      1. **Run Git Commands**: Execute git operations like status, add, commit, push
      2. **Package Management**: Run npm, pip, poetry commands for dependencies
      3. **Build Operations**: Execute build scripts and compilation tasks
      4. **System Utilities**: Use ls, grep, find for file system exploration
      5. **Development Tasks**: Run tests, linting, formatting tools
      
      Always provide clear feedback about command execution results.
    model: gpt-4o
    tools:
      - bash_operations
```

## Usage Examples

### Example 1: Git Operations Team

```yaml
name: Git Operations Team

tools:
  - name: git_bash_ops
    module: gnosari.tools.bash_operations
    class: BashOperationsTool
    args:
      base_directory: "./repository"
      allowed_commands: ["git", "ls", "pwd", "cat", "grep"]
      max_output_size: 1048576  # 1MB

agents:
  - name: GitManager
    instructions: >
      Manage Git repositories using git_bash_ops tool:
      - Check status: command="git status"
      - View history: command="git log --oneline -10"
      - Add files: command="git add ."
      - Commit changes: command="git commit -m 'message'"
      - Push to remote: command="git push origin main"
    model: gpt-4o
    tools:
      - git_bash_ops

  - name: GitAnalyst
    instructions: >
      Analyze Git repositories using git_bash_ops tool:
      - Show branches: command="git branch -a"
      - Diff changes: command="git diff"
      - Show file contents: command="cat README.md"
      - Search in files: command="grep -r 'pattern' ."
    model: gpt-4o
    tools:
      - git_bash_ops
```

### Example 2: Node.js Development Team

```yaml
name: Node.js Development Team

tools:
  - name: node_bash_ops
    module: gnosari.tools.bash_operations
    class: BashOperationsTool
    args:
      base_directory: "./nodejs-project"
      allowed_commands: ["npm", "node", "yarn", "ls", "cat", "mkdir", "touch"]
      blocked_commands: ["rm", "sudo"]
      max_output_size: 2097152  # 2MB

agents:
  - name: NodeDeveloper
    instructions: >
      Develop Node.js applications using node_bash_ops tool:
      - Install dependencies: command="npm install"
      - Run scripts: command="npm run start"
      - Run tests: command="npm test"
      - List files: command="ls -la"
      - Check package.json: command="cat package.json"
    model: gpt-4o
    tools:
      - node_bash_ops

  - name: PackageManager
    instructions: >
      Manage Node.js packages using node_bash_ops tool:
      - Install packages: command="npm install package-name"
      - Update packages: command="npm update"
      - Audit security: command="npm audit"
      - View dependencies: command="npm ls"
    model: gpt-4o
    tools:
      - node_bash_ops
```

### Example 3: Python Development Team

```yaml
name: Python Development Team

tools:
  - name: python_bash_ops
    module: gnosari.tools.bash_operations
    class: BashOperationsTool
    args:
      base_directory: "./python-project"
      allowed_commands: ["python", "pip", "poetry", "pytest", "black", "flake8", "ls", "cat", "mkdir"]
      blocked_commands: ["rm -rf", "sudo", "chmod 777"]
      max_output_size: 1048576  # 1MB

agents:
  - name: PythonDeveloper
    instructions: >
      Develop Python applications using python_bash_ops tool:
      - Run Python scripts: command="python main.py"
      - Install dependencies: command="pip install -r requirements.txt"
      - Run tests: command="pytest tests/"
      - Format code: command="black ."
      - Lint code: command="flake8 ."
    model: gpt-4o
    tools:
      - python_bash_ops

  - name: PythonTester
    instructions: >
      Test Python applications using python_bash_ops tool:
      - Run all tests: command="pytest -v"
      - Run specific test: command="pytest tests/test_module.py"
      - Coverage report: command="pytest --cov=src tests/"
      - Check test files: command="ls tests/"
    model: gpt-4o
    tools:
      - python_bash_ops
```

### Example 4: Unrestricted System Administration (⚠️ DANGEROUS)

```yaml
name: System Administration Team

tools:
  - name: unrestricted_bash
    module: gnosari.tools.bash_operations
    class: BashOperationsTool
    args:
      base_directory: "/"  # Root directory access
      unsafe_mode: true  # REMOVES ALL SAFETY MECHANISMS
      max_output_size: 10485760  # 10MB
      tool_name: "system_admin_bash"
      tool_description: "DANGEROUS: Full system access with no restrictions"

agents:
  - name: SystemAdmin
    instructions: >
      ⚠️ DANGER: You have UNRESTRICTED system access. This tool can execute ANY command including:
      
      **System Operations (BE EXTREMELY CAREFUL):**
      - File operations: ANY file anywhere on the system
      - Process management: kill, ps, top, systemctl
      - Network operations: netstat, ss, iptables, curl, wget
      - System info: df, du, free, uptime, uname
      - User management: useradd, usermod, passwd (if you have privileges)
      
      **ABSOLUTE PATHS ALLOWED:**
      - working_directory: "/etc" for config files
      - working_directory: "/var/log" for log files  
      - working_directory: "/home/user" for user directories
      
      **⚠️ WARNING: This tool can destroy the system. Use with extreme caution.**
    model: gpt-4o
    tools:
      - unrestricted_bash
```

:::danger System Administration Example Warning
The above example shows unsafe mode for system administration. This configuration:
- **Can destroy the entire system** with commands like `rm -rf /`
- **Has root access** if the agent process runs as root
- **Can access ANY file** on the system including secrets and configs
- **Should ONLY be used** in isolated containers or test environments
- **Is NOT recommended** for production systems

Always prefer using safe mode with specific `allowed_commands` for production use.
:::

## Tool Parameters

The bash operations tool accepts the following configuration parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_directory` | string | "./workspace" | Base directory for command execution |
| `allowed_commands` | list | None | List of allowed command prefixes (e.g., ["git", "npm"]) |
| `blocked_commands` | list | [] | List of blocked command prefixes |
| `max_output_size` | int | 1048576 | Maximum output size in bytes (1MB default) |
| `unsafe_mode` | bool | false | **⚠️ DANGEROUS**: Disables ALL security mechanisms |
| `tool_name` | string | "bash_operations" | Custom name for the tool |
| `tool_description` | string | "Execute bash commands..." | Custom description |

## Per-Call Parameters

When agents use the tool, they specify command execution details:

| Parameter | Type | Description |
|-----------|------|-------------|
| `command` | string | Bash command to execute |
| `working_directory` | string | Working directory relative to base directory (optional) |
| `timeout` | int | Command timeout in seconds (default: 30, max: 300) |
| `capture_output` | bool | Whether to capture command output (default: true) |

## Command Operations

### Basic Command Execution
Execute simple bash commands:

```yaml
# Agent instructions for basic commands
instructions: >
  To execute basic commands, use:
  - command: "ls -la"
  - working_directory: "." (optional)
  - timeout: 30 (optional)
  - capture_output: true (optional)
```

### Git Operations
Execute Git commands safely:

```yaml
# Agent instructions for Git operations
instructions: >
  To use Git commands, use:
  - command: "git status"
  - command: "git add ."
  - command: "git commit -m 'commit message'"
  - command: "git push origin main"
```

### Package Management
Install and manage packages:

```yaml
# Agent instructions for package management
instructions: >
  To manage packages, use:
  - command: "npm install"
  - command: "pip install -r requirements.txt"
  - command: "poetry install"
  - command: "yarn add package-name"
```

### Build and Test Operations
Run build and test commands:

```yaml
# Agent instructions for build/test operations
instructions: >
  To build and test, use:
  - command: "npm run build"
  - command: "pytest tests/"
  - command: "npm test"
  - command: "poetry run pytest"
```


## Security Features

### Command Validation
The tool validates all commands for security:

```yaml
tools:
  - name: secure_bash
    module: gnosari.tools.bash_operations
    class: BashOperationsTool
    args:
      allowed_commands: ["git", "npm", "python"]  # Only these commands allowed
      blocked_commands: ["rm", "sudo", "dd"]      # These commands blocked
```

:::info Security Protection
The tool automatically blocks dangerous commands like `rm -rf /`, `dd if=`, `sudo`, and other potentially harmful operations.
:::

### Directory Sandboxing
All commands execute within the configured base directory:

```yaml
tools:
  - name: sandboxed_bash
    module: gnosari.tools.bash_operations
    class: BashOperationsTool
    args:
      base_directory: "./secure_workspace"  # Commands limited to this directory
```

### Timeout Protection
Prevent long-running commands from hanging:

```yaml
# Agent instructions for timeout management
instructions: >
  Set appropriate timeouts for commands:
  - Quick commands: timeout=10
  - Build operations: timeout=120
  - Test suites: timeout=300 (maximum allowed)
```

### Output Size Limits
Prevent excessive memory usage:

```yaml
tools:
  - name: limited_bash
    module: gnosari.tools.bash_operations
    class: BashOperationsTool
    args:
      max_output_size: 512000  # 512KB limit
```

### Unsafe Mode (⚠️ EXTREMELY DANGEROUS)
Completely disable all security mechanisms:

```yaml
tools:
  - name: dangerous_bash
    module: gnosari.tools.bash_operations
    class: BashOperationsTool
    args:
      unsafe_mode: true  # REMOVES ALL SAFETY MECHANISMS
      base_directory: "/any/path"  # Can use absolute paths
      # allowed_commands and blocked_commands are ignored
```

:::danger Unsafe Mode Risks
When `unsafe_mode: true` is set:

- ✅ **Executes ANY command**: `rm -rf /`, `sudo rm -rf /`, `dd if=/dev/zero of=/dev/sda`
- ✅ **Directory traversal**: `../../../etc/passwd`, absolute paths like `/etc`
- ✅ **System modification**: `chmod 777 /`, `chown root:root /`
- ✅ **Privilege escalation**: `sudo su -`, `passwd root`
- ✅ **Code injection**: `eval`, `$(malicious_command)`, backticks
- ✅ **Data exfiltration**: `curl -X POST data @/etc/passwd`

**This mode bypasses ALL security protections. Use only in isolated containers or sandboxed environments.**
:::

## Agent Instructions

Provide clear instructions for bash operations:

```yaml
agents:
  - name: BashSpecialist
    instructions: >
      You are a bash specialist who executes system commands safely and efficiently. When using the bash_operations tool:
      
      **Command Execution:**
      - Use descriptive commands that are easy to understand
      - Set appropriate timeouts for different operation types
      - Capture output to provide feedback to users
      - Use working directories to organize operations
      
      **Best Practices:**
      - Always check command output for errors
      - Provide clear feedback about operation results
      - Use appropriate timeouts for different tasks
      - Handle command failures gracefully
      
      **Security:**
      - Only use allowed commands
      - Avoid potentially dangerous operations
      - Work within the configured directory
      - Be mindful of output size limits
      
      **Common Commands:**
      - Git: git status, git add, git commit, git push
      - Node.js: npm install, npm start, npm test
      - Python: python script.py, pip install, pytest
      - System: ls, pwd, cat, grep, mkdir
    model: gpt-4o
    tools:
      - bash_operations
```

## Best Practices

### 1. **Command Organization**
Structure commands logically:

```yaml
instructions: >
  Organize commands by purpose:
  - Setup: npm install, pip install requirements
  - Development: npm start, python main.py
  - Testing: npm test, pytest tests/
  - Build: npm run build, python setup.py build
```

### 2. **Error Handling**
Handle command failures gracefully:

```yaml
instructions: >
  When commands fail:
  - Check the exit code in the response
  - Read stderr output for error details
  - Provide helpful error messages to users
  - Suggest alternative approaches when possible
```

### 3. **Timeout Management**
Set appropriate timeouts:

```yaml
instructions: >
  Use appropriate timeouts:
  - Quick commands (ls, pwd): 10 seconds
  - Package installs: 60-120 seconds
  - Build operations: 120-300 seconds
  - Test suites: 60-300 seconds
```

### 4. **Working Directory Usage**
Use working directories effectively:

```yaml
instructions: >
  Manage working directories:
  - Use "." for base directory operations
  - Use "src" for source code operations
  - Use "tests" for test-related commands
  - Use "docs" for documentation tasks
```

## Error Handling

The bash operations tool provides comprehensive error handling:

- **Command Validation**: Validates commands against security restrictions
- **Path Validation**: Ensures working directory is within base directory
- **Timeout Protection**: Kills commands that exceed timeout limits
- **Output Size Limits**: Prevents excessive memory usage
- **Exit Code Reporting**: Reports command success/failure status
- **Error Output Capture**: Captures both stdout and stderr

## Troubleshooting

### Common Issues

1. **Command Not Allowed**
   - Check if command is in `allowed_commands` list
   - Verify command is not in `blocked_commands` list
   - Add the command to the allowed list if safe

2. **Command Timeout**
   - Increase timeout value for long-running commands
   - Check if command is hanging or requires input
   - Use background execution for very long tasks

3. **Permission Denied**
   - Check file system permissions
   - Ensure base directory is accessible
   - Verify command has necessary permissions

4. **Output Too Large**
   - Increase `max_output_size` if needed
   - Use commands that produce less output
   - Redirect large outputs to files

5. **Working Directory Issues**
   - Ensure working directory exists
   - Check path is relative to base directory
   - Verify directory permissions

### Debug Mode

Use debug mode to see detailed command execution logs:

```bash
poetry run gnosari --config "team.yaml" --message "Your message" --debug
```

:::tip Bash Operations Debugging
Debug mode shows detailed information about command execution, including validation, timeout handling, and output capture.
:::

## Related Tools

- [File Operations Tool](/docs/tools/file-operations) - For file system operations
- [API Request Tool](/docs/tools/api-request) - For external API interactions
- [MySQL Query Tool](/docs/tools/mysql-query) - For database operations
- [Delegate Agent Tool](/docs/tools/delegate-agent) - For multi-agent coordination

The bash operations tool is essential for creating agents that can interact with the operating system safely and efficiently. Use it to build agents that can execute development workflows, manage repositories, run builds, and perform system administration tasks within a secure environment.