"""Export commands for myquery CLI."""
import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from tools import ExportDataTool
from cli.utils import auto_connect
from core.agent import QueryAgent
from config import get_logger

app = typer.Typer()
console = Console()
logger = get_logger(__name__)


@app.command()
def query(
    prompt: str = typer.Argument(help="Natural language query to execute and export"),
    format: str = typer.Option(
        "all",
        "--format",
        "-f",
        help="Export format: csv, json, excel, or all"
    ),
    filename: Optional[str] = typer.Option(
        None,
        "--filename",
        "-n",
        help="Output filename (without extension)"
    ),
    output_dir: str = typer.Option(
        "outputs/exports",
        "--output",
        "-o",
        help="Output directory"
    ),
    auto: bool = typer.Option(
        True,
        "--auto/--no-auto",
        help="Auto-connect using .env or saved session",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Enable debug mode",
    ),
):
    """
    Execute a query and export results to file(s).
    
    Automatically executes the query and exports results in specified format(s).
    
    Examples:
        myquery export query "Show all customers" --format csv
        myquery export query "Top 10 products" --format all --filename top_products
        myquery export query "Revenue by region" -f excel -n revenue_report
    """
    try:
        console.print(Panel(
            f"[bold cyan]📊 Query & Export[/bold cyan]\n\n"
            f"Query: {prompt}\n"
            f"Format: {format}",
            border_style="cyan",
        ))
        
        # Initialize agent
        agent = QueryAgent()
        
        # Auto-connect
        if auto:
            agent = auto_connect(agent, show_messages=True)
        
        if not agent.is_connected():
            console.print("[red]❌ Not connected to database[/red]")
            console.print("Connect first with: myquery connect db")
            raise typer.Exit(1)
        
        # Execute query
        console.print("\n[cyan]🔄 Executing query...[/cyan]")
        results = agent.execute_query_flow(prompt, debug=debug, auto_visualize=False)
        
        if results.get("error"):
            console.print(f"[red]❌ Query failed: {results['error']}[/red]")
            raise typer.Exit(1)
        
        # Display results summary
        execution_result = results.get("execution_result")
        if execution_result:
            import json
            result_data = json.loads(execution_result)
            row_count = result_data.get("row_count", 0)
            console.print(f"[green]✅ Query executed: {row_count} rows retrieved[/green]")
        
        # Export data
        console.print(f"\n[cyan]💾 Exporting to {format}...[/cyan]")
        
        export_tool = ExportDataTool()
        export_result = export_tool._run(
            query_result_json=execution_result,
            format=format,
            filename=filename,
            output_dir=output_dir,
        )
        
        console.print(f"\n{export_result}")
        
        # Show analysis if available
        if results.get("analysis"):
            console.print(f"\n[bold green]💡 Analysis:[/bold green]")
            console.print(results["analysis"])
        
    except Exception as e:
        logger.error(f"Export failed: {str(e)}")
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def sql(
    sql_query: str = typer.Argument(help="SQL query to execute and export"),
    format: str = typer.Option(
        "all",
        "--format",
        "-f",
        help="Export format: csv, json, excel, or all"
    ),
    filename: Optional[str] = typer.Option(
        None,
        "--filename",
        "-n",
        help="Output filename (without extension)"
    ),
    output_dir: str = typer.Option(
        "outputs/exports",
        "--output",
        "-o",
        help="Output directory"
    ),
    auto: bool = typer.Option(
        True,
        "--auto/--no-auto",
        help="Auto-connect using .env or saved session",
    ),
):
    """
    Execute raw SQL and export results to file(s).
    
    Examples:
        myquery export sql "SELECT * FROM customers" --format csv
        myquery export sql "SELECT * FROM orders WHERE date > '2024-01-01'" -f excel
    """
    try:
        console.print(Panel(
            f"[bold cyan]📊 SQL Export[/bold cyan]\n\n"
            f"Format: {format}",
            border_style="cyan",
        ))
        
        # Initialize agent
        agent = QueryAgent()
        
        # Auto-connect
        if auto:
            agent = auto_connect(agent, show_messages=True)
        
        if not agent.is_connected():
            console.print("[red]❌ Not connected to database[/red]")
            raise typer.Exit(1)
        
        # Execute SQL
        console.print("\n[cyan]🔄 Executing SQL...[/cyan]")
        console.print(f"[dim]{sql_query}[/dim]\n")
        
        execution_result = agent.execute_query_tool._run(sql_query=sql_query)
        
        # Check if successful
        import json
        result_data = json.loads(execution_result)
        if not result_data.get("success"):
            console.print(f"[red]❌ Query failed: {result_data.get('error')}[/red]")
            raise typer.Exit(1)
        
        row_count = result_data.get("row_count", 0)
        console.print(f"[green]✅ Query executed: {row_count} rows retrieved[/green]")
        
        # Export
        console.print(f"\n[cyan]💾 Exporting to {format}...[/cyan]")
        
        export_tool = ExportDataTool()
        export_result = export_tool._run(
            query_result_json=execution_result,
            format=format,
            filename=filename,
            output_dir=output_dir,
        )
        
        console.print(f"\n{export_result}")
        
    except Exception as e:
        logger.error(f"SQL export failed: {str(e)}")
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

