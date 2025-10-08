"""SQL query generation tool for myquery."""
from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from config.logging import get_logger
import json
import re

logger = get_logger(__name__)


class GenerateQueryInput(BaseModel):
    """Input schema for GenerateQueryTool."""
    model_config = {"protected_namespaces": ()}
    
    user_prompt: str = Field(description="Natural language query from user")
    schema_json: str = Field(description="JSON string containing database schema")
    chat_history: Optional[str] = Field(
        default="", 
        description="Previous chat history for context"
    )


class GenerateQueryTool(BaseTool):
    """Tool for generating SQL queries from natural language."""
    
    name: str = "generate_query"
    description: str = """
    Generate SQL queries from natural language prompts.
    Takes user input and database schema to create accurate SQL queries.
    Use this tool to convert user questions into executable SQL.
    """
    args_schema: Type[BaseModel] = GenerateQueryInput
    
    llm: Optional[ChatOpenAI] = None
    
    def _run(
        self, 
        user_prompt: str, 
        schema_json: str, 
        chat_history: Optional[str] = ""
    ) -> str:
        """
        Generate SQL query from natural language.
        
        Args:
            user_prompt: User's natural language query
            schema_json: Database schema in JSON format
            chat_history: Previous conversation context
            
        Returns:
            Generated SQL query
        """
        if self.llm is None:
            return "❌ LLM not configured. Please set up OpenAI API key."
        
        try:
            logger.info(f"Generating SQL query for: {user_prompt}")
            
            schema_data = json.loads(schema_json)
            
            # Build a concise schema representation
            schema_summary = self._build_schema_summary(schema_data)
            
            # Create query generation prompt
            prompt = f"""
            You are an expert SQL query generator. Generate a SQL query based on the user's request.
            
            DATABASE SCHEMA:
            {schema_summary}
            
            USER REQUEST: {user_prompt}
            
            {f"PREVIOUS CONTEXT: {chat_history}" if chat_history else ""}
            
            RULES:
            1. Generate ONLY the SQL query, no explanations
            2. Use standard SQL syntax compatible with the database
            3. Include appropriate JOINs based on foreign key relationships
            4. Use meaningful column aliases where helpful
            5. Add LIMIT clauses for safety if not specified
            6. Ensure the query is optimized and follows best practices
            7. Do not include markdown code blocks or formatting
            
            SQL Query:
            """
            
            response = self.llm.invoke(prompt)
            sql_query = response.content.strip()
            
            # Clean up the query (remove markdown formatting if present)
            sql_query = self._clean_sql_query(sql_query)
            
            logger.info(f"✅ Generated SQL query: {sql_query[:100]}...")
            return sql_query
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid schema JSON: {str(e)}")
            return f"❌ Invalid schema JSON: {str(e)}"
        except Exception as e:
            logger.error(f"Query generation failed: {str(e)}")
            return f"❌ Failed to generate query: {str(e)}"
    
    async def _arun(self, *args, **kwargs) -> str:
        """Async version (not implemented)."""
        return self._run(*args, **kwargs)
    
    def _build_schema_summary(self, schema_data: dict) -> str:
        """Build a concise schema summary for the prompt."""
        summary_parts = []
        
        for table_name, table_info in schema_data.get("tables", {}).items():
            columns = table_info.get("columns", [])
            col_names = [f"{col['name']} ({col['type']})" for col in columns]
            
            pk = table_info.get("primary_keys", [])
            fk = table_info.get("foreign_keys", [])
            
            table_summary = f"Table: {table_name}\n"
            table_summary += f"  Columns: {', '.join(col_names)}\n"
            
            if pk:
                table_summary += f"  Primary Key: {', '.join(pk)}\n"
            
            if fk:
                fk_info = [
                    f"{fk_item['columns']} -> {fk_item['refers_to_table']}.{fk_item['refers_to_columns']}"
                    for fk_item in fk
                ]
                table_summary += f"  Foreign Keys: {'; '.join(fk_info)}\n"
            
            summary_parts.append(table_summary)
        
        return "\n".join(summary_parts)
    
    def _clean_sql_query(self, query: str) -> str:
        """Clean SQL query from markdown formatting."""
        # Remove markdown code blocks
        query = re.sub(r'```sql\s*', '', query)
        query = re.sub(r'```\s*', '', query)
        
        # Remove extra whitespace
        query = query.strip()
        
        # Ensure query ends with semicolon
        if not query.endswith(';'):
            query += ';'
        
        return query

