"""Interactive chat commands for myquery CLI."""
import typer
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown
from core.agent import QueryAgent
from config import get_logger
from cli.utils import auto_connect, ensure_connected
import sys

app = typer.Typer()
console = Console()
logger = get_logger(__name__)


@app.command()
def start(
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Enable debug mode to see generated SQL",
    ),
    auto: bool = typer.Option(
        True,
        "--auto/--no-auto",
        help="Auto-connect using .env or saved session",
    ),
):
    """
    Start interactive chat session with database.
    
    Type your questions in natural language and get instant results!
    
    If database credentials are in .env, it will auto-connect automatically.
    
    Special commands:
    - 'exit' or 'quit' - Exit chat
    - 'clear' - Clear chat history
    - 'tables' - Show all tables
    - 'help' - Show this help
    """
    try:
        # Initialize agent
        console.print(Panel(
            "[bold cyan]🤖 myquery Chat Assistant[/bold cyan]\n\n"
            "Ask me anything about your database in natural language!\n\n"
            "[dim]Type 'help' for commands, 'exit' to quit[/dim]",
            border_style="cyan",
        ))
        
        agent = QueryAgent()
        
        # Auto-connect if enabled and credentials available
        if auto:
            agent = auto_connect(agent, show_messages=True)
        elif not agent.is_connected():
            console.print("[yellow]⚠️  Not connected to a database.[/yellow]")
            console.print("\nPlease connect first using:")
            console.print("  [cyan]python -m cli.main connect db[/cyan]")
            console.print("\nOr enable auto-connect (it will use .env or saved session)")
            raise typer.Exit(1)
        
        # Get table list
        tables = agent.get_table_list()
        console.print(f"\n📊 Connected to database with {len(tables)} table(s)\n")
        
        # Chat loop
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
                
                if not user_input.strip():
                    continue
                
                # Handle special commands
                if user_input.lower() in ["exit", "quit", "q"]:
                    console.print("\n👋 Goodbye!")
                    break
                
                elif user_input.lower() == "clear":
                    agent.clear_history()
                    console.print("[green]✅ Chat history cleared[/green]")
                    continue
                
                elif user_input.lower() == "tables":
                    console.print("\n📋 Available tables:")
                    for table in tables:
                        console.print(f"  • {table}")
                    continue
                
                elif user_input.lower() == "help":
                    show_help()
                    continue
                
                # Process query with agent
                with console.status("[bold cyan]🤔 Thinking..."):
                    response = agent.chat(user_input, debug=debug)
                
                # Display response
                console.print(f"\n[bold green]Assistant:[/bold green]")
                console.print(Markdown(response))
                
            except KeyboardInterrupt:
                console.print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                logger.error(f"Chat error: {str(e)}")
                console.print(f"\n[red]❌ Error: {str(e)}[/red]")
                continue
    
    except Exception as e:
        logger.error(f"Chat initialization error: {str(e)}")
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        raise typer.Exit(1)


def show_help():
    """Show help information."""
    help_text = """
## 💬 Chat Commands

### Special Commands
- `exit`, `quit`, `q` - Exit chat session
- `clear` - Clear chat history
- `tables` - Show all database tables
- `help` - Show this help message

### Example Questions
- "Show me all tables"
- "List the top 10 customers by revenue"
- "What are the total sales by region?"
- "Find all orders from last month"
- "Show me products with low inventory"

### Tips
- Ask questions naturally, as if talking to a colleague
- The assistant will generate and execute SQL queries automatically
- Use debug mode (`--debug`) to see the generated SQL
- Build on previous questions - the chat has memory!
"""
    
    console.print(Panel(
        Markdown(help_text),
        title="❓ Help",
        border_style="blue",
    ))


if __name__ == "__main__":
    app()

