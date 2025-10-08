"""Utility functions for CLI commands."""
from typing import Optional, Tuple
from rich.console import Console
from rich.prompt import Prompt
from core.agent import QueryAgent
from config import settings
import json
import os

console = Console()
SESSION_FILE = ".myquery_session.json"


def get_db_credentials() -> Tuple[Optional[str], Optional[str], Optional[str], Optional[int], Optional[str], Optional[str]]:
    """
    Get database credentials from .env, session file, or prompt user.
    
    Returns:
        Tuple of (db_type, db_name, db_host, db_port, db_user, db_password)
    """
    # Try to load from .env first
    db_type = settings.db_type if settings else None
    db_name = settings.db_name if settings else None
    db_host = settings.db_host if settings else "localhost"
    db_port = settings.db_port if settings else None
    db_user = settings.db_user if settings else None
    db_password = settings.db_password if settings else None
    
    # Try to load from saved session if .env not complete
    if (not db_type or not db_name) and os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                session_data = json.load(f)
            
            db_type = db_type or session_data.get("db_type")
            db_name = db_name or session_data.get("db_name")
            db_host = db_host or session_data.get("db_host", "localhost")
            db_port = db_port or session_data.get("db_port")
            db_user = db_user or session_data.get("db_user")
            # Password never saved in session for security
        except:
            pass
    
    return db_type, db_name, db_host, db_port, db_user, db_password


def auto_connect(agent: Optional[QueryAgent] = None, show_messages: bool = True) -> QueryAgent:
    """
    Automatically connect to database using credentials from .env or session.
    
    Args:
        agent: Existing QueryAgent instance (creates new if None)
        show_messages: Whether to show connection messages
        
    Returns:
        Connected QueryAgent instance
        
    Raises:
        SystemExit: If connection fails or credentials not found
    """
    if agent is None:
        agent = QueryAgent()
    
    # Check if already connected
    if agent.is_connected():
        return agent
    
    # Get credentials
    db_type, db_name, db_host, db_port, db_user, db_password = get_db_credentials()
    
    # Validate required fields
    if not db_type or not db_name:
        console.print("[red]❌ Database credentials not configured.[/red]")
        console.print("\nPlease either:")
        console.print("1. Set DB_TYPE and DB_NAME in .env file")
        console.print("2. Run: [cyan]python -m cli.main connect db --db-type <type> --db-name <name>[/cyan]")
        console.print("3. Run: [cyan]python -m cli.main connect restore[/cyan] (if you have saved session)")
        raise SystemExit(1)
    
    # Prompt for password if needed and not provided
    if db_type.lower() != "sqlite" and not db_password:
        if show_messages:
            db_password = Prompt.ask("🔐 Database password", password=True)
        else:
            console.print("[red]❌ Database password required but not provided in .env[/red]")
            console.print("Either set DB_PASSWORD in .env or run with manual connect")
            raise SystemExit(1)
    
    # Show what we're connecting to
    if show_messages:
        console.print(f"\n[cyan]Auto-connecting to:[/cyan]")
        console.print(f"  Type: {db_type}")
        console.print(f"  Database: {db_name}")
        if db_type.lower() != "sqlite":
            console.print(f"  Host: {db_host}")
            console.print(f"  User: {db_user}")
        console.print()
    
    # Connect to database
    try:
        if show_messages:
            with console.status("[bold cyan]Connecting to database..."):
                result = agent.connect_database(
                    db_type=db_type,
                    db_name=db_name,
                    db_host=db_host,
                    db_port=db_port,
                    db_user=db_user,
                    db_password=db_password,
                )
        else:
            result = agent.connect_database(
                db_type=db_type,
                db_name=db_name,
                db_host=db_host,
                db_port=db_port,
                db_user=db_user,
                db_password=db_password,
            )
        
        if not result.startswith("✅"):
            console.print(f"[red]{result}[/red]")
            raise SystemExit(1)
        
        if show_messages:
            console.print(f"[green]{result}[/green]")
        
        return agent
        
    except SystemExit:
        raise
    except Exception as e:
        console.print(f"[red]❌ Connection failed: {str(e)}[/red]")
        raise SystemExit(1)


def ensure_connected(agent: QueryAgent, command_name: str = "this command") -> QueryAgent:
    """
    Ensure agent is connected, auto-connect if not.
    
    Args:
        agent: QueryAgent instance
        command_name: Name of command for error messages
        
    Returns:
        Connected QueryAgent instance
    """
    if not agent.is_connected():
        console.print(f"[yellow]⚠️  Not connected to database. Attempting auto-connect...[/yellow]\n")
        return auto_connect(agent, show_messages=True)
    return agent

