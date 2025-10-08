"""MCP Protocol implementation for myquery."""
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class MCPActionType(str, Enum):
    """MCP action types."""
    CONNECT_DB = "connect_db"
    GET_SCHEMA = "get_schema"
    GENERATE_QUERY = "generate_query"
    EXECUTE_QUERY = "execute_query"
    ANALYZE_RESULTS = "analyze_results"
    GET_STATUS = "get_status"
    CHAT = "chat"


class MCPRequest(BaseModel):
    """MCP request model."""
    action: MCPActionType = Field(..., description="Action to perform")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Action parameters")
    session_id: Optional[str] = Field(default=None, description="Session identifier")


class MCPResponse(BaseModel):
    """MCP response model."""
    success: bool = Field(..., description="Whether action succeeded")
    data: Optional[Any] = Field(default=None, description="Response data")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    session_id: Optional[str] = Field(default=None, description="Session identifier")
    context: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Additional context information"
    )


class MCPContext(BaseModel):
    """MCP session context."""
    session_id: str = Field(..., description="Session identifier")
    connected: bool = Field(default=False, description="Database connection status")
    db_type: Optional[str] = Field(default=None, description="Database type")
    db_name: Optional[str] = Field(default=None, description="Database name")
    schema_loaded: bool = Field(default=False, description="Schema loaded status")
    table_count: int = Field(default=0, description="Number of tables")
    table_names: List[str] = Field(default_factory=list, description="List of table names")
    last_query: Optional[str] = Field(default=None, description="Last executed query")
    last_result_count: Optional[int] = Field(default=None, description="Last result row count")


class MCPProtocol:
    """MCP Protocol handler."""
    
    @staticmethod
    def create_request(
        action: MCPActionType,
        parameters: Dict[str, Any],
        session_id: Optional[str] = None,
    ) -> MCPRequest:
        """Create an MCP request."""
        return MCPRequest(
            action=action,
            parameters=parameters,
            session_id=session_id,
        )
    
    @staticmethod
    def create_response(
        success: bool,
        data: Optional[Any] = None,
        error: Optional[str] = None,
        session_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> MCPResponse:
        """Create an MCP response."""
        return MCPResponse(
            success=success,
            data=data,
            error=error,
            session_id=session_id,
            context=context,
        )
    
    @staticmethod
    def create_error_response(
        error: str,
        session_id: Optional[str] = None,
    ) -> MCPResponse:
        """Create an error response."""
        return MCPResponse(
            success=False,
            error=error,
            session_id=session_id,
        )
    
    @staticmethod
    def create_success_response(
        data: Any,
        session_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> MCPResponse:
        """Create a success response."""
        return MCPResponse(
            success=True,
            data=data,
            session_id=session_id,
            context=context,
        )

