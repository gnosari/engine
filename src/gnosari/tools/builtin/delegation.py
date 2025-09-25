"""
OpenAI Delegate Agent Tool - Clean implementation following SOLID principles
"""

import logging
import asyncio
from typing import Any, Dict
from pydantic import BaseModel, Field
from agents import RunContextWrapper, FunctionTool
from ...tools.interfaces import AsyncTool


class DelegateAgentArgs(BaseModel):
    """Arguments for the delegate agent tool."""
    target_agent: str = Field(..., description="Name of the agent to delegate the task to")
    message: str = Field(..., description="The message or task to delegate to the target agent")


class DelegationResult:
    """Encapsulates delegation result processing logic."""
    
    def __init__(self, raw_result: Any, target_agent: str):
        self.raw_result = raw_result
        self.target_agent = target_agent
        self.response_content = ""
        self.reasoning_content = ""
        self._extract_content()
    
    def _extract_content(self) -> None:
        """Extract response and reasoning content from raw result."""
        if not self._has_outputs():
            self.response_content = str(self.raw_result)
            return
        
        for output in self.raw_result["outputs"]:
            output_type = output.get("type", "")
            content = output.get("content", "")
            
            if output_type == "response":
                self.response_content += self._extract_text_content(content)
            elif output_type == "reasoning":
                self.reasoning_content += self._extract_text_content(content)
            elif output_type == "completion":
                self.response_content = self._extract_text_content(content)
    
    def _has_outputs(self) -> bool:
        """Check if result has outputs structure."""
        return (hasattr(self.raw_result, '__getitem__') and 
                "outputs" in self.raw_result)
    
    def _extract_text_content(self, content: Any) -> str:
        """Extract text content from various content types."""
        if hasattr(content, 'plain'):
            return content.plain
        return str(content)
    
    def get_formatted_response(self) -> str:
        """Get formatted response text."""
        if self.reasoning_content:
            return f"Reasoning: {self.reasoning_content}\nResponse: {self.response_content}"
        return self.response_content

class DelegateAgentTool(AsyncTool):
    """Configurable Delegate Agent Tool following SOLID principles."""
    
    def __init__(self):
        """Initialize the delegate agent tool."""
        # Call parent constructor first
        super().__init__(
            name="delegate_agent",
            description="Delegate a task to another agent in the team",
            input_schema=DelegateAgentArgs
        )
        self.logger = logging.getLogger(__name__)
        
        # Create the FunctionTool (sync by default)
        self.tool = FunctionTool(
            name=self.name,
            description=self.description,
            params_json_schema=DelegateAgentArgs.model_json_schema(),
            on_invoke_tool=self._run_delegate_agent
        )
        
    async def _run_delegate_agent(self, ctx: RunContextWrapper[Any], args: str) -> str:
        """Delegate a task to another agent in the team.
        
        Args:
            ctx: Run context wrapper
            args: JSON string containing DelegateAgentArgs
            
        Returns:
            Delegation result as string
        """
        try:
            parsed_args = DelegateAgentArgs.model_validate_json(args)
            session_id = ctx.context.session_id
            original_config = ctx.context.original_config

            self._log_delegation_start(parsed_args)
            
            if not original_config:
                return "Error: No team configuration available in context for delegation"
            
            # Build team and execute delegation
            team = await self._build_team(original_config, session_id)
            if not team:
                return "Error: Failed to build team for delegation"
            
            target_agent = team.get_agent(parsed_args.target_agent)
            if not target_agent:
                available_agents = ', '.join(team.list_agents())
                return f"Error: Agent '{parsed_args.target_agent}' not found in the team. Available agents (names and IDs): {available_agents}"
            
            # Execute delegation
            result = await self._execute_delegation(team, target_agent, parsed_args, session_id)
            
            # Process and format result
            delegation_result = DelegationResult(result, parsed_args.target_agent)
            self._log_delegation_success(delegation_result, parsed_args.target_agent)
            
            return delegation_result.get_formatted_response()
            
        except Exception as e:
            try:
                target_agent = parsed_args.target_agent
            except NameError:
                target_agent = 'unknown'
            
            error_msg = f"Failed to delegate to agent '{target_agent}': {str(e)}"
            self.logger.error(f"❌ DELEGATION FAILED - {error_msg}")
            return error_msg
    
    def _log_delegation_start(self, parsed_args: DelegateAgentArgs) -> None:
        """Log delegation start information."""
        message_preview = f"{parsed_args.message[:100]}{'...' if len(parsed_args.message) > 100 else ''}"
        self.logger.info(f"🤝 DELEGATION STARTED - Target Agent: '{parsed_args.target_agent}' | Message: '{message_preview}'")
    
    async def _build_team(self, original_config: Dict[str, Any], session_id: str) -> Any:
        """Build team from configuration using existing TeamBuilder."""
        try:
            from ...engine.builder import TeamBuilder
            
            builder = TeamBuilder(session_id=session_id)
            temp_config_path = self._create_temp_config(original_config)
            
            try:
                team = await asyncio.wait_for(
                    builder.build_team(temp_config_path),
                    timeout=120.0  # 2 minute timeout for team building
                )
                return team
            finally:
                self._cleanup_temp_file(temp_config_path)
                
        except asyncio.TimeoutError:
            self.logger.error("❌ Team building timed out after 2 minutes")
            return None
        except Exception as e:
            self.logger.error(f"❌ Team building failed: {str(e)}")
            return None
    
    def _create_temp_config(self, config: Dict[str, Any]) -> str:
        """Create temporary YAML configuration file."""
        import tempfile
        import yaml
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
            yaml.dump(config, temp_file)
            return temp_file.name
    
    def _cleanup_temp_file(self, file_path: str) -> None:
        """Clean up temporary configuration file."""
        import os
        
        if os.path.exists(file_path):
            os.unlink(file_path)
    
    async def _execute_delegation(self, team: Any, target_agent: Any, parsed_args: DelegateAgentArgs, session_id: str) -> Any:
        """Execute delegation to target agent."""
        self.logger.info(f"Contacting Agent {parsed_args.target_agent}")
        
        from ...engine.runner import TeamRunner
        team_executor = TeamRunner(team)
        
        return await asyncio.wait_for(
            team_executor.run_agent_until_done_async(
                target_agent, 
                parsed_args.message, 
                session_id=session_id
            ),
            timeout=300.0  # 5 minute timeout for delegation
        )
    
    def _log_delegation_success(self, delegation_result: DelegationResult, target_agent: str) -> None:
        """Log successful delegation information."""
        response_text = delegation_result.get_formatted_response()
        response_preview = response_text[:200] + "..." if len(response_text) > 200 else response_text
        
        self.logger.info(f"[{target_agent}] Response: {delegation_result.response_content}")
        if delegation_result.reasoning_content:
            self.logger.info(f"[{target_agent}] Reasoning: {delegation_result.reasoning_content}")
        
        self.logger.info(f"✅ DELEGATION SUCCESSFUL - Agent '{target_agent}' responded with {len(response_text)} characters")
        self.logger.info(f"📄 Response preview: {response_preview}")
    
    async def _run_delegate_agent_async(self, ctx: RunContextWrapper[Any], args: str) -> str:
        """Send delegation task to queue for async execution.
        
        Args:
            ctx: Run context wrapper
            args: JSON string containing DelegateAgentArgs
            
        Returns:
            Queue task submission result
        """
        try:
            import uuid
            
            parsed_args = DelegateAgentArgs.model_validate_json(args)
            session_id = ctx.context.session_id
            original_config = ctx.context.team.original_config

            if not original_config:
                self.logger.warning("No original_config found in context - delegation will fail")
            
            task_id = str(uuid.uuid4())
            
            message_id = self.send_async_message(
                task_id=task_id,
                tool_module='gnosari.tools.builtin.delegation',
                tool_class='DelegateAgentTool',
                tool_args=args,
                context=ctx
            )
            
            return self.format_async_response(task_id, message_id, parsed_args.target_agent, session_id)
            
        except Exception as e:
            error_msg = f"Failed to queue delegation task: {str(e)}"
            self.logger.error(f"❌ ASYNC DELEGATION FAILED - {error_msg}")
            return error_msg
    
# Removed _format_async_response - now available in AsyncTool base class
    
    def get_tool(self) -> FunctionTool:
        """Get the FunctionTool instance (sync version).
        
        Returns:
            FunctionTool instance
        """
        return self.tool
    
    def get_async_tool(self) -> FunctionTool:
        """Get the async FunctionTool instance that sends messages to queue.
        
        Returns:
            FunctionTool instance for async execution
        """
        return FunctionTool(
            name=self.name,
            description=f"{self.description} (Async execution via queue)",
            params_json_schema=DelegateAgentArgs.model_json_schema(),
            on_invoke_tool=self._run_delegate_agent_async
        )
    
    def supports_async_execution(self) -> bool:
        """Check if this tool supports async execution.
        
        Returns:
            bool: True since delegation tools support async execution
        """
        return True
    
    def get_async_metadata(self) -> Dict[str, Any]:
        """Get metadata for async execution configuration.
        
        Returns:
            Dict containing async execution settings for delegation
        """
        return {
            "priority": 5,  # Normal priority for delegation
            "timeout": 900,  # 15 minutes for delegation operations
            "max_retries": 2,  # Limited retries for delegation
            "retry_delay": 3
        }
