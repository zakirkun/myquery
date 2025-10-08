"""Settings management for myquery using Pydantic."""
from typing import Optional, Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., description="OpenAI API key")
    openai_model: str = Field(
        default="gpt-4-turbo-preview", 
        description="OpenAI model to use"
    )
    
    # Database Configuration
    db_type: Optional[Literal["postgresql", "mysql", "sqlite"]] = Field(
        default=None, 
        description="Database type"
    )
    db_host: Optional[str] = Field(default="localhost", description="Database host")
    db_port: Optional[int] = Field(default=5432, description="Database port")
    db_name: Optional[str] = Field(default=None, description="Database name")
    db_user: Optional[str] = Field(default=None, description="Database user")
    db_password: Optional[str] = Field(default=None, description="Database password")
    
    # MCP Configuration
    mcp_port: int = Field(default=7766, description="MCP server port")
    mcp_host: str = Field(default="0.0.0.0", description="MCP server host")
    
    # Debug Configuration
    debug_mode: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    
    # Query Generation Settings
    max_query_retries: int = Field(default=3, description="Maximum query generation retries")
    query_timeout: int = Field(default=30, description="Query execution timeout in seconds")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    def get_db_url(self) -> Optional[str]:
        """Generate database URL from configuration."""
        if not self.db_type or not self.db_name:
            return None
            
        if self.db_type == "sqlite":
            return f"sqlite:///{self.db_name}"
        
        if not self.db_user or not self.db_password:
            return None
            
        if self.db_type == "postgresql":
            return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        elif self.db_type == "mysql":
            return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        
        return None


# Global settings instance
try:
    settings = Settings()
except Exception as e:
    # If settings cannot be loaded (e.g., missing API key), create a placeholder
    # The CLI will handle the error appropriately
    print(f"Warning: Could not load settings: {e}")
    settings = None

