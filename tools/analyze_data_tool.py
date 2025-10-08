"""Data analysis tool for myquery."""
from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from config.logging import get_logger
import json

logger = get_logger(__name__)


class AnalyzeDataInput(BaseModel):
    """Input schema for AnalyzeDataTool."""
    query_result_json: str = Field(description="JSON string containing query results")
    user_prompt: str = Field(description="Original user question/prompt")


class AnalyzeDataTool(BaseTool):
    """Tool for analyzing query results using AI."""
    
    name: str = "analyze_data"
    description: str = """
    Analyze query results and provide insights, summaries, or answers.
    Uses AI to interpret data and answer the user's original question.
    Use this tool to provide meaningful insights from query results.
    """
    args_schema: Type[BaseModel] = AnalyzeDataInput
    
    llm: Optional[ChatOpenAI] = None
    
    def _run(self, query_result_json: str, user_prompt: str) -> str:
        """
        Analyze query results.
        
        Args:
            query_result_json: JSON string with query results
            user_prompt: Original user question
            
        Returns:
            Analysis and insights
        """
        if self.llm is None:
            return "❌ LLM not configured. Please set up OpenAI API key."
        
        try:
            logger.info("Analyzing query results...")
            
            result_data = json.loads(query_result_json)
            
            # Check if query was successful
            if not result_data.get("success", False):
                return "Cannot analyze data: query execution failed."
            
            data = result_data.get("data", [])
            columns = result_data.get("columns", [])
            row_count = result_data.get("row_count", 0)
            
            if not data:
                return "No data to analyze."
            
            # Create analysis prompt
            prompt = f"""
            Analyze the following query results and provide insights based on the user's question.
            
            USER QUESTION: {user_prompt}
            
            QUERY RESULTS:
            Columns: {', '.join(columns)}
            Row Count: {row_count}
            
            Data Sample:
            {json.dumps(data[:10], indent=2, default=str)}
            
            Please provide:
            1. Direct answer to the user's question
            2. Key insights from the data
            3. Notable patterns or trends
            4. Any recommendations or observations
            
            Keep the analysis concise, practical, and focused on answering the user's question.
            """
            
            response = self.llm.invoke(prompt)
            analysis = response.content
            
            logger.info("✅ Data analysis completed")
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid result JSON: {str(e)}")
            return f"❌ Invalid result JSON: {str(e)}"
        except Exception as e:
            logger.error(f"Data analysis failed: {str(e)}")
            return f"❌ Failed to analyze data: {str(e)}"
    
    async def _arun(self, *args, **kwargs) -> str:
        """Async version (not implemented)."""
        return self._run(*args, **kwargs)

