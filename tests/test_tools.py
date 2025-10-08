"""Tests for myquery tools."""
import pytest
from unittest.mock import Mock, patch
from tools import (
    ConnectDBTool,
    GetSchemaTool,
    GenerateQueryTool,
    ExecuteQueryTool,
)


class TestConnectDBTool:
    """Tests for ConnectDBTool."""
    
    def test_sqlite_connection(self):
        """Test SQLite connection."""
        tool = ConnectDBTool()
        result = tool._run(
            db_type="sqlite",
            db_name=":memory:",
        )
        
        assert "✅" in result or "Successfully" in result
        assert tool.is_connected()
    
    def test_invalid_db_type(self):
        """Test invalid database type."""
        tool = ConnectDBTool()
        result = tool._run(
            db_type="invalid_type",
            db_name="test.db",
        )
        
        assert "❌" in result or "Unsupported" in result


class TestGenerateQueryTool:
    """Tests for GenerateQueryTool."""
    
    @patch('langchain_openai.ChatOpenAI')
    def test_query_generation(self, mock_llm):
        """Test SQL query generation."""
        # Mock LLM response
        mock_response = Mock()
        mock_response.content = "SELECT * FROM users LIMIT 10;"
        mock_llm.return_value.invoke.return_value = mock_response
        
        tool = GenerateQueryTool()
        tool.llm = mock_llm.return_value
        
        result = tool._run(
            user_prompt="Show me all users",
            schema_json='{"tables": {"users": {"columns": []}}}',
        )
        
        assert "SELECT" in result
        assert "users" in result


# Add more tests as needed

