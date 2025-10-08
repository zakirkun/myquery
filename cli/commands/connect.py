"""Database connection commands for myquery CLI."""
import typer
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from core.agent import QueryAgent
from config import get_logger, settings
from cli.utils import SESSION_FILE
import json
import os

app = typer.Typer()
console = Console()
logger = get_logger(__name__)


@app.command()
def db(
    db_type: Optional[str] = typer.Option(
        None,
        "--db-type",
        "-t",
        help="Database type: postgresql, mysql, or sqlite (uses .env if not provided)",
    ),
    db_name: Optional[str] = typer.Option(
        None,
        "--db-name",
        "-n",
        help="Database name or file path for SQLite (uses .env if not provided)",
    ),
    db_host: Optional[str] = typer.Option(
        None,
        "--db-host",
        "-h",
        help="Database host (uses .env if not provided)",
    ),
    db_port: Optional[int] = typer.Option(
        None,
        "--db-port",
        "-p",
        help="Database port (uses .env if not provided)",
    ),
    db_user: Optional[str] = typer.Option(
        None,
        "--db-user",
        "-u",
        help="Database username (uses .env if not provided)",
    ),
    db_password: Optional[str] = typer.Option(
        None,
        "--db-password",
        help="Database password (uses .env if not provided)",
    ),
    save_session: bool = typer.Option(
        True,
        "--save/--no-save",
        help="Save connection info for future sessions",
    ),
):
    """
    Connect to a database.
    
    If credentials are set in .env, you can simply run:
        myquery connect db
    
    Or override specific settings:
        myquery connect db --db-name other_database
    
    Examples:
        myquery connect db --db-type postgresql --db-name mydb --db-user postgres
        myquery connect db --db-type sqlite --db-name ./data.db
        myquery connect db  # Uses settings from .env
    """
    try:
        # Initialize agent
        agent = QueryAgent()
        
        # Use settings from .env as defaults
        db_type = db_type or (settings.db_type if settings else None)
        db_name = db_name or (settings.db_name if settings else None)
        db_host = db_host or (settings.db_host if settings else "localhost")
        db_port = db_port or (settings.db_port if settings else None)
        db_user = db_user or (settings.db_user if settings else None)
        db_password = db_password or (settings.db_password if settings else None)
        
        # Validate required fields
        if not db_type:
            console.print("[red]❌ Error: Database type is required.[/red]")
            console.print("Either set DB_TYPE in .env or use --db-type flag")
            raise typer.Exit(1)
        
        if not db_name:
            console.print("[red]❌ Error: Database name is required.[/red]")
            console.print("Either set DB_NAME in .env or use --db-name flag")
            raise typer.Exit(1)
        
        # Prompt for password if not provided and not SQLite
        if db_type.lower() != "sqlite" and not db_password:
            db_password = Prompt.ask(
                "🔐 Database password",
                password=True,
            )
        
        # Show what we're connecting to
        console.print(f"\n[cyan]Connecting to:[/cyan]")
        console.print(f"  Type: {db_type}")
        console.print(f"  Database: {db_name}")
        if db_type.lower() != "sqlite":
            console.print(f"  Host: {db_host}")
            console.print(f"  User: {db_user}\n")
        
        # Connect to database
        with console.status("[bold cyan]Connecting to database..."):
            result = agent.connect_database(
                db_type=db_type,
                db_name=db_name,
                db_host=db_host,
                db_port=db_port,
                db_user=db_user,
                db_password=db_password,
            )
        
        # Show result
        if result.startswith("✅"):
            console.print(Panel(
                result,
                title="🔌 Connection Status",
                border_style="green",
            ))
            
            # Get schema info
            with console.status("[bold cyan]Loading database schema..."):
                schema_json = agent.get_schema()
                schema_data = json.loads(schema_json)
            
            # Show table summary
            table_count = schema_data.get("total_tables", 0)
            table_names = list(schema_data.get("tables", {}).keys())
            
            console.print(f"\n📊 Found {table_count} table(s):")
            for table in table_names:
                console.print(f"  • {table}")
            
            # Save session if requested
            if save_session:
                session_data = {
                    "db_type": db_type,
                    "db_name": db_name,
                    "db_host": db_host,
                    "db_port": db_port,
                    "db_user": db_user,
                    # Note: We don't save password for security
                }
                
                with open(SESSION_FILE, "w") as f:
                    json.dump(session_data, f)
                
                console.print("\n💾 Connection info saved for future sessions")
        else:
            console.print(Panel(
                result,
                title="❌ Connection Failed",
                border_style="red",
            ))
            raise typer.Exit(1)
            
    except Exception as e:
        logger.error(f"Connection error: {str(e)}")
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def restore():
    """Restore connection from saved session."""
    try:
        if not os.path.exists(SESSION_FILE):
            console.print("[yellow]⚠️  No saved session found. Use 'myquery connect db' first.[/yellow]")
            raise typer.Exit(1)
        
        with open(SESSION_FILE, "r") as f:
            session_data = json.load(f)
        
        console.print(Panel(
            f"Restoring connection to:\n\n"
            f"Type: {session_data.get('db_type')}\n"
            f"Database: {session_data.get('db_name')}\n"
            f"Host: {session_data.get('db_host')}",
            title="🔄 Restoring Session",
            border_style="cyan",
        ))
        
        # Get password if needed
        db_password = None
        if session_data.get("db_type", "").lower() != "sqlite":
            db_password = Prompt.ask("🔐 Database password", password=True)
        
        # Connect
        agent = QueryAgent()
        
        with console.status("[bold cyan]Connecting..."):
            result = agent.connect_database(
                db_type=session_data.get("db_type"),
                db_name=session_data.get("db_name"),
                db_host=session_data.get("db_host"),
                db_port=session_data.get("db_port"),
                db_user=session_data.get("db_user"),
                db_password=db_password,
            )
        
        if result.startswith("✅"):
            console.print(Panel(result, title="✅ Connected", border_style="green"))
        else:
            console.print(Panel(result, title="❌ Failed", border_style="red"))
            raise typer.Exit(1)
            
    except Exception as e:
        logger.error(f"Restore error: {str(e)}")
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def status():
    """Show current connection status."""
    try:
        # Check .env settings
        has_env_config = False
        if settings and settings.db_type and settings.db_name:
            has_env_config = True
            console.print(Panel(
                f"Type: {settings.db_type}\n"
                f"Database: {settings.db_name}\n"
                f"Host: {settings.db_host}\n"
                f"User: {settings.db_user}",
                title="⚙️  .env Configuration",
                border_style="blue",
            ))
        
        # Check saved session
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "r") as f:
                session_data = json.load(f)
            
            console.print(Panel(
                f"Type: {session_data.get('db_type')}\n"
                f"Database: {session_data.get('db_name')}\n"
                f"Host: {session_data.get('db_host')}\n"
                f"User: {session_data.get('db_user')}",
                title="💾 Saved Session",
                border_style="cyan",
            ))
        
        if not has_env_config and not os.path.exists(SESSION_FILE):
            console.print("[yellow]ℹ️  No configuration found.[/yellow]")
            console.print("\nTo configure database:")
            console.print("1. Set credentials in .env file, or")
            console.print("2. Use: myquery connect db --db-type <type> --db-name <name>")
            
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")

