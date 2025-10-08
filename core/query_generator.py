"""Query generation utilities for myquery."""
from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from config.logging import get_logger

logger = get_logger(__name__)


class QueryGenerator:
    """Utility class for generating SQL queries."""
    
    def __init__(self, llm: ChatOpenAI):
        """
        Initialize QueryGenerator.
        
        Args:
            llm: LangChain ChatOpenAI instance
        """
        self.llm = llm
    
    def generate_sql(
        self,
        user_prompt: str,
        schema_summary: str,
        table_context: Optional[str] = None,
    ) -> str:
        """
        Generate SQL query from natural language.
        
        Args:
            user_prompt: User's natural language request
            schema_summary: Database schema summary
            table_context: Additional context about specific tables
            
        Returns:
            Generated SQL query
        """
        prompt_parts = [
            "You are an expert SQL query generator.",
            f"\nDATABASE SCHEMA:\n{schema_summary}",
        ]
        
        if table_context:
            prompt_parts.append(f"\nADDITIONAL CONTEXT:\n{table_context}")
        
        prompt_parts.append(f"\nUSER REQUEST: {user_prompt}")
        prompt_parts.append("""
RULES:
1. Generate ONLY the SQL query, no explanations
2. Use standard SQL syntax
3. Include appropriate JOINs based on foreign keys
4. Add LIMIT clauses for safety if not specified
5. Use meaningful aliases
6. Ensure the query is optimized
7. Do not include markdown formatting

SQL Query:
""")
        
        prompt = "\n".join(prompt_parts)
        
        try:
            response = self.llm.invoke(prompt)
            sql_query = response.content.strip()
            
            # Clean up the query
            sql_query = self._clean_query(sql_query)
            
            logger.info(f"Generated SQL: {sql_query[:100]}...")
            return sql_query
            
        except Exception as e:
            logger.error(f"Query generation failed: {str(e)}")
            raise
    
    def _clean_query(self, query: str) -> str:
        """Clean and format SQL query."""
        import re
        
        # Remove markdown code blocks
        query = re.sub(r'```sql\s*', '', query)
        query = re.sub(r'```\s*', '', query)
        
        # Remove extra whitespace
        query = query.strip()
        
        # Ensure semicolon at end
        if not query.endswith(';'):
            query += ';'
        
        return query
    
    def validate_query(self, query: str) -> Dict[str, Any]:
        """
        Validate SQL query for safety.
        
        Args:
            query: SQL query to validate
            
        Returns:
            Validation result dictionary
        """
        query_upper = query.upper().strip()
        
        # Check for destructive operations
        destructive_keywords = ["DROP", "DELETE", "TRUNCATE", "UPDATE", "ALTER"]
        is_destructive = any(query_upper.startswith(kw) for kw in destructive_keywords)
        
        # Check for SELECT query
        is_select = query_upper.startswith("SELECT")
        
        return {
            "is_valid": not is_destructive,
            "is_select": is_select,
            "is_destructive": is_destructive,
            "query": query,
        }

