"""Multi-database query tool for myquery."""
from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from core.multi_db_manager import MultiDBManager
from config.logging import get_logger
import json

logger = get_logger(__name__)


class MultiDBQueryInput(BaseModel):
    """Input schema for MultiDBQueryTool."""
    model_config = {"protected_namespaces": ()}
    
    query: str = Field(description="SQL query to execute on all databases")
    connections: Optional[str] = Field(
        default="all",
        description="Comma-separated connection names or 'all'"
    )


class MultiDBQueryTool(BaseTool):
    """Tool for querying multiple databases simultaneously."""
    
    name: str = "multi_db_query"
    description: str = """
    Execute queries across multiple connected databases simultaneously.
    Compare results from different databases.
    Use this tool when you need to query multiple databases at once.
    """
    args_schema: Type[BaseModel] = MultiDBQueryInput
    
    manager: Optional[MultiDBManager] = None
    
    def _run(
        self,
        query: str,
        connections: str = "all",
    ) -> str:
        """
        Execute query on multiple databases.
        
        Args:
            query: SQL query to execute
            connections: Connection names (comma-separated) or 'all'
            
        Returns:
            Combined results from all databases
        """
        if self.manager is None:
            return "❌ Multi-database manager not initialized"
        
        try:
            logger.info(f"Executing multi-DB query: {query[:100]}...")
            
            # Get list of connections to query
            if connections.lower() == "all":
                conn_list = self.manager.list_connections()
            else:
                conn_list = [c.strip() for c in connections.split(",")]
            
            if not conn_list:
                return "❌ No database connections available"
            
            # Execute query on each connection
            results = {}
            
            for conn_name in conn_list:
                engine = self.manager.get_connection(conn_name)
                if not engine:
                    results[conn_name] = {
                        "success": False,
                        "error": "Connection not found",
                    }
                    continue
                
                try:
                    with engine.connect() as conn:
                        result = conn.execute(query)
                        rows = result.fetchall()
                        columns = list(result.keys())
                        
                        results[conn_name] = {
                            "success": True,
                            "columns": columns,
                            "data": [dict(zip(columns, row)) for row in rows],
                            "row_count": len(rows),
                        }
                except Exception as e:
                    results[conn_name] = {
                        "success": False,
                        "error": str(e),
                    }
            
            logger.info(f"✅ Multi-DB query completed: {len(results)} database(s)")
            return json.dumps(results, indent=2, default=str)
            
        except Exception as e:
            logger.error(f"Multi-DB query failed: {str(e)}")
            return f"❌ Failed to execute multi-DB query: {str(e)}"
    
    async def _arun(self, *args, **kwargs) -> str:
        """Async version (not implemented)."""
        return self._run(*args, **kwargs)

