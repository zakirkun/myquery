"""Multi-database connection manager for myquery."""
from typing import Dict, Optional, List, Any
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from config.logging import get_logger
import json

logger = get_logger(__name__)


class MultiDBManager:
    """Manager for multiple database connections."""
    
    def __init__(self):
        """Initialize multi-database manager."""
        self.connections: Dict[str, Engine] = {}
        self.metadata: Dict[str, Dict[str, Any]] = {}
    
    def add_connection(
        self,
        name: str,
        db_type: str,
        db_name: str,
        db_host: Optional[str] = "localhost",
        db_port: Optional[int] = None,
        db_user: Optional[str] = None,
        db_password: Optional[str] = None,
    ) -> str:
        """
        Add a new database connection.
        
        Args:
            name: Connection name (identifier)
            db_type: Database type
            db_name: Database name
            db_host: Database host
            db_port: Database port
            db_user: Database username
            db_password: Database password
            
        Returns:
            Status message
        """
        try:
            # Build connection URL
            if db_type.lower() == "sqlite":
                db_url = f"sqlite:///{db_name}"
            elif db_type.lower() == "postgresql":
                port = db_port or 5432
                db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{port}/{db_name}"
            elif db_type.lower() == "mysql":
                port = db_port or 3306
                db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{port}/{db_name}"
            else:
                return f"❌ Unsupported database type: {db_type}"
            
            # Create engine
            engine = create_engine(db_url, pool_pre_ping=True)
            
            # Test connection
            from sqlalchemy import text
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            # Store connection
            self.connections[name] = engine
            self.metadata[name] = {
                "type": db_type,
                "name": db_name,
                "host": db_host,
                "port": db_port,
            }
            
            logger.info(f"✅ Added connection '{name}'")
            return f"✅ Connection '{name}' added successfully"
            
        except Exception as e:
            logger.error(f"Failed to add connection '{name}': {str(e)}")
            return f"❌ Failed to add connection '{name}': {str(e)}"
    
    def remove_connection(self, name: str) -> str:
        """Remove a database connection."""
        if name not in self.connections:
            return f"❌ Connection '{name}' not found"
        
        try:
            self.connections[name].dispose()
            del self.connections[name]
            del self.metadata[name]
            
            logger.info(f"✅ Removed connection '{name}'")
            return f"✅ Connection '{name}' removed"
            
        except Exception as e:
            logger.error(f"Failed to remove connection '{name}': {str(e)}")
            return f"❌ Failed to remove connection: {str(e)}"
    
    def get_connection(self, name: str) -> Optional[Engine]:
        """Get a database connection by name."""
        return self.connections.get(name)
    
    def list_connections(self) -> List[str]:
        """List all connection names."""
        return list(self.connections.keys())
    
    def get_connection_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get connection metadata."""
        return self.metadata.get(name)
    
    def execute_on_all(self, query: str) -> Dict[str, Any]:
        """
        Execute query on all connected databases.
        
        Args:
            query: SQL query to execute
            
        Returns:
            Dictionary with results from each database
        """
        results = {}
        
        from sqlalchemy import text
        
        for name, engine in self.connections.items():
            try:
                with engine.connect() as conn:
                    result = conn.execute(text(query))
                    rows = result.fetchall()
                    columns = list(result.keys())
                    
                    results[name] = {
                        "success": True,
                        "columns": columns,
                        "data": [dict(zip(columns, row)) for row in rows],
                        "row_count": len(rows),
                    }
            except Exception as e:
                results[name] = {
                    "success": False,
                    "error": str(e),
                }
        
        return results
    
    def compare_schemas(self) -> Dict[str, Any]:
        """Compare schemas across all connected databases."""
        from sqlalchemy import inspect
        
        schemas = {}
        
        for name, engine in self.connections.items():
            try:
                inspector = inspect(engine)
                table_names = inspector.get_table_names()
                
                schemas[name] = {
                    "table_count": len(table_names),
                    "tables": table_names,
                }
            except Exception as e:
                schemas[name] = {
                    "error": str(e),
                }
        
        return schemas

