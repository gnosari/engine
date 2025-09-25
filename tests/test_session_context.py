"""
Tests for SessionContext schema validation and functionality.
"""

import pytest
from pydantic import ValidationError
from gnosari.schemas import SessionContext


class TestSessionContext:
    """Test SessionContext schema validation."""
    
    def test_session_context_creation(self):
        """Test creating a valid SessionContext."""
        context = SessionContext(
            team_id="test_team_1",
            agent_id="test_agent_1"
        )
        
        assert context.team_id == "test_team_1"
        assert context.agent_id == "test_agent_1"
        assert context.account_id is None
        assert context.session_id is None
        assert context.original_config == {}
        assert context.metadata == {}
    
    def test_session_context_with_optional_fields(self):
        """Test creating SessionContext with all optional fields."""
        context = SessionContext(
            team_id="test_team_1",
            agent_id="test_agent_1",
            account_id=12345,
            session_id="sess_abc123",
            original_config={"id": "test_team_1", "name": "Test Team"},
            metadata={"key": "value", "priority": 5}
        )
        
        assert context.team_id == "test_team_1"
        assert context.agent_id == "test_agent_1"
        assert context.account_id == 12345
        assert context.session_id == "sess_abc123"
        assert context.original_config == {"id": "test_team_1", "name": "Test Team"}
        assert context.metadata == {"key": "value", "priority": 5}
    
    def test_session_context_missing_required_team_id(self):
        """Test that team_id is required."""
        with pytest.raises(ValidationError) as excinfo:
            SessionContext(agent_id="test_agent_1")
        
        assert "team_id" in str(excinfo.value)
        assert "Field required" in str(excinfo.value)
    
    def test_session_context_missing_required_agent_id(self):
        """Test that agent_id is required."""
        with pytest.raises(ValidationError) as excinfo:
            SessionContext(team_id="test_team_1")
        
        assert "agent_id" in str(excinfo.value)
        assert "Field required" in str(excinfo.value)
    
    def test_session_context_serialization(self):
        """Test SessionContext serialization to dict."""
        context = SessionContext(
            team_id="test_team_1",
            agent_id="test_agent_1",
            account_id=12345,
            session_id="sess_abc123"
        )
        
        data = context.model_dump()
        
        assert data["team_id"] == "test_team_1"
        assert data["agent_id"] == "test_agent_1"
        assert data["account_id"] == 12345
        assert data["session_id"] == "sess_abc123"
        assert data["metadata"] == {}
    
    def test_session_context_serialization_exclude_none(self):
        """Test SessionContext serialization excluding None values."""
        context = SessionContext(
            team_id="test_team_1",
            agent_id="test_agent_1"
        )
        
        data = context.model_dump(exclude_none=True)
        
        assert data["team_id"] == "test_team_1"
        assert data["agent_id"] == "test_agent_1"
        assert "account_id" not in data
        assert "session_id" not in data
        assert data["metadata"] == {}
    
    def test_session_context_deserialization(self):
        """Test creating SessionContext from dict."""
        data = {
            "team_id": "test_team_1",
            "agent_id": "test_agent_1",
            "account_id": 12345,
            "session_id": "sess_abc123",
            "metadata": {"env": "test"}
        }
        
        context = SessionContext(**data)
        
        assert context.team_id == "test_team_1"
        assert context.agent_id == "test_agent_1"
        assert context.account_id == 12345
        assert context.session_id == "sess_abc123"
        assert context.metadata == {"env": "test"}
    
    def test_session_context_invalid_account_id_type(self):
        """Test validation error for invalid account_id type."""
        with pytest.raises(ValidationError) as excinfo:
            SessionContext(
                team_id="test_team_1",
                agent_id="test_agent_1",
                account_id="invalid_string"
            )
        
        assert "account_id" in str(excinfo.value)
    
    def test_session_context_invalid_metadata_type(self):
        """Test validation error for invalid metadata type."""
        with pytest.raises(ValidationError) as excinfo:
            SessionContext(
                team_id="test_team_1",
                agent_id="test_agent_1",
                metadata="invalid_string"
            )
        
        assert "metadata" in str(excinfo.value)


class TestSessionContextHelpers:
    """Test helper methods in BaseTool for session context access."""
    
    def test_get_session_team_id_from_dict(self):
        """Test extracting team_id from dict."""
        from gnosari.tools.base import BaseTool
        
        session_context = {
            "team_id": "test_team_1",
            "agent_id": "test_agent_1"
        }
        
        team_id = BaseTool.get_session_team_id(session_context)
        assert team_id == "test_team_1"
    
    def test_get_session_team_id_from_object(self):
        """Test extracting team_id from SessionContext object."""
        from gnosari.tools.base import BaseTool
        
        context = SessionContext(
            team_id="test_team_1",
            agent_id="test_agent_1"
        )
        
        team_id = BaseTool.get_session_team_id(context)
        assert team_id == "test_team_1"
    
    def test_get_session_agent_id_from_dict(self):
        """Test extracting agent_id from dict."""
        from gnosari.tools.base import BaseTool
        
        session_context = {
            "team_id": "test_team_1",
            "agent_id": "test_agent_1"
        }
        
        agent_id = BaseTool.get_session_agent_id(session_context)
        assert agent_id == "test_agent_1"
    
    def test_get_session_agent_id_from_object(self):
        """Test extracting agent_id from SessionContext object."""
        from gnosari.tools.base import BaseTool
        
        context = SessionContext(
            team_id="test_team_1",
            agent_id="test_agent_1"
        )
        
        agent_id = BaseTool.get_session_agent_id(context)
        assert agent_id == "test_agent_1"
    
    def test_get_session_account_id_from_dict(self):
        """Test extracting account_id from dict."""
        from gnosari.tools.base import BaseTool
        
        session_context = {
            "team_id": "test_team_1",
            "agent_id": "test_agent_1",
            "account_id": 12345
        }
        
        account_id = BaseTool.get_session_account_id(session_context)
        assert account_id == 12345
    
    def test_get_session_account_id_from_object(self):
        """Test extracting account_id from SessionContext object."""
        from gnosari.tools.base import BaseTool
        
        context = SessionContext(
            team_id="test_team_1",
            agent_id="test_agent_1",
            account_id=12345
        )
        
        account_id = BaseTool.get_session_account_id(context)
        assert account_id == 12345
    
    def test_helper_methods_with_none(self):
        """Test helper methods return None for empty input."""
        from gnosari.tools.base import BaseTool
        
        assert BaseTool.get_session_team_id(None) is None
        assert BaseTool.get_session_agent_id(None) is None
        assert BaseTool.get_session_account_id(None) is None
    
    def test_helper_methods_with_empty_dict(self):
        """Test helper methods return None for empty dict."""
        from gnosari.tools.base import BaseTool
        
        session_context = {}
        assert BaseTool.get_session_team_id(session_context) is None
        assert BaseTool.get_session_agent_id(session_context) is None
        assert BaseTool.get_session_account_id(session_context) is None
    
    def test_validate_session_context_success(self):
        """Test successful validation of session context dict."""
        from gnosari.tools.base import BaseTool
        
        session_context = {
            "team_id": "test_team_1",
            "agent_id": "test_agent_1",
            "account_id": 12345
        }
        
        validated = BaseTool.validate_session_context(session_context)
        assert validated is not None
        assert isinstance(validated, SessionContext)
        assert validated.team_id == "test_team_1"
        assert validated.agent_id == "test_agent_1"
        assert validated.account_id == 12345
    
    def test_validate_session_context_failure(self):
        """Test validation failure for invalid session context."""
        from gnosari.tools.base import BaseTool
        
        # Missing required fields
        session_context = {"account_id": 12345}
        
        validated = BaseTool.validate_session_context(session_context)
        assert validated is None
    
    def test_validate_session_context_none(self):
        """Test validation with None input."""
        from gnosari.tools.base import BaseTool
        
        validated = BaseTool.validate_session_context(None)
        assert validated is None
    
    def test_get_session_context_from_ctx_with_session_context_object(self):
        """Test getting SessionContext from ctx with SessionContext object."""
        from gnosari.tools.base import BaseTool
        from unittest.mock import Mock
        
        # Create mock context with SessionContext object
        session_ctx = SessionContext(
            team_id="test_team",
            agent_id="test_agent"
        )
        
        mock_context = Mock()
        mock_context.get_session_context_obj.return_value = session_ctx
        
        mock_ctx = Mock()
        mock_ctx.context = mock_context
        
        result = BaseTool.get_session_context_from_ctx(mock_ctx)
        assert result == session_ctx
        assert result.team_id == "test_team"
        assert result.agent_id == "test_agent"
    
    def test_get_session_context_from_ctx_with_dict_fallback(self):
        """Test getting SessionContext from ctx with dict fallback."""
        from gnosari.tools.base import BaseTool
        from unittest.mock import Mock
        
        # Create mock context with session_context dict but no object methods
        mock_context = Mock()
        mock_context.session_context = {
            "team_id": "test_team",
            "agent_id": "test_agent"
        }
        # Remove attributes to simulate a context without SessionContext object methods
        del mock_context.get_session_context_obj
        del mock_context._session_context_obj
        
        mock_ctx = Mock()
        mock_ctx.context = mock_context
        
        result = BaseTool.get_session_context_from_ctx(mock_ctx)
        assert isinstance(result, SessionContext)
        assert result.team_id == "test_team"
        assert result.agent_id == "test_agent"
    
    def test_get_session_context_from_ctx_none(self):
        """Test getting SessionContext from ctx with None/invalid input."""
        from gnosari.tools.base import BaseTool
        
        assert BaseTool.get_session_context_from_ctx(None) is None
        
        # Mock with no context
        from unittest.mock import Mock
        mock_ctx = Mock()
        mock_ctx.context = None
        assert BaseTool.get_session_context_from_ctx(mock_ctx) is None