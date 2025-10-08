# 🚀 Quick Start Guide

Get started with myquery in 5 minutes!

## 📋 Prerequisites

- Python 3.9 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- A database to query (PostgreSQL, MySQL, or SQLite)

## ⚡ Installation

### Windows

```powershell
# Run the setup script
.\scripts\setup.bat
```

### Linux/Mac

```bash
# Make the script executable
chmod +x scripts/setup.sh

# Run the setup script
./scripts/setup.sh
```

### Manual Installation

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## 🔑 Configuration

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` and add your credentials:**
   ```env
   # Required: OpenAI API Key
   OPENAI_API_KEY=sk-your-api-key-here
   OPENAI_MODEL=gpt-4-turbo-preview
   
   # Optional: Database Configuration (saves you from typing flags!)
   DB_TYPE=postgresql
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=mydb
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```

   **💡 Tip:** If you set database credentials in `.env`, you can just run `myquery connect db` without any flags!

## 🎯 First Steps

### 1. Connect to a Database

**Option A: Use .env configuration (Recommended)**

If you set database credentials in `.env`, simply run:
```bash
python -m cli.main connect db
```

myquery will automatically use your .env settings! 🎉

**Option B: Use command-line flags**

**SQLite (easiest to test):**
```bash
python -m cli.main connect db --db-type sqlite --db-name example.db
```

**PostgreSQL:**
```bash
python -m cli.main connect db \
  --db-type postgresql \
  --db-name mydb \
  --db-user postgres \
  --db-host localhost
```

**MySQL:**
```bash
python -m cli.main connect db \
  --db-type mysql \
  --db-name mydb \
  --db-user root \
  --db-port 3306
```

**Option C: Mix .env and flags**

Override specific settings from .env:
```bash
# Use .env for most settings, but connect to different database
python -m cli.main connect db --db-name other_database
```

### 2. Start Chatting!

```bash
# Auto-connects using .env credentials! 🎉
python -m cli.main chat start
```

**That's it!** If your credentials are in `.env`, myquery auto-connects automatically.

### 3. Try Some Queries

Example questions to ask in chat mode:

- "What tables do we have?"
- "Show me the first 10 rows from the users table"
- "Find all customers who made purchases last month"
- "What's the total revenue by product category?"
- "Show me the top 5 best-selling products"

### 4. Execute a Single Query

```bash
# Auto-connects if needed! No manual connection required
python -m cli.main query execute "Show top 10 customers by revenue"
```

With debug mode to see the generated SQL:
```bash
python -m cli.main query execute "List all active users" --debug
```

Execute raw SQL (also auto-connects!):
```bash
python -m cli.main query sql "SELECT COUNT(*) FROM orders WHERE status='completed'"
```

## 🌐 MCP Server (Optional)

Start the MCP server for external integrations:

```bash
python -m cli.main server start
```

The server will be available at `http://localhost:7766`

Test it with the example client:
```bash
python examples/mcp_client_example.py
```

## 📚 Common Commands

```bash
# Show help
python -m cli.main --help

# Connect to database (uses .env if configured)
python -m cli.main connect db

# Or with specific credentials
python -m cli.main connect db --db-type sqlite --db-name data.db

# Start chat (auto-connects using .env!)
python -m cli.main chat start

# Execute query (auto-connects if needed!)
python -m cli.main query execute "your question here"

# Execute raw SQL (auto-connects too!)
python -m cli.main query sql "SELECT * FROM users LIMIT 10"

# Show connection status (shows .env config and saved session)
python -m cli.main connect status

# Restore saved connection
python -m cli.main connect restore

# Start MCP server
python -m cli.main server start

# Show version
python -m cli.main version

# Show system info
python -m cli.main info
```

## 🎓 Example Workflow

```bash
# 1. Set your database credentials in .env file (ONE TIME SETUP)
# DB_TYPE=postgresql
# DB_NAME=sales_db
# DB_USER=admin
# DB_PASSWORD=your_password

# 2. Start chatting directly! (Auto-connects using .env)
python -m cli.main chat start

# That's it! No manual connection needed anymore! 🎉

# In chat mode:
You: What tables are available?
Assistant: 📊 Found 5 table(s): customers, orders, products, sales, inventory

You: Show me total sales by month for 2024
Assistant: [Displays table with results and analysis]

You: Which products have inventory below 10 units?
Assistant: [Generates query, shows results, provides insights]

# Type 'exit' to quit chat mode

# Or execute single queries directly (also auto-connects!)
python -m cli.main query execute "Show me top performing products this quarter"
```

## 🐛 Troubleshooting

### "No module named 'config'"

Make sure you're in the project directory and have activated the virtual environment:
```bash
cd myquery
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### "OpenAI API key is required"

Edit your `.env` file and add your API key:
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

### Database connection failed

- Check your database is running
- Verify credentials are correct
- For PostgreSQL/MySQL, ensure the database exists
- Check firewall settings

### Import errors

Reinstall dependencies:
```bash
pip install --upgrade -r requirements.txt
```

## 💡 Tips

1. **Set credentials in .env** - No need to type flags every time!
2. **Use debug mode** to see generated SQL: `--debug` flag
3. **Check your config** anytime with: `python -m cli.main connect status`
4. **Chat mode has memory** - you can ask follow-up questions
5. **Type 'tables'** in chat to see all available tables
6. **Use quotes** around queries with spaces: `"Show me all users"`
7. **Override .env settings** by using flags: `--db-name other_db`

## 🎉 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore [examples/](examples/) for programmatic usage
- Check out [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Start the MCP server for API access

## ❓ Need Help?

- Check the [README.md](README.md)
- Open an issue on GitHub
- Read the [CONTRIBUTING.md](CONTRIBUTING.md) guide

---

**Happy querying! 🚀**

