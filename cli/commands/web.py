"""Web UI commands for myquery CLI."""
import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from config import get_logger, settings

app = typer.Typer()
console = Console()
logger = get_logger(__name__)


@app.command()
def start(
    host: Optional[str] = typer.Option(
        None,
        "--host",
        "-h",
        help="Server host (default: 0.0.0.0)",
    ),
    port: Optional[int] = typer.Option(
        None,
        "--port",
        "-p",
        help="Server port (default: 8000)",
    ),
):
    """
    Start the Web UI server.
    
    The web interface provides:
    - Interactive query interface
    - Visual schema explorer
    - Real-time chat with database
    - Data visualization
    
    Examples:
        myquery web start
        myquery web start --port 3000
    """
    try:
        server_host = host or "0.0.0.0"
        server_port = port or 8000
        
        console.print(Panel(
            f"🌐 Starting Web UI Server\n\n"
            f"Host: {server_host}\n"
            f"Port: {server_port}\n\n"
            f"Open in browser:\n"
            f"  🔗 http://localhost:{server_port}\n\n"
            f"Features:\n"
            f"  • Interactive query interface\n"
            f"  • Schema explorer\n"
            f"  • Real-time chat\n"
            f"  • Data visualization\n\n"
            f"Press Ctrl+C to stop the server",
            title="🚀 myquery Web UI",
            border_style="cyan",
        ))
        
        # Import and start web server
        from web.main import start_web_server
        start_web_server(host=server_host, port=server_port)
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]🛑 Server stopped[/yellow]")
    except Exception as e:
        logger.error(f"Web server error: {str(e)}")
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

