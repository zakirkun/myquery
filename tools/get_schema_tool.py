"""Database schema extraction tool for myquery."""
from typing import Optional, Type, Dict, List, Any
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from sqlalchemy import inspect, MetaData
from sqlalchemy.engine import Engine
from config.logging import get_logger
import json

logger = get_logger(__name__)


class GetSchemaInput(BaseModel):
    """Input schema for GetSchemaTool."""
    include_sample_data: bool = Field(
        default=False, 
        description="Whether to include sample data from each table"
    )


class GetSchemaTool(BaseTool):
    """Tool for extracting database schema information."""
    
    name: str = "get_schema"
    description: str = """
    Extract schema information from the connected database.
    Returns details about tables, columns, data types, and relationships.
    Use this tool when you need to understand the database structure.
    """
    args_schema: Type[BaseModel] = GetSchemaInput
    
    # Reference to database engine
    engine: Optional[Engine] = None
    _cached_schema: Optional[Dict[str, Any]] = None
    
    def _run(self, include_sample_data: bool = False) -> str:
        """
        Extract database schema.
        
        Args:
            include_sample_data: Whether to include sample data
            
        Returns:
            JSON string with schema information
        """
        if self.engine is None:
            return "❌ No database connection. Please connect to a database first."
        
        try:
            logger.info("Extracting database schema...")
            
            inspector = inspect(self.engine)
            schema_info = {
                "tables": {},
                "total_tables": 0,
            }
            
            # Get all table names
            table_names = inspector.get_table_names()
            schema_info["total_tables"] = len(table_names)
            
            for table_name in table_names:
                table_info = {
                    "columns": [],
                    "primary_keys": [],
                    "foreign_keys": [],
                    "indexes": [],
                }
                
                # Get columns
                columns = inspector.get_columns(table_name)
                for col in columns:
                    table_info["columns"].append({
                        "name": col["name"],
                        "type": str(col["type"]),
                        "nullable": col["nullable"],
                        "default": str(col.get("default", "")),
                    })
                
                # Get primary keys
                pk = inspector.get_pk_constraint(table_name)
                if pk and pk.get("constrained_columns"):
                    table_info["primary_keys"] = pk["constrained_columns"]
                
                # Get foreign keys
                fks = inspector.get_foreign_keys(table_name)
                for fk in fks:
                    table_info["foreign_keys"].append({
                        "columns": fk["constrained_columns"],
                        "refers_to_table": fk["referred_table"],
                        "refers_to_columns": fk["referred_columns"],
                    })
                
                # Get indexes
                indexes = inspector.get_indexes(table_name)
                for idx in indexes:
                    table_info["indexes"].append({
                        "name": idx["name"],
                        "columns": idx["column_names"],
                        "unique": idx["unique"],
                    })
                
                # Get sample data if requested
                if include_sample_data:
                    try:
                        with self.engine.connect() as conn:
                            result = conn.execute(
                                f"SELECT * FROM {table_name} LIMIT 3"
                            )
                            sample_data = [dict(row) for row in result]
                            table_info["sample_data"] = sample_data
                    except Exception as e:
                        logger.warning(f"Could not fetch sample data for {table_name}: {e}")
                
                schema_info["tables"][table_name] = table_info
            
            # Cache the schema
            self._cached_schema = schema_info
            
            logger.info(f"✅ Schema extracted: {len(table_names)} tables found")
            return json.dumps(schema_info, indent=2, default=str)
            
        except Exception as e:
            logger.error(f"Schema extraction failed: {str(e)}")
            return f"❌ Failed to extract schema: {str(e)}"
    
    async def _arun(self, *args, **kwargs) -> str:
        """Async version (not implemented)."""
        return self._run(*args, **kwargs)
    
    def get_cached_schema(self) -> Optional[Dict[str, Any]]:
        """Get cached schema information."""
        return self._cached_schema
    
    def get_table_names(self) -> List[str]:
        """Get list of table names."""
        if self._cached_schema:
            return list(self._cached_schema["tables"].keys())
        return []

