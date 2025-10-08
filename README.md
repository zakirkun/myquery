<div align="center">

<img src="./assets/myquery-logo.png"/>

**Natural language database interactions powered by AI**

Transform your questions into SQL, visualize data, and get instant insights — all through conversation.

[Quick Start](#quick-start) • [Features](#features) • [Documentation](#documentation) • [Examples](#examples)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://langchain.com/)

</div>

---

## Overview

**myquery** is an AI-powered CLI and web interface that lets you interact with databases using natural language. Ask questions, get answers, visualize data, and export results — without writing SQL.

Built on **LangChain** and **OpenAI**, myquery bridges the gap between business questions and database queries.

```bash
You: "Show me top 10 customers by revenue"
myquery: [Generates SQL, executes query, displays table, provides AI analysis]
```

---

## Features

### Core Capabilities

- **Natural Language to SQL** — Ask questions in plain English (or Indonesian)
- **Interactive Chat** — Conversational interface with context memory
- **Smart Visualizations** — Auto-generates charts when you ask
- **AI Analysis** — Automatic insights and summaries from query results
- **Data Export** — Export to CSV, JSON, Excel with one command

### Advanced Features

- **Multi-Database Support** — PostgreSQL, MySQL, SQLite
- **Cross-DB Merge/Join** — Combine data from multiple databases
- **Query Optimization** — AI-powered performance suggestions
- **Schema Discovery** — Automatic analysis and exploration
- **Web UI** — Beautiful interface with real-time chat
- **MCP Server** — REST API for external integrations

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/zakirkun/myquery.git
cd myquery

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Configuration

Create a `.env` file:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Auto-connect database
DB_TYPE=postgresql
DB_NAME=mydb
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### First Query

```bash
# Start interactive chat (auto-connects using .env)
myquery chat start

# Ask a question
You: "Show me all tables"
You: "List top 10 products by sales"
You: "Show me a chart of revenue by month"
```

That's it! No manual connection, no SQL needed.

---

## Usage

### Interactive Chat

```bash
myquery chat start
```

Chat naturally with your database:

```
You: show me all customers
→ Displays formatted table + AI analysis

You: show me a bar chart of sales by region
→ Table + Analysis + Interactive chart (opens in browser)

You: export this to excel
→ Exports last result to Excel file
```

### Single Queries

```bash
# Natural language
myquery query execute "Find all orders from last month"

# Raw SQL
myquery query sql "SELECT * FROM customers LIMIT 10"

# With debug mode
myquery query execute "Show revenue" --debug
```

### Data Export

```bash
# Export query results
myquery export query "Show all customers" --format csv
myquery export query "Top products" --format excel --filename report
myquery export query "Revenue data" --format all  # CSV + JSON + Excel
```

### Visualizations

```bash
# Auto-detected chart type
myquery visualize chart "Sales by month"

# Specific chart type
myquery visualize chart "Revenue by region" --type bar
myquery visualize chart "Category distribution" --type pie
```

### Multi-Database Operations

```bash
# Add database connections
myquery multidb add prod --type postgresql --name proddb --user admin
myquery multidb add staging --type postgresql --name stagingdb --user admin

# Query all databases
myquery multidb query "SELECT COUNT(*) FROM users"

# Merge results (union)
myquery multidb query "SELECT * FROM products" --merge --merge-type union

# Join by key
myquery multidb query "SELECT id, revenue FROM sales" \
  --merge --merge-type join --merge-key id
```

### Web Interface

```bash
# Start web server
myquery web start

# Access at http://localhost:8000
# Features: Interactive chat, schema explorer, visualizations
```

### MCP Server

```bash
# Start MCP server for external integrations
myquery server start --port 7766
```

---

## Examples

### Business Analytics

```bash
# Revenue analysis
"What's our total revenue by month for this year?"
"Show top performing products"
"Which customers haven't ordered in 90 days?"

# Visualize trends
"Line chart of monthly sales trends"
"Pie chart showing revenue by category"
```

### Data Exploration

```bash
# Schema discovery
"What tables do we have?"
"Show me the structure of the orders table"
"Find tables with foreign key relationships"

# Sample data
"Show me a sample of the users table"
"What are the distinct values in the status column?"
```

### Cross-Database Comparison

```bash
# Compare environments
myquery multidb add prod --type postgresql --name prod_db
myquery multidb add staging --type postgresql --name staging_db

# Compare data
myquery multidb query "SELECT COUNT(*) FROM users"
myquery multidb compare
```

### Export & Share

```bash
# Generate reports
myquery export query "Monthly sales summary" --format excel
myquery export query "Customer list" --format csv
myquery export query "Analytics data" --format all
```

---

## Documentation

### Command Reference

| Command | Description |
|---------|-------------|
| `myquery chat start` | Interactive chat session |
| `myquery query execute "<question>"` | Execute natural language query |
| `myquery query sql "<sql>"` | Execute raw SQL |
| `myquery export query "<question>"` | Execute and export results |
| `myquery visualize chart "<question>"` | Create visualization |
| `myquery multidb add <name>` | Add database connection |
| `myquery multidb query "<sql>"` | Query multiple databases |
| `myquery web start` | Start web UI |
| `myquery server start` | Start MCP server |
| `myquery connect db` | Connect to database |
| `myquery --help` | Show all commands |

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (**required**) | - |
| `OPENAI_MODEL` | Model to use | `gpt-4-turbo-preview` |
| `DB_TYPE` | Database type | - |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |
| `DB_NAME` | Database name | - |
| `DB_USER` | Database user | - |
| `DB_PASSWORD` | Database password | - |
| `MCP_PORT` | MCP server port | `7766` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Supported Databases

- **PostgreSQL** — Full support with all features
- **MySQL** — Full support with all features
- **SQLite** — Full support, perfect for local development

### Export Formats

- **CSV** — Universal format, Excel/Google Sheets compatible
- **JSON** — Structured data with metadata
- **Excel** (.xlsx) — Formatted spreadsheet with auto-adjusted columns

### Chart Types

- **Auto** — Smart detection based on data
- **Bar** — Comparisons and rankings
- **Line** — Trends and time series
- **Pie** — Distributions and proportions
- **Scatter** — Correlations and relationships
- **Table** — Interactive data table

---

## Architecture

```
myquery/
├── cli/              # CLI interface (Typer)
│   ├── main.py       # Entry point
│   └── commands/     # Command modules
├── core/             # Core logic
│   ├── agent.py      # Main orchestrator
│   └── *.py          # Specialized modules
├── tools/            # LangChain tools
│   ├── connect_db_tool.py
│   ├── execute_query_tool.py
│   ├── visualize_data_tool.py
│   ├── export_data_tool.py
│   └── *.py
├── web/              # Web UI (FastAPI)
│   └── main.py
├── mcp/              # MCP Protocol
│   └── server.py
└── config/           # Configuration
    └── settings.py
```

### Query Flow

1. **User Input** → Natural language question
2. **Schema Analysis** → Understand database structure
3. **SQL Generation** → LLM creates SQL using schema context
4. **Validation** → Safety checks (no destructive operations)
5. **Execution** → Run query on database
6. **Formatting** → Display results in rich tables
7. **Analysis** → AI-powered insights
8. **Visualization** (optional) → Generate charts
9. **Export** (optional) → Save to file

---

## Safety Features

- **Read-Only by Default** — Blocks DROP, DELETE, TRUNCATE, UPDATE, ALTER
- **Connection Validation** — Tests connections before executing
- **Query Timeout** — Configurable timeout for long queries
- **Password Security** — Credentials never saved in session files
- **Error Handling** — Graceful failures with helpful messages

---

## Advanced Usage

### Programmatic API

```python
from core.agent import QueryAgent

# Initialize agent
agent = QueryAgent()

# Connect to database
agent.connect_database(
    db_type="postgresql",
    db_name="mydb",
    db_user="postgres",
    db_password="password"
)

# Execute query flow
results = agent.execute_query_flow(
    user_prompt="Show top 10 customers by revenue",
    debug=True,
    auto_visualize=True,
    optimize=True
)

# Access results
print(results["sql_query"])
print(results["analysis"])
print(results["visualization"])

# Export results
agent.export_results(
    query_result_json=results["execution_result"],
    format="excel",
    filename="top_customers"
)

# Get optimization suggestions
optimization = agent.optimize_query(results["sql_query"])
print(optimization)
```

### MCP Client

```python
from mcp.client import MCPClient

client = MCPClient("http://localhost:7766")

# Connect to database
response = client.connect_db(
    db_type="postgresql",
    db_name="mydb",
    db_user="postgres",
    db_password="password"
)

# Execute query
response = client.execute_query(
    prompt="Show top 10 customers by revenue"
)

print(response.data)
```

### Custom Tools

Extend myquery with custom tools:

```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class CustomToolInput(BaseModel):
    query: str = Field(description="Custom query parameter")

class CustomTool(BaseTool):
    name: str = "custom_tool"
    description: str = "Description of what this tool does"
    args_schema: Type[BaseModel] = CustomToolInput
    
    def _run(self, query: str) -> str:
        # Your custom logic here
        return f"Processed: {query}"

# Register with agent
agent = QueryAgent()
agent.tools.append(CustomTool())
```

---

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run with coverage
pytest --cov=. tests/
```

### Code Quality

```bash
# Format code
black .

# Lint
ruff check .

# Type checking
mypy .
```

### Running Examples

```bash
# Full features demo
python examples/full_features_demo.py

# SQLite demo with sample data
python examples/demo_sqlite.py

# MCP client example
python examples/mcp_client_example.py
```

---

## Requirements

- **Python** 3.8 or higher
- **OpenAI API Key** — Required for AI features
- **Database** — PostgreSQL, MySQL, or SQLite

### Python Dependencies

```
langchain>=0.1.0
langchain-openai>=0.0.5
openai>=1.12.0
typer>=0.9.0
rich>=13.7.0
sqlalchemy>=2.0.25
pandas>=2.1.0
plotly>=5.18.0
fastapi>=0.109.0
openpyxl>=3.1.0
```

Full list in [requirements.txt](requirements.txt)

---

## Roadmap

### Current Version (v0.4.0)

- ✅ Natural language queries
- ✅ Smart visualizations
- ✅ Data export (CSV, JSON, Excel)
- ✅ Multi-database merge/join
- ✅ Query optimization
- ✅ Web UI
- ✅ MCP server

### Upcoming Features

- [ ] Query result caching
- [ ] Query history and favorites
- [ ] Advanced chart customization
- [ ] Authentication for Web UI
- [ ] Scheduled queries and alerts
- [ ] Dashboard with multiple charts
- [ ] MongoDB and Redis support
- [ ] Natural language to database schema
- [ ] Query templates library

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

Built with these amazing open-source projects:

- [LangChain](https://github.com/langchain-ai/langchain) — LLM orchestration
- [OpenAI](https://openai.com/) — AI models
- [Typer](https://typer.tiangolo.com/) — CLI framework
- [Rich](https://rich.readthedocs.io/) — Terminal formatting
- [SQLAlchemy](https://www.sqlalchemy.org/) — Database toolkit
- [FastAPI](https://fastapi.tiangolo.com/) — Web framework
- [Plotly](https://plotly.com/) — Interactive visualizations
- [Pandas](https://pandas.pydata.org/) — Data manipulation

---

## Support

- 📖 [Documentation](QUICKSTART.md)
- 💬 [Discussions](https://github.com/zakirkun/myquery/discussions)
- 🐛 [Issue Tracker](https://github.com/zakirkun/myquery/issues)
- 📧 Email: support@myquery.dev

---

<div align="center">

**Made with ❤️ by the myquery team**

[⭐ Star us on GitHub](https://github.com/zakirkun/myquery) • [🐦 Follow on Twitter](https://twitter.com/myquery)

</div>
