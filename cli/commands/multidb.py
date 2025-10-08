"""Multi-database commands for myquery CLI."""
import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from core.agent import QueryAgent
from config import get_logger
import json

app = typer.Typer()
console = Console()
logger = get_logger(__name__)


@app.command()
def add(
    name: str = typer.Argument(..., help="Connection name"),
    db_type: str = typer.Option(..., "--type", "-t", help="Database type"),
    db_name: str = typer.Option(..., "--name", "-n", help="Database name"),
    db_host: Optional[str] = typer.Option("localhost", "--host", "-h"),
    db_port: Optional[int] = typer.Option(None, "--port", "-p"),
    db_user: Optional[str] = typer.Option(None, "--user", "-u"),
    db_password: Optional[str] = typer.Option(None, "--password"),
):
    """
    Add a database connection to multi-DB manager.
    
    Examples:
        myquery multidb add prod --type postgresql --name proddb --user admin
        myquery multidb add dev --type sqlite --name dev.db
    """
    try:
        agent = QueryAgent()
        
        result = agent.multi_db_manager.add_connection(
            name=name,
            db_type=db_type,
            db_name=db_name,
            db_host=db_host,
            db_port=db_port,
            db_user=db_user,
            db_password=db_password,
        )
        
        if result.startswith("✅"):
            console.print(Panel(result, title="Connection Added", border_style="green"))
        else:
            console.print(Panel(result, title="Failed", border_style="red"))
            
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def list():
    """List all database connections."""
    try:
        agent = QueryAgent()
        connections = agent.multi_db_manager.list_connections()
        
        if not connections:
            console.print("[yellow]No database connections configured[/yellow]")
            return
        
        table = Table(title="🗄️  Database Connections", show_header=True, header_style="bold cyan")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Database", style="yellow")
        table.add_column("Host", style="blue")
        
        for conn_name in connections:
            info = agent.multi_db_manager.get_connection_info(conn_name)
            if info:
                table.add_row(
                    conn_name,
                    info.get("type", "?"),
                    info.get("name", "?"),
                    info.get("host", "?") or "N/A",
                )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def remove(name: str = typer.Argument(..., help="Connection name to remove")):
    """Remove a database connection."""
    try:
        agent = QueryAgent()
        result = agent.multi_db_manager.remove_connection(name)
        
        if result.startswith("✅"):
            console.print(f"[green]{result}[/green]")
        else:
            console.print(f"[red]{result}[/red]")
            
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def query(
    sql: str = typer.Argument(..., help="SQL query to execute on all databases"),
    connections: Optional[str] = typer.Option(
        "all",
        "--connections",
        "-c",
        help="Comma-separated connection names or 'all'",
    ),
):
    """
    Execute query on multiple databases.
    
    Examples:
        myquery multidb query "SELECT COUNT(*) FROM users"
        myquery multidb query "SELECT * FROM products LIMIT 10" --connections prod,dev
    """
    try:
        agent = QueryAgent()
        
        console.print(Panel(
            f"[bold]SQL:[/bold] {sql}\n"
            f"[bold]Databases:[/bold] {connections}",
            title="🔍 Multi-Database Query",
            border_style="cyan",
        ))
        
        with console.status("[bold cyan]Executing on all databases..."):
            result_json = agent.multi_db_query_tool._run(
                query=sql,
                connections=connections,
            )
        
        results = json.loads(result_json)
        
        # Display results for each database
        for db_name, db_result in results.items():
            console.print(f"\n[bold cyan]━━━ {db_name} ━━━[/bold cyan]")
            
            if not db_result.get("success"):
                console.print(f"[red]❌ Error: {db_result.get('error')}[/red]")
                continue
            
            data = db_result.get("data", [])
            columns = db_result.get("columns", [])
            
            if not data:
                console.print("[yellow]No results[/yellow]")
                continue
            
            # Create table
            table = Table(show_header=True, header_style="bold green")
            for col in columns:
                table.add_column(str(col))
            
            for row in data[:10]:  # Show first 10 rows
                table.add_row(*[str(row.get(col, "")) for col in columns])
            
            console.print(table)
            console.print(f"[dim]{db_result.get('row_count', 0)} row(s)[/dim]")
        
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def compare():
    """Compare schemas across all connected databases."""
    try:
        agent = QueryAgent()
        
        with console.status("[bold cyan]Comparing schemas..."):
            schemas = agent.multi_db_manager.compare_schemas()
        
        table = Table(title="📊 Schema Comparison", show_header=True, header_style="bold cyan")
        table.add_column("Database", style="cyan")
        table.add_column("Tables", style="green")
        table.add_column("Table Names", style="yellow")
        
        for db_name, schema_info in schemas.items():
            if "error" in schema_info:
                table.add_row(db_name, "[red]Error[/red]", schema_info["error"])
            else:
                table_count = schema_info.get("table_count", 0)
                table_names = ", ".join(schema_info.get("tables", []))
                table.add_row(db_name, str(table_count), table_names[:50] + "..." if len(table_names) > 50 else table_names)
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

