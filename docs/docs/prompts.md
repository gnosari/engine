# Prompt Templates

Manage and process reusable prompt templates with variable substitution for structured content generation.

## Commands

### List Templates
```bash
gnosari prompts list
```
Lists all `.md` templates in `prompts/` directory with variable counts.

### View Template
```bash
# Full template with rich formatting (default)
gnosari prompts view <template_name>

# Plain markdown output
gnosari prompts view <template_name> --format markdown

# With variable preview (partial substitution)
gnosari prompts view <template_name> --var1 "value" --var2 "value"

# Variables only
gnosari prompts view <template_name> variables
```

### Process Template
```bash
# Rich formatted output (default)
gnosari prompts use <template_name> "message" --var1 "value" --var2 "value"

# Plain markdown output
gnosari prompts use <template_name> "message" --format markdown --var1 "value"
```

### Create File from Template
```bash
gnosari prompts create <template_name> <filepath> "message" --var1 "value" --var2 "value"
```
Creates new file at `<filepath>` with processed template content.

## Format Options

| Format | Output | Use Case |
|--------|---------|----------|
| `rich` | Formatted with colors, headers, metadata | Interactive use |
| `markdown` | Plain markdown text | Piping, automation, file output |

## Variable Substitution

- **Pattern**: `{variable_name}` in template files
- **Partial substitution**: Provided variables are replaced, others remain as placeholders
- **No variables required**: All commands work with zero to all variables
- **Smart detection**: Filters out markdown syntax (code blocks, etc.)

## Examples

### Basic Usage
```bash
# List available templates
gnosari prompts list

# View planning template
gnosari prompts view planning

# See required variables
gnosari prompts view planning variables
```

### Variable Substitution
```bash
# Partial substitution
gnosari prompts view planning --feature_name "search" --project "MyApp"

# Generate to stdout
gnosari prompts use planning "Create feature" --format markdown \
  --feature_name "file_search" --description "Advanced search tool"

# Create file
gnosari prompts create planning "./docs/search-plan.md" "Feature planning" \
  --feature_name "file_search" --feature_description "Advanced file search"
```

### Pipeline Usage
```bash
# Direct file output
gnosari prompts use planning "New feature" --format markdown \
  --feature_name "api_client" > ./planning/api-client.md

# Edit in VS Code
gnosari prompts view planning --format markdown | code -
```

## Template Structure

Templates are standard markdown files in `prompts/` directory:

```markdown
# {project_name} Implementation Plan

## Overview
Feature: {feature_name}
Description: {description}

## Implementation
- Create {component_type} component
- Add {feature_name} configuration
```

## Built-in Templates

### planning.md
Comprehensive feature implementation plan with 22 variables including:
- `feature_name`, `feature_description`
- `project`, `priority`, `technology`
- `component_type`, `integration_point`

## Error Handling

- **Missing template**: Shows available templates
- **Invalid path**: Creates directories automatically
- **Format errors**: Clear error messages with context

## Integration

Templates integrate with existing CLI workflows:
- Use with team configurations
- Generate planning documents
- Create structured content
- Automate documentation