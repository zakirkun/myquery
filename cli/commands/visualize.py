"""Visualization commands for myquery CLI."""
import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from core.agent import QueryAgent
from config import get_logger
from cli.utils import auto_connect, ensure_connected

app = typer.Typer()
console = Console()
logger = get_logger(__name__)


@app.command()
def chart(
    prompt: str = typer.Argument(
        ...,
        help="Natural language query for data to visualize",
    ),
    chart_type: str = typer.Option(
        "auto",
        "--type",
        "-t",
        help="Chart type: auto, bar, line, scatter, pie, table",
    ),
    auto_connect_db: bool = typer.Option(
        True,
        "--auto/--no-auto",
        help="Auto-connect using .env or saved session",
    ),
):
    """
    Execute query and visualize results.
    
    Examples:
        myquery visualize chart "Show sales by month"
        myquery visualize chart "Top 10 products" --type bar
    """
    try:
        # Initialize agent
        agent = QueryAgent()
        
        # Auto-connect if enabled
        if auto_connect_db:
            agent = ensure_connected(agent, "visualization")
        elif not agent.is_connected():
            console.print("[yellow]⚠️  Not connected to database.[/yellow]")
            raise typer.Exit(1)
        
        console.print(Panel(
            f"[bold]Query:[/bold] {prompt}\n"
            f"[bold]Chart Type:[/bold] {chart_type}",
            title="📊 Creating Visualization",
            border_style="cyan",
        ))
        
        # Execute query
        with console.status("[bold cyan]Executing query..."):
            results = agent.execute_query_flow(prompt, debug=False)
        
        if results.get("error"):
            console.print(f"[red]❌ Error: {results['error']}[/red]")
            raise typer.Exit(1)
        
        # Visualize results
        with console.status("[bold cyan]Creating visualization..."):
            viz_result = agent.visualize_data_tool._run(
                query_result_json=results.get("execution_result"),
                chart_type=chart_type,
                title=prompt[:50] + "..." if len(prompt) > 50 else prompt,
            )
        
        console.print(f"\n[green]{viz_result}[/green]")
        
    except Exception as e:
        logger.error(f"Visualization error: {str(e)}")
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

