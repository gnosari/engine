"""
Integration tests for session context population from YAML configurations.
"""

import pytest
from unittest.mock import Mock, patch
from gnosari.engine.runners.base_runner import BaseRunner
from gnosari.core.team import Team
from gnosari.schemas import SessionContext


class TestSessionContextIntegration:
    """Test session context population in runners."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create mock team with original config
        self.mock_orchestrator = Mock()
        self.mock_orchestrator.name = "orchestrator_agent"
        
        self.mock_worker = Mock()
        self.mock_worker.name = "worker_agent"
        
        self.team_config = {
            "id": "test_team_123",
            "name": "Test Team",
            "agents": [
                {"id": "orchestrator_agent", "name": "Orchestrator Agent"},
                {"id": "worker_agent", "name": "Worker Agent"}
            ]
        }
        
        self.team = Team(
            orchestrator=self.mock_orchestrator,
            workers={"worker_agent": self.mock_worker},
            name="Test Team",
            original_config=self.team_config
        )
        
        # Create a concrete implementation of BaseRunner for testing
        class TestRunner(BaseRunner):
            pass
        
        self.runner = TestRunner(self.team)
    
    def test_enrich_session_context_with_team_config(self):
        """Test context enrichment with valid team config."""
        original_context = {
            "account_id": 12345,
            "session_id": "sess_abc123"
        }
        
        enriched = self.runner._enrich_session_context(
            original_context, 
            agent_id="orchestrator_agent"
        )
        
        # Should return SessionContext object
        assert isinstance(enriched, SessionContext)
        assert enriched.team_id == "test_team_123"
        assert enriched.agent_id == "orchestrator_agent"
        assert enriched.account_id == 12345
        assert enriched.session_id == "sess_abc123"
    
    def test_enrich_session_context_no_original_context(self):
        """Test context enrichment with no original context."""
        enriched = self.runner._enrich_session_context(
            None, 
            agent_id="worker_agent"
        )
        
        # Should return SessionContext object
        assert isinstance(enriched, SessionContext)
        assert enriched.team_id == "test_team_123"
        assert enriched.agent_id == "worker_agent"
        assert enriched.account_id is None
    
    def test_enrich_session_context_no_team_id_in_config(self):
        """Test context enrichment when team config has no id."""
        # Team with no id field
        team_config_no_id = {
            "name": "Test Team",
            "agents": [{"id": "agent_1", "name": "Agent 1"}]
        }
        
        team_no_id = Team(
            orchestrator=self.mock_orchestrator,
            workers={},
            name="Test Team",
            original_config=team_config_no_id
        )
        
        class TestRunner(BaseRunner):
            pass
        
        runner = TestRunner(team_no_id)
        
        enriched = runner._enrich_session_context(
            {"account_id": 999}, 
            agent_id="agent_1"
        )
        
        # Should return SessionContext object with fallback team_id
        assert isinstance(enriched, SessionContext)
        assert enriched.agent_id == "agent_1"
        assert enriched.team_id == "unknown"  # fallback value
        assert enriched.account_id == 999
    
    def test_enrich_session_context_no_original_config(self):
        """Test context enrichment when team has no original config."""
        team_no_config = Team(
            orchestrator=self.mock_orchestrator,
            workers={},
            name="Test Team",
            original_config=None
        )
        
        class TestRunner(BaseRunner):
            pass
        
        runner = TestRunner(team_no_config)
        
        with patch.object(runner, 'logger') as mock_logger:
            enriched = runner._enrich_session_context(
                {"account_id": 999}, 
                agent_id="agent_1"
            )
            
            # Should return SessionContext object with fallback team_id
            assert isinstance(enriched, SessionContext)
            assert enriched.agent_id == "agent_1"
            assert enriched.team_id == "unknown"  # fallback value
    
    def test_enrich_session_context_validation_success(self):
        """Test that enriched context is already a valid SessionContext."""
        enriched = self.runner._enrich_session_context(
            {"account_id": 12345}, 
            agent_id="orchestrator_agent"
        )
        
        # Should already be a SessionContext object
        assert isinstance(enriched, SessionContext)
        assert enriched.team_id == "test_team_123"
        assert enriched.agent_id == "orchestrator_agent"
        assert enriched.account_id == 12345
    
    def test_enrich_session_context_preserves_metadata(self):
        """Test that existing metadata is preserved."""
        original_context = {
            "account_id": 12345,
            "metadata": {"custom_key": "custom_value", "priority": 1}
        }
        
        enriched = self.runner._enrich_session_context(
            original_context, 
            agent_id="worker_agent"
        )
        
        assert isinstance(enriched, SessionContext)
        assert enriched.team_id == "test_team_123"
        assert enriched.agent_id == "worker_agent"
        assert enriched.account_id == 12345
        assert enriched.metadata == {"custom_key": "custom_value", "priority": 1}
    
    def test_enrich_session_context_different_agents(self):
        """Test context enrichment for different agents."""
        # Test with orchestrator
        enriched_orch = self.runner._enrich_session_context(
            {}, 
            agent_id="orchestrator_agent"
        )
        assert isinstance(enriched_orch, SessionContext)
        assert enriched_orch.agent_id == "orchestrator_agent"
        assert enriched_orch.team_id == "test_team_123"
        
        # Test with worker
        enriched_worker = self.runner._enrich_session_context(
            {}, 
            agent_id="worker_agent"
        )
        assert isinstance(enriched_worker, SessionContext)
        assert enriched_worker.agent_id == "worker_agent"
        assert enriched_worker.team_id == "test_team_123"
    
    def test_context_validation_with_real_yaml_structure(self):
        """Test with structure similar to real YAML configs."""
        # Simulate the structure from examples/neomanex_demo.yaml
        yaml_config = {
            "id": "neomanex_demo_team_1",
            "name": "Neomanex Team Demo",
            "description": "Single Agent Team with various capabilities",
            "agents": [
                {
                    "id": "neomanex_expert_agent",
                    "name": "Neomanex Knowledge Expert",
                    "description": "AI expert specializing in Neomanex content"
                },
                {
                    "id": "neomanex_general_agent", 
                    "name": "General Agent",
                    "description": "Helpful assistant"
                }
            ]
        }
        
        team = Team(
            orchestrator=self.mock_orchestrator,
            workers={"neomanex_general_agent": self.mock_worker},
            name="Neomanex Team Demo",
            original_config=yaml_config
        )
        
        class TestRunner(BaseRunner):
            pass
        
        runner = TestRunner(team)
        
        # Test context enrichment
        enriched = runner._enrich_session_context(
            {"account_id": 42}, 
            agent_id="neomanex_expert_agent"
        )
        
        # Should return SessionContext object
        assert isinstance(enriched, SessionContext)
        assert enriched.team_id == "neomanex_demo_team_1"
        assert enriched.agent_id == "neomanex_expert_agent"
        assert enriched.account_id == 42
    
    def test_account_id_extraction_from_yaml(self):
        """Test account_id extraction from YAML root configuration."""
        # Simulate YAML config with account_id
        yaml_config_with_account = {
            "id": "test_team_with_account",
            "account_id": 999,
            "name": "Test Team with Account",
            "agents": [
                {"id": "test_agent", "name": "Test Agent"}
            ]
        }
        
        team = Team(
            orchestrator=self.mock_orchestrator,
            workers={},
            name="Test Team with Account",
            original_config=yaml_config_with_account
        )
        
        class TestRunner(BaseRunner):
            pass
        
        runner = TestRunner(team)
        
        # Test context enrichment with no existing account_id
        enriched = runner._enrich_session_context(
            {}, 
            agent_id="test_agent"
        )
        
        # Should extract account_id from YAML config
        assert isinstance(enriched, SessionContext)
        assert enriched.team_id == "test_team_with_account"
        assert enriched.agent_id == "test_agent"
        assert enriched.account_id == 999  # From YAML
    
    def test_account_id_preservation_over_yaml(self):
        """Test that existing account_id is preserved over YAML account_id."""
        # Simulate YAML config with account_id
        yaml_config_with_account = {
            "id": "test_team_with_account",
            "account_id": 999,
            "name": "Test Team with Account",
            "agents": [
                {"id": "test_agent", "name": "Test Agent"}
            ]
        }
        
        team = Team(
            orchestrator=self.mock_orchestrator,
            workers={},
            name="Test Team with Account",
            original_config=yaml_config_with_account
        )
        
        class TestRunner(BaseRunner):
            pass
        
        runner = TestRunner(team)
        
        # Test context enrichment with existing account_id (should be preserved)
        enriched = runner._enrich_session_context(
            {"account_id": 777}, 
            agent_id="test_agent"
        )
        
        # Should preserve existing account_id, not use YAML value
        assert isinstance(enriched, SessionContext)
        assert enriched.team_id == "test_team_with_account"
        assert enriched.agent_id == "test_agent"
        assert enriched.account_id == 777  # Preserved existing value, not 999 from YAML