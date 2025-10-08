"""MCP server management commands for myquery CLI."""
import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from mcp.server import start_mcp_server
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
        help="Server port (default: 7766)",
    ),
):
    """
    Start the MCP (Model Context Protocol) server.
    
    The MCP server allows external applications to interact with myquery
    through a REST API on port 7766.
    
    Examples:
        myquery server start
        myquery server start --port 8080
    """
    try:
        server_host = host or (settings.mcp_host if settings else "0.0.0.0")
        server_port = port or (settings.mcp_port if settings else 7766)
        
        console.print(Panel(
            f"🚀 Starting MCP Server\n\n"
            f"Host: {server_host}\n"
            f"Port: {server_port}\n\n"
            f"API Endpoints:\n"
            f"  • POST /mcp/action - Execute actions\n"
            f"  • GET /mcp/context/<session_id> - Get context\n"
            f"  • GET /mcp/sessions - List sessions\n\n"
            f"Press Ctrl+C to stop the server",
            title="🌐 MCP Server",
            border_style="cyan",
        ))
        
        # Start server
        start_mcp_server(host=server_host, port=server_port)
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]🛑 Server stopped[/yellow]")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

