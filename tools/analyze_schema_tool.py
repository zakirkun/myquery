"""Schema analysis tool for myquery."""
from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from config.logging import get_logger
import json

logger = get_logger(__name__)


class AnalyzeSchemaInput(BaseModel):
    """Input schema for AnalyzeSchemaTool."""
    model_config = {"protected_namespaces": ()}
    
    schema_json: str = Field(description="JSON string containing database schema")


class AnalyzeSchemaTool(BaseTool):
    """Tool for analyzing database schema using AI."""
    
    name: str = "analyze_schema"
    description: str = """
    Analyze database schema to understand relationships, patterns, and data structure.
    Provides insights about table purposes, relationships, and recommended query patterns.
    Use this tool to get a high-level understanding of the database.
    """
    args_schema: Type[BaseModel] = AnalyzeSchemaInput
    
    llm: Optional[ChatOpenAI] = None
    
    def _run(self, schema_json: str) -> str:
        """
        Analyze database schema using AI.
        
        Args:
            schema_json: JSON string with schema information
            
        Returns:
            Analysis results as a formatted string
        """
        if self.llm is None:
            return "❌ LLM not configured. Please set up OpenAI API key."
        
        try:
            logger.info("Analyzing database schema...")
            
            schema_data = json.loads(schema_json)
            
            # Create analysis prompt
            prompt = f"""
            Analyze the following database schema and provide insights:
            
            {json.dumps(schema_data, indent=2)}
            
            Please provide:
            1. Overview of the database purpose based on table names
            2. Key relationships between tables
            3. Main entities and their roles
            4. Common query patterns that would be useful
            5. Any notable observations about the schema design
            
            Keep the analysis concise and practical.
            """
            
            response = self.llm.invoke(prompt)
            analysis = response.content
            
            logger.info("✅ Schema analysis completed")
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid schema JSON: {str(e)}")
            return f"❌ Invalid schema JSON: {str(e)}"
        except Exception as e:
            logger.error(f"Schema analysis failed: {str(e)}")
            return f"❌ Failed to analyze schema: {str(e)}"
    
    async def _arun(self, *args, **kwargs) -> str:
        """Async version (not implemented)."""
        return self._run(*args, **kwargs)

