# Getting Started with myquery

Get up and running with myquery in just 5 minutes.

## Prerequisites

- **Python 3.8 or higher**
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **Database** (PostgreSQL, MySQL, or SQLite)

## Installation

### Method 1: From Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/zakirkun/myquery.git
cd myquery

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Method 2: Direct Installation

```bash
# Install dependencies directly
pip install -r requirements.txt
```

### Verify Installation

```bash
myquery --help
```

You should see the myquery help menu.

## Configuration

### Step 1: Create Environment File

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

### Step 2: Add Your OpenAI API Key

Edit `.env` and add your OpenAI API key:

```env
# Required
OPENAI_API_KEY=sk-your-actual-api-key-here

# Optional: Choose model (default: gpt-4-turbo-preview)
OPENAI_MODEL=gpt-4-turbo-preview
```

### Step 3: (Optional) Configure Default Database

For auto-connect feature, add database credentials:

```env
# Default database connection
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydb
DB_USER=postgres
DB_PASSWORD=your_password
```

## First Steps

### Option 1: Use Auto-Connect

If you configured database in `.env`:

```bash
# Start chat (auto-connects automatically)
myquery chat start
```

### Option 2: Connect Manually

```bash
# Connect to database first
myquery connect db --db-type postgresql --db-name mydb --db-user postgres

# Then start chat
myquery chat start
```

## Your First Query

Once in chat mode:

```
You: show me all tables
→ Lists all tables in your database

You: show top 10 customers by total orders
→ Generates SQL, executes, displays results + AI analysis

You: show me a bar chart of orders by month
→ Creates interactive chart and opens in browser
```

## Quick Command Reference

```bash
# Chat mode (interactive)
myquery chat start

# Single query
myquery query execute "Show all products with low inventory"

# Export data
myquery export query "Top 10 customers" --format excel

# Visualize
myquery visualize chart "Sales by region" --type bar

# Web UI
myquery web start

# MCP Server
myquery server start
```

## What's Next?

### Learn Core Features

- [Natural Language Queries](features/natural-language-queries.md) - Deep dive into querying
- [Data Export](features/data-export.md) - Export your data
- [Visualizations](features/visualizations.md) - Create charts
- [Multi-Database](features/multi-database.md) - Work with multiple DBs

### Explore Advanced Usage

- [Programmatic API](api/programmatic-usage.md) - Use in Python code
- [Custom Tools](advanced/custom-tools.md) - Extend myquery
- [MCP Server](features/mcp-server.md) - API integration

### Get Help

- [CLI Command Reference](cli/commands.md) - All commands
- [Troubleshooting](troubleshooting.md) - Common issues
- [GitHub Discussions](https://github.com/zakirkun/myquery/discussions) - Ask questions

## Examples to Try

### Business Analytics

```bash
myquery chat start

You: "What's our total revenue by month this year?"
You: "Show top 5 performing products"
You: "Which customers haven't ordered in 90 days?"
```

### Data Exploration

```bash
You: "What tables do we have?"
You: "Show me the structure of the orders table"
You: "Give me a sample of the users table"
```

### Visualizations

```bash
You: "Line chart of monthly sales"
You: "Pie chart of revenue by category"
You: "Bar chart comparing products"
```

## Common Issues

### "Module not found" error

```bash
# Make sure you're in the project directory
cd myquery

# Reinstall dependencies
pip install -r requirements.txt
```

### "OpenAI API key not found"

```bash
# Check .env file exists
ls -la .env

# Verify OPENAI_API_KEY is set
cat .env | grep OPENAI_API_KEY
```

### "Cannot connect to database"

```bash
# Test connection manually
myquery connect db --db-type postgresql --db-name mydb --db-user postgres

# Check credentials in .env
cat .env | grep DB_
```

For more help, see [Troubleshooting Guide](troubleshooting.md).

## Tips for Success

1. **Start Simple** - Try basic queries first
2. **Use Debug Mode** - Add `--debug` to see generated SQL
3. **Explore Examples** - Run example scripts in `examples/`
4. **Read Docs** - Check feature-specific documentation
5. **Ask for Help** - Use GitHub Discussions for questions

---

**Ready to dive deeper?** Explore the [Natural Language Queries](features/natural-language-queries.md) guide!

