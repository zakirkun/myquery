"""Query execution commands for myquery CLI."""
import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from core.agent import QueryAgent
from config import get_logger
from cli.utils import auto_connect, ensure_connected

app = typer.Typer()
console = Console()
logger = get_logger(__name__)


@app.command()
def execute(
    prompt: str = typer.Argument(
        ...,
        help="Natural language query prompt",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Show generated SQL query before execution",
    ),
    analyze: bool = typer.Option(
        True,
        "--analyze/--no-analyze",
        help="Show AI analysis of results",
    ),
    auto: bool = typer.Option(
        True,
        "--auto/--no-auto",
        help="Auto-connect using .env or saved session if not connected",
    ),
):
    """
    Execute a single query using natural language.
    
    If database credentials are in .env, it will auto-connect automatically.
    
    Examples:
        myquery query execute "Show top 10 customers by revenue"
        myquery query execute "List all products" --debug
        myquery query execute "Find all active users" --no-auto
    """
    try:
        # Initialize agent
        agent = QueryAgent()
        
        # Auto-connect if enabled
        if auto:
            agent = ensure_connected(agent, "query execution")
        elif not agent.is_connected():
            console.print("[yellow]⚠️  Not connected to database.[/yellow]")
            console.print("Use: [cyan]python -m cli.main connect db[/cyan]")
            raise typer.Exit(1)
        
        # Execute query flow
        console.print(Panel(
            f"[bold]Query:[/bold] {prompt}",
            title="🔍 Executing Query",
            border_style="cyan",
        ))
        
        with console.status("[bold cyan]Processing..."):
            results = agent.execute_query_flow(prompt, debug=debug)
        
        # Check for errors
        if results.get("error"):
            console.print(Panel(
                results["error"],
                title="❌ Error",
                border_style="red",
            ))
            raise typer.Exit(1)
        
        # Show generated SQL in debug mode
        if debug and results.get("sql_query"):
            console.print("\n[bold cyan]📝 Generated SQL:[/bold cyan]")
            syntax = Syntax(
                results["sql_query"],
                "sql",
                theme="monokai",
                line_numbers=False,
            )
            console.print(syntax)
        
        # Results are already formatted and displayed by the tool
        # Show analysis if enabled
        if analyze and results.get("analysis"):
            console.print(f"\n[bold green]💡 Analysis:[/bold green]")
            console.print(results["analysis"])
        
        console.print("\n[green]✅ Query completed successfully[/green]")
        
    except Exception as e:
        logger.error(f"Query execution error: {str(e)}")
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def sql(
    sql_query: str = typer.Argument(
        ...,
        help="Raw SQL query to execute",
    ),
    confirm: bool = typer.Option(
        True,
        "--confirm/--no-confirm",
        help="Confirm before executing",
    ),
    auto: bool = typer.Option(
        True,
        "--auto/--no-auto",
        help="Auto-connect using .env or saved session if not connected",
    ),
):
    """
    Execute a raw SQL query directly.
    
    If database credentials are in .env, it will auto-connect automatically.
    
    Examples:
        myquery query sql "SELECT * FROM users LIMIT 10"
        myquery query sql "SELECT COUNT(*) FROM orders" --no-confirm
    """
    try:
        # Initialize agent
        agent = QueryAgent()
        
        # Auto-connect if enabled
        if auto:
            agent = ensure_connected(agent, "SQL execution")
        elif not agent.is_connected():
            console.print("[yellow]⚠️  Not connected to database.[/yellow]")
            raise typer.Exit(1)
        
        # Show query
        console.print("\n[bold cyan]SQL Query:[/bold cyan]")
        syntax = Syntax(sql_query, "sql", theme="monokai")
        console.print(syntax)
        
        # Confirm if needed
        if confirm:
            proceed = typer.confirm("\nExecute this query?")
            if not proceed:
                console.print("[yellow]❌ Query cancelled[/yellow]")
                raise typer.Exit(0)
        
        # Execute
        with console.status("[bold cyan]Executing..."):
            execution_result = agent.execute_query_tool._run(sql_query=sql_query)
        
        # Format and display
        formatted = agent.format_table_tool._run(
            query_result_json=execution_result,
            title="Query Results"
        )
        
        console.print("\n[green]✅ Query executed successfully[/green]")
        
    except Exception as e:
        logger.error(f"SQL execution error: {str(e)}")
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

