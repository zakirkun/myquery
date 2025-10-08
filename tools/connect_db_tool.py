"""Database connection tool for myquery."""
from typing import Optional, Type, Dict, Any
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from config.logging import get_logger

logger = get_logger(__name__)


class ConnectDBInput(BaseModel):
    """Input schema for ConnectDBTool."""
    db_type: str = Field(description="Database type: postgresql, mysql, or sqlite")
    db_name: str = Field(description="Database name or file path for SQLite")
    db_host: Optional[str] = Field(default="localhost", description="Database host")
    db_port: Optional[int] = Field(default=None, description="Database port")
    db_user: Optional[str] = Field(default=None, description="Database username")
    db_password: Optional[str] = Field(default=None, description="Database password")


class ConnectDBTool(BaseTool):
    """Tool for connecting to a database."""
    
    name: str = "connect_db"
    description: str = """
    Connect to a database (PostgreSQL, MySQL, or SQLite).
    Returns a connection status message.
    Use this tool when you need to establish a database connection.
    """
    args_schema: Type[BaseModel] = ConnectDBInput
    
    # Store the engine instance
    _engine: Optional[Engine] = None
    
    def _run(
        self,
        db_type: str,
        db_name: str,
        db_host: Optional[str] = "localhost",
        db_port: Optional[int] = None,
        db_user: Optional[str] = None,
        db_password: Optional[str] = None,
    ) -> str:
        """
        Connect to database.
        
        Args:
            db_type: Database type (postgresql, mysql, sqlite)
            db_name: Database name or file path
            db_host: Database host
            db_port: Database port
            db_user: Database username
            db_password: Database password
            
        Returns:
            Connection status message
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
            logger.info(f"Connecting to {db_type} database: {db_name}")
            self._engine = create_engine(db_url, pool_pre_ping=True)
            
            # Test connection
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            logger.info("✅ Database connection successful")
            return f"✅ Successfully connected to {db_type} database: {db_name}"
            
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            return f"❌ Failed to connect to database: {str(e)}"
    
    async def _arun(self, *args, **kwargs) -> str:
        """Async version (not implemented)."""
        return self._run(*args, **kwargs)
    
    def get_engine(self) -> Optional[Engine]:
        """Get the SQLAlchemy engine instance."""
        return self._engine
    
    def is_connected(self) -> bool:
        """Check if database is connected."""
        if self._engine is None:
            return False
        try:
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except:
            return False

