"""SQL query execution tool for myquery."""
from typing import Optional, Type, List, Dict, Any
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from sqlalchemy import text
from sqlalchemy.engine import Engine
from config.logging import get_logger
import json

logger = get_logger(__name__)


class ExecuteQueryInput(BaseModel):
    """Input schema for ExecuteQueryTool."""
    sql_query: str = Field(description="SQL query to execute")
    max_rows: int = Field(
        default=100, 
        description="Maximum number of rows to return"
    )


class ExecuteQueryTool(BaseTool):
    """Tool for executing SQL queries."""
    
    name: str = "execute_query"
    description: str = """
    Execute SQL queries on the connected database.
    Returns query results as JSON.
    Use this tool to run generated SQL queries and retrieve data.
    """
    args_schema: Type[BaseModel] = ExecuteQueryInput
    
    engine: Optional[Engine] = None
    
    def _run(self, sql_query: str, max_rows: int = 100) -> str:
        """
        Execute SQL query.
        
        Args:
            sql_query: SQL query to execute
            max_rows: Maximum rows to return
            
        Returns:
            JSON string with query results
        """
        if self.engine is None:
            return "❌ No database connection. Please connect to a database first."
        
        # Check for destructive commands
        if self._is_destructive_query(sql_query):
            return "❌ Destructive queries (DROP, DELETE, TRUNCATE, UPDATE) are not allowed without explicit confirmation."
        
        try:
            logger.info(f"Executing query: {sql_query[:100]}...")
            
            with self.engine.connect() as conn:
                result = conn.execute(text(sql_query))
                
                # Fetch results
                rows = result.fetchmany(max_rows)
                
                # Convert to list of dicts
                columns = list(result.keys())
                data = [dict(zip(columns, row)) for row in rows]
                
                # Get row count
                row_count = len(data)
                
                result_info = {
                    "success": True,
                    "row_count": row_count,
                    "columns": columns,
                    "data": data,
                    "truncated": row_count >= max_rows,
                }
                
                logger.info(f"✅ Query executed successfully: {row_count} rows returned")
                return json.dumps(result_info, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            error_info = {
                "success": False,
                "error": str(e),
                "query": sql_query,
            }
            return json.dumps(error_info, indent=2)
    
    async def _arun(self, *args, **kwargs) -> str:
        """Async version (not implemented)."""
        return self._run(*args, **kwargs)
    
    def _is_destructive_query(self, query: str) -> bool:
        """Check if query contains destructive operations."""
        query_upper = query.upper().strip()
        destructive_keywords = ["DROP", "DELETE", "TRUNCATE", "UPDATE", "ALTER", "CREATE"]
        
        for keyword in destructive_keywords:
            if query_upper.startswith(keyword):
                return True
        
        return False

