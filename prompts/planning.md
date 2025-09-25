# Gnosari AI Teams Feature Planning Template

## Feature Implementation Plan Template

Use this template to create comprehensive implementation plans for new features or bug fixes in the Gnosari AI Teams framework. Save the completed plan as `planning/{feature-name}.md`.

---

### Usage Instructions

Replace the placeholders with specific details for your feature/bug:

**Template Command:**
```
Write an implementation plan and save it in planning/{filename}.md for this feature: {feature_description}.
```

---

## Template Structure

### 1. Overview & Scope

**Feature:** {feature_description}

**Context:**
- **Project:** Gnosari AI Teams - Multi-agent orchestration framework using OpenAI Agents SDK
- **Technology Stack:** Python 3.11+, Poetry, Pydantic v2, OpenAI Agents SDK, AsyncIO
- **Architecture:** SOLID principles, dependency injection, async-first design
- **Relevant modules/files:** {files_or_components}

**Scope:**
- ✅ In Scope: [List what will be implemented]
- ❌ Out of Scope: [List what won't be included]
- 🔄 Future Considerations: [Items for later phases]

---

### 2. Architecture & SOLID Boundaries

**Current System Context:**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CLI Layer     │    │   Engine Layer   │    │  Provider Layer │
│   (cli.py)      │───▶│ (Team Builder/   │───▶│ (OpenAI, etc.)  │
│                 │    │  Team Runner)    │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Schemas Layer  │    │   Tools Layer    │    │ Knowledge Layer │
│  (Pydantic)     │    │  (BaseTool)      │    │ (Embedchain)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

**SOLID Application:**
- **S** - Single Responsibility: [How each component has one responsibility]
- **O** - Open/Closed: [Extension points for new features]
- **L** - Liskov Substitution: [Interface implementations]
- **I** - Interface Segregation: [Specific interfaces for different concerns]
- **D** - Dependency Inversion: [Abstractions over concrete implementations]

**Boundaries:**
- **Presentation:** CLI commands → Engine orchestration
- **Application:** Team building/running → Domain logic
- **Domain:** Agent coordination → Tool execution
- **Infrastructure:** Provider APIs, MCP servers, knowledge bases

---

### 3. Implementation Components

#### 3.1 Schema Definitions (Pydantic v2)
```python
# Example schemas needed
class {FeatureName}Config(BaseIOSchema):
    """Configuration schema for {feature_name}."""
    # Define fields with validation
    
class {FeatureName}Request(BaseIOSchema):
    """Request schema for {feature_name}."""
    # Define request structure
    
class {FeatureName}Response(BaseIOSchema):
    """Response schema for {feature_name}."""
    # Define response structure
```

#### 3.2 Tool Implementation
```python
class {FeatureName}Tool(BaseTool[{Input}Schema, {Output}Schema]):
    """Tool for {feature_description}."""
    
    def __init__(self):
        super().__init__(
            name="{tool_name}",
            description="{tool_description}",
            input_schema={Input}Schema,
            output_schema={Output}Schema
        )
    
    async def run(self, input_data: {Input}Schema) -> Any:
        # Implementation
        pass
```

#### 3.3 Team Configuration Extensions
```yaml
# Example YAML configuration additions
tools:
  - name: "{tool_name}"
    module: "gnosari.tools.builtin.{feature_name}"
    class: "{FeatureName}Tool"
    args:
      # Configuration parameters
```

#### 3.4 CLI Integration
```python
# CLI command additions to cli.py
@click.command()
@click.option('--{option}', help='{description}')
def {command_name}({parameters}):
    """Command for {feature_description}."""
    # Implementation
```

---

### 4. File Structure Changes

**New Files:**
```
src/gnosari/
├── tools/builtin/{feature_name}.py          # Tool implementation
├── schemas/{feature_name}.py                # Schema definitions
└── engine/{feature_area}/                  # Engine components (if needed)

planning/{feature_name}.md                   # This implementation plan
examples/{feature_name}_example.yaml        # Usage example
tests/test_{feature_name}.py                # Test suite
```

**Modified Files:**
```
src/gnosari/tools/builtin/__init__.py       # Export new tool
src/gnosari/schemas/__init__.py             # Export new schemas
src/gnosari/cli.py                          # Add CLI commands
CHANGELOG.md                                # Document changes
```

---

### 5. Data Flow & Integration Points

**Data Flow:**
1. {Step 1 description}
2. {Step 2 description}
3. {Step 3 description}

**Integration Points:**
- **Tool Registry:** Registration and discovery
- **Team Builder:** Tool inclusion in team configuration
- **Agent Factory:** Tool availability to agents
- **Session Context:** State management and context passing
- **MCP Integration:** External tool server communication (if applicable)

**State Management:**
```python
# Session context extensions
class SessionContext(BaseIOSchema):
    # Add new context fields if needed
    {feature_name}_state: Optional[Dict[str, Any]] = None
```

---

### 6. Error Handling & Edge Cases

**Error Scenarios:**
- [ ] Invalid configuration parameters
- [ ] Network/connectivity failures (if applicable)
- [ ] Resource unavailability
- [ ] Concurrent access conflicts
- [ ] Schema validation failures
- [ ] Permission/authentication errors

**Error Response Format:**
```python
class {FeatureName}Error(BaseException):
    """Custom exception for {feature_name} errors."""
    
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
```

**Edge Cases:**
- [ ] Empty/null inputs
- [ ] Large data sets
- [ ] Rate limiting
- [ ] Timeout scenarios
- [ ] Partial failures

---

### 7. Testing Strategy

#### 7.1 Unit Tests
```python
# test_{feature_name}.py
class Test{FeatureName}Tool:
    """Unit tests for {FeatureName}Tool."""
    
    @pytest.mark.asyncio
    async def test_{functionality}(self):
        # Test implementation
        pass
        
    @pytest.mark.asyncio
    async def test_error_handling(self):
        # Error scenario testing
        pass
```

#### 7.2 Integration Tests
- [ ] Tool registration and discovery
- [ ] Team configuration loading
- [ ] Agent execution with new tool
- [ ] Session context handling
- [ ] Error propagation

#### 7.3 Example Configuration
```yaml
# examples/{feature_name}_example.yaml
name: "{Feature Name} Demo Team"
description: "Demonstration of {feature_name} functionality"

tools:
  - name: "{tool_name}"
    module: "gnosari.tools.builtin.{feature_name}"
    class: "{FeatureName}Tool"
    args:
      # Example configuration

agents:
  - name: "Demo Agent"
    instructions: "Use the {tool_name} tool to {functionality}"
    tools: ["{tool_name}"]
    model: "gpt-4o"
    temperature: 0.1
    orchestrator: true
```

---

### 8. Performance & Monitoring

**Performance Considerations:**
- [ ] Async operation efficiency
- [ ] Memory usage optimization
- [ ] Concurrent execution handling
- [ ] Caching strategies (if applicable)
- [ ] Rate limiting compliance

**Monitoring:**
```python
# Logging integration
import logging
from gnosari.utils.logging import get_logger

logger = get_logger(__name__)

class {FeatureName}Tool(BaseTool):
    async def run(self, input_data):
        logger.info(f"Executing {self.name} with input: {input_data}")
        # Implementation with proper logging
```

**Metrics:**
- Execution time tracking
- Success/failure rates
- Resource utilization
- Error frequency

---

### 9. Security & Validation

**Input Validation:**
- [ ] Pydantic schema validation
- [ ] Type checking
- [ ] Range/format validation
- [ ] Sanitization requirements

**Security Measures:**
- [ ] Permission checks (if applicable)
- [ ] Data privacy compliance
- [ ] Secure credential handling
- [ ] Output sanitization

**Configuration Security:**
```python
# Secure configuration handling
class {FeatureName}Config(BaseIOSchema):
    secret_key: Optional[str] = Field(None, description="Secret key")
    
    @validator('secret_key')
    def validate_secret(cls, v):
        if v and len(v) < 16:
            raise ValueError('Secret key must be at least 16 characters')
        return v
```

---

### 10. Implementation Steps

#### Phase 1: Core Implementation
- [ ] 1.1 Create schema definitions in `schemas/{feature_name}.py`
- [ ] 1.2 Implement base tool class in `tools/builtin/{feature_name}.py`
- [ ] 1.3 Add tool registration to `tools/builtin/__init__.py`
- [ ] 1.4 Write unit tests for core functionality

#### Phase 2: Integration
- [ ] 2.1 Add CLI commands to `cli.py` (if needed)
- [ ] 2.2 Create example team configuration
- [ ] 2.3 Write integration tests
- [ ] 2.4 Update documentation

#### Phase 3: Validation
- [ ] 3.1 Run full test suite
- [ ] 3.2 Test with example configurations
- [ ] 3.3 Performance testing
- [ ] 3.4 Security review

#### Phase 4: Documentation
- [ ] 4.1 Update CHANGELOG.md
- [ ] 4.2 Create usage documentation
- [ ] 4.3 Update CLI help text
- [ ] 4.4 Example team configurations

---

### 11. Dependencies & Prerequisites

**Python Dependencies:**
```toml
# Add to pyproject.toml if needed
[tool.poetry.dependencies]
{dependency_name} = "{version}"
```

**External Services:**
- [ ] API endpoints (if applicable)
- [ ] Database requirements (if applicable)
- [ ] External tool servers (if applicable)

**Environment Variables:**
```bash
# Add to .env if needed
{FEATURE_NAME}_API_KEY=your_api_key
{FEATURE_NAME}_BASE_URL=https://api.service.com
```

---

### 12. Risks & Assumptions

**Technical Risks:**
- [ ] {Risk description} - **Mitigation:** {mitigation strategy}
- [ ] {Risk description} - **Mitigation:** {mitigation strategy}

**Business Risks:**
- [ ] {Risk description} - **Mitigation:** {mitigation strategy}

**Assumptions:**
- [ ] {Assumption description}
- [ ] {Assumption description}

**Dependencies:**
- [ ] External service availability
- [ ] API rate limits
- [ ] Team configuration compatibility

---

### 13. Success Criteria

**Functional Requirements:**
- [ ] Tool executes successfully with valid inputs
- [ ] Proper error handling for invalid inputs
- [ ] Integration with team configuration system
- [ ] CLI accessibility (if applicable)

**Non-Functional Requirements:**
- [ ] Response time < {X} seconds for typical operations
- [ ] Memory usage within acceptable limits
- [ ] Concurrent execution support
- [ ] Proper logging and monitoring

**User Experience:**
- [ ] Clear error messages
- [ ] Intuitive configuration options
- [ ] Comprehensive documentation
- [ ] Working examples

---

### 14. Rollback Plan

**Rollback Triggers:**
- Critical bugs in production
- Performance degradation
- Security vulnerabilities

**Rollback Steps:**
1. Disable feature in configuration
2. Remove from team configurations
3. Revert code changes
4. Update documentation

**Monitoring Post-Rollback:**
- [ ] Verify system stability
- [ ] Check for related issues
- [ ] Plan remediation

---

## Example Usage

### Create Implementation Plan
```bash
# Use this template to plan your feature
cp prompts/planning.md planning/my-new-feature.md
# Edit the file with your specific requirements
```

### Test Implementation
```bash
# Run with Poetry
poetry run gnosari --config "examples/my_feature_example.yaml" --message "Test the new feature" --stream
```

### Validate Integration
```bash
# Run tests
poetry run pytest tests/test_my_feature.py -v

# Run full test suite
poetry run pytest --cov=gnosari
```

---

**Notes:**
- Follow existing code patterns in the Gnosari codebase
- Use async/await consistently throughout the implementation
- Ensure proper error handling and logging
- Add comprehensive test coverage
- Update documentation and examples
- Consider backwards compatibility
- Review security implications