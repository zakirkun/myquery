"""Table formatting tool for myquery."""
from typing import Optional, Type, List, Dict, Any
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from rich.console import Console
from rich.table import Table
from rich import box
from config.logging import get_logger
import json

logger = get_logger(__name__)


class FormatTableInput(BaseModel):
    """Input schema for FormatTableTool."""
    query_result_json: str = Field(description="JSON string containing query results")
    title: Optional[str] = Field(default="Query Results", description="Table title")


class FormatTableTool(BaseTool):
    """Tool for formatting query results as rich CLI tables."""
    
    name: str = "format_table"
    description: str = """
    Format query results as a beautiful CLI table using Rich.
    Takes JSON query results and displays them in a formatted table.
    Use this tool to present data to users in a readable format.
    """
    args_schema: Type[BaseModel] = FormatTableInput
    
    def _run(self, query_result_json: str, title: Optional[str] = "Query Results") -> str:
        """
        Format query results as a table.
        
        Args:
            query_result_json: JSON string with query results
            title: Table title
            
        Returns:
            Formatted table as string (Rich will render it)
        """
        try:
            logger.info("Formatting query results...")
            
            result_data = json.loads(query_result_json)
            
            # Check if query was successful
            if not result_data.get("success", False):
                error_msg = result_data.get("error", "Unknown error")
                return f"❌ Query failed: {error_msg}"
            
            data = result_data.get("data", [])
            columns = result_data.get("columns", [])
            row_count = result_data.get("row_count", 0)
            truncated = result_data.get("truncated", False)
            
            if not data:
                return "ℹ️  Query executed successfully but returned no results."
            
            # Create Rich table
            console = Console()
            table = Table(
                title=title,
                box=box.ROUNDED,
                show_header=True,
                header_style="bold cyan",
                title_style="bold magenta",
            )
            
            # Add columns
            for col in columns:
                table.add_column(str(col), style="white", no_wrap=False)
            
            # Add rows
            for row in data:
                row_values = [str(row.get(col, "")) for col in columns]
                table.add_row(*row_values)
            
            # Print table
            console.print(table)
            
            # Print summary
            summary = f"\n📊 Results: {row_count} row(s)"
            if truncated:
                summary += " (truncated, use LIMIT to see more)"
            
            console.print(summary, style="dim")
            
            logger.info(f"✅ Table formatted: {row_count} rows")
            return f"Table displayed with {row_count} rows"
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid result JSON: {str(e)}")
            return f"❌ Invalid result JSON: {str(e)}"
        except Exception as e:
            logger.error(f"Table formatting failed: {str(e)}")
            return f"❌ Failed to format table: {str(e)}"
    
    async def _arun(self, *args, **kwargs) -> str:
        """Async version (not implemented)."""
        return self._run(*args, **kwargs)

