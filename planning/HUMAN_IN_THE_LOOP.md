# Human-in-the-Loop Implementation Plan for Gnosari Cloud

## Executive Summary

This document outlines a comprehensive implementation plan for human-in-the-loop (HITL) functionality in Gnosari AI Teams, enabling seamless integration between AI agent workflows and human oversight through Gnosari Cloud's workstation interface. The implementation follows SOLID principles and provides enterprise-grade reliability, scalability, and user experience.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Configuration Schema](#configuration-schema)
3. [Core Components](#core-components)
4. [API Interfaces](#api-interfaces)
5. [Event System](#event-system)
6. [Workflow Integration](#workflow-integration)
7. [Security & Permissions](#security--permissions)
8. [Implementation Phases](#implementation-phases)
9. [Testing Strategy](#testing-strategy)
10. [Monitoring & Observability](#monitoring--observability)

## Architecture Overview

### High-Level Design

The human-in-the-loop system integrates seamlessly with the existing Gnosari architecture through:

- **MCP Server Integration**: Human supervision implemented as an MCP server tool, following existing tool patterns
- **Session-Based Execution**: Teams continue execution and pause at intervention points, resuming when human responds
- **Asynchronous Communication**: Non-blocking communication with Gnosari Cloud workstation
- **Persistent Session State**: Complete session state tracking including conversation history, context, and intervention points
- **Natural Language Escalation**: Agents receive natural language instructions on when and how to escalate
- **Configurable Intervention Points**: Flexible configuration for when and how human oversight is required

### System Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Gnosari       │    │   Gnosari Cloud  │    │   Human         │
│   Engine        │◄──►│   Workstation    │◄──►│   Operator      │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌──────────────────┐
│   Human         │    │   Notification   │
│   Supervision   │    │   Service        │
│   MCP Server    │    │                  │
└─────────────────┘    └──────────────────┘
         │
         ▼
┌─────────────────┐
│   Session       │
│   Manager       │
│   & State Mgmt  │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│   Natural       │
│   Language      │
│   Escalation    │
│   Engine        │
└─────────────────┘
```

## Configuration Schema

### Enhanced Team Configuration

```yaml
# Enhanced team configuration with human supervision
human_supervision:
  enabled: true
  
  # Global settings
  global:
    timeout: 300                    # Default timeout for human responses (seconds)
    auto_continue: false            # Whether to continue automatically after timeout
    escalation_enabled: true        # Enable escalation to supervisors
    escalation_timeout: 600         # Timeout before escalation (seconds)
    max_escalation_levels: 3        # Maximum escalation levels
    
  # Intervention types and their configurations
  intervention_types:
    decision:
      enabled: true
      timeout: 180
      auto_continue: false
      escalation_enabled: true
      escalation_timeout: 300
      escalation_levels:
        - role: "supervisor"
          timeout: 300
        - role: "manager"
          timeout: 600
        - role: "admin"
          timeout: 900
      triggers:
        - condition: "confidence_score < 0.7"
          context: "decision_making"
        - condition: "risk_level == 'high'"
          context: "risk_assessment"
        - condition: "cost_threshold > 1000"
          context: "budget_approval"
      ui_config:
        layout: "decision_panel"
        show_context: true
        show_alternatives: true
        show_impact_analysis: true
        require_reason: true
        
    follow_up:
      enabled: true
      timeout: 120
      auto_continue: true
      escalation_enabled: false
      triggers:
        - condition: "task_completion"
          context: "quality_review"
        - condition: "error_occurred"
          context: "error_resolution"
        - condition: "milestone_reached"
          context: "progress_review"
      ui_config:
        layout: "review_panel"
        show_progress: true
        show_metrics: true
        allow_modifications: true
        
    approval:
      enabled: true
      timeout: 240
      auto_continue: false
      escalation_enabled: true
      escalation_timeout: 480
      triggers:
        - condition: "external_api_call"
          context: "api_approval"
        - condition: "file_modification"
          context: "file_approval"
        - condition: "data_access"
          context: "data_approval"
      ui_config:
        layout: "approval_panel"
        show_risk_assessment: true
        show_audit_trail: true
        require_signature: true
        
    escalation:
      enabled: true
      timeout: 360
      auto_continue: false
      escalation_enabled: true
      escalation_timeout: 720
      triggers:
        - condition: "error_count > 3"
          context: "error_escalation"
        - condition: "execution_time > 1800"
          context: "performance_escalation"
        - condition: "resource_usage > 80%"
          context: "resource_escalation"
      ui_config:
        layout: "escalation_panel"
        show_diagnostics: true
        show_recommendations: true
        allow_override: true

  # Notification configuration
  notifications:
    channels:
      - type: "websocket"
        enabled: true
        real_time: true
        events: ["intervention_required", "intervention_resolved", "escalation"]
      - type: "email"
        enabled: true
        real_time: false
        events: ["intervention_required", "escalation"]
        template: "intervention_notification"
      - type: "slack"
        enabled: true
        real_time: true
        events: ["intervention_required", "escalation"]
        webhook_url: "${SLACK_WEBHOOK_URL}"
      - type: "sms"
        enabled: false
        real_time: true
        events: ["critical_escalation"]
        provider: "twilio"
    
    # Notification templates
    templates:
      intervention_required:
        subject: "Human Intervention Required - {{team_name}}"
        body: |
          Team: {{team_name}}
          Agent: {{agent_name}}
          Type: {{intervention_type}}
          Context: {{context_summary}}
          Timeout: {{timeout}} seconds
          Link: {{workstation_url}}
      
      escalation:
        subject: "URGENT: Escalation Required - {{team_name}}"
        body: |
          Team: {{team_name}}
          Level: {{escalation_level}}
          Reason: {{escalation_reason}}
          Timeout: {{timeout}} seconds
          Link: {{workstation_url}}

  # Workstation integration
  workstation:
    base_url: "${GNOSARI_CLOUD_URL}"
    api_key: "${GNOSARI_CLOUD_API_KEY}"
    workspace_id: "${WORKSPACE_ID}"
    team_id: "${TEAM_ID}"
    
    # UI customization
    ui_customization:
      theme: "gnosari_dark"
      branding:
        logo_url: "${COMPANY_LOGO_URL}"
        primary_color: "#1a73e8"
        secondary_color: "#34a853"
      layout:
        sidebar_enabled: true
        context_panel_enabled: true
        metrics_panel_enabled: true
        chat_enabled: true
      
    # Real-time features
    real_time:
      enabled: true
      websocket_url: "${WEBSOCKET_URL}"
      heartbeat_interval: 30
      reconnect_attempts: 5
      reconnect_delay: 1000

  # Audit and compliance
  audit:
    enabled: true
    log_all_interactions: true
    retention_days: 90
    compliance_standards: ["SOC2", "GDPR", "HIPAA"]
    
    # Audit events
    events:
      - "intervention_requested"
      - "intervention_resolved"
      - "escalation_triggered"
      - "timeout_occurred"
      - "auto_continue_triggered"
      - "human_override"
      - "configuration_changed"

  # Performance and reliability
  performance:
    max_concurrent_interventions: 10
    intervention_queue_size: 100
    retry_attempts: 3
    retry_delay: 1000
    circuit_breaker:
      enabled: true
      failure_threshold: 5
      recovery_timeout: 30000
      half_open_max_calls: 3

  # Security
  security:
    authentication:
      method: "oauth2"
      provider: "gnosari_cloud"
      scopes: ["read", "write", "admin"]
    
    authorization:
      rbac_enabled: true
      roles:
        - name: "operator"
          permissions: ["intervention.resolve", "intervention.escalate"]
        - name: "supervisor"
          permissions: ["intervention.resolve", "intervention.escalate", "intervention.override"]
        - name: "admin"
          permissions: ["*"]
    
    encryption:
      data_in_transit: "TLS1.3"
      data_at_rest: "AES256"
      key_rotation_days: 90

# Agent-specific human supervision configuration
agents:
  - name: "Manager"
    instructions: |
      You are a team manager coordinating AI agents. You have access to human supervision capabilities.
      
      ## Human Supervision Guidelines
      
      **When to Request Human Intervention:**
      - When making decisions involving budget over $500
      - When encountering ethical dilemmas or sensitive topics
      - When team members disagree and you need mediation
      - When external API calls could have significant impact
      - When confidence in your decision is below 70%
      
      **How to Request Intervention:**
      - Clearly explain the situation and context
      - Provide your recommended action and reasoning
      - Highlight any risks or implications
      - Ask specific questions if you need guidance
      
      **Escalation Triggers:**
      - If human doesn't respond within 5 minutes for critical decisions
      - If budget impact exceeds $1000
      - If there are compliance or legal concerns
      - If team performance is significantly impacted
      
      **Natural Language Escalation Examples:**
      - "I need human approval for this budget decision as it exceeds our threshold"
      - "This ethical dilemma requires human judgment - should I proceed?"
      - "Team conflict detected - requesting mediation guidance"
      - "Low confidence in this decision - seeking human input"
      
    orchestrator: true
    model: "gpt-4o"
    temperature: 0.1
    
    # Agent-specific human supervision
    human_supervision:
      enabled: true
      intervention_types: ["decision", "approval"]
      escalation_enabled: true
      
      # Natural language escalation instructions
      escalation_instructions: |
        You should escalate to human supervision in these situations:
        
        1. **Budget Decisions**: When making financial decisions over $500, always request human approval. Explain the cost, benefits, and risks clearly.
        
        2. **Ethical Concerns**: If you encounter situations involving ethics, privacy, or sensitive topics, pause and request human guidance.
        
        3. **Team Conflicts**: When team members disagree or there are coordination issues, request human mediation.
        
        4. **Low Confidence**: If your confidence in a decision is below 70%, explain your reasoning and ask for human input.
        
        5. **External Dependencies**: Before making calls to external APIs that could have significant impact, request approval.
        
        **Escalation Language**: Use natural, conversational language. Explain the situation clearly, provide context, and ask specific questions.
        
      custom_triggers:
        - condition: "budget_exceeded"
          context: "budget_approval"
          intervention_type: "approval"
          natural_language: "This decision involves a budget of ${{amount}} which exceeds our approval threshold. I recommend {{recommendation}} because {{reasoning}}. Should I proceed?"
          options:
            - id: "approve_recommended"
              label: "Approve Recommended Option"
              description: "{{recommendation}} - {{reasoning}}"
              value: "approve"
              metadata:
                budget_impact: "{{amount}}"
                risk_level: "{{risk_level}}"
            - id: "approve_alternative"
              label: "Approve Alternative Option"
              description: "{{alternative_recommendation}} - {{alternative_reasoning}}"
              value: "approve_alternative"
              metadata:
                budget_impact: "{{alternative_amount}}"
                risk_level: "{{alternative_risk}}"
            - id: "reject"
              label: "Reject All Options"
              description: "Cancel this decision and explore other approaches"
              value: "reject"
              metadata:
                action: "cancel"
        - condition: "team_conflict"
          context: "conflict_resolution"
          intervention_type: "decision"
          natural_language: "I've detected a conflict between team members regarding {{issue}}. Here are my suggested resolutions:"
          options:
            - id: "resolution_a"
              label: "Resolution A: {{resolution_a_title}}"
              description: "{{resolution_a_description}}"
              value: "resolution_a"
              metadata:
                impact: "{{resolution_a_impact}}"
                effort: "{{resolution_a_effort}}"
            - id: "resolution_b"
              label: "Resolution B: {{resolution_b_title}}"
              description: "{{resolution_b_description}}"
              value: "resolution_b"
              metadata:
                impact: "{{resolution_b_impact}}"
                effort: "{{resolution_b_effort}}"
            - id: "mediation"
              label: "Request Human Mediation"
              description: "Have a human supervisor mediate the conflict"
              value: "mediation"
              metadata:
                escalation_level: 1
        - condition: "confidence_low"
          context: "decision_making"
          intervention_type: "decision"
          natural_language: "I'm only {{confidence}}% confident in this decision. Here are the options I'm considering:"
          options:
            - id: "proceed_cautiously"
              label: "Proceed with Caution"
              description: "Continue with the current plan but with additional safeguards"
              value: "proceed_cautiously"
              metadata:
                confidence: "{{confidence}}"
                safeguards: "{{safeguards}}"
            - id: "gather_more_info"
              label: "Gather More Information"
              description: "Pause to collect additional data before deciding"
              value: "gather_info"
              metadata:
                info_needed: "{{info_needed}}"
                estimated_time: "{{info_gathering_time}}"
            - id: "consult_expert"
              label: "Consult Domain Expert"
              description: "Get input from a human expert in this area"
              value: "consult_expert"
              metadata:
                expertise_area: "{{expertise_area}}"
        - condition: "ethical_concern"
          context: "ethics_review"
          intervention_type: "decision"
          natural_language: "I've encountered an ethical concern: {{concern}}. Here are my suggested approaches:"
          options:
            - id: "ethical_approach_a"
              label: "Approach A: {{ethical_approach_a_title}}"
              description: "{{ethical_approach_a_description}}"
              value: "ethical_approach_a"
              metadata:
                ethical_score: "{{ethical_score_a}}"
                risk_level: "{{risk_level_a}}"
            - id: "ethical_approach_b"
              label: "Approach B: {{ethical_approach_b_title}}"
              description: "{{ethical_approach_b_description}}"
              value: "ethical_approach_b"
              metadata:
                ethical_score: "{{ethical_score_b}}"
                risk_level: "{{risk_level_b}}"
            - id: "halt_and_review"
              label: "Halt and Review"
              description: "Stop current action and conduct thorough ethical review"
              value: "halt_review"
              metadata:
                action: "pause"
                review_required: true
      
      # Agent-specific UI configuration
      ui_config:
        show_team_status: true
        show_budget_info: true
        show_performance_metrics: true
        custom_fields:
          - name: "budget_impact"
            type: "currency"
            required: true
          - name: "risk_level"
            type: "select"
            options: ["low", "medium", "high", "critical"]
            required: true
          - name: "confidence_score"
            type: "percentage"
            required: true
          - name: "ethical_concerns"
            type: "text"
            required: false
```

## MCP Server Implementation

### 1. Human Supervision MCP Server

```python
# src/gnosari/tools/mcp/human_supervision_server.py

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field

from ...schemas.human_supervision import (
    InterventionRequest, InterventionOption, HumanResponse,
    InterventionType, InterventionUrgency, SessionStatus
)
from ...engine.human_supervision import HumanSupervisionManager, SessionManager

class HumanSupervisionMCPServer:
    """MCP Server for human supervision functionality."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.server = Server("human-supervision")
        self.supervision_manager = HumanSupervisionManager(config)
        self.session_manager = SessionManager(config)
        self._setup_tools()
        
    def _setup_tools(self):
        """Set up MCP tools for human supervision."""
        
        @self.server.tool()
        async def request_human_intervention(
            intervention_type: str,
            message: str,
            context: Dict[str, Any],
            urgency: str = "normal",
            options: Optional[List[Dict[str, Any]]] = None,
            async_mode: bool = False
        ) -> str:
            """
            Request human intervention for a decision or approval.
            
            Args:
                intervention_type: Type of intervention (decision, approval, escalation, etc.)
                message: Natural language message explaining the situation
                context: Context information about the current situation
                urgency: Urgency level (low, normal, high, critical)
                options: Optional list of suggested options for human to choose from
                async_mode: Whether to continue team execution in async mode after intervention
                
            Returns:
                Human response or intervention result
            """
            try:
                # Convert options to InterventionOption objects
                intervention_options = []
                if options:
                    for i, option_data in enumerate(options):
                        option = InterventionOption(
                            option_id=option_data.get("id", f"option_{i}"),
                            label=option_data.get("label", f"Option {i+1}"),
                            description=option_data.get("description", ""),
                            value=option_data.get("value", ""),
                            metadata=option_data.get("metadata", {}),
                            recommended=option_data.get("recommended", False)
                        )
                        intervention_options.append(option)
                
                # Create intervention request
                intervention_request = InterventionRequest(
                    intervention_id=f"intervention_{datetime.now().timestamp()}",
                    session_id=context.get("session_id", "default"),
                    intervention_type=InterventionType(intervention_type),
                    agent_name=context.get("agent_name", "unknown"),
                    natural_language_message=message,
                    context=context,
                    urgency=InterventionUrgency(urgency),
                    options=intervention_options
                )
                
                # Request intervention
                result = await self.supervision_manager.request_intervention(
                    intervention_request.session_id,
                    intervention_request.intervention_type.value,
                    intervention_request.agent_name,
                    intervention_request.context,
                    intervention_request.urgency,
                    intervention_request.natural_language_message,
                    intervention_request.options,
                    async_mode
                )
                
                return json.dumps({
                    "status": "intervention_requested",
                    "intervention_id": result.intervention_id,
                    "message": "Human intervention requested. Session paused until human responds.",
                    "workstation_url": result.workstation_url,
                    "timeout": result.timeout
                })
                
            except Exception as e:
                return json.dumps({
                    "status": "error",
                    "message": f"Failed to request human intervention: {str(e)}"
                })
        
        @self.server.tool()
        async def check_intervention_status(
            intervention_id: str
        ) -> str:
            """
            Check the status of a pending human intervention.
            
            Args:
                intervention_id: ID of the intervention to check
                
            Returns:
                Current status of the intervention
            """
            try:
                status = await self.supervision_manager.get_intervention_status(intervention_id)
                return json.dumps({
                    "intervention_id": intervention_id,
                    "status": status.status.value,
                    "resolved": status.resolved,
                    "human_response": status.human_response,
                    "session_resumed": status.session_resumed
                })
            except Exception as e:
                return json.dumps({
                    "status": "error",
                    "message": f"Failed to check intervention status: {str(e)}"
                })
        
        @self.server.tool()
        async def escalate_to_human(
            escalation_reason: str,
            escalation_level: int = 1,
            context: Dict[str, Any] = None
        ) -> str:
            """
            Escalate current situation to human supervisor.
            
            Args:
                escalation_reason: Reason for escalation
                escalation_level: Level of escalation (1-3)
                context: Additional context for escalation
                
            Returns:
                Escalation result
            """
            try:
                escalation_result = await self.supervision_manager.escalate_intervention(
                    escalation_reason=escalation_reason,
                    escalation_level=escalation_level,
                    context=context or {}
                )
                
                return json.dumps({
                    "status": "escalated",
                    "escalation_level": escalation_level,
                    "reason": escalation_reason,
                    "message": "Situation escalated to human supervisor"
                })
                
            except Exception as e:
                return json.dumps({
                    "status": "error",
                    "message": f"Failed to escalate: {str(e)}"
                })
        
        @self.server.tool()
        async def get_session_context(
            session_id: str
        ) -> str:
            """
            Get current session context and conversation history.
            
            Args:
                session_id: ID of the session
                
            Returns:
                Session context and history
            """
            try:
                session = await self.session_manager.get_session(session_id)
                return json.dumps({
                    "session_id": session_id,
                    "status": session.status.value,
                    "conversation_history": session.conversation_history,
                    "context": session.context,
                    "intervention_points": [
                        {
                            "intervention_id": ip.intervention_id,
                            "agent_name": ip.agent_name,
                            "intervention_type": ip.intervention_type.value,
                            "message": ip.message,
                            "timestamp": ip.timestamp.isoformat()
                        }
                        for ip in session.intervention_points
                    ]
                })
            except Exception as e:
                return json.dumps({
                    "status": "error",
                    "message": f"Failed to get session context: {str(e)}"
                })

# Tool definitions for OpenAI function calling
HUMAN_SUPERVISION_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "request_human_intervention",
            "description": "Request human intervention for decisions, approvals, or escalations. Use this when you need human input to proceed safely.",
            "parameters": {
                "type": "object",
                "properties": {
                    "intervention_type": {
                        "type": "string",
                        "enum": ["decision", "approval", "escalation", "follow_up", "quality_review"],
                        "description": "Type of intervention needed"
                    },
                    "message": {
                        "type": "string",
                        "description": "Natural language message explaining the situation and what you need from the human"
                    },
                    "context": {
                        "type": "object",
                        "description": "Context information about the current situation",
                        "properties": {
                            "budget_impact": {"type": "number", "description": "Financial impact if applicable"},
                            "risk_level": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                            "confidence": {"type": "number", "minimum": 0, "maximum": 1, "description": "Your confidence level"},
                            "urgency": {"type": "string", "enum": ["low", "normal", "high", "critical"]},
                            "deadline": {"type": "string", "description": "Any relevant deadlines"},
                            "stakeholders": {"type": "array", "items": {"type": "string"}, "description": "Affected parties"}
                        }
                    },
                    "urgency": {
                        "type": "string",
                        "enum": ["low", "normal", "high", "critical"],
                        "default": "normal",
                        "description": "Urgency level of the intervention"
                    },
                    "options": {
                        "type": "array",
                        "description": "Suggested options for the human to choose from",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string", "description": "Unique option identifier"},
                                "label": {"type": "string", "description": "Human-readable option label"},
                                "description": {"type": "string", "description": "Detailed description of the option"},
                                "value": {"type": "string", "description": "Value to pass back when selected"},
                                "recommended": {"type": "boolean", "default": False, "description": "Whether this is the recommended option"},
                                "metadata": {
                                    "type": "object",
                                    "description": "Additional metadata (budget impact, risk level, etc.)"
                                }
                            },
                            "required": ["id", "label", "description", "value"]
                        }
                    },
                    "async_mode": {
                        "type": "boolean",
                        "default": false,
                        "description": "Whether to continue team execution in async mode after human responds"
                    }
                },
                "required": ["intervention_type", "message", "context"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_intervention_status",
            "description": "Check the status of a pending human intervention",
            "parameters": {
                "type": "object",
                "properties": {
                    "intervention_id": {
                        "type": "string",
                        "description": "ID of the intervention to check"
                    }
                },
                "required": ["intervention_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "escalate_to_human",
            "description": "Escalate current situation to human supervisor",
            "parameters": {
                "type": "object",
                "properties": {
                    "escalation_reason": {
                        "type": "string",
                        "description": "Clear explanation of why escalation is needed"
                    },
                    "escalation_level": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 3,
                        "default": 1,
                        "description": "Level of escalation (1=supervisor, 2=manager, 3=admin)"
                    },
                    "context": {
                        "type": "object",
                        "description": "Additional context for the escalation"
                    }
                },
                "required": ["escalation_reason"]
            }
        }
    }
]
```

### 2. Tool Integration in Team Configuration

```yaml
# Enhanced team configuration with human supervision MCP server
tools:
  # Human Supervision MCP Server
  - name: "Human Supervision"
    id: human_supervision_tool
    description: "Request human intervention for decisions, approvals, and escalations"
    module: gnosari.tools.mcp.human_supervision_server
    class: HumanSupervisionMCPServer
    args:
      workstation_url: "${GNOSARI_CLOUD_URL}"
      api_key: "${GNOSARI_CLOUD_API_KEY}"
      timeout: 300
      escalation_enabled: true
      notification_channels: ["websocket", "email", "slack"]
      async_mode_enabled: true
      queue_priority: 3
      
  # Other tools...
  - name: "File Manager"
    id: file_tool
    module: gnosari.tools.builtin.file_operations
    class: FileOperationsTool
    args:
      base_directory: "./workspace"
      allowed_extensions: [".txt", ".json", ".md", ".html", ".xml"]
```

### 3. Async Execution Configuration

```yaml
# Team configuration with async execution support
human_supervision:
  enabled: true
  
  # Async execution settings
  async_execution:
    enabled: true
    default_mode: "async"  # "sync" or "async"
    queue_priority: 3      # 1-10, lower = higher priority
    queue_name: "team_execution_queue"
    max_retries: 3
    retry_delay: 60        # seconds
    
  # Intervention types with async support
  intervention_types:
    decision:
      enabled: true
      async_mode: true
      timeout: 180
      auto_continue: false
      
    approval:
      enabled: true
      async_mode: true
      timeout: 240
      auto_continue: false
      
    follow_up:
      enabled: true
      async_mode: false  # Follow-ups can be sync
      timeout: 120
      auto_continue: true
```

### 3. Prompt Integration

```python
# src/gnosari/prompts/prompts.py - Updated functions

def build_orchestrator_system_prompt(name: str, instructions: str, team_config: Dict[str, Any], agent_tools: List[str] = None, tool_manager = None, agent_config: Dict[str, Any] = None, knowledge_descriptions: Dict[str, str] = None) -> Dict[str, List[str]]:
    """Build system prompt components for an orchestrator agent."""
    
    # ... existing code ...
    
    # Add human supervision instructions if enabled
    if agent_config and agent_config.get('human_supervision', {}).get('enabled', False):
        supervision_config = agent_config['human_supervision']
        background.append("HUMAN SUPERVISION:")
        background.append("You have access to human supervision capabilities through the human supervision tool.")
        background.append("Use request_human_intervention when you need human input for:")
        
        # Add specific supervision instructions
        if 'escalation_instructions' in supervision_config:
            background.append(supervision_config['escalation_instructions'])
        
        # Add custom triggers
        if 'custom_triggers' in supervision_config:
            background.append("Specific situations requiring human intervention:")
            for trigger in supervision_config['custom_triggers']:
                condition = trigger.get('condition', '')
                context_desc = trigger.get('context', '')
                natural_lang = trigger.get('natural_language', '')
                if condition and context_desc:
                    background.append(f"- {condition}: {context_desc}")
                    if natural_lang:
                        background.append(f"  Example message: \"{natural_lang}\"")
        
        background.append("")
        background.append("When requesting intervention:")
        background.append("- Clearly explain the situation and context")
        background.append("- Provide your recommended action and reasoning")
        background.append("- Highlight any risks or implications")
        background.append("- Suggest specific options when appropriate")
        background.append("- Ask specific questions if you need guidance")
        background.append("")

def build_specialized_agent_system_prompt(name: str, instructions: str, agent_tools: List[str] = None, tool_manager = None, agent_config: Dict[str, Any] = None, knowledge_descriptions: Dict[str, str] = None) -> Dict[str, List[str]]:
    """Build system prompt components for a specialized agent."""
    
    # ... existing code ...
    
    # Add human supervision instructions if enabled
    if agent_config and agent_config.get('human_supervision', {}).get('enabled', False):
        supervision_config = agent_config['human_supervision']
        background.append("HUMAN SUPERVISION:")
        background.append("You have access to human supervision capabilities through the human supervision tool.")
        background.append("Use request_human_intervention when you need human input for:")
        
        # Add specific supervision instructions
        if 'escalation_instructions' in supervision_config:
            background.append(supervision_config['escalation_instructions'])
        
        # Add custom triggers
        if 'custom_triggers' in supervision_config:
            background.append("Specific situations requiring human intervention:")
            for trigger in supervision_config['custom_triggers']:
                condition = trigger.get('condition', '')
                context_desc = trigger.get('context', '')
                natural_lang = trigger.get('natural_language', '')
                if condition and context_desc:
                    background.append(f"- {condition}: {context_desc}")
                    if natural_lang:
                        background.append(f"  Example message: \"{natural_lang}\"")
        
        background.append("")
        background.append("When requesting intervention:")
        background.append("- Clearly explain the situation and context")
        background.append("- Provide your recommended action and reasoning")
        background.append("- Highlight any risks or implications")
        background.append("- Suggest specific options when appropriate")
        background.append("- Ask specific questions if you need guidance")
        background.append("")
```

## Core Components

### 1. Human Supervision Manager (MCP Server Backend)

```python
class HumanSupervisionManager:
    """Backend manager for human supervision MCP server."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.workstation_client = WorkstationClient(config)
        self.notification_service = NotificationService(config)
        self.queue_client = QueueClient(config)
        
    async def request_intervention(
        self,
        session_id: str,
        intervention_type: str,
        agent_name: str,
        context: Dict[str, Any],
        urgency: str,
        message: str,
        options: List[InterventionOption] = None,
        async_mode: bool = False
    ) -> str:
        """Request human intervention and return workstation URL."""
        
        intervention_id = f"intervention_{datetime.now().timestamp()}"
        
        # Create intervention payload
        intervention_data = {
            "intervention_id": intervention_id,
            "session_id": session_id,
            "agent_name": agent_name,
            "intervention_type": intervention_type,
            "message": message,
            "context": context,
            "urgency": urgency,
            "options": [option.to_dict() for option in (options or [])],
            "async_mode": async_mode,
            "timestamp": datetime.now().isoformat()
        }
        
        # Send to workstation
        workstation_url = await self.workstation_client.create_intervention_session(intervention_data)
        
        # Send notifications
        await self.notification_service.send_intervention_notification(intervention_data)
        
        # If async mode, queue team execution continuation
        if async_mode:
            await self.queue_client.queue_team_continuation(session_id, intervention_id)
        
        return json.dumps({
            "status": "intervention_requested",
            "intervention_id": intervention_id,
            "workstation_url": workstation_url,
            "async_mode": async_mode,
            "message": "Human intervention requested. Please check the workstation for response."
        })
        
    async def acknowledge_human_response(
        self,
        session_id: str,
        intervention_id: str,
        human_response: Dict[str, Any]
    ) -> str:
        """Acknowledge human response and continue team execution."""
        
        # Send acknowledgment to workstation
        await self.workstation_client.send_acknowledgment(session_id, intervention_id, human_response)
        
        # Queue team continuation with human context
        await self.queue_client.queue_team_continuation_with_context(
            session_id, intervention_id, human_response
        )
        
        return json.dumps({
            "status": "acknowledged",
            "session_id": session_id,
            "intervention_id": intervention_id,
            "message": "Human response acknowledged. Team execution continuing in async mode."
        })
```

### 2. Queue Client for Async Team Execution

```python
class QueueClient:
    """Client for queuing team execution tasks."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.celery_app = get_celery_app()
        
    async def queue_team_continuation(
        self,
        session_id: str,
        intervention_id: str,
        priority: int = 5
    ) -> str:
        """Queue team execution continuation after human intervention."""
        
        message_data = {
            "task_id": f"team_continuation_{session_id}_{intervention_id}",
            "session_id": session_id,
            "intervention_id": intervention_id,
            "task_type": "team_continuation",
            "priority": priority,
            "created_at": datetime.now().isoformat()
        }
        
        # Send to queue
        task = self.celery_app.send_task(
            'gnosari.queue.consumers.team_execution.process_team_continuation',
            args=[message_data],
            priority=priority
        )
        
        return task.id
        
    async def queue_team_continuation_with_context(
        self,
        session_id: str,
        intervention_id: str,
        human_response: Dict[str, Any],
        priority: int = 5
    ) -> str:
        """Queue team execution continuation with human response context."""
        
        message_data = {
            "task_id": f"team_continuation_context_{session_id}_{intervention_id}",
            "session_id": session_id,
            "intervention_id": intervention_id,
            "human_response": human_response,
            "task_type": "team_continuation_with_context",
            "priority": priority,
            "created_at": datetime.now().isoformat()
        }
        
        # Send to queue
        task = self.celery_app.send_task(
            'gnosari.queue.consumers.team_execution.process_team_continuation_with_context',
            args=[message_data],
            priority=priority
        )
        
        return task.id
```

### 3. Team Execution Consumer

```python
# src/gnosari/queue/consumers/team_execution.py

import asyncio
from typing import Dict, Any
from ..base import BaseConsumer, BaseMessage
from ...engine.team_builder import TeamBuilder
from ...engine.runner import TeamRunner
from pydantic import Field

class TeamExecutionMessage(BaseMessage):
    """Message for team execution tasks."""
    
    session_id: str = Field(description="Session ID")
    intervention_id: str = Field(description="Intervention ID")
    human_response: Dict[str, Any] = Field(default_factory=dict, description="Human response context")
    task_type: str = Field(description="Type of team execution task")
    team_config_path: str = Field(description="Path to team configuration")
    
    @classmethod
    def create(
        cls,
        session_id: str,
        intervention_id: str,
        task_type: str,
        team_config_path: str,
        human_response: Dict[str, Any] = None
    ) -> "TeamExecutionMessage":
        """Create a new team execution message."""
        return cls(
            message_id=f"team_exec_{session_id}_{intervention_id}",
            session_id=session_id,
            intervention_id=intervention_id,
            task_type=task_type,
            team_config_path=team_config_path,
            human_response=human_response or {}
        )

class TeamExecutionConsumer(BaseConsumer):
    """Consumer for processing team execution tasks."""
    
    async def process(self, message: TeamExecutionMessage) -> Dict[str, Any]:
        """Process team execution message."""
        
        if message.task_type == "team_continuation":
            return await self._continue_team_execution(message)
        elif message.task_type == "team_continuation_with_context":
            return await self._continue_team_execution_with_context(message)
        else:
            raise ValueError(f"Unknown task type: {message.task_type}")
    
    async def _continue_team_execution(self, message: TeamExecutionMessage) -> Dict[str, Any]:
        """Continue team execution after human intervention."""
        
        # Build team
        team_builder = TeamBuilder()
        team = await team_builder.build_team(message.team_config_path)
        
        # Create team runner
        team_runner = TeamRunner(team)
        
        # Continue execution with session context
        result = await team_runner.run_team_async(
            message=f"Continuing execution after human intervention {message.intervention_id}",
            session_id=message.session_id,
            debug=False
        )
        
        return {
            "message_id": message.message_id,
            "session_id": message.session_id,
            "intervention_id": message.intervention_id,
            "status": "completed",
            "result": result,
            "processed_at": datetime.now().isoformat()
        }
    
    async def _continue_team_execution_with_context(
        self, 
        message: TeamExecutionMessage
    ) -> Dict[str, Any]:
        """Continue team execution with human response context."""
        
        # Build team
        team_builder = TeamBuilder()
        team = await team_builder.build_team(message.team_config_path)
        
        # Create team runner
        team_runner = TeamRunner(team)
        
        # Create context message with human response
        context_message = f"""
Human Response Received:
- Intervention ID: {message.intervention_id}
- Response Type: {message.human_response.get('response_type', 'unknown')}
- Selected Option: {message.human_response.get('selected_option', {}).get('label', 'N/A')}
- Custom Input: {message.human_response.get('custom_input', 'None')}
- Human Reasoning: {message.human_response.get('reasoning', 'None')}

Please acknowledge this human input and continue with the task accordingly.
        """
        
        # Continue execution with human context
        result = await team_runner.run_team_async(
            message=context_message,
            session_id=message.session_id,
            debug=False
        )
        
        return {
            "message_id": message.message_id,
            "session_id": message.session_id,
            "intervention_id": message.intervention_id,
            "status": "completed_with_context",
            "human_response": message.human_response,
            "result": result,
            "processed_at": datetime.now().isoformat()
        }
    
    def on_success(self, result: Dict[str, Any], message: TeamExecutionMessage) -> None:
        """Called when team execution succeeds."""
        print(f"✅ Team execution completed for session {message.session_id}")
        
    def on_failure(self, exc: Exception, message: TeamExecutionMessage) -> None:
        """Called when team execution fails."""
        print(f"❌ Team execution failed for session {message.session_id}: {exc}")
        
    def should_retry(self, exc: Exception, message: TeamExecutionMessage) -> bool:
        """Determine if team execution should be retried."""
        # Don't retry configuration errors
        if isinstance(exc, (ValueError, FileNotFoundError)):
            return False
        return message.retry_count < message.max_retries

# Celery tasks
@celery_app.task(bind=True)
def process_team_continuation(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
    """Celery task for team continuation."""
    consumer = TeamExecutionConsumer()
    message = TeamExecutionMessage.from_dict(message_data)
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(consumer.process(message))
        loop.close()
        
        consumer.on_success(result, message)
        return result
    except Exception as exc:
        consumer.on_failure(exc, message)
        
        if consumer.should_retry(exc, message):
            message.retry_count += 1
            raise self.retry(
                countdown=2 ** message.retry_count,
                max_retries=message.max_retries
            )
        raise

@celery_app.task(bind=True)
def process_team_continuation_with_context(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
    """Celery task for team continuation with human context."""
    consumer = TeamExecutionConsumer()
    message = TeamExecutionMessage.from_dict(message_data)
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(consumer.process(message))
        loop.close()
        
        consumer.on_success(result, message)
        return result
    except Exception as exc:
        consumer.on_failure(exc, message)
        
        if consumer.should_retry(exc, message):
            message.retry_count += 1
            raise self.retry(
                countdown=2 ** message.retry_count,
                max_retries=message.max_retries
            )
        raise
```

### 2. Workstation Client

```python
class WorkstationClient:
    """Client for communicating with Gnosari Cloud workstation."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.base_url = config.get("workstation_url")
        self.api_key = config.get("api_key")
        self.http_client = httpx.AsyncClient()
        
    async def create_intervention_session(self, intervention_data: Dict[str, Any]) -> str:
        """Create a new intervention session in the workstation."""
        
        response = await self.http_client.post(
            f"{self.base_url}/api/interventions",
            json=intervention_data,
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        
        if response.status_code == 201:
            result = response.json()
            return result["workstation_url"]
        else:
            raise Exception(f"Failed to create intervention session: {response.text}")
```

### 3. Notification Service

```python
class NotificationService:
    """Service for sending notifications about interventions."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.channels = config.get("notification_channels", [])
        
    async def send_intervention_notification(self, intervention_data: Dict[str, Any]):
        """Send notification about new intervention."""
        
        for channel in self.channels:
            if channel == "websocket":
                await self._send_websocket_notification(intervention_data)
            elif channel == "email":
                await self._send_email_notification(intervention_data)
            elif channel == "slack":
                await self._send_slack_notification(intervention_data)
                
    async def _send_websocket_notification(self, intervention_data: Dict[str, Any]):
        """Send WebSocket notification."""
        # Implementation for WebSocket notifications
        pass
        
    async def _send_email_notification(self, intervention_data: Dict[str, Any]):
        """Send email notification."""
        # Implementation for email notifications
        pass
        
    async def _send_slack_notification(self, intervention_data: Dict[str, Any]):
        """Send Slack notification."""
        # Implementation for Slack notifications
        pass
```

### 2. Intervention Types and Options

```python
class InterventionType(Enum):
    DECISION = "decision"
    FOLLOW_UP = "follow_up"
    APPROVAL = "approval"
    ESCALATION = "escalation"
    QUALITY_REVIEW = "quality_review"
    ERROR_RESOLUTION = "error_resolution"
    RISK_ASSESSMENT = "risk_assessment"
    COMPLIANCE_CHECK = "compliance_check"

class InterventionUrgency(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

class InterventionResolution(Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFIED = "modified"
    ESCALATED = "escalated"
    TIMEOUT = "timeout"
    AUTO_CONTINUE = "auto_continue"
    OPTION_SELECTED = "option_selected"

class InterventionOption:
    """Represents an option presented to human during intervention."""
    
    def __init__(
        self,
        option_id: str,
        label: str,
        description: str,
        value: str,
        metadata: Dict[str, Any] = None,
        recommended: bool = False,
        disabled: bool = False
    ):
        self.option_id = option_id
        self.label = label
        self.description = description
        self.value = value
        self.metadata = metadata or {}
        self.recommended = recommended
        self.disabled = disabled
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert option to dictionary for API responses."""
        return {
            "id": self.option_id,
            "label": self.label,
            "description": self.description,
            "value": self.value,
            "metadata": self.metadata,
            "recommended": self.recommended,
            "disabled": self.disabled
        }

class InterventionRequest:
    """Request for human intervention with options."""
    
    def __init__(
        self,
        intervention_id: str,
        session_id: str,
        intervention_type: InterventionType,
        agent_name: str,
        natural_language_message: str,
        context: Dict[str, Any],
        urgency: InterventionUrgency = InterventionUrgency.NORMAL,
        options: List[InterventionOption] = None,
        timeout: int = 300,
        workstation_url: str = None
    ):
        self.intervention_id = intervention_id
        self.session_id = session_id
        self.intervention_type = intervention_type
        self.agent_name = agent_name
        self.natural_language_message = natural_language_message
        self.context = context
        self.urgency = urgency
        self.options = options or []
        self.timeout = timeout
        self.workstation_url = workstation_url
        self.created_at = datetime.now()
        self.status = InterventionStatus.PENDING
        
    def add_option(
        self,
        option_id: str,
        label: str,
        description: str,
        value: str,
        metadata: Dict[str, Any] = None,
        recommended: bool = False
    ) -> InterventionOption:
        """Add an option to the intervention request."""
        option = InterventionOption(
            option_id=option_id,
            label=label,
            description=description,
            value=value,
            metadata=metadata or {},
            recommended=recommended
        )
        self.options.append(option)
        return option
        
    def get_recommended_option(self) -> Optional[InterventionOption]:
        """Get the recommended option if any."""
        for option in self.options:
            if option.recommended:
                return option
        return None
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert intervention request to dictionary."""
        return {
            "intervention_id": self.intervention_id,
            "session_id": self.session_id,
            "intervention_type": self.intervention_type.value,
            "agent_name": self.agent_name,
            "message": self.natural_language_message,
            "context": self.context,
            "urgency": self.urgency.value,
            "options": [option.to_dict() for option in self.options],
            "timeout": self.timeout,
            "workstation_url": self.workstation_url,
            "created_at": self.created_at.isoformat(),
            "status": self.status.value
        }

class HumanResponse:
    """Human response to an intervention with option selection."""
    
    def __init__(
        self,
        response_type: str,
        content: str,
        selected_option: Optional[InterventionOption] = None,
        custom_input: Optional[str] = None,
        metadata: Dict[str, Any] = None
    ):
        self.response_type = response_type  # "approve", "reject", "modify", "escalate", "select_option"
        self.content = content
        self.selected_option = selected_option
        self.custom_input = custom_input
        self.metadata = metadata or {}
        self.timestamp = datetime.now()
        
    def to_context_update(self) -> Dict[str, Any]:
        """Convert human response to context update."""
        context_update = {
            "human_response": self.content,
            "response_type": self.response_type,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat()
        }
        
        if self.selected_option:
            context_update["selected_option"] = self.selected_option.to_dict()
            
        if self.custom_input:
            context_update["custom_input"] = self.custom_input
            
        return context_update
```

### 3. Event System Integration

```python
class HumanSupervisionEventHandler:
    """Handles human supervision events during team execution."""
    
    def __init__(self, supervision_manager: HumanSupervisionManager):
        self.supervision_manager = supervision_manager
        self.event_handlers = {
            'agent_handoff': self._handle_agent_handoff,
            'tool_call': self._handle_tool_call,
            'error_occurred': self._handle_error,
            'milestone_reached': self._handle_milestone,
            'confidence_low': self._handle_low_confidence,
        }
    
    async def handle_event(self, event: ExecutionEvent) -> AsyncGenerator[Dict[str, Any], None]:
        """Process execution events and trigger interventions when needed."""
        
    async def _check_intervention_triggers(
        self,
        event: ExecutionEvent,
        agent_config: Dict[str, Any]
    ) -> Optional[InterventionRequest]:
        """Check if an event should trigger human intervention."""
```

### 4. Workstation Client

```python
class WorkstationClient:
    """Client for communicating with Gnosari Cloud workstation."""
    
    def __init__(self, config: WorkstationConfig):
        self.config = config
        self.websocket_client = None
        self.http_client = httpx.AsyncClient()
        self.authenticator = OAuth2Authenticator(config)
        
    async def create_intervention_session(
        self,
        intervention_request: InterventionRequest
    ) -> InterventionSession:
        """Create a new intervention session in the workstation."""
        
    async def send_intervention_update(
        self,
        session_id: str,
        update: InterventionUpdate
    ) -> bool:
        """Send real-time updates to the workstation."""
        
    async def wait_for_resolution(
        self,
        session_id: str,
        timeout: int
    ) -> InterventionResolution:
        """Wait for human resolution of an intervention."""
```

## Session Management

### 1. Session Lifecycle

```python
class SessionStatus(Enum):
    ACTIVE = "active"
    PAUSED_FOR_INTERVENTION = "paused_for_intervention"
    WAITING_FOR_HUMAN = "waiting_for_human"
    RESUMING = "resuming"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"

class SessionManager:
    """Manages team execution sessions with human supervision."""
    
    async def create_session(
        self,
        team_id: str,
        initial_message: str,
        context: Dict[str, Any]
    ) -> Session:
        """Create a new execution session."""
        
    async def pause_session_for_intervention(
        self,
        session_id: str,
        intervention_request: InterventionRequest
    ) -> bool:
        """Pause session execution and request human intervention."""
        
    async def resume_session_after_intervention(
        self,
        session_id: str,
        intervention_id: str,
        human_response: HumanResponse
    ) -> bool:
        """Resume session execution after human intervention."""
        
    async def get_session_state(self, session_id: str) -> SessionState:
        """Get current session state."""
        
    async def update_session_context(
        self,
        session_id: str,
        context_updates: Dict[str, Any]
    ) -> bool:
        """Update session context with human input."""

class HumanResponse:
    """Human response to an intervention."""
    
    def __init__(self, response_type: str, content: str, metadata: Dict[str, Any] = None):
        self.response_type = response_type  # "approve", "reject", "modify", "escalate"
        self.content = content
        self.metadata = metadata or {}
        self.timestamp = datetime.now()
        
    def to_context_update(self) -> Dict[str, Any]:
        """Convert human response to context update."""
        return {
            "human_response": self.content,
            "response_type": self.response_type,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat()
        }
```

### 2. Session Storage

```python
class SessionStorage:
    """Persistent storage for session data."""
    
    def __init__(self, config: HumanSupervisionConfig):
        self.config = config
        self.redis_client = redis.Redis.from_url(config.redis_url)
        self.db_client = DatabaseClient(config.database_url)
        
    async def save_session(self, session: Session) -> bool:
        """Save session to persistent storage."""
        
    async def load_session(self, session_id: str) -> Optional[Session]:
        """Load session from persistent storage."""
        
    async def update_session_context(
        self,
        session_id: str,
        context_updates: Dict[str, Any]
    ) -> bool:
        """Update session context in storage."""
        
    async def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a session."""
```

## API Interfaces

### 1. REST API Endpoints

```python
# Session Management API
@router.post("/sessions")
async def create_session(
    request: CreateSessionRequest,
    current_user: User = Depends(get_current_user)
) -> SessionResponse:
    """Create a new team execution session."""

@router.get("/sessions/{session_id}")
async def get_session(
    session_id: str,
    current_user: User = Depends(get_current_user)
) -> SessionResponse:
    """Get session details and current state."""

@router.post("/sessions/{session_id}/resume")
async def resume_session(
    session_id: str,
    human_response: HumanResponseRequest,
    current_user: User = Depends(get_current_user)
) -> SessionResumeResponse:
    """Resume session after human intervention."""

@router.get("/sessions/{session_id}/history")
async def get_session_history(
    session_id: str,
    limit: int = 100,
    offset: int = 0,
    current_user: User = Depends(get_current_user)
) -> SessionHistoryResponse:
    """Get conversation history for a session."""

# Human Supervision API
@router.post("/interventions")
async def create_intervention(
    request: CreateInterventionRequest,
    current_user: User = Depends(get_current_user)
) -> InterventionResponse:
    """Create a new human intervention request."""

@router.get("/interventions/{intervention_id}")
async def get_intervention(
    intervention_id: str,
    current_user: User = Depends(get_current_user)
) -> InterventionResponse:
    """Get intervention details."""

@router.post("/interventions/{intervention_id}/resolve")
async def resolve_intervention(
    intervention_id: str,
    resolution: InterventionResolutionRequest,
    current_user: User = Depends(get_current_user)
) -> ResolutionResponse:
    """Resolve a human intervention and resume session."""

@router.post("/interventions/{intervention_id}/select-option")
async def select_intervention_option(
    intervention_id: str,
    option_selection: OptionSelectionRequest,
    current_user: User = Depends(get_current_user)
) -> OptionSelectionResponse:
    """Select an option from an intervention and resume session."""

@router.post("/interventions/{intervention_id}/custom-response")
async def provide_custom_response(
    intervention_id: str,
    custom_response: CustomResponseRequest,
    current_user: User = Depends(get_current_user)
) -> CustomResponseResponse:
    """Provide a custom response to an intervention."""

@router.post("/interventions/{intervention_id}/escalate")
async def escalate_intervention(
    intervention_id: str,
    escalation: EscalationRequest,
    current_user: User = Depends(get_current_user)
) -> EscalationResponse:
    """Escalate an intervention."""

@router.get("/interventions")
async def list_interventions(
    status: Optional[InterventionStatus] = None,
    intervention_type: Optional[InterventionType] = None,
    team_id: Optional[str] = None,
    session_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user)
) -> InterventionListResponse:
    """List interventions with filtering and pagination."""

@router.get("/teams/{team_id}/interventions/stats")
async def get_intervention_stats(
    team_id: str,
    time_range: Optional[TimeRange] = None,
    current_user: User = Depends(get_current_user)
) -> InterventionStatsResponse:
    """Get intervention statistics for a team."""
```

### 2. WebSocket API

```python
# Real-time WebSocket events
class WorkstationWebSocket:
    """WebSocket handler for real-time workstation communication."""
    
    async def handle_intervention_request(self, websocket, path):
        """Handle real-time intervention requests."""
        
    async def handle_intervention_resolution(self, websocket, path):
        """Handle real-time intervention resolutions."""
        
    async def handle_session_updates(self, websocket, path):
        """Handle real-time session status updates."""
        
    async def handle_team_status_updates(self, websocket, path):
        """Handle real-time team status updates."""

# WebSocket event types
class WebSocketEvent:
    """Base class for WebSocket events."""
    
    def __init__(self, event_type: str, data: Dict[str, Any]):
        self.event_type = event_type
        self.data = data
        self.timestamp = datetime.now()

class InterventionRequestEvent(WebSocketEvent):
    """WebSocket event for intervention requests."""
    
    def __init__(self, intervention_request: InterventionRequest):
        super().__init__("intervention_requested", {
            "intervention_id": intervention_request.intervention_id,
            "session_id": intervention_request.session_id,
            "agent_name": intervention_request.agent_name,
            "intervention_type": intervention_request.intervention_type,
            "message": intervention_request.natural_language_message,
            "urgency": intervention_request.urgency,
            "workstation_url": intervention_request.workstation_url,
            "timeout": intervention_request.timeout
        })

class SessionStatusEvent(WebSocketEvent):
    """WebSocket event for session status changes."""
    
    def __init__(self, session_id: str, status: SessionStatus, context: Dict[str, Any] = None):
        super().__init__("session_status_changed", {
            "session_id": session_id,
            "status": status.value,
            "context": context or {}
        })
```

### 3. Request/Response Schemas

```python
class OptionSelectionRequest(BaseModel):
    """Request to select an intervention option."""
    option_id: str = Field(description="ID of the selected option")
    custom_input: Optional[str] = Field(default=None, description="Additional custom input")
    reasoning: Optional[str] = Field(default=None, description="Human reasoning for the selection")

class OptionSelectionResponse(BaseModel):
    """Response to option selection."""
    success: bool = Field(description="Whether the selection was successful")
    session_id: str = Field(description="Session ID")
    intervention_id: str = Field(description="Intervention ID")
    selected_option: Dict[str, Any] = Field(description="Selected option details")
    session_resumed: bool = Field(description="Whether session was resumed")
    message: str = Field(description="Status message")

class CustomResponseRequest(BaseModel):
    """Request to provide custom response to intervention."""
    response_text: str = Field(description="Custom response text")
    response_type: str = Field(description="Type of response (approve, reject, modify, etc.)")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

class CustomResponseResponse(BaseModel):
    """Response to custom response."""
    success: bool = Field(description="Whether the response was processed successfully")
    session_id: str = Field(description="Session ID")
    intervention_id: str = Field(description="Intervention ID")
    session_resumed: bool = Field(description="Whether session was resumed")
    message: str = Field(description="Status message")

class InterventionResolutionRequest(BaseModel):
    """Request to resolve an intervention."""
    resolution_type: str = Field(description="Type of resolution (approve, reject, modify, escalate)")
    reasoning: Optional[str] = Field(default=None, description="Human reasoning for the resolution")
    modifications: Optional[Dict[str, Any]] = Field(default=None, description="Modifications if resolution_type is 'modify'")
    escalation_level: Optional[int] = Field(default=None, description="Escalation level if resolution_type is 'escalate'")

class ResolutionResponse(BaseModel):
    """Response to intervention resolution."""
    success: bool = Field(description="Whether the resolution was successful")
    session_id: str = Field(description="Session ID")
    intervention_id: str = Field(description="Intervention ID")
    resolution: str = Field(description="Resolution type")
    session_resumed: bool = Field(description="Whether session was resumed")
    message: str = Field(description="Status message")
```

### 4. GraphQL API

```graphql
type InterventionOption {
  id: ID!
  label: String!
  description: String!
  value: String!
  metadata: JSON!
  recommended: Boolean!
  disabled: Boolean!
}

type Intervention {
  id: ID!
  type: InterventionType!
  status: InterventionStatus!
  agentName: String!
  teamId: String!
  sessionId: String!
  context: JSON!
  urgency: InterventionUrgency!
  message: String!
  options: [InterventionOption!]!
  createdAt: DateTime!
  resolvedAt: DateTime
  resolvedBy: User
  resolution: InterventionResolution
  escalationLevel: Int
  timeout: Int
  workstationUrl: String!
}

type Session {
  id: ID!
  teamId: String!
  status: SessionStatus!
  initialMessage: String!
  conversationHistory: [ConversationTurn!]!
  context: JSON!
  interventionPoints: [InterventionPoint!]!
  createdAt: DateTime!
  lastActivity: DateTime!
}

type ConversationTurn {
  agentName: String!
  input: String!
  response: String!
  timestamp: DateTime!
}

type InterventionPoint {
  interventionId: String!
  agentName: String!
  interventionType: InterventionType!
  message: String!
  options: [InterventionOption!]!
  timestamp: DateTime!
}

type Query {
  intervention(id: ID!): Intervention
  interventions(
    filter: InterventionFilter
    pagination: PaginationInput
  ): InterventionConnection!
  teamInterventions(teamId: ID!): [Intervention!]!
  sessionInterventions(sessionId: ID!): [Intervention!]!
  interventionStats(teamId: ID!, timeRange: TimeRangeInput): InterventionStats!
  session(id: ID!): Session
  sessions(
    teamId: ID
    status: SessionStatus
    pagination: PaginationInput
  ): SessionConnection!
}

type Mutation {
  resolveIntervention(
    id: ID!
    resolution: InterventionResolutionInput!
  ): InterventionResolutionResult!
  selectInterventionOption(
    id: ID!
    optionId: ID!
    customInput: String
    reasoning: String
  ): OptionSelectionResult!
  provideCustomResponse(
    id: ID!
    responseText: String!
    responseType: String!
    metadata: JSON
  ): CustomResponseResult!
  escalateIntervention(
    id: ID!
    escalation: EscalationInput!
  ): EscalationResult!
  resumeSession(
    sessionId: ID!
    humanResponse: HumanResponseInput!
  ): SessionResumeResult!
}

type Subscription {
  interventionUpdates(teamId: ID): Intervention!
  sessionUpdates(sessionId: ID): Session!
  teamStatusUpdates(teamId: ID): TeamStatus!
}
```

## Event System

### 1. Event Types

```python
class HumanSupervisionEvent(BaseModel):
    """Base class for human supervision events."""
    event_id: str
    timestamp: datetime
    team_id: str
    agent_name: str
    event_type: str
    context: Dict[str, Any]

class InterventionRequestedEvent(HumanSupervisionEvent):
    intervention_type: InterventionType
    urgency: InterventionUrgency
    timeout: int
    workstation_url: str

class InterventionResolvedEvent(HumanSupervisionEvent):
    intervention_id: str
    resolution: InterventionResolution
    operator_id: str
    resolution_time: float

class EscalationTriggeredEvent(HumanSupervisionEvent):
    intervention_id: str
    escalation_level: int
    escalation_reason: str
    previous_timeout: int
```

### 2. Event Handlers

```python
class EventHandlerRegistry:
    """Registry for event handlers."""
    
    def __init__(self):
        self.handlers = {}
        
    def register_handler(self, event_type: str, handler: Callable):
        """Register an event handler."""
        
    async def handle_event(self, event: HumanSupervisionEvent):
        """Handle an event by calling registered handlers."""

class NotificationEventHandler:
    """Handles notification events."""
    
    async def handle_intervention_requested(self, event: InterventionRequestedEvent):
        """Send notifications for intervention requests."""
        
    async def handle_escalation_triggered(self, event: EscalationTriggeredEvent):
        """Send notifications for escalations."""

class AuditEventHandler:
    """Handles audit events."""
    
    async def handle_intervention_resolved(self, event: InterventionResolvedEvent):
        """Log intervention resolution for audit."""
```

## Workflow Integration

### 1. Session-Based Team Execution

```python
class HumanSupervisionTeamRunner(TeamRunner):
    """Enhanced team runner with session-based human supervision."""
    
    def __init__(self, team: Team, supervision_config: HumanSupervisionConfig):
        super().__init__(team)
        self.supervision_manager = HumanSupervisionManager(supervision_config)
        self.session_manager = SessionManager(supervision_config)
        self.event_handler = HumanSupervisionEventHandler(self.supervision_manager)
        
    async def run_team_stream(
        self,
        message: str,
        debug: bool = False,
        session_id: Optional[str] = None,
        session_context: Optional[Dict[str, Any]] = None,
        max_turns: Optional[int] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Run team with session-based human supervision."""
        
        # Create or resume session
        if session_id:
            session = await self.session_manager.get_session(session_id)
            if session.status == SessionStatus.PAUSED_FOR_INTERVENTION:
                # Resume from intervention point
                yield {"type": "session_resumed", "session_id": session_id}
                message = session.get_resumption_message()
            else:
                session = await self.session_manager.create_session(
                    self.team.id, message, session_context or {}
                )
        else:
            session = await self.session_manager.create_session(
                self.team.id, message, session_context or {}
            )
            session_id = session.session_id
            
        yield {"type": "session_created", "session_id": session_id}
        
        # Run team execution with intervention monitoring
        async for event in super().run_team_stream(message, debug, session_id, session_context, max_turns):
            # Check for intervention triggers
            intervention_request = await self._check_intervention_triggers(event, session)
            
            if intervention_request:
                # Pause session and request human intervention
                await self.session_manager.pause_session_for_intervention(
                    session_id, intervention_request
                )
                
                yield {
                    "type": "intervention_requested",
                    "intervention_id": intervention_request.intervention_id,
                    "session_id": session_id,
                    "agent_name": intervention_request.agent_name,
                    "intervention_type": intervention_request.intervention_type,
                    "message": intervention_request.natural_language_message,
                    "workstation_url": intervention_request.workstation_url,
                    "timeout": intervention_request.timeout
                }
                
                # Session is now paused - wait for human response
                return  # Exit stream, session will be resumed when human responds
                
            # Add event to session history
            session.add_conversation_turn(
                event.get('agent_name', 'unknown'),
                event.get('input', ''),
                event.get('content', '')
            )
            
            yield event
            
        # Mark session as completed
        await self.session_manager.complete_session(session_id)
        yield {"type": "session_completed", "session_id": session_id}
        
    async def resume_session_after_intervention(
        self,
        session_id: str,
        intervention_id: str,
        human_response: HumanResponse
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Resume session execution after human intervention."""
        
        # Update session with human response
        await self.session_manager.update_session_context(
            session_id, {"human_response": human_response}
        )
        
        # Resume execution from intervention point
        session = await self.session_manager.get_session(session_id)
        resumption_context = session.get_context_for_resumption()
        
        yield {"type": "session_resuming", "session_id": session_id}
        
        # Continue execution with human input integrated
        async for event in self.run_team_stream(
            resumption_context["message"],
            debug=False,
            session_id=session_id,
            session_context=resumption_context,
            max_turns=resumption_context.get("remaining_turns")
        ):
            yield event
```

### 2. Agent Integration with Natural Language Escalation

```python
class HumanSupervisionAgent:
    """Agent wrapper with natural language escalation capabilities."""
    
    def __init__(self, agent: Agent, supervision_config: AgentSupervisionConfig):
        self.agent = agent
        self.supervision_config = supervision_config
        self.supervision_manager = HumanSupervisionManager(supervision_config)
        self.escalation_engine = NaturalLanguageEscalationEngine(supervision_config)
        
    async def run_with_supervision(
        self,
        input_data: str,
        context: Dict[str, Any],
        session_id: str
    ) -> AgentResult:
        """Run agent with natural language escalation capabilities."""
        
        # Check for escalation triggers before execution
        escalation_check = await self._check_escalation_triggers(input_data, context)
        if escalation_check.should_escalate:
            # Generate natural language escalation message
            escalation_message = self.escalation_engine.generate_escalation_message(
                self.supervision_config,
                escalation_check.trigger_condition,
                context,
                escalation_check.agent_reasoning
            )
            
            # Request intervention with natural language message
            intervention_request = await self.supervision_manager.request_intervention(
                session_id=session_id,
                intervention_type=escalation_check.intervention_type,
                agent_name=self.agent.name,
                context=context,
                urgency=escalation_check.urgency,
                natural_language_message=escalation_message
            )
            
            # Pause execution and wait for human response
            return AgentResult(
                status="paused_for_intervention",
                intervention_request=intervention_request,
                escalation_message=escalation_message
            )
        
        # Execute agent normally
        result = await self.agent.run(input_data, context)
        
        # Check for post-execution escalation triggers
        post_escalation_check = await self._check_post_execution_triggers(result, context)
        if post_escalation_check.should_escalate:
            escalation_message = self.escalation_engine.generate_escalation_message(
                self.supervision_config,
                post_escalation_check.trigger_condition,
                context,
                post_escalation_check.agent_reasoning
            )
            
            intervention_request = await self.supervision_manager.request_intervention(
                session_id=session_id,
                intervention_type=post_escalation_check.intervention_type,
                agent_name=self.agent.name,
                context=context,
                urgency=post_escalation_check.urgency,
                natural_language_message=escalation_message
            )
            
            return AgentResult(
                status="paused_for_intervention",
                intervention_request=intervention_request,
                escalation_message=escalation_message
            )
                
        return result
        
    async def _check_escalation_triggers(
        self,
        input_data: str,
        context: Dict[str, Any]
    ) -> EscalationCheck:
        """Check if current situation requires escalation."""
        
        escalation_check = EscalationCheck()
        
        # Check budget thresholds
        if "budget" in context and context["budget"] > self.supervision_config.budget_threshold:
            escalation_check.should_escalate = True
            escalation_check.trigger_condition = "budget_exceeded"
            escalation_check.intervention_type = InterventionType.APPROVAL
            escalation_check.urgency = InterventionUrgency.HIGH
            escalation_check.agent_reasoning = f"Budget of ${context['budget']} exceeds threshold of ${self.supervision_config.budget_threshold}"
            
        # Check confidence levels
        elif "confidence" in context and context["confidence"] < 0.7:
            escalation_check.should_escalate = True
            escalation_check.trigger_condition = "confidence_low"
            escalation_check.intervention_type = InterventionType.DECISION
            escalation_check.urgency = InterventionUrgency.NORMAL
            escalation_check.agent_reasoning = f"Confidence level of {context['confidence']:.1%} is below threshold"
            
        # Check for ethical concerns
        elif self._detect_ethical_concerns(input_data, context):
            escalation_check.should_escalate = True
            escalation_check.trigger_condition = "ethical_concern"
            escalation_check.intervention_type = InterventionType.DECISION
            escalation_check.urgency = InterventionUrgency.HIGH
            escalation_check.agent_reasoning = "Detected potential ethical concerns in the request"
            
        return escalation_check
        
    def _detect_ethical_concerns(self, input_data: str, context: Dict[str, Any]) -> bool:
        """Detect potential ethical concerns in input or context."""
        # Implement ethical concern detection logic
        ethical_keywords = ["personal data", "privacy", "discrimination", "bias", "harmful"]
        return any(keyword in input_data.lower() for keyword in ethical_keywords)

class EscalationCheck:
    """Result of escalation trigger check."""
    
    def __init__(self):
        self.should_escalate = False
        self.trigger_condition = ""
        self.intervention_type = InterventionType.DECISION
        self.urgency = InterventionUrgency.NORMAL
        self.agent_reasoning = ""
```

### 3. Natural Language Escalation Templates with Options

```python
class EscalationTemplateEngine:
    """Engine for generating natural language escalation messages with options."""
    
    def __init__(self):
        self.templates = {
            "budget_exceeded": """
I need your approval for a financial decision. 

**Situation**: {{situation}}
**Budget Impact**: ${{budget_amount}}
**Threshold**: ${{budget_threshold}}

Here are the options I'm considering:

**Option 1 (Recommended)**: {{recommendation}}
- Reasoning: {{reasoning}}
- Budget Impact: ${{budget_amount}}
- Risk Level: {{risk_level}}

**Option 2**: {{alternative_recommendation}}
- Reasoning: {{alternative_reasoning}}
- Budget Impact: ${{alternative_amount}}
- Risk Level: {{alternative_risk}}

**Option 3**: Cancel this decision
- Action: Explore other approaches
- Impact: No immediate cost but may delay progress

Which option would you like me to proceed with?
            """,
            
            "confidence_low": """
I'm requesting your guidance on a decision where I have low confidence.

**Situation**: {{situation}}
**My Confidence**: {{confidence}}%
**Context**: {{context}}

Here are the approaches I'm considering:

**Option 1**: Proceed with Caution
- Description: Continue with the current plan but with additional safeguards
- Safeguards: {{safeguards}}
- Confidence Level: {{confidence}}%

**Option 2**: Gather More Information
- Description: Pause to collect additional data before deciding
- Information Needed: {{info_needed}}
- Estimated Time: {{info_gathering_time}}

**Option 3**: Consult Domain Expert
- Description: Get input from a human expert in this area
- Expertise Area: {{expertise_area}}

What approach would you recommend?
            """,
            
            "ethical_concern": """
I've encountered a situation that raises ethical concerns and need your guidance.

**Concern**: {{concern}}
**Context**: {{context}}
**Potential Impact**: {{impact}}

Here are the ethical approaches I'm considering:

**Option 1**: {{ethical_approach_a_title}}
- Description: {{ethical_approach_a_description}}
- Ethical Score: {{ethical_score_a}}
- Risk Level: {{risk_level_a}}

**Option 2**: {{ethical_approach_b_title}}
- Description: {{ethical_approach_b_description}}
- Ethical Score: {{ethical_score_b}}
- Risk Level: {{risk_level_b}}

**Option 3**: Halt and Review
- Description: Stop current action and conduct thorough ethical review
- Action: Pause all activities until ethical review is complete

How should I handle this ethically sensitive situation?
            """,
            
            "team_conflict": """
I've detected a conflict between team members that requires mediation.

**Conflict**: {{conflict_description}}
**Involved Parties**: {{parties}}
**Root Cause**: {{root_cause}}

Here are the resolution approaches I'm considering:

**Option 1**: {{resolution_a_title}}
- Description: {{resolution_a_description}}
- Impact: {{resolution_a_impact}}
- Effort Required: {{resolution_a_effort}}

**Option 2**: {{resolution_b_title}}
- Description: {{resolution_b_description}}
- Impact: {{resolution_b_impact}}
- Effort Required: {{resolution_b_effort}}

**Option 3**: Request Human Mediation
- Description: Have a human supervisor mediate the conflict
- Escalation Level: 1
- Action: Transfer to human supervisor

Which resolution approach do you recommend?
            """,
            
            "external_api_call": """
I need approval before making an external API call that could have significant impact.

**API Call**: {{api_call}}
**Purpose**: {{purpose}}
**Data Being Sent**: {{data}}
**Potential Impact**: {{impact}}

Here are the options I'm considering:

**Option 1 (Recommended)**: Proceed with API Call
- Description: {{recommendation}}
- Security Considerations: {{security}}
- Risk Assessment: {{risk_assessment}}

**Option 2**: Modify API Call
- Description: Adjust the API call to reduce risk
- Modifications: {{modifications}}
- Reduced Risk: {{reduced_risk}}

**Option 3**: Use Alternative Approach
- Description: Find an alternative way to achieve the same goal
- Alternative Method: {{alternative_method}}
- Trade-offs: {{trade_offs}}

**Option 4**: Cancel API Call
- Description: Abandon this approach entirely
- Impact: {{cancellation_impact}}

Should I proceed with the API call, or would you prefer a different approach?
            """
        }
        
    def generate_message_with_options(
        self,
        template_name: str,
        context: Dict[str, Any],
        options: List[InterventionOption]
    ) -> Tuple[str, List[InterventionOption]]:
        """Generate escalation message with options from template."""
        template = self.templates.get(template_name, self.templates["confidence_low"])
        message = template.format(**context)
        
        # Ensure options are properly formatted
        formatted_options = []
        for i, option in enumerate(options, 1):
            formatted_option = InterventionOption(
                option_id=option.option_id,
                label=f"Option {i}: {option.label}",
                description=option.description,
                value=option.value,
                metadata=option.metadata,
                recommended=option.recommended,
                disabled=option.disabled
            )
            formatted_options.append(formatted_option)
            
        return message, formatted_options
        
    def generate_message(
        self,
        template_name: str,
        context: Dict[str, Any]
    ) -> str:
        """Generate escalation message from template."""
        template = self.templates.get(template_name, self.templates["confidence_low"])
        return template.format(**context)
        
    def add_custom_template(self, name: str, template: str):
        """Add custom escalation template."""
        self.templates[name] = template

class OptionGenerator:
    """Generates intervention options based on context and agent reasoning."""
    
    def __init__(self):
        self.option_templates = {
            "budget_exceeded": self._generate_budget_options,
            "confidence_low": self._generate_confidence_options,
            "ethical_concern": self._generate_ethical_options,
            "team_conflict": self._generate_conflict_options,
            "external_api_call": self._generate_api_options
        }
        
    def generate_options(
        self,
        trigger_condition: str,
        context: Dict[str, Any],
        agent_reasoning: str
    ) -> List[InterventionOption]:
        """Generate options for a specific trigger condition."""
        generator = self.option_templates.get(trigger_condition, self._generate_default_options)
        return generator(context, agent_reasoning)
        
    def _generate_budget_options(
        self,
        context: Dict[str, Any],
        agent_reasoning: str
    ) -> List[InterventionOption]:
        """Generate budget-related options."""
        options = []
        
        # Recommended option
        options.append(InterventionOption(
            option_id="approve_recommended",
            label="Approve Recommended Option",
            description=f"{context.get('recommendation', 'Proceed with current plan')} - {agent_reasoning}",
            value="approve",
            metadata={
                "budget_impact": context.get("budget_amount", 0),
                "risk_level": context.get("risk_level", "medium")
            },
            recommended=True
        ))
        
        # Alternative option if available
        if "alternative_recommendation" in context:
            options.append(InterventionOption(
                option_id="approve_alternative",
                label="Approve Alternative Option",
                description=f"{context['alternative_recommendation']} - {context.get('alternative_reasoning', 'Alternative approach')}",
                value="approve_alternative",
                metadata={
                    "budget_impact": context.get("alternative_amount", 0),
                    "risk_level": context.get("alternative_risk", "medium")
                }
            ))
        
        # Reject option
        options.append(InterventionOption(
            option_id="reject",
            label="Reject All Options",
            description="Cancel this decision and explore other approaches",
            value="reject",
            metadata={"action": "cancel"}
        ))
        
        return options
        
    def _generate_confidence_options(
        self,
        context: Dict[str, Any],
        agent_reasoning: str
    ) -> List[InterventionOption]:
        """Generate confidence-related options."""
        options = []
        
        # Proceed cautiously
        options.append(InterventionOption(
            option_id="proceed_cautiously",
            label="Proceed with Caution",
            description="Continue with the current plan but with additional safeguards",
            value="proceed_cautiously",
            metadata={
                "confidence": context.get("confidence", 0.5),
                "safeguards": context.get("safeguards", "Additional monitoring")
            },
            recommended=True
        ))
        
        # Gather more info
        options.append(InterventionOption(
            option_id="gather_more_info",
            label="Gather More Information",
            description="Pause to collect additional data before deciding",
            value="gather_info",
            metadata={
                "info_needed": context.get("info_needed", "Additional context"),
                "estimated_time": context.get("info_gathering_time", "30 minutes")
            }
        ))
        
        # Consult expert
        options.append(InterventionOption(
            option_id="consult_expert",
            label="Consult Domain Expert",
            description="Get input from a human expert in this area",
            value="consult_expert",
            metadata={
                "expertise_area": context.get("expertise_area", "General domain knowledge")
            }
        ))
        
        return options
        
    def _generate_default_options(
        self,
        context: Dict[str, Any],
        agent_reasoning: str
    ) -> List[InterventionOption]:
        """Generate default options when no specific generator is available."""
        return [
            InterventionOption(
                option_id="proceed",
                label="Proceed",
                description="Continue with the current approach",
                value="proceed",
                recommended=True
            ),
            InterventionOption(
                option_id="modify",
                label="Modify Approach",
                description="Adjust the current approach based on your input",
                value="modify"
            ),
            InterventionOption(
                option_id="cancel",
                label="Cancel",
                description="Stop current action and explore alternatives",
                value="cancel"
            )
        ]
```

## Security & Permissions

### 1. Authentication & Authorization

```python
class HumanSupervisionSecurityManager:
    """Manages security for human supervision features."""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.auth_provider = OAuth2Provider(config.auth)
        self.rbac_manager = RBACManager(config.authorization)
        
    async def authenticate_user(self, token: str) -> User:
        """Authenticate user and return user object."""
        
    async def authorize_intervention_access(
        self,
        user: User,
        intervention: Intervention
    ) -> bool:
        """Check if user can access specific intervention."""
        
    async def authorize_intervention_resolution(
        self,
        user: User,
        intervention: Intervention,
        resolution: InterventionResolution
    ) -> bool:
        """Check if user can resolve intervention with specific resolution."""
```

### 2. Data Encryption & Privacy

```python
class DataEncryptionManager:
    """Manages data encryption for sensitive information."""
    
    def __init__(self, config: EncryptionConfig):
        self.config = config
        self.encryption_key = self._load_encryption_key()
        
    def encrypt_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt sensitive data in intervention context."""
        
    def decrypt_sensitive_data(self, encrypted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Decrypt sensitive data."""
        
    def mask_sensitive_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mask sensitive fields for display."""
```

## Implementation Phases

### Phase 1: MCP Server Foundation (Weeks 1-4)

**Deliverables:**
- Human supervision MCP server implementation
- Basic intervention types (decision, follow-up, approval)
- Core supervision manager
- Basic workstation client
- Prompt integration for agents

**Tasks:**
1. Implement `HumanSupervisionMCPServer` class
2. Create `HumanSupervisionConfig` schema
3. Implement basic intervention types and options
4. Create workstation client with REST API
5. Integrate MCP server with existing tool system
6. Update prompt injection in `prompts.py`
7. Add basic event handling

**Success Criteria:**
- MCP server can be loaded as a tool
- Agents can request human intervention via tool calls
- Basic intervention types work
- Workstation can receive and display interventions
- Human can resolve interventions
- Team execution continues after resolution

### Phase 2: Advanced Features (Weeks 5-8)

**Deliverables:**
- Escalation system
- Advanced notification system
- Real-time WebSocket communication
- UI customization
- Performance optimization

**Tasks:**
1. Implement escalation manager
2. Create notification service with multiple channels
3. Add WebSocket support for real-time updates
4. Implement UI customization features
5. Add performance monitoring and optimization
6. Create comprehensive logging and metrics

**Success Criteria:**
- Escalation system works correctly
- Multiple notification channels functional
- Real-time updates work smoothly
- UI customization options available
- Performance meets requirements

### Phase 3: Enterprise Features (Weeks 9-12)

**Deliverables:**
- Advanced security and compliance
- Audit logging
- Advanced intervention types
- Custom triggers and conditions
- Analytics and reporting

**Tasks:**
1. Implement comprehensive security features
2. Add audit logging and compliance features
3. Create advanced intervention types
4. Implement custom trigger system
5. Add analytics and reporting capabilities
6. Create comprehensive documentation

**Success Criteria:**
- Security requirements met
- Compliance standards supported
- Advanced features functional
- Analytics provide valuable insights
- Documentation complete

### Phase 4: Integration & Testing (Weeks 13-16)

**Deliverables:**
- Complete integration with Gnosari Cloud
- Comprehensive testing suite
- Performance testing
- Security testing
- User acceptance testing

**Tasks:**
1. Complete integration with Gnosari Cloud workstation
2. Create comprehensive test suite
3. Perform performance testing
4. Conduct security testing
5. User acceptance testing
6. Bug fixes and optimizations

**Success Criteria:**
- Full integration with Gnosari Cloud
- All tests pass
- Performance requirements met
- Security requirements validated
- User acceptance achieved

## Testing Strategy

### 1. Unit Testing

```python
class TestHumanSupervisionManager:
    """Unit tests for human supervision manager."""
    
    async def test_request_intervention(self):
        """Test intervention request creation."""
        
    async def test_resolve_intervention(self):
        """Test intervention resolution."""
        
    async def test_escalation_flow(self):
        """Test escalation functionality."""
        
    async def test_timeout_handling(self):
        """Test timeout scenarios."""
```

### 2. Integration Testing

```python
class TestHumanSupervisionIntegration:
    """Integration tests for human supervision."""
    
    async def test_team_execution_with_intervention(self):
        """Test team execution with human intervention."""
        
    async def test_workstation_communication(self):
        """Test communication with workstation."""
        
    async def test_notification_delivery(self):
        """Test notification delivery."""
```

### 3. End-to-End Testing

```python
class TestHumanSupervisionE2E:
    """End-to-end tests for human supervision."""
    
    async def test_complete_intervention_flow(self):
        """Test complete intervention flow from request to resolution."""
        
    async def test_escalation_scenario(self):
        """Test escalation scenario."""
        
    async def test_multiple_concurrent_interventions(self):
        """Test handling multiple concurrent interventions."""
```

### 4. Performance Testing

```python
class TestHumanSupervisionPerformance:
    """Performance tests for human supervision."""
    
    async def test_intervention_response_time(self):
        """Test intervention response time."""
        
    async def test_concurrent_intervention_handling(self):
        """Test handling concurrent interventions."""
        
    async def test_workstation_connection_scalability(self):
        """Test workstation connection scalability."""
```

## Monitoring & Observability

### 1. Metrics

```python
class HumanSupervisionMetrics:
    """Metrics for human supervision system."""
    
    def __init__(self):
        self.intervention_requests_total = Counter("intervention_requests_total")
        self.intervention_resolution_time = Histogram("intervention_resolution_time")
        self.escalation_count = Counter("escalation_count")
        self.timeout_count = Counter("timeout_count")
        self.active_interventions = Gauge("active_interventions")
        
    def record_intervention_request(self, intervention_type: str):
        """Record intervention request metric."""
        
    def record_intervention_resolution(self, resolution_time: float):
        """Record intervention resolution time."""
        
    def record_escalation(self, escalation_level: int):
        """Record escalation metric."""
```

### 2. Logging

```python
class HumanSupervisionLogger:
    """Structured logging for human supervision."""
    
    def __init__(self):
        self.logger = structlog.get_logger("human_supervision")
        
    def log_intervention_request(self, intervention: InterventionRequest):
        """Log intervention request."""
        
    def log_intervention_resolution(self, resolution: InterventionResolution):
        """Log intervention resolution."""
        
    def log_escalation(self, escalation: EscalationEvent):
        """Log escalation event."""
```

### 3. Health Checks

```python
class HumanSupervisionHealthCheck:
    """Health checks for human supervision system."""
    
    async def check_workstation_connectivity(self) -> HealthStatus:
        """Check workstation connectivity."""
        
    async def check_intervention_queue_health(self) -> HealthStatus:
        """Check intervention queue health."""
        
    async def check_notification_service_health(self) -> HealthStatus:
        """Check notification service health."""
```

## Intervention Options System

### 1. Option Types and Categories

```python
class OptionCategory(Enum):
    """Categories of intervention options."""
    APPROVAL = "approval"           # Approve/reject decisions
    SELECTION = "selection"         # Choose from multiple alternatives
    MODIFICATION = "modification"    # Modify existing approach
    ESCALATION = "escalation"       # Escalate to higher authority
    INFORMATION = "information"     # Request more information
    EXPERT_CONSULTATION = "expert_consultation"  # Consult domain expert
    CUSTOM = "custom"               # Custom response

class OptionMetadata:
    """Metadata for intervention options."""
    
    def __init__(self):
        self.budget_impact: Optional[float] = None
        self.risk_level: Optional[str] = None
        self.confidence_score: Optional[float] = None
        self.estimated_time: Optional[str] = None
        self.resource_requirements: Optional[Dict[str, Any]] = None
        self.compliance_impact: Optional[str] = None
        self.escalation_level: Optional[int] = None
        self.custom_fields: Dict[str, Any] = {}
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        return {
            "budget_impact": self.budget_impact,
            "risk_level": self.risk_level,
            "confidence_score": self.confidence_score,
            "estimated_time": self.estimated_time,
            "resource_requirements": self.resource_requirements,
            "compliance_impact": self.compliance_impact,
            "escalation_level": self.escalation_level,
            "custom_fields": self.custom_fields
        }
```

### 2. Dynamic Option Generation

```python
class DynamicOptionGenerator:
    """Generates options dynamically based on context and agent capabilities."""
    
    def __init__(self, config: HumanSupervisionConfig):
        self.config = config
        self.option_templates = self._load_option_templates()
        self.context_analyzer = ContextAnalyzer()
        
    def generate_options_for_context(
        self,
        intervention_type: InterventionType,
        context: Dict[str, Any],
        agent_capabilities: List[str],
        team_constraints: Dict[str, Any]
    ) -> List[InterventionOption]:
        """Generate options based on specific context and constraints."""
        
        base_options = self._get_base_options(intervention_type)
        contextual_options = self._generate_contextual_options(context, agent_capabilities)
        constraint_filtered_options = self._filter_by_constraints(
            base_options + contextual_options, team_constraints
        )
        
        return self._rank_and_prioritize_options(constraint_filtered_options, context)
        
    def _generate_contextual_options(
        self,
        context: Dict[str, Any],
        agent_capabilities: List[str]
    ) -> List[InterventionOption]:
        """Generate options based on current context."""
        options = []
        
        # Budget-aware options
        if "budget" in context:
            options.extend(self._generate_budget_options(context))
            
        # Risk-aware options
        if "risk_level" in context:
            options.extend(self._generate_risk_options(context))
            
        # Time-sensitive options
        if "urgency" in context:
            options.extend(self._generate_urgency_options(context))
            
        # Capability-based options
        for capability in agent_capabilities:
            options.extend(self._generate_capability_options(capability, context))
            
        return options
        
    def _rank_and_prioritize_options(
        self,
        options: List[InterventionOption],
        context: Dict[str, Any]
    ) -> List[InterventionOption]:
        """Rank options by relevance and priority."""
        # Implement ranking logic based on context
        scored_options = []
        for option in options:
            score = self._calculate_option_score(option, context)
            scored_options.append((score, option))
            
        # Sort by score (highest first) and return options
        scored_options.sort(key=lambda x: x[0], reverse=True)
        return [option for _, option in scored_options]
```

### 3. Option Validation and Constraints

```python
class OptionValidator:
    """Validates intervention options against constraints and policies."""
    
    def __init__(self, config: HumanSupervisionConfig):
        self.config = config
        self.policy_engine = PolicyEngine(config.policies)
        
    def validate_option(
        self,
        option: InterventionOption,
        context: Dict[str, Any],
        user_permissions: List[str]
    ) -> ValidationResult:
        """Validate an option against constraints and user permissions."""
        
        validation_result = ValidationResult()
        
        # Check policy compliance
        policy_result = self.policy_engine.check_option_policy(option, context)
        if not policy_result.allowed:
            validation_result.add_error(f"Policy violation: {policy_result.reason}")
            
        # Check user permissions
        permission_result = self._check_user_permissions(option, user_permissions)
        if not permission_result.allowed:
            validation_result.add_error(f"Permission denied: {permission_result.reason}")
            
        # Check resource constraints
        resource_result = self._check_resource_constraints(option, context)
        if not resource_result.allowed:
            validation_result.add_error(f"Resource constraint: {resource_result.reason}")
            
        return validation_result
        
    def filter_valid_options(
        self,
        options: List[InterventionOption],
        context: Dict[str, Any],
        user_permissions: List[str]
    ) -> List[InterventionOption]:
        """Filter options to only include valid ones."""
        valid_options = []
        
        for option in options:
            validation_result = self.validate_option(option, context, user_permissions)
            if validation_result.is_valid:
                valid_options.append(option)
            else:
                # Log validation errors for debugging
                self.logger.warning(f"Option {option.option_id} filtered out: {validation_result.errors}")
                
        return valid_options

class ValidationResult:
    """Result of option validation."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def add_error(self, error: str):
        """Add a validation error."""
        self.errors.append(error)
        
    def add_warning(self, warning: str):
        """Add a validation warning."""
        self.warnings.append(warning)
        
    @property
    def is_valid(self) -> bool:
        """Check if validation passed."""
        return len(self.errors) == 0
```

### 4. Option Selection Processing

```python
class OptionSelectionProcessor:
    """Processes human option selections and integrates them into session context."""
    
    def __init__(self, config: HumanSupervisionConfig):
        self.config = config
        self.session_manager = SessionManager(config)
        self.context_updater = ContextUpdater()
        
    async def process_option_selection(
        self,
        intervention_id: str,
        selected_option: InterventionOption,
        custom_input: Optional[str] = None,
        human_reasoning: Optional[str] = None
    ) -> OptionProcessingResult:
        """Process human option selection and update session context."""
        
        # Get intervention and session
        intervention = await self._get_intervention(intervention_id)
        session = await self.session_manager.get_session(intervention.session_id)
        
        # Validate selection
        validation_result = await self._validate_selection(selected_option, intervention)
        if not validation_result.is_valid:
            return OptionProcessingResult(
                success=False,
                errors=validation_result.errors,
                message="Option selection validation failed"
            )
            
        # Process the selected option
        context_updates = await self._process_selected_option(
            selected_option, custom_input, human_reasoning, intervention.context
        )
        
        # Update session context
        await self.session_manager.update_session_context(
            intervention.session_id, context_updates
        )
        
        # Create human response
        human_response = HumanResponse(
            response_type="select_option",
            content=f"Selected option: {selected_option.label}",
            selected_option=selected_option,
            custom_input=custom_input,
            metadata={
                "human_reasoning": human_reasoning,
                "selection_timestamp": datetime.now().isoformat()
            }
        )
        
        # Resume session
        await self.session_manager.resume_session_after_intervention(
            intervention.session_id, intervention_id, human_response
        )
        
        return OptionProcessingResult(
            success=True,
            session_id=intervention.session_id,
            intervention_id=intervention_id,
            selected_option=selected_option,
            context_updates=context_updates,
            message="Option selection processed successfully"
        )
        
    async def _process_selected_option(
        self,
        selected_option: InterventionOption,
        custom_input: Optional[str],
        human_reasoning: Optional[str],
        current_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process the selected option and generate context updates."""
        
        context_updates = {
            "selected_option": selected_option.to_dict(),
            "option_selection_timestamp": datetime.now().isoformat(),
            "human_reasoning": human_reasoning
        }
        
        if custom_input:
            context_updates["custom_input"] = custom_input
            
        # Add option-specific context updates
        if selected_option.value == "approve":
            context_updates["approval_granted"] = True
            context_updates["approval_reasoning"] = human_reasoning
            
        elif selected_option.value == "reject":
            context_updates["approval_denied"] = True
            context_updates["rejection_reasoning"] = human_reasoning
            
        elif selected_option.value == "modify":
            context_updates["modification_requested"] = True
            context_updates["modification_details"] = custom_input
            
        elif selected_option.value == "escalate":
            context_updates["escalation_requested"] = True
            context_updates["escalation_level"] = selected_option.metadata.get("escalation_level", 1)
            
        # Add metadata from selected option
        context_updates.update(selected_option.metadata)
        
        return context_updates
```

## Conclusion

This comprehensive implementation plan provides a robust, scalable, and enterprise-ready human-in-the-loop system for Gnosari AI Teams. The design follows SOLID principles, ensures high quality through comprehensive testing, and provides the flexibility needed for various use cases while maintaining security and compliance standards.

### Key Innovations

1. **MCP Server Integration**: Human supervision implemented as a standard MCP server tool, following existing Gnosari architecture patterns
2. **Session-Based Integration**: Leverages existing Gnosari session system - human responses are integrated into session context and team execution continues naturally
3. **Natural Language Escalation**: Agents receive natural language instructions on when and how to escalate, making the system intuitive
4. **Dynamic Option Generation**: Agents can suggest multiple options with rich metadata, making human decisions more informed
5. **Flexible Configuration**: Extensive configuration options allow customization for different organizational needs
6. **Real-Time Integration**: Seamless integration with Gnosari Cloud workstation for real-time human interaction

### Benefits

- **Improved Decision Quality**: Human oversight ensures better decisions in complex scenarios
- **Reduced Risk**: Proactive intervention prevents costly mistakes
- **Enhanced Trust**: Transparent escalation process builds confidence in AI systems
- **Scalable Operations**: Session-based approach allows handling multiple concurrent interventions
- **Compliance Ready**: Built-in audit trails and compliance features meet enterprise requirements

The phased approach allows for iterative development and validation, ensuring that each component is thoroughly tested before moving to the next phase. The extensive configuration options provide the flexibility needed for different organizational requirements while maintaining simplicity for basic use cases.

The integration with Gnosari Cloud workstation provides a seamless user experience, while leveraging the existing session system ensures natural workflow continuation. The option-based intervention system makes human interaction more efficient and effective, reducing the cognitive load on human operators while providing them with the context and alternatives they need to make informed decisions.


### Implementation Simplicity

Since Gnosari already has a robust session system, the human-in-the-loop implementation becomes straightforward:

1. **Agent calls MCP tool**: Agent uses `request_human_intervention` tool when it needs human input
2. **Session status updated**: Session status changes to `WAITING_FOR_HUMAN`
3. **Workstation receives request**: Human sees the intervention request with options in the workstation
4. **Human responds**: Human selects an option or provides custom input
5. **Session status updated**: Session status changes to `PROCESSING_INTERVENTION`
6. **Session continues**: Human response is integrated into the session context, and team execution continues naturally
7. **Session status updated**: Session status changes to `CONTINUING_ASYNC` or `ACTIVE`

This approach eliminates the complexity of pause/resume mechanisms and leverages the existing session infrastructure for seamless integration while providing clear status tracking.

---

## API and Database Components (Gnosari Cloud Implementation)

*Note: The following components will be implemented in the Gnosari Cloud API, not in the Gnosari engine.*

### Database Schema Updates

#### Sessions Table Enhancement

```sql
-- Add status column to sessions table
ALTER TABLE sessions ADD COLUMN status VARCHAR(50) DEFAULT 'active';

-- Add intervention tracking columns
ALTER TABLE sessions ADD COLUMN current_intervention_id VARCHAR(255) NULL;
ALTER TABLE sessions ADD COLUMN intervention_count INTEGER DEFAULT 0;
ALTER TABLE sessions ADD COLUMN last_intervention_at TIMESTAMP NULL;

-- Create index for status queries
CREATE INDEX idx_sessions_status ON sessions(status);
CREATE INDEX idx_sessions_intervention ON sessions(current_intervention_id);
```

#### Interventions Table

```sql
-- Create interventions table
CREATE TABLE interventions (
    id VARCHAR(255) PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    agent_name VARCHAR(255) NOT NULL,
    intervention_type VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    context JSON,
    urgency VARCHAR(20) DEFAULT 'normal',
    options JSON,
    status VARCHAR(50) DEFAULT 'pending',
    workstation_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    resolved_by VARCHAR(255) NULL,
    human_response JSON,
    timeout INTEGER DEFAULT 300,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

-- Create indexes
CREATE INDEX idx_interventions_session ON interventions(session_id);
CREATE INDEX idx_interventions_status ON interventions(status);
CREATE INDEX idx_interventions_created ON interventions(created_at);
```

#### Session Status Values

```python
class SessionStatus(Enum):
    ACTIVE = "active"                           # Normal execution
    WAITING_FOR_HUMAN = "waiting_for_human"     # Waiting for human intervention
    PROCESSING_INTERVENTION = "processing_intervention"  # Processing human response
    CONTINUING_ASYNC = "continuing_async"       # Continuing in async mode
    COMPLETED = "completed"                     # Session completed
    FAILED = "failed"                           # Session failed
    TIMEOUT = "timeout"                         # Session timed out

class InterventionStatus(Enum):
    PENDING = "pending"                         # Waiting for human response
    RESOLVED = "resolved"                       # Human responded
    TIMEOUT = "timeout"                         # Timed out
    CANCELLED = "cancelled"                     # Cancelled
```

### API Endpoints (Gnosari Cloud)

#### Intervention Management

```python
# POST /api/interventions
async def create_intervention(
    intervention_data: CreateInterventionRequest,
    current_user: User = Depends(get_current_user)
) -> InterventionResponse:
    """Create a new intervention request."""
    
    # Create intervention record
    intervention = await intervention_service.create_intervention(intervention_data)
    
    # Update session status
    await session_service.update_session_status(
        intervention_data.session_id,
        SessionStatus.WAITING_FOR_HUMAN,
        intervention.id
    )
    
    # Send notifications
    await notification_service.send_intervention_notification(intervention)
    
    return InterventionResponse.from_intervention(intervention)

# GET /api/interventions/{intervention_id}
async def get_intervention(
    intervention_id: str,
    current_user: User = Depends(get_current_user)
) -> InterventionResponse:
    """Get intervention details."""
    
    intervention = await intervention_service.get_intervention(intervention_id)
    if not intervention:
        raise HTTPException(status_code=404, detail="Intervention not found")
    
    return InterventionResponse.from_intervention(intervention)

# POST /api/interventions/{intervention_id}/resolve
async def resolve_intervention(
    intervention_id: str,
    resolution: InterventionResolutionRequest,
    current_user: User = Depends(get_current_user)
) -> ResolutionResponse:
    """Resolve an intervention."""
    
    # Update intervention
    intervention = await intervention_service.resolve_intervention(
        intervention_id, resolution, current_user.id
    )
    
    # Update session status
    await session_service.update_session_status(
        intervention.session_id,
        SessionStatus.PROCESSING_INTERVENTION
    )
    
    # Queue team continuation
    await queue_service.queue_team_continuation(
        intervention.session_id,
        intervention_id,
        resolution.to_dict()
    )
    
    return ResolutionResponse(
        success=True,
        intervention_id=intervention_id,
        session_id=intervention.session_id,
        message="Intervention resolved successfully"
    )

# GET /api/sessions/{session_id}/interventions
async def get_session_interventions(
    session_id: str,
    current_user: User = Depends(get_current_user)
) -> List[InterventionResponse]:
    """Get all interventions for a session."""
    
    interventions = await intervention_service.get_session_interventions(session_id)
    return [InterventionResponse.from_intervention(i) for i in interventions]
```

#### Session Management

```python
# GET /api/sessions/{session_id}
async def get_session(
    session_id: str,
    current_user: User = Depends(get_current_user)
) -> SessionResponse:
    """Get session details and current status."""
    
    session = await session_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return SessionResponse.from_session(session)

# GET /api/sessions
async def list_sessions(
    status: Optional[SessionStatus] = None,
    team_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user)
) -> SessionListResponse:
    """List sessions with filtering."""
    
    sessions = await session_service.list_sessions(
        status=status,
        team_id=team_id,
        limit=limit,
        offset=offset
    )
    
    return SessionListResponse(
        sessions=[SessionResponse.from_session(s) for s in sessions],
        total=len(sessions),
        limit=limit,
        offset=offset
    )

# POST /api/sessions/{session_id}/status
async def update_session_status(
    session_id: str,
    status_update: SessionStatusUpdate,
    current_user: User = Depends(get_current_user)
) -> SessionResponse:
    """Update session status."""
    
    session = await session_service.update_session_status(
        session_id,
        status_update.status,
        status_update.intervention_id
    )
    
    return SessionResponse.from_session(session)
```

#### WebSocket Events

```python
# WebSocket endpoint for real-time updates
@app.websocket("/ws/interventions/{session_id}")
async def websocket_interventions(
    websocket: WebSocket,
    session_id: str,
    token: str = Query(...)
):
    """WebSocket for real-time intervention updates."""
    
    # Authenticate user
    user = await auth_service.authenticate_token(token)
    if not user:
        await websocket.close(code=1008, reason="Unauthorized")
        return
    
    await websocket.accept()
    
    try:
        # Subscribe to session events
        async for event in event_service.subscribe_to_session_events(session_id):
            await websocket.send_json(event.to_dict())
    except WebSocketDisconnect:
        pass
    finally:
        await websocket.close()

# Event types for WebSocket
class InterventionEvent(BaseModel):
    event_type: str  # "intervention_created", "intervention_resolved", "status_changed"
    session_id: str
    intervention_id: Optional[str] = None
    data: Dict[str, Any]
    timestamp: datetime
```

### Service Layer (Gnosari Cloud)

#### Intervention Service

```python
class InterventionService:
    """Service for managing interventions."""
    
    def __init__(self, db_client: DatabaseClient):
        self.db_client = db_client
        
    async def create_intervention(
        self,
        intervention_data: CreateInterventionRequest
    ) -> Intervention:
        """Create a new intervention."""
        
        intervention = Intervention(
            id=f"intervention_{uuid.uuid4()}",
            session_id=intervention_data.session_id,
            agent_name=intervention_data.agent_name,
            intervention_type=intervention_data.intervention_type,
            message=intervention_data.message,
            context=intervention_data.context,
            urgency=intervention_data.urgency,
            options=intervention_data.options,
            status=InterventionStatus.PENDING,
            timeout=intervention_data.timeout or 300,
            created_at=datetime.now()
        )
        
        await self.db_client.create_intervention(intervention)
        return intervention
        
    async def resolve_intervention(
        self,
        intervention_id: str,
        resolution: InterventionResolutionRequest,
        user_id: str
    ) -> Intervention:
        """Resolve an intervention."""
        
        intervention = await self.db_client.get_intervention(intervention_id)
        if not intervention:
            raise ValueError(f"Intervention {intervention_id} not found")
            
        intervention.status = InterventionStatus.RESOLVED
        intervention.resolved_at = datetime.now()
        intervention.resolved_by = user_id
        intervention.human_response = resolution.to_dict()
        
        await self.db_client.update_intervention(intervention)
        return intervention
```

#### Session Service

```python
class SessionService:
    """Service for managing sessions."""
    
    def __init__(self, db_client: DatabaseClient):
        self.db_client = db_client
        
    async def update_session_status(
        self,
        session_id: str,
        status: SessionStatus,
        intervention_id: Optional[str] = None
    ) -> Session:
        """Update session status."""
        
        session = await self.db_client.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
            
        session.status = status
        session.updated_at = datetime.now()
        
        if intervention_id:
            session.current_intervention_id = intervention_id
            session.intervention_count += 1
            session.last_intervention_at = datetime.now()
            
        await self.db_client.update_session(session)
        return session
        
    async def cleanup_stale_sessions(self, timeout_hours: int = 24) -> int:
        """Clean up stale sessions."""
        
        cutoff_time = datetime.now() - timedelta(hours=timeout_hours)
        
        stale_sessions = await self.db_client.get_stale_sessions(
            status=SessionStatus.WAITING_FOR_HUMAN.value,
            cutoff_time=cutoff_time
        )
        
        cleaned_count = 0
        for session in stale_sessions:
            await self.update_session_status(session.id, SessionStatus.TIMEOUT)
            cleaned_count += 1
            
        return cleaned_count
```

### Queue Service (Gnosari Cloud)

```python
class QueueService:
    """Service for managing queue operations."""
    
    def __init__(self, celery_app):
        self.celery_app = celery_app
        
    async def queue_team_continuation(
        self,
        session_id: str,
        intervention_id: str,
        human_response: Dict[str, Any],
        priority: int = 5
    ) -> str:
        """Queue team continuation with human response."""
        
        message_data = {
            "session_id": session_id,
            "intervention_id": intervention_id,
            "human_response": human_response,
            "task_type": "team_continuation_with_context",
            "priority": priority,
            "created_at": datetime.now().isoformat()
        }
        
        task = self.celery_app.send_task(
            'gnosari.queue.consumers.team_execution.process_team_continuation_with_context',
            args=[message_data],
            priority=priority
        )
        
        return task.id
```

This separation ensures that the Gnosari engine implementation focuses on the MCP server and tool integration, while the API and database components are clearly defined for the Gnosari Cloud implementation.