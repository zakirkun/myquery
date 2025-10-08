"""Main CLI entrypoint for myquery."""
import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from config import setup_logging, get_logger, settings
from cli.commands import chat, connect, query, server, visualize, web, multidb, export

# Initialize Typer app
app = typer.Typer(
    name="myquery",
    help="🤖 AI-powered CLI for natural language database interactions",
    add_completion=False,
)

# Add command modules
app.add_typer(chat.app, name="chat", help="💬 Interactive chat with database")
app.add_typer(connect.app, name="connect", help="🔌 Connect to a database")
app.add_typer(query.app, name="query", help="🔍 Execute queries")
app.add_typer(export.app, name="export", help="💾 Export query results")
app.add_typer(visualize.app, name="visualize", help="📊 Data visualization")
app.add_typer(multidb.app, name="multidb", help="🗄️  Multi-database operations")
app.add_typer(server.app, name="server", help="🌐 MCP server management")
app.add_typer(web.app, name="web", help="🌐 Web UI server")

console = Console()


@app.callback()
def main(
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Enable debug mode with detailed logging",
    ),
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        "-l",
        help="Set logging level (DEBUG, INFO, WARNING, ERROR)",
    ),
):
    """
    🤖 myquery - AI-powered database query assistant
    
    Connect to databases and query them using natural language.
    """
    # Setup logging
    setup_logging(level=log_level, debug_mode=debug)


@app.command()
def version():
    """Show version information."""
    console.print(Panel(
        "[bold cyan]myquery[/bold cyan] [dim]v0.1.0[/dim]\n\n"
        "AI-powered CLI for natural language database interactions\n\n"
        "Built with ❤️  using LangChain, OpenAI, and Typer",
        title="📦 Version Info",
        border_style="cyan",
    ))


@app.command()
def info():
    """Show system information and configuration."""
    logger = get_logger(__name__)
    
    info_text = f"""
## 🔧 Configuration

- **OpenAI Model**: {settings.openai_model if settings else 'Not configured'}
- **MCP Port**: {settings.mcp_port if settings else 'Not configured'}
- **Debug Mode**: {settings.debug_mode if settings else 'Not configured'}

## 🗄️ Database Configuration

- **Type**: {settings.db_type if settings and settings.db_type else 'Not set'}
- **Host**: {settings.db_host if settings and settings.db_host else 'Not set'}
- **Database**: {settings.db_name if settings and settings.db_name else 'Not set'}

## 📚 Available Commands

- `myquery connect` - Connect to a database
- `myquery chat` - Start interactive chat session
- `myquery query` - Execute a single query
- `myquery info` - Show this information
- `myquery version` - Show version

## 🚀 Quick Start

```bash
# Connect to a database
myquery connect --db-type postgresql --db-name mydb --db-user user

# Start chatting
myquery chat

# Or execute a single query
myquery query "Show me the top 10 customers"
```
"""
    
    console.print(Panel(
        Markdown(info_text),
        title="ℹ️  System Information",
        border_style="blue",
    ))


if __name__ == "__main__":
    app()

