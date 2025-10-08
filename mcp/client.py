"""MCP Client for testing and integration."""
from typing import Dict, Any, Optional
import requests
from mcp.protocol import MCPRequest, MCPResponse, MCPActionType


class MCPClient:
    """Client for interacting with MCP server."""
    
    def __init__(self, base_url: str = "http://localhost:7766"):
        """
        Initialize MCP Client.
        
        Args:
            base_url: Base URL of MCP server
        """
        self.base_url = base_url
        self.session_id: Optional[str] = None
    
    def execute_action(
        self,
        action: MCPActionType,
        parameters: Dict[str, Any],
    ) -> MCPResponse:
        """
        Execute an MCP action.
        
        Args:
            action: Action type
            parameters: Action parameters
            
        Returns:
            MCP response
        """
        request = MCPRequest(
            action=action,
            parameters=parameters,
            session_id=self.session_id,
        )
        
        response = requests.post(
            f"{self.base_url}/mcp/action",
            json=request.model_dump(),
        )
        
        response.raise_for_status()
        mcp_response = MCPResponse(**response.json())
        
        # Update session ID
        if mcp_response.session_id:
            self.session_id = mcp_response.session_id
        
        return mcp_response
    
    def connect_db(
        self,
        db_type: str,
        db_name: str,
        db_host: str = "localhost",
        db_port: Optional[int] = None,
        db_user: Optional[str] = None,
        db_password: Optional[str] = None,
    ) -> MCPResponse:
        """Connect to database."""
        return self.execute_action(
            action=MCPActionType.CONNECT_DB,
            parameters={
                "db_type": db_type,
                "db_name": db_name,
                "db_host": db_host,
                "db_port": db_port,
                "db_user": db_user,
                "db_password": db_password,
            },
        )
    
    def get_schema(self, include_sample_data: bool = False) -> MCPResponse:
        """Get database schema."""
        return self.execute_action(
            action=MCPActionType.GET_SCHEMA,
            parameters={"include_sample_data": include_sample_data},
        )
    
    def generate_query(self, prompt: str, chat_history: str = "") -> MCPResponse:
        """Generate SQL query."""
        return self.execute_action(
            action=MCPActionType.GENERATE_QUERY,
            parameters={
                "prompt": prompt,
                "chat_history": chat_history,
            },
        )
    
    def execute_query(self, prompt: str, debug: bool = False) -> MCPResponse:
        """Execute query."""
        return self.execute_action(
            action=MCPActionType.EXECUTE_QUERY,
            parameters={
                "prompt": prompt,
                "debug": debug,
            },
        )
    
    def chat(self, message: str, debug: bool = False) -> MCPResponse:
        """Chat with database."""
        return self.execute_action(
            action=MCPActionType.CHAT,
            parameters={
                "message": message,
                "debug": debug,
            },
        )
    
    def get_status(self) -> MCPResponse:
        """Get connection status."""
        return self.execute_action(
            action=MCPActionType.GET_STATUS,
            parameters={},
        )
    
    def get_context(self) -> Dict[str, Any]:
        """Get session context."""
        if not self.session_id:
            raise ValueError("No active session")
        
        response = requests.get(f"{self.base_url}/mcp/context/{self.session_id}")
        response.raise_for_status()
        return response.json()
    
    def delete_session(self):
        """Delete current session."""
        if not self.session_id:
            return
        
        response = requests.delete(f"{self.base_url}/mcp/session/{self.session_id}")
        response.raise_for_status()
        self.session_id = None

