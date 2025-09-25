# Interactive Bash Operations Tool

The Interactive Bash Operations Tool allows agents to execute bash commands that require interactive input, handle blocking processes, and maintain persistent sessions for complex workflows.

## Key Features

- **Interactive Process Handling**: Detect and respond to interactive prompts
- **Session Management**: Maintain persistent sessions across multiple tool calls
- **Prompt Detection**: Automatically detect common interactive prompts
- **Input Response**: Send input to blocking processes waiting for user interaction
- **Safe Execution**: Same security features as the regular bash operations tool

## Basic Usage

### Starting an Interactive Command

```yaml
tools:
  - name: "interactive_bash"
    module: "gnosari.tools.builtin.interactive_bash_operations" 
    class: "InteractiveBashOperationsTool"
    args:
      base_directory: "./workspace"
      allowed_commands: ["npm", "git", "python", "pip", "make"]
      max_output_size: 5242880  # 5MB
```

### Example: Handling npm init

```python
# Agent starts npm init
result = await tool.run({
    "command": "npm init",
    "expect_prompt": True,
    "timeout": 120
})

# Output will include:
# - Session ID for continuation
# - Detected prompts
# - Current process state

# Agent responds to prompts
result = await tool.run({
    "session_id": "interactive_session_1_1234567890",
    "input_text": "my-awesome-package"
})

# Continue with more inputs
result = await tool.run({
    "session_id": "interactive_session_1_1234567890", 
    "input_text": "1.0.0"
})
```

### Example: Arrow Key Navigation

```python
# Start a tool with menu navigation
result = await tool.run({
    "command": "npm audit",
    "timeout": 60
})

# Navigate down in menu and select option
result = await tool.run({
    "session_id": "interactive_session_2_1234567890",
    "special_keys": ["down", "down", "enter"]
})

# Use arrow keys to navigate and ESC to exit
result = await tool.run({
    "session_id": "interactive_session_2_1234567890", 
    "special_keys": ["up", "escape"]
})
```

### Example: Interactive Menu Selection

```python
# Start a tool with complex menu system
result = await tool.run({
    "command": "docker system prune",
    "timeout": 120
})

# Navigate menu options with arrow keys
result = await tool.run({
    "session_id": "interactive_session_3_1234567890",
    "special_keys": ["down", "down", "space", "enter"]  # Select options and confirm
})

# Use function keys if available
result = await tool.run({
    "session_id": "interactive_session_3_1234567890",
    "special_keys": ["f1"]  # Help key
})
```

### Example: Control Key Combinations

```python
# Start an interactive editor
result = await tool.run({
    "command": "nano myfile.txt",
    "timeout": 300
})

# Use control combinations for editor commands
result = await tool.run({
    "session_id": "interactive_session_4_1234567890",
    "input_text": "Hello World!"
})

# Save and exit with Ctrl+O, Enter, Ctrl+X
result = await tool.run({
    "session_id": "interactive_session_4_1234567890",
    "special_keys": ["ctrl_o"]  # Save
})

result = await tool.run({
    "session_id": "interactive_session_4_1234567890", 
    "special_keys": ["enter", "ctrl_x"]  # Confirm filename and exit
})
```

### Example: Raw Escape Sequences (Advanced)

```python
# Send custom escape sequences for specialized applications
result = await tool.run({
    "command": "htop",
    "timeout": 60
})

# Send custom escape sequence (advanced usage)
result = await tool.run({
    "session_id": "interactive_session_5_1234567890",
    "key_sequence": "\033[5~"  # Page Up in htop
})

# Quit htop
result = await tool.run({
    "session_id": "interactive_session_5_1234567890",
    "input_text": "q"
})
```

### Example: Interactive Git Operations

```python
# Start interactive rebase
result = await tool.run({
    "command": "git rebase -i HEAD~3",
    "working_directory": "my-project",
    "timeout": 300
})

# Agent can respond to editor prompts, conflict resolution, etc.
result = await tool.run({
    "session_id": "interactive_session_2_1234567891",
    "input_text": ":wq"  # Save and quit vim
})
```

### Example: Python Interactive Shell

```python
# Start Python REPL
result = await tool.run({
    "command": "python3",
    "timeout": 600  # 10 minutes for longer sessions
})

# Send Python code
result = await tool.run({
    "session_id": "interactive_session_3_1234567892",
    "input_text": "import os; print(os.getcwd())"
})

# Continue working in the same Python session
result = await tool.run({
    "session_id": "interactive_session_3_1234567892",
    "input_text": "x = 42; print(x * 2)"
})
```

## Configuration Options

### Tool Initialization Parameters

```python
InteractiveBashOperationsTool(
    base_directory="./workspace",           # Working directory root
    allowed_commands=["git", "npm", "pip"],  # Whitelist of allowed commands  
    blocked_commands=["rm", "sudo"],        # Blacklist of blocked commands
    max_output_size=5242880,                # Max output size (5MB)
    unsafe_mode=False,                      # Disable safety checks
    session_timeout=3600                    # Session timeout (1 hour)
)
```

### Function Parameters

- **command**: The bash command to execute
- **working_directory**: Relative path within base directory
- **timeout**: Command timeout in seconds (max 1800)
- **input_text**: Text to send to interactive process
- **special_keys**: List of special keys to send (e.g., `["down", "down", "enter"]`)
- **key_sequence**: Raw escape sequence for advanced usage (e.g., `"\033[5~"`)
- **expect_prompt**: Whether to wait for interactive prompts
- **session_id**: ID to continue existing session

### Available Special Keys

**Navigation:**
- `up`, `down`, `left`, `right` - Arrow keys
- `home`, `end` - Home/End keys  
- `page_up`, `page_down` - Page navigation
- `tab` - Tab key

**Control:**
- `enter` - Enter/Return key
- `escape` - Escape key
- `space` - Space bar
- `backspace`, `delete` - Delete keys
- `insert` - Insert key

**Function Keys:**
- `f1` through `f12` - Function keys

**Control Combinations:**
- `ctrl_c` - Ctrl+C (interrupt)
- `ctrl_d` - Ctrl+D (EOF)
- `ctrl_z` - Ctrl+Z (suspend)
- `ctrl_a` - Ctrl+A (beginning of line)
- `ctrl_e` - Ctrl+E (end of line)

## Prompt Detection

The tool automatically detects common interactive patterns:

- `Press any key to continue`
- `Do you want to continue? [Y/n]`
- `Are you sure? [y/N]`
- `Enter your choice:`
- `Select an option:`
- `Please enter`
- `Password:`
- `Username:`
- Shell prompts (`$ `, `# `, `> `)

## Session Management

### Session Lifecycle

1. **Creation**: New session created when starting interactive command
2. **Interaction**: Use session_id to send input and receive output
3. **Monitoring**: Sessions automatically cleaned up after timeout
4. **Completion**: Sessions end when process exits

### Session Information

Each session tracks:
- Process state (alive/dead)
- Working directory
- Command being executed
- Last activity timestamp
- Whether waiting for input
- Detected prompts

## Security Considerations

### Safe Mode (Default)
- Command validation against dangerous patterns
- Path traversal protection
- Command whitelist/blacklist enforcement
- Output size limits

### Unsafe Mode
- Disables ALL security mechanisms
- Allows any command execution
- Permits directory traversal
- Use only in trusted environments

## Error Handling

The tool handles various error conditions:

- **Process Timeout**: Kills runaway processes
- **Invalid Input**: Validates commands and parameters  
- **Session Expiry**: Cleans up inactive sessions
- **Process Death**: Detects when processes exit unexpectedly
- **Output Overflow**: Limits output size to prevent memory issues

## Best Practices

### For Agent Developers

1. **Always check session state** before sending input
2. **Handle timeouts gracefully** for long-running processes
3. **Use appropriate timeouts** based on expected process duration
4. **Monitor prompt detection** to respond appropriately
5. **Clean up sessions** by letting processes complete naturally

### For Team Configuration

1. **Use command whitelists** in production environments
2. **Set reasonable timeouts** to prevent resource exhaustion
3. **Configure appropriate output limits** based on use case
4. **Enable unsafe mode only** in controlled environments
5. **Monitor session usage** to prevent resource leaks

## Common Use Cases

- **Package Management**: npm install, pip install with interactive prompts
- **Version Control**: Interactive git operations (rebase, merge conflicts)
- **Development Tools**: Interactive debuggers, REPLs, build tools
- **System Administration**: Interactive configuration tools
- **File Editing**: Using interactive editors like vim/nano

## Integration Example

```yaml
name: "Development Team"
description: "Team for interactive development tasks"

tools:
  - name: "interactive_bash"
    module: "gnosari.tools.builtin.interactive_bash_operations"
    class: "InteractiveBashOperationsTool"
    args:
      base_directory: "./workspace"
      allowed_commands: ["npm", "git", "python", "pip", "make", "docker"]
      session_timeout: 1800  # 30 minutes
      max_output_size: 10485760  # 10MB

agents:
  - name: "DevOps"
    instructions: "Handle interactive development and deployment tasks"
    tools: ["interactive_bash"]
    model: "gpt-4o"
```

This tool enables agents to handle complex interactive workflows that would otherwise require manual intervention, making them more capable of autonomous development and system administration tasks.