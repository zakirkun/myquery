"""Tests for QueryAgent."""
import pytest
from unittest.mock import Mock, patch
from core.agent import QueryAgent


class TestQueryAgent:
    """Tests for QueryAgent."""
    
    @patch('core.agent.ChatOpenAI')
    def test_agent_initialization(self, mock_llm):
        """Test agent initialization."""
        agent = QueryAgent(api_key="test_key")
        
        assert agent is not None
        assert agent.llm is not None
    
    def test_agent_without_api_key(self):
        """Test agent initialization without API key."""
        with patch('config.settings.settings', None):
            with pytest.raises(ValueError):
                QueryAgent()
    
    @patch('core.agent.ChatOpenAI')
    def test_database_connection_status(self, mock_llm):
        """Test database connection status."""
        agent = QueryAgent(api_key="test_key")
        
        # Initially not connected
        assert not agent.is_connected()
        
        # Connect to SQLite
        agent.connect_database(
            db_type="sqlite",
            db_name=":memory:",
        )
        
        # Should be connected
        assert agent.is_connected()


# Add more tests as needed

