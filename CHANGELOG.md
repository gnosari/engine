# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- **Reasoning Parameter for OpenAI Models**: Fixed streaming error "missing 'reasoning' item" when using reasoning_effort parameter
  - **Root Cause**: The `reasoning_effort` configuration parameter was not being properly converted to OpenAI's `reasoning` parameter in ModelSettings
  - **Fix**: Updated `AgentFactory` to properly handle reasoning configuration:
    - Only applies `reasoning` parameter to reasoning models (gpt-5)
    - Forces temperature=1 for reasoning models as required by OpenAI
    - Validates reasoning_effort values (minimal, low, medium, high)
    - Converts `reasoning_effort` config to `reasoning` ModelSettings parameter
  - **Result**: Resolves Error 400 "Item was provided without its required 'reasoning' item" when using Documentation Specialist or other agents with reasoning_effort
  - **Files Changed**: `src/gnosari/engine/agents/agent_factory.py`

### Enhanced
- **Knowledge Management System**: Completely redesigned knowledge base management to eliminate database conflicts and improve caching
  - **BREAKING**: Knowledge bases now require unique `id` field in YAML configuration (no fallback to name)
  - **Database Isolation**: Each knowledge base now uses unique ChromaDB collection named `gnosari_{knowledge_id}`
  - **Configuration Hash Caching**: Implemented hash-based cache system in `.cache/knowledge/` directory
    - Tracks loaded knowledge bases by configuration hash to detect changes
    - Skips reloading unchanged knowledge sources automatically  
    - Cache invalidation when knowledge configuration changes
    - Cache statistics and management utilities
  - **Loading Indicators**: Added "Loading Knowledge {name}..." indicators in CLI output
  - **Validation**: Enforced required fields validation for `id`, `name`, and `type` in knowledge configurations
  - **Error Prevention**: Eliminated "Collection embedchain_store already exists" errors by using unique collection names
  - **Cache Management**: Added cache statistics, invalidation, and cleanup methods to KnowledgeManager
  - **SOLID Principles**: Knowledge cache system follows Single Responsibility Principle with separate concerns

- **Generic Cache System**: Created enterprise-grade caching framework following SOLID principles
  - **NEW**: `src/gnosari/core/cache/` - Comprehensive cache system for all modules
  - **Type Safety**: Generic cache manager with full TypeScript-style type safety using Python generics
  - **Pluggable Architecture**: Abstract interfaces for hash strategies, storage backends, and validators
  - **Multiple Hash Strategies**: SHA256, MD5, Content, and Combined hash strategies
  - **Flexible Storage**: JSON file storage with extensible backend architecture
  - **Rich Metadata**: Comprehensive status tracking, timestamps, expiration, and custom metadata
  - **Cache Validation**: Hash-based validation with automatic invalidation on configuration changes
  - **Resource Management**: Max entries enforcement, automatic cleanup, and TTL support
  - **Direct Integration**: Knowledge system uses generic cache directly (no compatibility layer)
  - **Enterprise Features**: Cache statistics, monitoring, persistence, and management utilities
  - **SOLID Design**: 
    - Single Responsibility: Separate classes for entries, managers, storage, validation
    - Open/Closed: Extensible via interfaces without modifying existing code
    - Liskov Substitution: All implementations are interchangeable
    - Interface Segregation: Focused interfaces for specific concerns
    - Dependency Inversion: Depends on abstractions, not concretions
  - **Clean Architecture**: Removed knowledge-specific cache layer for direct generic cache usage

### Fixed
- **Delegation Tool Circular References**: Completely redesigned async tool execution
  - Fixed datetime serialization in BaseMessage.to_dict() method
  - **BREAKING**: Removed complex AsyncWrapper system entirely
  - Added original_config storage to Team class for clean team reconstruction
  - Tools now handle async execution directly via `get_async_tool()` method
  - Delegation tool sends queue messages directly without circular references
  - Simplified tool registry to avoid modifying original tool configurations
- **KnowledgeManager TypeError**: Fixed "object of type 'KnowledgeManager' has no len()" error
  - **Root Cause**: AgentFactory was incorrectly overwriting agent_tools list with KnowledgeManager object
  - **Fix**: Removed faulty logic that replaced agent_tools with knowledge_manager (agent_factory.py:173)
  - **Defensive Fix**: Added type checking in ToolResolver._should_add_knowledge_tool() to handle invalid knowledge config
  - Knowledge tools are now handled automatically by tool_resolver based on agent_config['knowledge']
- **AgentFactory Code Quality Improvements**: Refactored following SOLID principles
  - **Single Responsibility**: Extracted methods for specific concerns (_build_agent_context, _get_knowledge_descriptions, _format_prompt_components)
  - **DRY Principle**: Removed redundant knowledge manager access patterns with _has_knowledge_manager() helper
  - **Error Handling**: Added comprehensive validation and error handling for agent creation
  - **Input Validation**: Added validation for agent names, instructions, model, and temperature parameters
  - **Better Maintainability**: Simplified complex methods and improved readability

### Added
- **TeamContext System**: Added context object to pass team data to tools
  - Created `TeamContext` dataclass with original_config and session data
  - Updated all Runner.run methods to pass TeamContext via context parameter
  - Tools can now access clean original_config without circular references
  - Context available in both sync and async tool execution modes

- **AsyncTool Interface**: Added explicit interface for async-capable tools
  - Created `AsyncTool` and `SyncTool` interfaces for clear tool capability definition
  - Tools implementing `AsyncTool` explicitly support queue-based async execution
  - Added `supports_async_execution()` and `get_async_metadata()` methods to interface
  - DelegateAgentTool now implements AsyncTool interface with async configuration metadata
  - Tool registry uses interface checking instead of hasattr() for better type safety
  - Queue consumer specifically processes AsyncTool implementations
  - **DRY PRINCIPLE**: Moved common async functionality to AsyncTool base class:
    - `serialize_context()` - Context serialization for queue messages
    - `send_async_message()` - Standard queue message sending
    - `format_async_response()` - Consistent async response formatting
  - Eliminated code duplication when creating new async-capable tools

### Fixed (continued)
- **Queue Message Handling**: Fixed tool initialization in async mode
  - Removed team_config from DelegateAgentTool constructor parameters
  - Fixed queue consumer to properly reconstruct teams from clean config data
  - Simplified team reconstruction using temporary YAML approach
  - Fixed TypeError when initializing delegation tools in worker processes

### Changed
- **BREAKING: Removed Legacy Tool Support**: Eliminated all backward compatibility layers
  - **REMOVED**: `LegacyToolAdapter`, `OpenAISDKToolAdapter`, `AsyncToolAdapter` classes
  - **REMOVED**: `_adapt_legacy_tool()` method and legacy tool detection
  - **REQUIREMENT**: All tools must now implement `AsyncTool` or `SyncTool` interfaces
  - **SIMPLIFIED**: Tool registry no longer attempts automatic adaptation of old tools
  - **CLEANER**: Eliminated complex adapter pattern in favor of direct interface implementation
  - **UPDATED**: All builtin tools now implement `SyncTool` interface (except delegation which uses `AsyncTool`)
  - **CONSISTENT**: Uniform interface implementation across all builtin tools

- **Delegation Tool Architecture**: Refactored following SOLID principles
  - **BREAKING**: Removed `set_team_dependencies` method and related setup
  - **REFACTORING**: Extracted specialized classes following Single Responsibility Principle:
    - `DelegationResult`: Handles result processing without isinstance checks
    - `ContextSerializer`: Manages context serialization for queue messages
  - Eliminated `isinstance` checks in favor of duck typing and composition
  - Split large methods into focused, single-purpose methods
  - Tools now access team config via TeamContext instead of storing team references
  - DelegateAgentTool builds team from original_config when needed, avoiding circular references
  - Removed complex team reconstruction and cleanup methods
  - Updated TeamContext to include team object reference for direct access
  - Delegation tools no longer maintain internal team/team_executor state

- **Queue Tool Execution**: Enhanced context serialization and handling
  - Replaced custom MockContext with native OpenAI RunContextWrapper
  - **OPTIMIZATION**: Delegation tools now serialize RunContextWrapper directly instead of reconstructing
  - **STRICT VALIDATION**: All tools now require proper context_wrapper data and fail fast if missing
  - **CONSISTENCY**: Removed tool-specific logic from queue consumer - all tools now work the same way
  - Eliminated special handling for delegate_agent tool in favor of consistent context_wrapper approach
  - **SIMPLIFICATION**: Removed conditional tool interface checks (hasattr) since all tools use FunctionTool with on_invoke_tool
  - Simplified _execute_tool method to assume consistent FunctionTool interface across all tools
  - Queue consumer creates RunContextWrapper with TeamContext for consistent tool interface
  - Both FunctionTool and BaseTool interfaces receive same RunContextWrapper format
  - Removed redundant session_id duplication in queue messages (available in context)
  - Removed unnecessary `tool_init_args` parameter from queue messages
  - Enhanced context creation with multi-level fallback logic for maximum compatibility
  - Tools accepting context parameter receive RunContextWrapper with TeamContext
  - Maintains backwards compatibility for tools without context parameter
  - Added debugging for async delegation context availability

### Removed
- **Legacy Team Dependencies**: Cleaned up outdated team dependency management
  - Removed `set_team_dependencies` function and all references
  - Removed `_reconstruct_team_for_async` and `_cleanup_team_resources` methods
  - Removed AsyncWrapper system entirely
  - Removed team_config parameter from DelegateAgentTool constructor
  - Simplified queue consumer to use clean context-based approach

- **Queue Debugging**: Added detailed debugging for circular reference detection in tool execution messages
  - Added JSON serialization test before sending to Celery queue 
  - Added field-by-field analysis to identify which message fields contain circular references
  - Located in `send_tool_execution_message()` in `queue/consumers/tool_execution.py:597`

### Added
- **Celery Queue System**: Introduced robust async job processing framework
  - Added Redis service to docker-compose.yml for message broker and result backend
  - Implemented Celery configuration with best practices (`CeleryConfig` class)
  - Created base classes `BaseMessage` and `BaseConsumer` following Single Responsibility Principle
  - Added example message and consumer implementation (`ExampleMessage`, `ExampleConsumer`)
  - Integrated CLI worker command: `poetry run gnosari worker` with concurrency and queue options
  - Added comprehensive QUEUE.md documentation with patterns for creating messages and consumers
  - Dependencies: `celery[redis]` and `redis` added to pyproject.toml
  - Features: message validation with Pydantic, exponential backoff retry logic, type-safe serialization
- **Flower Monitoring UI**: Added Celery task monitoring and management interface

### Changed
- **MAJOR REFACTORING: TeamBuilder SOLID Compliance**: Refactored the monolithic TeamBuilder class following SOLID principles
  - **Single Responsibility Principle**: Split ~950 line TeamBuilder into focused components:
    - `ConfigLoader`: Handles YAML loading and environment variable substitution  
    - `EnvironmentVariableSubstitutor`: Manages environment variable replacement logic
    - `ConfigValidator`: Validates team configuration structure and references
    - `MCPServerFactory`: Creates different types of MCP servers (SSE, HTTP, Stdio)
    - `MCPConnectionManager`: Manages MCP server connections and lifecycle
    - `MCPServerRegistry`: Tracks server references and ID-to-name mappings
    - `KnowledgeLoader`: Handles knowledge base initialization and data loading
    - `KnowledgeRegistry`: Manages knowledge base descriptions and metadata
    - `AgentFactory`: Creates OpenAI SDK agents with proper configuration
    - `ToolResolver`: Resolves and prepares tools for agent creation
    - `HandoffConfigurator`: Configures handoffs between agents
  - **Open/Closed Principle**: Easy to extend with new MCP connection types, tool types, etc.
  - **Dependency Inversion Principle**: Uses dependency injection for better testability
  - **Interface Segregation**: Smaller, focused interfaces instead of monolithic classes
  - **Maintainability**: Reduced main TeamBuilder from ~950 lines to ~200 lines
  - **Testability**: Isolated components can be independently unit tested
  - **Code Reuse**: Eliminated duplication and extracted common patterns
  - **Backward Compatibility**: All existing imports and APIs remain unchanged

### Fixed
- **Async Tool Context Passing**: Fixed session ID and agent ID extraction in async tool execution
  - Enhanced `AsyncToolWrapper._extract_context_data()` to properly extract session and agent information from `RunContextWrapper`
  - Added comprehensive context extraction from inner context objects, dictionaries, and fallbacks
  - Fixed `ToolExecutionConsumer` to properly wrap mock context in `RunContextWrapper` for OpenAI Agents SDK compatibility
  - Enhanced `AgentFactory` to inject agent identification (`agent_id`, `agent_name`) into agent context
  - Updated async delegation tool creation to pass session context properly
  - **Issue**: Previously async tools showed "Agent: Unknown" and "Session: Unknown" in logs
  - **Fix**: Now properly extracts and passes session_id and agent_id to async tool execution queue
- **Enhanced Session ID Propagation**: Improved session context passing throughout the system
  - Added `session_id` parameter to `TeamBuilder.__init__()` for proper context propagation
  - Enhanced `AgentFactory` to inject session_id into agent context during creation
  - Updated CLI to pass session_id to TeamBuilder during team building
  - Updated API service (`gnosari_chat_service.py`) to pass session_id to all TeamBuilder instances
  - **Benefit**: Session information now flows from CLI/API → TeamBuilder → AgentFactory → Agent Context → Tools
  - **Result**: Async tools will now correctly display session_id and agent_id in logs and execution tracking
- **Complete Session ID Flow**: Fixed final session_id propagation to AsyncToolWrapper instantiation
  - Updated `ToolResolver.__init__()` to accept session_id parameter from TeamBuilder
  - Modified `TeamBuilder._ensure_agent_components()` to pass session_id when creating ToolResolver
  - Fixed async delegation tool creation in `ToolResolver._create_async_delegation_tool()` to use `self.session_id`
  - **Issue**: AsyncToolWrapper was being created with session_id=None in async delegation tools
  - **Fix**: Now properly passes session_id from TeamBuilder → AgentFactory → ToolResolver → AsyncToolWrapper
  - **Result**: Complete session context flow ensures proper identification in all async tool executions
- **Async Delegation Session Context**: Fixed session_id propagation in async delegation team reconstruction
  - Modified `DelegateAgentTool._reconstruct_team_for_async()` to accept session_id parameter
  - Enhanced `DelegateAgentTool._run_delegate_agent()` to extract session_id from RunContextWrapper
  - Added comprehensive session_id extraction from context (direct attribute, inner context, dictionary format)
  - **Issue**: Async delegation showed "No session_id provided - running without persistent memory"
  - **Fix**: Now properly extracts session_id from async execution context and passes to TeamBuilder during reconstruction
  - **Result**: Async delegation maintains session context and enables persistent conversation memory
- **Critical Fix**: Pass session_id to agent execution in async delegation
  - Updated `DelegateAgentTool._run_delegate_agent()` to pass extracted session_id to `run_agent_until_done_async()`
  - **Issue**: Session context was extracted but not passed to the actual agent execution method
  - **Fix**: Now properly calls `run_agent_until_done_async(agent, message, session_id=session_id)`
  - **Result**: Async delegation now has complete session context flow and eliminates "No session_id provided" messages
  - Added `flower` package dependency (v2.0.0+) to pyproject.toml
  - Created Flower service in docker-compose.yml with basic authentication
  - Integrated CLI flower command: `poetry run gnosari flower` with port and auth options
  - Environment variables for Redis broker configuration in .env.example
  - Web UI available at http://localhost:5555 with admin:admin default credentials
- **Worker Management Commands**: Enhanced worker CLI with process management capabilities
  - Added `psutil` dependency (v6.1.0+) for process monitoring and control
  - Enhanced `poetry run gnosari worker` command with action support: start, stop, restart, status
  - Worker status command shows running worker PIDs and process information
  - Worker stop command gracefully terminates all running Celery workers with fallback to kill
  - Worker restart command stops existing workers and starts new ones
  - Automatic process discovery and management for all Celery worker processes
- **Comprehensive Queue Documentation**: Added complete documentation section for async processing
  - Created new "Queues & Async Processing" documentation section in docs/docs/queues/
  - Added intro.md with architecture overview and getting started guide
  - Added async-configuration.md with detailed tool and delegation async mode examples
  - Added cli-commands.md with comprehensive CLI reference for worker management
  - Added worker-management.md with advanced scaling, monitoring, and production deployment guidance
  - Documentation covers configuration, best practices, troubleshooting, and production deployment strategies
- **Session Context Support for Async Tools**: Enhanced async tool execution with session context management
  - Updated `AsyncToolWrapper` to automatically extract and pass session_id from runtime context
  - Modified tool execution messages to include session_id and agent_id for conversation continuity
  - Enhanced `ToolExecutionConsumer` to properly handle session context in async processing
  - Session context now flows through the entire async execution pipeline
  - Enables async tools to add messages back to conversations once task processing is complete
  - Improved async execution feedback with session and agent information in status messages
- **Comprehensive Logging for Tool Execution Consumer**: Added detailed debug, warning, and error logging
  - Enhanced `ToolExecutionConsumer` with structured logging using Python's logging module
  - Added DEBUG level logging for tool instantiation, context creation, and execution flow
  - Added INFO level logging for task lifecycle events and successful completions
  - Added WARNING level logging for retry attempts and dependency issues
  - Added ERROR level logging for failures with full exception details and stack traces
  - Improved `send_tool_execution_message` function with detailed message sending logs
  - All logging respects project-wide LOG_LEVEL environment variable configuration
- **Async Delegation Team Context Reconstruction**: Implemented complete team reconstruction for async delegation
  - Enhanced `ToolExecutionConsumer` to reconstruct team dependencies using existing `TeamBuilder` class
  - Team context now properly serialized and passed through queue messages for async delegation
  - Reuses existing `TeamBuilder.build_team()` and `TeamRunner` methods without code duplication
  - Async delegation tools can now reconstruct full team context from serialized configuration data
  - Added comprehensive error handling and logging for team reconstruction process
  - Created example configuration `examples/async_delegation_test.yaml` to demonstrate async delegation
  - Resolves "Team not available for delegation" errors by properly reconstructing team context
- **Async Tool Execution**: Enhanced all builtin tools with optional async execution capability
  - Created `AsyncToolWrapper` for transparent async/sync tool execution
  - Generic `ToolExecutionConsumer` can execute any builtin tool asynchronously
  - Dynamic tool instantiation from queue messages (module, class, args)
  - Tool configuration supports `mode: async` parameter in YAML
  - Priority-based task processing with configurable queue names
- **Async Delegation**: Added async delegation functionality for agent coordination
  - Enhanced team builder to detect `mode: async` in delegation configuration
  - Automatic async wrapper creation for delegation tools when async mode specified
  - Queue-based delegation allows non-blocking agent coordination
  - Updated documentation_keeper.yaml example with async delegation
  - Maintains backward compatibility with existing sync delegation

### Added
- **Pull Team Configuration Command**: Added `gnosari pull` command to pull team configurations from the Gnosari API
  - Fetches team configuration by identifier from GET `/api/v1/teams/{identifier}/pull` endpoint
  - Transforms JSON response into proper YAML structure preserving team hierarchy
  - Saves the configuration as a YAML file named `{identifier}.yaml`
  - Supports custom API URL with `--api-url` parameter
  - Uses same authentication mechanism as push command (GNOSARI_API_KEY environment variable)
  - Provides detailed error handling for common HTTP status codes (404, 401, 403)
  - Properly structures knowledge bases, tools, and agents in YAML format
  - Usage: `poetry run gnosari pull "team_identifier"`
  - Added documentation to CLAUDE.md with usage examples
- **Kubernetes Helm Chart for Documentation Deployment**
  - Created complete Helm chart in `docs/chart/` directory for deploying Docusaurus documentation
  - Added Chart.yaml with project metadata and version information
  - Created comprehensive values.yaml with configurable deployment parameters (image, service, ingress, autoscaling, resources)
  - Implemented Kubernetes deployment template with health checks and probes
  - Added service template for internal cluster communication
  - Created ingress template with TLS support and compatibility across multiple Kubernetes versions
  - Implemented ServiceAccount template with optional creation
  - Added HorizontalPodAutoscaler (HPA) template for automatic CPU/memory-based scaling
  - Created helper template functions (_helpers.tpl) for consistent naming and labeling
  - Comprehensive deployment documentation in `docs/DEPLOYMENT.md` with step-by-step instructions, production examples, troubleshooting guide, and security considerations

### Fixed
- **Knowledge Base Query by ID**: Fixed issue where knowledge query tool couldn't find knowledge bases when agents referenced them by ID instead of name
  - Modified TeamBuilder to create knowledge bases using their ID as the primary key (fallback to name if no ID provided)
  - Simplified knowledge base resolution by using IDs consistently throughout the system
  - Removed unnecessary ID-to-name mapping complexity
  - Knowledge bases are now stored and queried by ID, resolving "Knowledge base 'gnosari_framework_documentation' not found" errors
- **Embedchain Search Response Handling**: Fixed "sequence item 0: expected str instance, list found" error when using embedchain.search()
  - Updated EmbedchainKnowledgeBase.query() method to handle different response formats from embedchain
  - Added support for string responses, list of strings, list of dictionaries, and other data types
  - Enhanced logging to debug response types and formats
  - Properly converts all response formats to KnowledgeResult objects
- **Knowledge Module Logging**: Fixed issue where knowledge module logs weren't appearing in output
  - Added 'gnosari.knowledge' to the list of configured loggers in CLI setup_logging()
  - Knowledge base operations now properly log debug, info, and error messages
  - Embedchain adapter logging now visible for troubleshooting knowledge base issues
- **Knowledge Base ID Resolution in TeamBuilder**: Fixed issue where agents referencing knowledge bases by ID couldn't find the knowledge base during team building
  - Enhanced TeamBuilder to support both name and ID-based knowledge base lookups
  - Added `knowledge_id_to_name` mapping in TeamBuilder initialization
  - Updated agent building logic to resolve knowledge references by ID to actual names before creating agents
  - Knowledge bases can now be properly referenced by either name or ID in agent configurations
  - Example: Knowledge base with `name: "Neomanex Website Knowledge"` and `id: "neomanex_knowledge_base"` can be referenced as `neomanex_knowledge_base` in agent knowledge list

- **MCP Server ID Resolution in TeamBuilder**: Fixed issue where agents referencing MCP servers by ID couldn't find the server during team building
  - Enhanced TeamBuilder to support both name and ID-based MCP server lookups
  - Added `mcp_server_id_to_name` mapping in TeamBuilder initialization
  - Updated `_get_mcp_server_names` method to resolve MCP server references by ID to actual names before filtering
  - MCP servers can now be properly referenced by either name or ID in agent configurations
  - Example: MCP server with `name: "Slack Tool"` and `id: "slack_tool"` can be referenced as `slack_tool` in agent mcp_servers list

### Changed
- **BREAKING: MCP Servers as Regular Tools**: MCP servers can now be included directly in the agent's `tools` array instead of requiring a separate `mcp_servers` field
  - Enhanced TeamBuilder with `_is_mcp_tool()` method to automatically detect MCP servers in tools configuration
  - Updated agent building logic to separate regular tools from MCP tools during processing
  - MCP tools are automatically identified by presence of `url` or `command` fields in tool configuration
  - Backward compatibility maintained: existing `mcp_servers` field still supported
  - Example: `tools: [website_tool, file_tool, slack_tool, playwright_tool]` now works seamlessly
  - Simplifies agent configuration by using a single `tools` array for all tool types

### Added
- **Built-in Tools Examples**: Added comprehensive example files demonstrating all built-in tools
  - `examples/builtin_tools_showcase.yaml`: Multi-agent team showcasing API requests, file operations, bash operations, and knowledge queries
  - `examples/builtin_tools_demo.yaml`: Single-agent demonstration of all four built-in tools with practical examples
  - Examples show proper tool configuration with IDs, parameters, and real-world usage patterns
- **Enhanced Neomanex Demo**: Updated `examples/neomanex_demo.yaml` with comprehensive tool integration
  - Added Website Content Fetcher and File Manager tools
  - Implemented proper ID structure with user-friendly names and computer-friendly IDs
  - Added descriptions to all components (team, agents, tools, knowledge bases)
  - Demonstrates best practices for team configuration structure

### Changed
- **Tool Organization**: Consolidated all tools into `src/gnosari/tools/builtin/` directory
  - Moved `interactive_bash_operations.py`, `mysql_query.py`, `website_content.py` to builtin directory
  - Removed duplicate tools and compatibility modules since builtin tools are automatically available
  - Updated imports in cleanup manager to use new builtin paths
  - All tools now accessible through unified `from gnosari.tools.builtin import ToolName` import pattern

### Fixed
- **Tool ID Resolution in TeamBuilder**: Fixed issue where agents referencing tools by ID (e.g., `file_ops_2`) couldn't find the tool during team building
  - Enhanced ToolRegistry to support both name and ID-based lookups
  - Updated TeamBuilder to use registry directly for tool resolution instead of relying on `list_available_tools()`
  - Tools can now be properly registered with an `id` field and referenced by either name or ID in agent configurations
  - Example: Tool with `name: file_ops` and `id: file_ops_2` can be referenced as `file_ops_2` in agent tools list

### Changed
- **BREAKING**: Team configuration field renamed from `identifier` to `id` for consistency
  - CLI now expects `id` field instead of `identifier` in team YAML configurations
  - Error messages updated to reference `id` field
  - Console output now displays "Team ID" instead of "Team identifier"
  - API backend already supported `id` field through JsonToDatabaseConverter

### Added
- Enhanced `examples/multiagent_handoff_delegation.yaml` with proper field structure:
  - Added `id` field to team level (`multiagent_handoff_delegation_team`)
  - Added `id` fields to all agents (`coordinator_agent`, `alice_agent`, `bob_agent`)
  - Added `id` field to tools (`delegate_agent_tool`)
  - Added descriptive `description` fields for all agents and tools
  - Updated agent references in delegation and handoff configurations to use agent IDs

### Technical Details
- Updated `src/gnosari/cli.py` in `push_team_config()` function:
  - Line 64-66: Changed validation from `identifier` to `id`
  - Line 70: Updated console output to display "Team ID"
- No changes required in python-api as it already handles `id` field correctly
- JSON payload sent to external Gnosari API includes the `id` field as expected
- Tools require `id` fields for proper API compatibility (JsonToDatabaseConverter skips tools without IDs)# Fix environment variable substitution in TeamBuilder

## Changes Made

### Enhanced Environment Variable Substitution in `src/gnosari/engine/builder.py`

1. **Added comprehensive type conversion**: The `_substitute_env_variables` method now automatically converts string values to appropriate Python types:
   - Boolean values: `true`/`false` → Python `True`/`False`
   - Integer values: `123` → Python `int`
   - Float values: `0.2` → Python `float`
   - String values: remain as strings

2. **Enhanced debugging**: Added debug logging to track environment variable processing and substitution.

3. **Fixed temperature parsing**: Environment variables like `${MANAGER_TEMP:0.2}` now properly resolve to float values instead of remaining as strings.

## Example Usage

YAML configuration can now use environment variables anywhere:

```yaml
agents:
  - name: "Manager"
    model: "${MANAGER_MODEL:gpt-4o}"
    temperature: ${MANAGER_TEMP:0.2}
    orchestrator: ${IS_ORCHESTRATOR:true}
    max_turns: ${MAX_TURNS:10}
```

These will be properly substituted and converted to appropriate types:
- `temperature: 0.2` (float)
- `orchestrator: true` (boolean) 
- `max_turns: 10` (integer)
- `model: "gpt-4o"` (string)

## Impact

- Fixes the ModelSettings temperature validation error
- Enables environment variable usage throughout YAML configurations
- Maintains type safety and proper data conversion
- Adds better debugging for troubleshooting env var issues

## Fixed Environment Variable Substitution in TeamBuilder

### Problem
Environment variables like `${MANAGER_TEMP:0.2}` in YAML configs were not being substituted properly, causing Pydantic validation errors when values remained as literal strings instead of being converted to proper types.

### Root Cause
The original implementation performed environment variable substitution **after** YAML parsing, which meant that YAML had already parsed numeric values as strings, and the recursive substitution couldn't properly convert them back to the correct types.

### Solution
Changed the approach to perform environment variable substitution **before** YAML parsing:

1. **Read raw YAML as string**: Load the YAML file content as a plain string
2. **Substitute environment variables**: Use regex to find and replace `${VAR_NAME:default}` patterns in the raw string
3. **Parse substituted YAML**: Use `yaml.safe_load()` on the string with variables already substituted

### Implementation Details
- Added `_substitute_env_variables_in_string()` method for string-level substitution
- Modified `load_team_config()` to use string substitution before YAML parsing
- Maintains all existing functionality and debug logging

### Result
✅ Environment variables like `${MANAGER_TEMP:0.2}` now correctly resolve to float `0.2`
✅ Fixes ModelSettings temperature validation errors
✅ Works with all data types: strings, numbers, booleans
✅ Maintains backward compatibility

### Example
```yaml
agents:
  - name: "Manager"
    model: "${MANAGER_MODEL:gpt-4o}"      # → "gpt-4o" (string)
    temperature: ${MANAGER_TEMP:0.2}        # → 0.2 (float)
    orchestrator: ${IS_ORCHESTRATOR:true}   # → true (boolean)
```

### Changed
- **BREAKING: Unified Agent Prompt System**: Refactored prompt generation following Single Responsibility Principle
  - **BREAKING**: Removed `build_orchestrator_system_prompt` and `build_specialized_agent_system_prompt` functions
  - **NEW**: Single `build_agent_system_prompt` function handles both orchestrator and specialized agents
  - **DRY Principle**: Eliminated code duplication between orchestrator and specialized agent prompts
  - **Cleaner Structure**: Unified prompt structure with better organization of collaboration, knowledge, and tool sections
  - **Concise Prompts**: Reduced verbose and redundant text in agent system prompts
  - **Better Context**: Improved collaboration instructions and knowledge base guidance
  - **Fixed Display Issues**: Resolved `\n\n\n\n` artifacts in prompt display output
  - **Updated Imports**: All imports now use `build_agent_system_prompt` instead of deprecated functions
  - **Markdown Formatting**: Agent prompts now use proper markdown formatting with headers, bold text, and structured sections
  - **Rich Markdown Display**: CLI `--show-prompts` now renders prompts as formatted markdown instead of plain text
  - **Removed Unnecessary Agent Lists**: Agents no longer see generic team member lists unless explicit delegation/handoff is configured
  - **Better Visual Hierarchy**: Clear H1 agent names, H2 section headers, and bold emphasis for important information
  - **Enhanced Tool Information**: Added "Available Tools" section to agent prompts showing tool names, IDs, and descriptions
  - **Tool Registry Integration**: Tools section now pulls information from tool registry with proper name, ID, and description formatting

### Removed
- **Unused Prompt Constants**: Removed unused prompt constants that were never referenced in the codebase
  - Removed `TOOL_EXECUTION_RESULT_PROMPT`, `TOOL_EXECUTION_ERROR_PROMPT`, `TOOL_NOT_AVAILABLE_PROMPT`
  - Removed `CONTINUE_PROCESSING_PROMPT`, `ORCHESTRATION_PLANNING_PROMPT`, `FEEDBACK_LOOP_PROMPT`
  - Cleaned up exports in `__init__.py` file
  - Reduced code clutter and improved maintainability
