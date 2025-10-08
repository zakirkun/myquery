# 🤖 myquery

**AI-powered CLI for natural language database interactions**

myquery is a Python-based CLI assistant that lets you query, explore, and analyze your databases through natural language. Built with LangChain and OpenAI, it transforms your questions into SQL queries and provides intelligent insights.

---

## ✨ Features

- 🗣️ **Natural Language Queries** - Ask questions in plain English, get SQL results
- 🔌 **Multi-Database Support** - Works with PostgreSQL, MySQL, and SQLite
- 🧠 **AI-Powered Analysis** - Automatic insights and summaries from query results
- 💬 **Interactive Chat Mode** - Conversational interface with context awareness
- 🔍 **Schema Discovery** - Automatic database schema analysis and exploration
- 📊 **Data Visualization** - Interactive charts with Plotly (bar, line, scatter, pie)
- 🗄️  **Multi-Database Queries** - Query multiple databases simultaneously
- 🌐 **Web UI** - Beautiful web interface with FastAPI + WebSocket chat
- 🌐 **MCP Protocol** - REST API server for external integrations (port 7766)
- 🎨 **Beautiful CLI** - Rich formatting with tables, colors, and syntax highlighting
- 🐛 **Debug Mode** - See generated SQL queries before execution
- 🔄 **Auto-Connect** - Automatically connects using .env credentials

---

## 🚀 Quick Start

### Installation

```bash
# Clone or navigate to the project directory
cd myquery

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Configuration

Create a `.env` file in the project root:

```env
# Required: OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Model selection
OPENAI_MODEL=gpt-4-turbo-preview

# Optional: Default database connection
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydb
DB_USER=postgres
DB_PASSWORD=your_password

# Optional: MCP server configuration
MCP_PORT=7766
MCP_HOST=0.0.0.0
```

### Basic Usage

#### 1. Connect to a Database

**Easy way (using .env):**
```bash
# Set DB_TYPE, DB_NAME, DB_USER, DB_PASSWORD in .env
# Then simply run:
myquery connect db
```

**Or use command-line flags:**
```bash
# PostgreSQL
myquery connect db --db-type postgresql --db-name mydb --db-user postgres

# MySQL
myquery connect db --db-type mysql --db-name mydb --db-user root --db-port 3306

# SQLite
myquery connect db --db-type sqlite --db-name ./data.db

# Mix both: use .env defaults but override database name
myquery connect db --db-name other_database
```

#### 2. Start Interactive Chat

```bash
# Auto-connects using .env! No manual connect needed
myquery chat start
```

Example conversation:
```
You: show me all tables
Assistant: 📊 Found 5 table(s): users, orders, products, customers, transactions

You: show top 10 customers by total revenue
Assistant: [Generates and executes SQL, displays results in a table]

💡 Analysis: The top 10 customers account for 45% of total revenue...
```

#### 3. Execute Single Queries

```bash
# Natural language query (auto-connects!)
myquery query execute "Show all products with low inventory"

# With debug mode to see generated SQL
myquery query execute "List customers who made purchases last month" --debug

# Execute raw SQL (also auto-connects!)
myquery query sql "SELECT * FROM users LIMIT 10"

# Disable auto-connect if needed
myquery query execute "Show data" --no-auto
```

#### 4. Start MCP Server

```bash
# Start the MCP server on port 7766
myquery server start

# Custom port
myquery server start --port 8080
```

---

## 📚 Command Reference

### `myquery connect`

Connect to a database (uses .env if configured).

**Commands:**
- `db` - Connect to a database
- `restore` - Restore connection from saved session
- `status` - Show current connection status

**Example:**
```bash
# Uses .env automatically
myquery connect db

# Or specify credentials
myquery connect db \
  --db-type postgresql \
  --db-name mydb \
  --db-host localhost \
  --db-user postgres \
  --save
```

### `myquery chat`

Interactive chat with your database (auto-connects using .env).

**Commands:**
- `start` - Start interactive chat session

**Special Chat Commands:**
- `exit`, `quit`, `q` - Exit chat
- `clear` - Clear chat history
- `tables` - Show all database tables
- `help` - Show help message

**Example:**
```bash
myquery chat start --debug
```

### `myquery query`

Execute queries on your database (auto-connects if needed).

**Commands:**
- `execute` - Execute natural language query
- `sql` - Execute raw SQL query

**Example:**
```bash
# Natural language (auto-connects!)
myquery query execute "Find all orders from last week"

# Raw SQL
myquery query sql "SELECT COUNT(*) FROM users"
```

### `myquery visualize`

Create interactive visualizations from query results.

**Commands:**
- `chart` - Execute query and create chart

**Chart Types:**
- `auto` - Auto-detect best chart type
- `bar` - Bar chart
- `line` - Line chart
- `scatter` - Scatter plot
- `pie` - Pie chart
- `table` - Interactive table

**Example:**
```bash
myquery visualize chart "Show sales by month" --type line
myquery visualize chart "Product distribution" --type pie
```

### `myquery multidb`

Manage and query multiple databases simultaneously.

**Commands:**
- `add` - Add a database connection
- `list` - List all connections
- `remove` - Remove a connection
- `query` - Execute query on all/selected databases
- `compare` - Compare schemas across databases

**Example:**
```bash
# Add connections
myquery multidb add prod --type postgresql --name proddb --user admin
myquery multidb add dev --type sqlite --name dev.db

# Query all
myquery multidb query "SELECT COUNT(*) FROM users"

# Query specific databases
myquery multidb query "SELECT * FROM products" --connections prod,dev

# Compare schemas
myquery multidb compare
```

### `myquery web`

Start the web UI server.

**Commands:**
- `start` - Start the FastAPI web server

**Example:**
```bash
myquery web start
myquery web start --port 3000
```

Features:
- Interactive query interface
- Visual schema explorer  
- Real-time WebSocket chat
- Data visualization dashboard

### `myquery server`

Manage the MCP server.

**Commands:**
- `start` - Start the MCP server

**Example:**
```bash
myquery server start --host 0.0.0.0 --port 7766
```

### General Commands

- `myquery version` - Show version information
- `myquery info` - Show system information and configuration
- `myquery --help` - Show help for any command

---

## 🏗️ Architecture

### Core Components

```
myquery/
├── cli/              # CLI interface (Typer)
│   ├── main.py       # Main entrypoint
│   └── commands/     # Command modules
│       ├── chat.py   # Chat commands
│       ├── connect.py # Connection commands
│       ├── query.py  # Query commands
│       └── server.py # Server commands
│
├── core/             # Core logic
│   ├── agent.py      # Main orchestration agent
│   ├── schema_analyzer.py
│   ├── query_generator.py
│   └── data_analyzer.py
│
├── tools/            # LangChain tools
│   ├── connect_db_tool.py
│   ├── get_schema_tool.py
│   ├── analyze_schema_tool.py
│   ├── generate_query_tool.py
│   ├── execute_query_tool.py
│   ├── format_table_tool.py
│   └── analyze_data_tool.py
│
├── mcp/              # MCP Protocol
│   ├── server.py     # FastAPI server
│   ├── protocol.py   # Protocol definitions
│   └── client.py     # Python client
│
└── config/           # Configuration
    ├── settings.py   # Settings management
    └── logging.py    # Logging setup
```

### Query Flow

1. **User Input** → Natural language question
2. **Schema Extraction** → Load database structure
3. **Query Generation** → LLM generates SQL using schema context
4. **Validation** → Safety checks for destructive operations
5. **Execution** → Run SQL query on database
6. **Formatting** → Display results in rich tables
7. **Analysis** → AI-powered insights and summaries

---

## 🌐 MCP (Model Context Protocol)

myquery exposes a REST API on port 7766 for external integrations.

### Starting the Server

```bash
myquery server start
```

### API Endpoints

#### `POST /mcp/action`

Execute an MCP action.

**Request:**
```json
{
  "action": "connect_db",
  "parameters": {
    "db_type": "postgresql",
    "db_name": "mydb",
    "db_user": "postgres",
    "db_password": "password"
  },
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "success": true,
  "data": {"message": "✅ Successfully connected..."},
  "session_id": "abc-123",
  "context": {
    "connected": true,
    "db_type": "postgresql",
    "db_name": "mydb",
    "table_count": 5
  }
}
```

#### Available Actions

- `connect_db` - Connect to database
- `get_schema` - Get database schema
- `generate_query` - Generate SQL from natural language
- `execute_query` - Execute complete query flow
- `analyze_results` - Analyze query results
- `get_status` - Get connection status
- `chat` - Chat interaction

#### `GET /mcp/context/{session_id}`

Get session context and state.

#### `GET /mcp/sessions`

List all active sessions.

#### `DELETE /mcp/session/{session_id}`

Delete a session.

### Python Client Example

```python
from mcp.client import MCPClient

# Create client
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

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (**required**) | - |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4-turbo-preview` |
| `DB_TYPE` | Default database type (auto-used by all commands) | - |
| `DB_HOST` | Default database host | `localhost` |
| `DB_PORT` | Default database port | `5432` |
| `DB_NAME` | Default database name (auto-used by all commands) | - |
| `DB_USER` | Default database user | - |
| `DB_PASSWORD` | Default database password | - |
| `MCP_PORT` | MCP server port | `7766` |
| `MCP_HOST` | MCP server host | `0.0.0.0` |
| `DEBUG_MODE` | Enable debug logging | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |

**💡 Pro Tip:** Set `DB_TYPE`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` in `.env` once, and all commands will auto-connect without needing flags!

### Auto-Connect Feature

**NEW!** All commands now support auto-connect. Set credentials in `.env` once:

```env
DB_TYPE=postgresql
DB_NAME=mydb
DB_USER=admin
DB_PASSWORD=secret
```

Then simply run commands without connection flags:
```bash
myquery chat start          # Auto-connects!
myquery query execute "..."  # Auto-connects!
myquery visualize chart "..."  # Auto-connects!
```

### Session Persistence

Connection information is saved to `.myquery_session.json` when you use the `--save` flag:

```bash
myquery connect db --db-type postgresql --db-name mydb --save
```

Restore the connection:
```bash
myquery connect restore
```

---

## 🛡️ Safety Features

- **Destructive Query Prevention** - Blocks DROP, DELETE, TRUNCATE, UPDATE, ALTER by default
- **Connection Validation** - Tests database connections before proceeding
- **Query Timeout** - Configurable timeout for long-running queries
- **Password Security** - Passwords are not saved in session files
- **Error Handling** - Graceful error messages with helpful suggestions

---

## 🎯 Use Cases

### 1. Data Exploration & Visualization
```bash
# Interactive chat
myquery chat start
> "What tables do we have?"
> "Show me a sample of the users table"

# Visualize data
myquery visualize chart "Show sales trends by month" --type line
myquery visualize chart "Product category distribution" --type pie
```

### 2. Business Analytics
```bash
# Quick queries with auto-connect
myquery query execute "What's our total revenue by month for this year?"
myquery query execute "Show top performing products"
myquery query execute "Which customers haven't ordered in the last 90 days?"

# Visualize results
myquery visualize chart "Revenue by region" --type bar
```

### 3. Multi-Database Comparison
```bash
# Compare data across environments
myquery multidb add prod --type postgresql --name prod_db --user admin
myquery multidb add staging --type postgresql --name staging_db --user admin

# Query all databases
myquery multidb query "SELECT COUNT(*) as user_count FROM users"
myquery multidb compare
```

### 4. Database Administration
```bash
# Schema exploration
myquery chat start
> "Show all tables and their row counts"
> "Find tables with foreign key relationships"
> "List all columns in the orders table"

# Use web UI for visual exploration
myquery web start
# Navigate to http://localhost:8000
```

### 5. Team Collaboration via Web UI
```bash
# Start web server for team access
myquery web start --host 0.0.0.0 --port 8000

# Team members can access at:
# http://your-server-ip:8000
# - No CLI knowledge needed
# - Visual query interface
# - Real-time results
# - Interactive charts
```

---

## 🧪 Development

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
# Complete features demo
python examples/full_features_demo.py

# Basic usage example
python examples/example_usage.py

# MCP client example
python examples/mcp_client_example.py

# SQLite demo with sample data
python examples/demo_sqlite.py
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

Built with:
- [LangChain](https://github.com/langchain-ai/langchain) - LLM framework
- [OpenAI](https://openai.com/) - AI models
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database toolkit
- [FastAPI](https://fastapi.tiangolo.com/) - API framework
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Pandas](https://pandas.pydata.org/) - Data manipulation

---

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ by the myquery team**

