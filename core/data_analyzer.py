"""Data analysis utilities for myquery."""
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from config.logging import get_logger
import json

logger = get_logger(__name__)


class DataAnalyzer:
    """Utility class for analyzing query results."""
    
    def __init__(self, llm: ChatOpenAI):
        """
        Initialize DataAnalyzer.
        
        Args:
            llm: LangChain ChatOpenAI instance
        """
        self.llm = llm
    
    def analyze_results(
        self,
        data: List[Dict[str, Any]],
        columns: List[str],
        user_question: str,
    ) -> str:
        """
        Analyze query results and provide insights.
        
        Args:
            data: Query result data
            columns: Column names
            user_question: Original user question
            
        Returns:
            Analysis text
        """
        if not data:
            return "No data to analyze."
        
        prompt = f"""
        Analyze the following query results and provide insights.
        
        USER QUESTION: {user_question}
        
        COLUMNS: {', '.join(columns)}
        ROW COUNT: {len(data)}
        
        DATA SAMPLE:
        {json.dumps(data[:10], indent=2, default=str)}
        
        Provide:
        1. Direct answer to the user's question
        2. Key insights and patterns
        3. Notable observations
        4. Recommendations if applicable
        
        Keep it concise and actionable.
        """
        
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            return f"❌ Analysis failed: {str(e)}"
    
    def summarize_data(
        self,
        data: List[Dict[str, Any]],
        columns: List[str],
    ) -> Dict[str, Any]:
        """
        Generate statistical summary of data.
        
        Args:
            data: Query result data
            columns: Column names
            
        Returns:
            Summary statistics
        """
        if not data:
            return {"row_count": 0}
        
        summary = {
            "row_count": len(data),
            "column_count": len(columns),
            "columns": columns,
        }
        
        # Count non-null values per column
        null_counts = {col: 0 for col in columns}
        
        for row in data:
            for col in columns:
                if row.get(col) is None or row.get(col) == "":
                    null_counts[col] += 1
        
        summary["null_counts"] = null_counts
        
        return summary
    
    def format_insight(
        self,
        insight_type: str,
        message: str,
        data: Optional[Any] = None,
    ) -> str:
        """
        Format insight message with appropriate emoji and styling.
        
        Args:
            insight_type: Type of insight (info, warning, success, error)
            message: Insight message
            data: Optional data to include
            
        Returns:
            Formatted insight string
        """
        emoji_map = {
            "info": "ℹ️ ",
            "warning": "⚠️ ",
            "success": "✅",
            "error": "❌",
            "insight": "💡",
            "trend": "📈",
        }
        
        emoji = emoji_map.get(insight_type, "")
        formatted = f"{emoji} {message}"
        
        if data:
            formatted += f"\n{json.dumps(data, indent=2, default=str)}"
        
        return formatted

