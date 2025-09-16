"""
Team Runner - Uses OpenAI Agents SDK Runner to execute teams.
"""

import asyncio
import logging
import numpy as np
from agents import Runner, RunConfig
from agents.voice import SingleAgentVoiceWorkflow, VoicePipeline, AudioInput
from typing import Optional, AsyncGenerator, Dict, Any

from .event_handlers import StreamEventHandler, ErrorHandler, MCPServerManager
from .team import Team


class TeamRunner:
    """Team runner using OpenAI Agents SDK Runner."""
    
    def __init__(self, team: Team):
        self.team = team
        self.logger = logging.getLogger(__name__)
        self._custom_session_provider = None
    
    def set_custom_session_provider(self, provider_factory):
        """Set a custom session provider factory function.
        
        Args:
            provider_factory: Function that takes session_id and returns a session provider
        """
        self._custom_session_provider = provider_factory
    
    async def _cleanup_interactive_bash_sessions(self):
        """Clean up all interactive bash sessions using global registry."""
        try:
            from ..tools.interactive_bash_operations import cleanup_all_global_interactive_bash_sessions
            await cleanup_all_global_interactive_bash_sessions()
        except Exception as e:
            self.logger.error(f"Error cleaning up interactive bash sessions: {e}")
    
    async def _cleanup_session(self, session):
        """Clean up session resources."""
        if session and hasattr(session, 'cleanup'):
            try:
                await session.cleanup()
            except Exception as e:
                self.logger.error(f"Error cleaning up session: {e}")
    
    def _get_session(self, session_id: Optional[str] = None, session_context: Optional[dict] = None):
        """Get session for persistence based on environment configuration."""
        if not session_id:
            self.logger.info("No session_id provided - running without persistent memory")
            return None
        
        # Use custom session provider if set
        if self._custom_session_provider:
            try:
                session = self._custom_session_provider(session_id)
                if session:
                    self.logger.info(f"Using custom session provider for session: {session_id}")
                    return session
            except Exception as e:
                self.logger.error(f"Custom session provider failed: {e}, falling back to default")
        
        # Always use GnosariContextSession for all providers
        try:
            from ..sessions import GnosariContextSession
            self.logger.info(f"Using Gnosari context session for session: {session_id}, context: {session_context}")
            return GnosariContextSession(session_id, session_context)
        except ImportError as e:
            self.logger.error(f"Failed to import GnosariContextSession: {e}")
            raise
    
    async def run_team_async(self, message: str, debug: bool = False, session_id: Optional[str] = None, session_context: Optional[dict] = None, max_turns: Optional[int] = None) -> Dict[str, Any]:
        """
        Run team asynchronously using OpenAI Agents SDK Runner.
        
        Args:
            message: User message
            debug: Whether to show debug info
            session_id: Session ID for conversation persistence
            
        Returns:
            Dict with outputs and completion status
        """
        if debug:
            self.logger.info(f"Contacting {self.team.orchestrator.name}")
        
        # Initialize MCP manager and connect servers
        mcp_manager = MCPServerManager()
        all_agents = [self.team.orchestrator] + list(self.team.workers.values())
        await mcp_manager.connect_servers(all_agents)

        session = None
        try:
            run_config = RunConfig(
                workflow_name=self.team.name or "Unknown Team",
            )
            
            session = self._get_session(session_id, session_context)
            if session:
                self.logger.info(f"Running team with persistent session: {session_id}")
            else:
                self.logger.info("Running team without session persistence")
            result = await Runner.run(self.team.orchestrator, input=message, run_config=run_config, session=session, max_turns=max_turns or self.team.max_turns)
            
            # Convert result to our expected format
            return {
                "outputs": [{"type": "completion", "content": result.final_output}],
                "agent_name": self.team.orchestrator.name,
                "is_done": True
            }
        finally:
            # Clean up interactive bash sessions first
            await self._cleanup_interactive_bash_sessions()
            # Clean up session resources
            await self._cleanup_session(session)
            # Clean up MCP servers after running
            await mcp_manager.cleanup_servers(all_agents)
    
    def run_team(self, message: str, debug: bool = False, session_id: Optional[str] = None, max_turns: Optional[int] = None) -> Dict[str, Any]:
        """Run team synchronously."""
        return asyncio.run(self.run_team_async(message, debug, session_id, max_turns=max_turns))
    
    async def run_team_stream(self, message: str, debug: bool = False, session_id: Optional[str] = None, session_context: Optional[dict] = None, max_turns: Optional[int] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Run team with streaming outputs using OpenAI Agents SDK.
        
        Args:
            message: User message
            debug: Whether to show debug info
            session_id: Session ID for conversation persistence
            
        Yields:
            Dict: Stream outputs (response chunks, tool calls, handoffs, etc.)
        """
        self.logger.info(f"Contacting {self.team.orchestrator.name}")
        
        # Initialize handlers
        current_agent = self.team.orchestrator.name
        event_handler = StreamEventHandler(current_agent)
        error_handler = ErrorHandler(current_agent)
        mcp_manager = MCPServerManager()
        
        # Connect MCP servers before running
        all_agents = [self.team.orchestrator] + list(self.team.workers.values())
        await mcp_manager.connect_servers(all_agents)

        session = None
        try:
            # Stream from orchestrator using OpenAI Agents SDK
            run_config = RunConfig(
                workflow_name=self.team.name or "Unknown Team",
            )
            
            session = self._get_session(session_id, session_context)
            if session:
                self.logger.info(f"Running team stream with persistent session: {session_id}")
            else:
                self.logger.info("Running team stream without session persistence")
            result = Runner.run_streamed(self.team.orchestrator, input=message, run_config=run_config, session=session, max_turns=max_turns or self.team.max_turns)
            
            self.logger.info("Starting to process streaming events...")
            
            async for event in result.stream_events():
                self.logger.debug(f"Received event: {event.type}. Item: {event}")
                
                # Use event handler to process events
                async for response in event_handler.handle_event(event):
                    # Update current agent if changed
                    if response.get('type') == 'agent_updated':
                        current_agent = response.get('agent_name', current_agent)
                        event_handler.current_agent = current_agent
                    yield response

            # Yield final completion
            yield {
                "type": "completion",
                "content": result.final_output,
                "output": result.final_output,
                "agent_name": current_agent,
                "is_done": True
            }
            
        except Exception as e:
            # Use simplified error handler
            error_response = error_handler.handle_error(e)
            yield error_response
            raise e
        finally:
            # Clean up interactive bash sessions first
            await self._cleanup_interactive_bash_sessions()
            # Clean up session resources
            await self._cleanup_session(session)
            # Clean up MCP servers after streaming is complete
            await mcp_manager.cleanup_servers(all_agents)
    
    async def run_agent_until_done_async(self, agent, message: str, session_id: Optional[str] = None, session_context: Optional[dict] = None, max_turns: Optional[int] = None) -> Dict[str, Any]:
        """
        Run a specific agent until completion.
        
        Args:
            agent: The agent to run
            message: Message to send
            session_id: Session ID for conversation persistence
            
        Returns:
            Dict with agent outputs
        """
        session = self._get_session(session_id, session_context)
        if session:
            self.logger.info(f"Running agent '{agent.name}' with persistent session: {session_id}")
        else:
            self.logger.info(f"Running agent '{agent.name}' without session persistence")

        mcp_manager = MCPServerManager()
        await mcp_manager.connect_servers([agent])

        try:
            effective_max_turns = max_turns or self.team.max_turns
            run_config = RunConfig() if effective_max_turns else None
            result = await Runner.run(agent, input=message, session=session, run_config=run_config, max_turns=effective_max_turns)
            
            return {
                "outputs": [{"type": "completion", "content": result.final_output}],
                "agent_name": agent.name,
                "is_done": True
            }
        finally:
            # Clean up interactive bash sessions first
            await self._cleanup_interactive_bash_sessions()
            # Clean up session resources
            await self._cleanup_session(session)
            # Clean up MCP servers after running
            await mcp_manager.cleanup_servers([agent])
    
    async def run_single_agent_stream(self, agent_name: str, message: str, debug: bool = False, session_id: Optional[str] = None, session_context: Optional[dict] = None, max_turns: Optional[int] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Run a specific agent with streaming outputs using OpenAI Agents SDK.
        
        Args:
            agent_name: Name of the agent to run
            message: User message
            debug: Whether to show debug info
            session_id: Session ID for conversation persistence
            
        Yields:
            Dict: Stream outputs (response chunks, tool calls, etc.)
        """
        # Get the target agent
        target_agent = self.team.get_agent(agent_name)
        if not target_agent:
            yield {
                "type": "error",
                "content": f"Agent '{agent_name}' not found in team configuration"
            }
            return
        
        self.logger.info(f"Executing single agent: {agent_name}")
        
        # Initialize handlers
        from .event_handlers import StreamEventHandler, ErrorHandler, MCPServerManager
        event_handler = StreamEventHandler(agent_name)
        error_handler = ErrorHandler(agent_name)
        mcp_manager = MCPServerManager()
        
        # Connect MCP servers for the target agent
        await mcp_manager.connect_servers([target_agent])
        
        session = None
        try:
            # Stream from the target agent using OpenAI Agents SDK
            run_config = RunConfig(
                workflow_name=agent_name,
            )

            session = self._get_session(session_id, session_context)
            if session:
                self.logger.info(f"Running single agent '{agent_name}' stream with persistent session: {session_id}")
            else:
                self.logger.info(f"Running single agent '{agent_name}' stream without session persistence")
            result = Runner.run_streamed(target_agent, input=message, run_config=run_config, session=session, max_turns=max_turns or self.team.max_turns)
            
            self.logger.info(f"Starting to process streaming events for agent: {agent_name}")
            
            async for event in result.stream_events():
                self.logger.debug(f"Received event: {event.type}")
                
                # Use event handler to process events
                async for response in event_handler.handle_event(event):
                    yield response

            # Yield final completion
            yield {
                "type": "completion",
                "content": result.final_output,
                "output": result.final_output,
                "agent_name": agent_name,
                "is_done": True
            }
            
        except Exception as e:
            self.logger.error(f"EXCEPTION occurred!!!! : {e}")
            # Use error handler
            error_response = error_handler.handle_error(e)
            yield error_response
            raise e
        finally:
            # Clean up interactive bash sessions first
            await self._cleanup_interactive_bash_sessions()
            # Clean up session resources
            await self._cleanup_session(session)
            # Clean up MCP servers
            await mcp_manager.cleanup_servers([target_agent])
    
    async def run_team_voice_stream(self, audio_buffer: np.ndarray, debug: bool = False, session_id: Optional[str] = None, session_context: Optional[dict] = None, max_turns: Optional[int] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Run team with voice input and streaming audio/text outputs.
        
        Args:
            audio_buffer: NumPy array of audio samples (int16, 24kHz sample rate)
            debug: Whether to show debug info
            session_id: Session ID for conversation persistence
            
        Yields:
            Dict: Stream outputs including voice_stream_event_audio and text responses
        """
        self.logger.info(f"Starting voice processing with {self.team.orchestrator.name}")
        
        # Initialize MCP manager and connect servers
        mcp_manager = MCPServerManager()
        all_agents = [self.team.orchestrator] + list(self.team.workers.values())
        await mcp_manager.connect_servers(all_agents)
        
        
        session = None
        try:
            # Create voice pipeline with the orchestrator
            voice_workflow = SingleAgentVoiceWorkflow(self.team.orchestrator)
            voice_pipeline = VoicePipeline(workflow=voice_workflow)
            
            # Create audio input from buffer
            audio_input = AudioInput(buffer=audio_buffer)
            
            # Get session for persistence
            session = self._get_session(session_id, session_context)
            if session:
                self.logger.info(f"Running voice team with persistent session: {session_id}")
            else:
                self.logger.info("Running voice team without session persistence")
            
            # Run the voice pipeline
            result = await voice_pipeline.run(audio_input)
            
            self.logger.info("Starting to process voice streaming events...")
            
            # Stream events from voice pipeline
            async for event in result.stream():
                self.logger.debug(f"Received voice event: {event.type}, event object: {type(event)}")
                if hasattr(event, '__dict__'):
                    self.logger.debug(f"Event attributes: {vars(event)}")
                
                if event.type == "voice_stream_event_audio":
                    # Audio output from TTS - ensure data is bytes-like
                    try:
                        if hasattr(event.data, 'tobytes'):
                            audio_data = event.data.tobytes()
                        elif isinstance(event.data, (bytes, bytearray)):
                            audio_data = bytes(event.data)
                        elif isinstance(event.data, np.ndarray):
                            audio_data = event.data.tobytes()
                        else:
                            self.logger.warning(f"Unknown audio data type: {type(event.data)}, trying to convert to bytes")
                            audio_data = bytes(event.data)
                        
                        self.logger.debug(f"Yielding voice audio: {len(audio_data)} bytes, original type: {type(event.data)}")
                        yield {
                            "type": "voice_audio",
                            "data": audio_data,
                            "agent_name": self.team.orchestrator.name,
                            "is_done": False
                        }
                    except Exception as audio_error:
                        self.logger.error(f"Error processing voice audio data: {audio_error}")
                        self.logger.error(f"Audio data type: {type(event.data)}, length: {len(event.data) if hasattr(event.data, '__len__') else 'N/A'}")
                        # Continue without yielding this audio chunk
                        continue
                elif event.type == "voice_stream_event_text":
                    # Text response from agent
                    text_content = getattr(event, 'text', None) or getattr(event, 'content', None) or getattr(event, 'data', None) or str(event)
                    self.logger.debug(f"Voice text event - content: {text_content}")
                    yield {
                        "type": "text_response",
                        "content": text_content,
                        "agent_name": self.team.orchestrator.name,
                        "is_done": False
                    }
                elif hasattr(event, 'final_output') and event.final_output:
                    # Final completion
                    yield {
                        "type": "completion",
                        "content": event.final_output,
                        "agent_name": self.team.orchestrator.name,
                        "is_done": True
                    }
            
        except Exception as e:
            self.logger.error(f"Voice processing error: {e}")
            yield {
                "type": "error",
                "content": f"Voice processing failed: {str(e)}",
                "agent_name": self.team.orchestrator.name,
                "is_done": True
            }
            raise e
        finally:
            # Clean up interactive bash sessions first
            await self._cleanup_interactive_bash_sessions()
            # Clean up session resources
            await self._cleanup_session(session)
            # Clean up MCP servers
            await mcp_manager.cleanup_servers(all_agents)
    
    async def run_single_agent_voice_stream(self, agent_name: str, audio_buffer: np.ndarray, debug: bool = False, session_id: Optional[str] = None, session_context: Optional[dict] = None, max_turns: Optional[int] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Run a specific agent with voice input and streaming audio/text outputs.
        
        Args:
            agent_name: Name of the agent to run
            audio_buffer: NumPy array of audio samples (int16, 24kHz sample rate)
            debug: Whether to show debug info
            session_id: Session ID for conversation persistence
            
        Yields:
            Dict: Stream outputs including voice_stream_event_audio and text responses
        """
        # Get the target agent
        target_agent = self.team.get_agent(agent_name)
        if not target_agent:
            yield {
                "type": "error",
                "content": f"Agent '{agent_name}' not found in team configuration"
            }
            return
        
        self.logger.info(f"Starting voice processing with agent: {agent_name}")
        
        # Initialize MCP manager
        mcp_manager = MCPServerManager()
        await mcp_manager.connect_servers([target_agent])
        
        
        session = None
        try:
            # Create voice pipeline with the target agent
            voice_workflow = SingleAgentVoiceWorkflow(target_agent)
            voice_pipeline = VoicePipeline(workflow=voice_workflow)
            
            # Create audio input from buffer
            audio_input = AudioInput(buffer=audio_buffer)
            
            # Get session for persistence
            session = self._get_session(session_id, session_context)
            if session:
                self.logger.info(f"Running voice agent '{agent_name}' with persistent session: {session_id}")
            else:
                self.logger.info(f"Running voice agent '{agent_name}' without session persistence")
            
            # Run the voice pipeline
            result = await voice_pipeline.run(audio_input)
            
            self.logger.info(f"Starting to process voice streaming events for agent: {agent_name}")
            
            # Stream events from voice pipeline
            async for event in result.stream():
                self.logger.debug(f"Received voice event: {event.type}, event object: {type(event)}")
                if hasattr(event, '__dict__'):
                    self.logger.debug(f"Event attributes: {vars(event)}")
                
                if event.type == "voice_stream_event_audio":
                    # Audio output from TTS - ensure data is bytes-like
                    try:
                        if hasattr(event.data, 'tobytes'):
                            audio_data = event.data.tobytes()
                        elif isinstance(event.data, (bytes, bytearray)):
                            audio_data = bytes(event.data)
                        elif isinstance(event.data, np.ndarray):
                            audio_data = event.data.tobytes()
                        else:
                            self.logger.warning(f"Unknown audio data type: {type(event.data)}, trying to convert to bytes")
                            audio_data = bytes(event.data)
                        
                        self.logger.debug(f"Yielding voice audio for agent {agent_name}: {len(audio_data)} bytes, original type: {type(event.data)}")
                        yield {
                            "type": "voice_audio",
                            "data": audio_data,
                            "agent_name": agent_name,
                            "is_done": False
                        }
                    except Exception as audio_error:
                        self.logger.error(f"Error processing voice audio data for agent {agent_name}: {audio_error}")
                        self.logger.error(f"Audio data type: {type(event.data)}, length: {len(event.data) if hasattr(event.data, '__len__') else 'N/A'}")
                        # Continue without yielding this audio chunk
                        continue
                elif event.type == "voice_stream_event_text":
                    # Text response from agent
                    text_content = getattr(event, 'text', None) or getattr(event, 'content', None) or getattr(event, 'data', None) or str(event)
                    self.logger.debug(f"Voice text event for agent {agent_name} - content: {text_content}")
                    yield {
                        "type": "text_response",
                        "content": text_content,
                        "agent_name": agent_name,
                        "is_done": False
                    }
                elif hasattr(event, 'final_output') and event.final_output:
                    # Final completion
                    yield {
                        "type": "completion",
                        "content": event.final_output,
                        "agent_name": agent_name,
                        "is_done": True
                    }
            
        except Exception as e:
            self.logger.error(f"Voice processing error for agent {agent_name}: {e}")
            yield {
                "type": "error",
                "content": f"Voice processing failed: {str(e)}",
                "agent_name": agent_name,
                "is_done": True
            }
            raise e
        finally:
            # Clean up interactive bash sessions first
            await self._cleanup_interactive_bash_sessions()
            # Clean up session resources
            await self._cleanup_session(session)
            # Clean up MCP servers
            await mcp_manager.cleanup_servers([target_agent])
    
    def process_audio_chunk(self, audio_chunk, sample_rate: int = 16000) -> np.ndarray:
        """
        Process audio chunk from websocket (typically from VAD) into numpy array.
        
        Args:
            audio_chunk: Raw audio data from websocket (bytes, bytearray, or memoryview)
            sample_rate: Sample rate of the audio (default 16kHz from VAD)
            
        Returns:
            np.ndarray: Processed audio buffer ready for voice pipeline
        """
        try:
            # Handle different input types
            if hasattr(audio_chunk, 'tobytes'):
                # Handle memoryview or similar objects
                audio_bytes = audio_chunk.tobytes()
            elif isinstance(audio_chunk, (bytes, bytearray)):
                # Handle bytes or bytearray directly
                audio_bytes = bytes(audio_chunk)
            else:
                # Try to convert to bytes if it's not already
                try:
                    audio_bytes = bytes(audio_chunk)
                except Exception as convert_error:
                    self.logger.error(f"Unable to convert audio_chunk to bytes: {convert_error}")
                    self.logger.error(f"Audio chunk type: {type(audio_chunk)}")
                    raise ValueError(f"Unsupported audio chunk type: {type(audio_chunk)}")
            
            self.logger.debug(f"Processing audio chunk: {len(audio_bytes)} bytes, type: {type(audio_chunk)}")
            
            # Convert bytes to numpy array (assuming float32 from VAD web)
            try:
                audio_float32 = np.frombuffer(audio_bytes, dtype=np.float32)
                self.logger.debug(f"Converted to float32 array: {len(audio_float32)} samples")
            except ValueError as e:
                # If float32 doesn't work, try other formats
                self.logger.warning(f"Failed to parse as float32: {e}. Trying other formats...")
                
                # Try int16 format
                try:
                    audio_int16_raw = np.frombuffer(audio_bytes, dtype=np.int16)
                    audio_float32 = audio_int16_raw.astype(np.float32) / 32767.0
                    self.logger.debug(f"Converted from int16 to float32: {len(audio_float32)} samples")
                except ValueError:
                    # Try uint8 format
                    try:
                        audio_uint8 = np.frombuffer(audio_bytes, dtype=np.uint8)
                        audio_float32 = (audio_uint8.astype(np.float32) - 128) / 128.0
                        self.logger.debug(f"Converted from uint8 to float32: {len(audio_float32)} samples")
                    except ValueError as final_error:
                        self.logger.error(f"Unable to parse audio data in any known format: {final_error}")
                        raise ValueError(f"Unable to parse audio data: {final_error}")
            
            # Resample to 24kHz if needed (voice pipeline expects 24kHz)
            if sample_rate != 24000:
                # Simple resampling - for production use proper resampling library
                resample_ratio = 24000 / sample_rate
                new_length = int(len(audio_float32) * resample_ratio)
                indices = np.linspace(0, len(audio_float32) - 1, new_length)
                audio_float32 = np.interp(indices, np.arange(len(audio_float32)), audio_float32)
                self.logger.debug(f"Resampled from {sample_rate}Hz to 24kHz: {new_length} samples")
            
            # Convert to int16 as expected by voice pipeline
            audio_int16 = (audio_float32 * 32767).astype(np.int16)
            
            self.logger.debug(f"Final processed audio: {len(audio_int16)} samples at 24kHz")
            return audio_int16
            
        except Exception as e:
            self.logger.error(f"Audio processing error: {e}")
            self.logger.error(f"Audio chunk info - Type: {type(audio_chunk)}, Length: {len(audio_chunk) if hasattr(audio_chunk, '__len__') else 'N/A'}")
            raise e
