"""Query optimization suggestion tool for myquery."""
from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from config.logging import get_logger
import json
import re

logger = get_logger(__name__)


class QueryOptimizationInput(BaseModel):
    """Input schema for QueryOptimizationTool."""
    sql_query: str = Field(description="SQL query to optimize")
    schema_json: Optional[str] = Field(
        default=None,
        description="Database schema context (optional)"
    )


class QueryOptimizationTool(BaseTool):
    """Tool for analyzing and suggesting query optimizations."""
    
    name: str = "optimize_query"
    description: str = """
    Analyze SQL queries and provide optimization suggestions.
    Detects performance issues like missing indexes, inefficient joins,
    SELECT *, N+1 queries, and suggests improvements.
    Use this tool to help users write better, faster queries.
    """
    args_schema: Type[BaseModel] = QueryOptimizationInput
    
    llm: Optional[ChatOpenAI] = None
    
    def _run(
        self,
        sql_query: str,
        schema_json: Optional[str] = None
    ) -> str:
        """
        Analyze query and provide optimization suggestions.
        
        Args:
            sql_query: SQL query to analyze
            schema_json: Optional schema context
            
        Returns:
            Optimization suggestions and analysis
        """
        try:
            logger.info("Analyzing query for optimization...")
            
            # Basic static analysis
            static_issues = self._static_analysis(sql_query)
            
            # AI-powered optimization suggestions
            if self.llm:
                ai_suggestions = self._ai_optimization(sql_query, schema_json)
            else:
                ai_suggestions = None
            
            # Build response
            response = "🔍 **Query Optimization Analysis**\n\n"
            
            # Add SQL query
            response += f"**Query:**\n```sql\n{sql_query}\n```\n\n"
            
            # Static analysis results
            if static_issues:
                response += "**⚠️  Potential Issues Detected:**\n\n"
                for i, issue in enumerate(static_issues, 1):
                    response += f"{i}. **{issue['type']}**: {issue['message']}\n"
                    if issue.get('suggestion'):
                        response += f"   💡 *Suggestion*: {issue['suggestion']}\n"
                    response += "\n"
            else:
                response += "✅ No obvious issues detected in static analysis.\n\n"
            
            # AI suggestions
            if ai_suggestions:
                response += "**🧠 AI-Powered Suggestions:**\n\n"
                response += ai_suggestions + "\n"
            
            # General best practices
            response += "\n**📚 General Best Practices:**\n\n"
            response += "- Use specific column names instead of SELECT *\n"
            response += "- Add indexes on frequently queried columns\n"
            response += "- Use WHERE clauses to filter early\n"
            response += "- Consider using LIMIT for large result sets\n"
            response += "- Use EXPLAIN/EXPLAIN ANALYZE to check execution plan\n"
            
            logger.info("✅ Query optimization analysis completed")
            return response
            
        except Exception as e:
            logger.error(f"Query optimization failed: {str(e)}")
            return f"❌ Failed to analyze query: {str(e)}"
    
    async def _arun(self, *args, **kwargs) -> str:
        """Async version (not implemented)."""
        return self._run(*args, **kwargs)
    
    def _static_analysis(self, sql_query: str) -> list:
        """Perform static analysis on SQL query."""
        issues = []
        query_upper = sql_query.upper()
        
        # Check for SELECT *
        if re.search(r'\bSELECT\s+\*', query_upper):
            issues.append({
                'type': 'SELECT *',
                'message': 'Using SELECT * can be inefficient',
                'suggestion': 'Specify only the columns you need'
            })
        
        # Check for missing WHERE clause in SELECT
        if 'SELECT' in query_upper and 'WHERE' not in query_upper and 'LIMIT' not in query_upper:
            if 'FROM' in query_upper:
                issues.append({
                    'type': 'No WHERE clause',
                    'message': 'Query may return entire table',
                    'suggestion': 'Add WHERE clause to filter results or use LIMIT'
                })
        
        # Check for OR in WHERE clause (can prevent index usage)
        if re.search(r'\bWHERE\b.*\bOR\b', query_upper, re.DOTALL):
            issues.append({
                'type': 'OR in WHERE',
                'message': 'OR conditions can prevent index usage',
                'suggestion': 'Consider using UNION or IN clause instead'
            })
        
        # Check for NOT IN with subquery
        if 'NOT IN' in query_upper and '(' in sql_query:
            issues.append({
                'type': 'NOT IN with subquery',
                'message': 'NOT IN with subqueries can be slow',
                'suggestion': 'Consider using NOT EXISTS or LEFT JOIN with NULL check'
            })
        
        # Check for function on indexed column in WHERE
        if re.search(r'\bWHERE\b.*\b(UPPER|LOWER|SUBSTRING|DATE)\s*\(', query_upper, re.DOTALL):
            issues.append({
                'type': 'Function on column',
                'message': 'Functions on columns in WHERE prevent index usage',
                'suggestion': 'Consider functional indexes or restructuring query'
            })
        
        # Check for implicit type conversion
        if re.search(r"WHERE\s+\w+\s*=\s*'\d+'", sql_query, re.IGNORECASE):
            issues.append({
                'type': 'Implicit conversion',
                'message': 'Comparing numeric column with string can prevent index usage',
                'suggestion': 'Use proper data types in comparisons'
            })
        
        # Check for multiple JOINs without WHERE
        join_count = query_upper.count('JOIN')
        if join_count >= 3 and 'WHERE' not in query_upper:
            issues.append({
                'type': 'Multiple JOINs',
                'message': f'{join_count} JOINs without WHERE clause may be inefficient',
                'suggestion': 'Add WHERE clause to filter intermediate results'
            })
        
        # Check for LIKE with leading wildcard
        if re.search(r"LIKE\s+'%", query_upper):
            issues.append({
                'type': 'Leading wildcard',
                'message': 'LIKE with leading % prevents index usage',
                'suggestion': 'Use full-text search or avoid leading wildcards'
            })
        
        # Check for DISTINCT with ORDER BY
        if 'DISTINCT' in query_upper and 'ORDER BY' in query_upper:
            issues.append({
                'type': 'DISTINCT with ORDER BY',
                'message': 'DISTINCT with ORDER BY requires additional sorting',
                'suggestion': 'Ensure ORDER BY columns are in SELECT list'
            })
        
        return issues
    
    def _ai_optimization(self, sql_query: str, schema_json: Optional[str]) -> str:
        """Get AI-powered optimization suggestions."""
        if not self.llm:
            return ""
        
        try:
            schema_context = ""
            if schema_json:
                schema_data = json.loads(schema_json)
                tables = schema_data.get('tables', {})
                schema_context = f"\n\nDatabase Schema:\n{json.dumps(tables, indent=2)}"
            
            prompt = f"""
            Analyze this SQL query and provide specific optimization suggestions.
            
            SQL Query:
            {sql_query}
            {schema_context}
            
            Please provide:
            1. Performance optimization suggestions
            2. Index recommendations (if schema provided)
            3. Query rewrite suggestions (if applicable)
            4. Estimated impact of each suggestion
            
            Be concise and practical. Focus on actionable improvements.
            """
            
            response = self.llm.invoke(prompt)
            return response.content
            
        except Exception as e:
            logger.warning(f"AI optimization failed: {str(e)}")
            return ""
    
    def get_query_complexity_score(self, sql_query: str) -> dict:
        """
        Calculate query complexity score.
        
        Returns:
            Dict with complexity metrics
        """
        query_upper = sql_query.upper()
        
        metrics = {
            'join_count': query_upper.count('JOIN'),
            'subquery_count': sql_query.count('SELECT') - 1,  # -1 for main query
            'aggregate_count': sum([
                query_upper.count('COUNT'),
                query_upper.count('SUM'),
                query_upper.count('AVG'),
                query_upper.count('MAX'),
                query_upper.count('MIN'),
            ]),
            'has_group_by': 'GROUP BY' in query_upper,
            'has_having': 'HAVING' in query_upper,
            'has_order_by': 'ORDER BY' in query_upper,
            'has_distinct': 'DISTINCT' in query_upper,
        }
        
        # Calculate complexity score (0-100)
        score = 0
        score += min(metrics['join_count'] * 10, 30)
        score += min(metrics['subquery_count'] * 15, 30)
        score += min(metrics['aggregate_count'] * 5, 20)
        score += 5 if metrics['has_group_by'] else 0
        score += 5 if metrics['has_having'] else 0
        score += 3 if metrics['has_order_by'] else 0
        score += 2 if metrics['has_distinct'] else 0
        
        metrics['complexity_score'] = min(score, 100)
        metrics['complexity_level'] = self._get_complexity_level(metrics['complexity_score'])
        
        return metrics
    
    def _get_complexity_level(self, score: int) -> str:
        """Get complexity level from score."""
        if score < 20:
            return "Simple"
        elif score < 40:
            return "Moderate"
        elif score < 60:
            return "Complex"
        else:
            return "Very Complex"

