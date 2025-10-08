"""MCP Server implementation for myquery."""
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import uuid
import json
from core.agent import QueryAgent
from mcp.protocol import (
    MCPRequest,
    MCPResponse,
    MCPContext,
    MCPActionType,
    MCPProtocol,
)
from config import get_logger, settings

logger = get_logger(__name__)


class MCPServer:
    """MCP Server for myquery."""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 7766):
        """
        Initialize MCP Server.
        
        Args:
            host: Server host
            port: Server port
        """
        self.host = host
        self.port = port
        self.app = FastAPI(
            title="myquery MCP Server",
            description="Model Context Protocol server for myquery",
            version="0.1.0",
        )
        
        # Session storage
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.agents: Dict[str, QueryAgent] = {}
        
        # Setup CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Register routes
        self._register_routes()
        
        logger.info(f"MCP Server initialized on {host}:{port}")
    
    def _register_routes(self):
        """Register API routes."""
        
        @self.app.get("/")
        async def root():
            """Root endpoint."""
            return {
                "service": "myquery MCP Server",
                "version": "0.1.0",
                "status": "running",
                "port": self.port,
            }
        
        @self.app.post("/mcp/action", response_model=MCPResponse)
        async def execute_action(request: MCPRequest):
            """Execute an MCP action."""
            try:
                # Get or create session
                session_id = request.session_id or str(uuid.uuid4())
                
                if session_id not in self.sessions:
                    self.sessions[session_id] = {
                        "id": session_id,
                        "context": MCPContext(session_id=session_id),
                    }
                    self.agents[session_id] = QueryAgent()
                
                agent = self.agents[session_id]
                context = self.sessions[session_id]["context"]
                
                # Execute action
                result = await self._execute_action(
                    agent=agent,
                    context=context,
                    action=request.action,
                    parameters=request.parameters,
                )
                
                # Update context
                self.sessions[session_id]["context"] = context
                
                return MCPProtocol.create_success_response(
                    data=result,
                    session_id=session_id,
                    context=context.model_dump(),
                )
                
            except Exception as e:
                logger.error(f"Action execution failed: {str(e)}")
                return MCPProtocol.create_error_response(
                    error=str(e),
                    session_id=request.session_id,
                )
        
        @self.app.get("/mcp/context/{session_id}", response_model=MCPContext)
        async def get_context(session_id: str):
            """Get session context."""
            if session_id not in self.sessions:
                raise HTTPException(status_code=404, detail="Session not found")
            
            return self.sessions[session_id]["context"]
        
        @self.app.delete("/mcp/session/{session_id}")
        async def delete_session(session_id: str):
            """Delete a session."""
            if session_id in self.sessions:
                del self.sessions[session_id]
                del self.agents[session_id]
                return {"message": "Session deleted", "session_id": session_id}
            
            raise HTTPException(status_code=404, detail="Session not found")
        
        @self.app.get("/mcp/sessions")
        async def list_sessions():
            """List all active sessions."""
            return {
                "sessions": [
                    {
                        "session_id": sid,
                        "connected": ctx["context"].connected,
                        "db_name": ctx["context"].db_name,
                    }
                    for sid, ctx in self.sessions.items()
                ]
            }
    
    async def _execute_action(
        self,
        agent: QueryAgent,
        context: MCPContext,
        action: MCPActionType,
        parameters: Dict[str, Any],
    ) -> Any:
        """
        Execute an MCP action.
        
        Args:
            agent: QueryAgent instance
            context: Session context
            action: Action type
            parameters: Action parameters
            
        Returns:
            Action result
        """
        logger.info(f"Executing action: {action}")
        
        if action == MCPActionType.CONNECT_DB:
            result = agent.connect_database(
                db_type=parameters.get("db_type"),
                db_name=parameters.get("db_name"),
                db_host=parameters.get("db_host", "localhost"),
                db_port=parameters.get("db_port"),
                db_user=parameters.get("db_user"),
                db_password=parameters.get("db_password"),
            )
            
            if agent.is_connected():
                context.connected = True
                context.db_type = parameters.get("db_type")
                context.db_name = parameters.get("db_name")
            
            return {"message": result}
        
        elif action == MCPActionType.GET_SCHEMA:
            schema_json = agent.get_schema(
                include_sample_data=parameters.get("include_sample_data", False)
            )
            
            schema_data = json.loads(schema_json)
            context.schema_loaded = True
            context.table_count = schema_data.get("total_tables", 0)
            context.table_names = list(schema_data.get("tables", {}).keys())
            
            return schema_data
        
        elif action == MCPActionType.GENERATE_QUERY:
            schema_json = agent.get_schema()
            sql_query = agent.generate_query_tool._run(
                user_prompt=parameters.get("prompt"),
                schema_json=schema_json,
                chat_history=parameters.get("chat_history", ""),
            )
            
            return {"sql_query": sql_query}
        
        elif action == MCPActionType.EXECUTE_QUERY:
            results = agent.execute_query_flow(
                user_prompt=parameters.get("prompt"),
                debug=parameters.get("debug", False),
            )
            
            if results.get("sql_query"):
                context.last_query = results.get("sql_query")
            
            return results
        
        elif action == MCPActionType.ANALYZE_RESULTS:
            analysis = agent.analyze_data_tool._run(
                query_result_json=parameters.get("query_result_json"),
                user_prompt=parameters.get("prompt"),
            )
            
            return {"analysis": analysis}
        
        elif action == MCPActionType.GET_STATUS:
            return {
                "connected": agent.is_connected(),
                "tables": agent.get_table_list(),
                "context": context.model_dump(),
            }
        
        elif action == MCPActionType.CHAT:
            response = agent.chat(
                user_input=parameters.get("message"),
                debug=parameters.get("debug", False),
            )
            
            return {"response": response}
        
        else:
            raise ValueError(f"Unknown action: {action}")
    
    def run(self):
        """Run the MCP server."""
        logger.info(f"Starting MCP server on {self.host}:{self.port}")
        uvicorn.run(
            self.app,
            host=self.host,
            port=self.port,
            log_level="info",
        )


def start_mcp_server(host: Optional[str] = None, port: Optional[int] = None):
    """
    Start the MCP server.
    
    Args:
        host: Server host (uses settings if not provided)
        port: Server port (uses settings if not provided)
    """
    server_host = host or (settings.mcp_host if settings else "0.0.0.0")
    server_port = port or (settings.mcp_port if settings else 7766)
    
    server = MCPServer(host=server_host, port=server_port)
    server.run()


if __name__ == "__main__":
    start_mcp_server()

