"""Multi-database query tool for myquery."""
from typing import Optional, Type, List, Dict, Any
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from core.multi_db_manager import MultiDBManager
from config.logging import get_logger
import json
import pandas as pd

logger = get_logger(__name__)


class MultiDBQueryInput(BaseModel):
    """Input schema for MultiDBQueryTool."""
    model_config = {"protected_namespaces": ()}
    
    query: str = Field(description="SQL query to execute on all databases")
    connections: Optional[str] = Field(
        default="all",
        description="Comma-separated connection names or 'all'"
    )
    merge_results: Optional[bool] = Field(
        default=False,
        description="Merge results from all databases into single dataset"
    )
    merge_type: Optional[str] = Field(
        default="union",
        description="Merge type: union (stack rows) or join (merge by key)"
    )
    merge_key: Optional[str] = Field(
        default=None,
        description="Column name to use as key for join merge"
    )


class MultiDBQueryTool(BaseTool):
    """Tool for querying multiple databases simultaneously with merge/join support."""
    
    name: str = "multi_db_query"
    description: str = """
    Execute queries across multiple connected databases simultaneously.
    Compare results from different databases.
    Can merge/join results from multiple databases.
    Supports union (stack rows) and join (merge by key) operations.
    Use this tool when you need to query and combine data from multiple databases.
    """
    args_schema: Type[BaseModel] = MultiDBQueryInput
    
    manager: Optional[MultiDBManager] = None
    
    def _run(
        self,
        query: str,
        connections: str = "all",
        merge_results: bool = False,
        merge_type: str = "union",
        merge_key: Optional[str] = None,
    ) -> str:
        """
        Execute query on multiple databases with optional merge/join.
        
        Args:
            query: SQL query to execute
            connections: Connection names (comma-separated) or 'all'
            merge_results: Whether to merge results into single dataset
            merge_type: Merge type (union or join)
            merge_key: Column name for join operations
            
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
            
            # Merge results if requested
            if merge_results and len(results) > 1:
                try:
                    merged_data = self._merge_results(
                        results,
                        merge_type=merge_type,
                        merge_key=merge_key
                    )
                    logger.info(f"✅ Multi-DB query completed and merged: {len(results)} database(s)")
                    return json.dumps(merged_data, indent=2, default=str)
                except Exception as e:
                    logger.error(f"Merge failed: {str(e)}")
                    # Return unmerged results with error note
                    error_note = {
                        "merge_error": str(e),
                        "note": "Returning unmerged results",
                        "individual_results": results
                    }
                    return json.dumps(error_note, indent=2, default=str)
            
            logger.info(f"✅ Multi-DB query completed: {len(results)} database(s)")
            return json.dumps(results, indent=2, default=str)
            
        except Exception as e:
            logger.error(f"Multi-DB query failed: {str(e)}")
            return f"❌ Failed to execute multi-DB query: {str(e)}"
    
    async def _arun(self, *args, **kwargs) -> str:
        """Async version (not implemented)."""
        return self._run(*args, **kwargs)
    
    def _merge_results(
        self,
        results: Dict[str, dict],
        merge_type: str = "union",
        merge_key: Optional[str] = None
    ) -> dict:
        """
        Merge results from multiple databases.
        
        Args:
            results: Results dict from multiple databases
            merge_type: Type of merge (union or join)
            merge_key: Key column for join operations
            
        Returns:
            Merged result dict
        """
        # Filter successful results
        successful_results = {
            name: res for name, res in results.items()
            if res.get("success", False)
        }
        
        if not successful_results:
            raise ValueError("No successful results to merge")
        
        if merge_type == "union":
            return self._union_merge(successful_results)
        elif merge_type == "join":
            if not merge_key:
                raise ValueError("merge_key is required for join operations")
            return self._join_merge(successful_results, merge_key)
        else:
            raise ValueError(f"Invalid merge_type: {merge_type}")
    
    def _union_merge(self, results: Dict[str, dict]) -> dict:
        """
        Union merge: Stack rows from all databases.
        
        Args:
            results: Results from multiple databases
            
        Returns:
            Merged result with all rows
        """
        all_data = []
        all_columns = set()
        
        # Collect all unique columns
        for db_name, result in results.items():
            all_columns.update(result.get("columns", []))
        
        all_columns = sorted(list(all_columns))
        
        # Combine data from all databases
        for db_name, result in results.items():
            data = result.get("data", [])
            
            # Add source database column
            for row in data:
                row_with_source = {"_source_db": db_name}
                # Ensure all columns present (fill missing with None)
                for col in all_columns:
                    row_with_source[col] = row.get(col, None)
                all_data.append(row_with_source)
        
        return {
            "success": True,
            "merge_type": "union",
            "source_databases": list(results.keys()),
            "columns": ["_source_db"] + all_columns,
            "data": all_data,
            "row_count": len(all_data),
            "metadata": {
                "total_rows": len(all_data),
                "source_count": len(results),
                "rows_per_source": {
                    name: res.get("row_count", 0)
                    for name, res in results.items()
                }
            }
        }
    
    def _join_merge(self, results: Dict[str, dict], merge_key: str) -> dict:
        """
        Join merge: Merge rows by key column.
        
        Args:
            results: Results from multiple databases
            merge_key: Column to use as join key
            
        Returns:
            Merged result with joined rows
        """
        # Convert to DataFrames
        dfs = {}
        
        for db_name, result in results.items():
            data = result.get("data", [])
            if not data:
                continue
            
            df = pd.DataFrame(data)
            
            # Check if merge key exists
            if merge_key not in df.columns:
                raise ValueError(f"Merge key '{merge_key}' not found in {db_name}")
            
            # Add suffix to column names (except merge key)
            df = df.rename(columns={
                col: f"{col}_{db_name}" if col != merge_key else col
                for col in df.columns
            })
            
            dfs[db_name] = df
        
        if not dfs:
            raise ValueError("No data available for join")
        
        # Perform sequential outer joins
        merged_df = None
        for db_name, df in dfs.items():
            if merged_df is None:
                merged_df = df
            else:
                merged_df = pd.merge(
                    merged_df,
                    df,
                    on=merge_key,
                    how='outer',
                    suffixes=('', f'_{db_name}')
                )
        
        # Convert back to dict format
        merged_data = merged_df.to_dict('records')
        columns = list(merged_df.columns)
        
        return {
            "success": True,
            "merge_type": "join",
            "merge_key": merge_key,
            "source_databases": list(results.keys()),
            "columns": columns,
            "data": merged_data,
            "row_count": len(merged_data),
            "metadata": {
                "total_rows": len(merged_data),
                "source_count": len(results),
                "join_type": "outer",
                "rows_per_source": {
                    name: res.get("row_count", 0)
                    for name, res in results.items()
                }
            }
        }

