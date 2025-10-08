# CLI Command Reference

Complete reference for all myquery CLI commands.

## Global Options

```bash
myquery [OPTIONS] COMMAND [ARGS]
```

**Options:**
- `--help` - Show help message
- `--version` - Show version
- `-d, --debug` - Enable debug mode
- `-l, --log-level <LEVEL>` - Set log level (DEBUG, INFO, WARNING, ERROR)

## Commands

### `myquery chat`

Interactive chat with your database.

```bash
myquery chat start [OPTIONS]
```

**Options:**
- `-d, --debug` - Show generated SQL
- `--auto/--no-auto` - Auto-connect from .env

**Special Chat Commands:**
- `exit`, `quit`, `q` - Exit chat
- `clear` - Clear history
- `tables` - Show all tables
- `help` - Show help

### `myquery query`

Execute queries on your database.

**Commands:**
- `execute` - Natural language query
- `sql` - Raw SQL query

```bash
# Natural language
myquery query execute "Show all customers" [OPTIONS]

# Raw SQL
myquery query sql "SELECT * FROM users" [OPTIONS]
```

**Options:**
- `-d, --debug` - Show generated SQL
- `--auto/--no-auto` - Auto-connect

### `myquery export`

Export query results to files.

**Commands:**
- `query` - Execute and export natural language query
- `sql` - Execute and export raw SQL

```bash
myquery export query "Show customers" [OPTIONS]
myquery export sql "SELECT * FROM users" [OPTIONS]
```

**Options:**
- `-f, --format <FORMAT>` - csv, json, excel, or all
- `-n, --filename <NAME>` - Custom filename
- `-o, --output <DIR>` - Output directory
- `-d, --debug` - Debug mode
- `--auto/--no-auto` - Auto-connect

### `myquery visualize`

Create visualizations from queries.

```bash
myquery visualize chart "Show sales by month" [OPTIONS]
```

**Options:**
- `--type <TYPE>` - Chart type: auto, bar, line, pie, scatter, table
- `-d, --debug` - Debug mode
- `--auto/--no-auto` - Auto-connect

### `myquery multidb`

Multi-database operations.

**Commands:**
- `add` - Add database connection
- `list` - List all connections
- `remove` - Remove connection
- `query` - Query multiple databases
- `compare` - Compare schemas

```bash
# Add connection
myquery multidb add <NAME> [OPTIONS]

# List connections
myquery multidb list

# Query
myquery multidb query "SELECT * FROM users" [OPTIONS]
```

**Query Options:**
- `--connections <NAMES>` - Comma-separated connection names
- `--merge` - Merge results
- `--merge-type <TYPE>` - union or join
- `--merge-key <COLUMN>` - Join key column

### `myquery connect`

Database connection management.

**Commands:**
- `db` - Connect to database
- `restore` - Restore saved session
- `status` - Show connection status

```bash
myquery connect db [OPTIONS]
```

**Options:**
- `--db-type <TYPE>` - postgresql, mysql, sqlite
- `--db-name <NAME>` - Database name
- `--db-host <HOST>` - Host (default: localhost)
- `--db-port <PORT>` - Port
- `--db-user <USER>` - Username
- `--db-password <PASS>` - Password
- `--save` - Save connection

### `myquery web`

Start web UI server.

```bash
myquery web start [OPTIONS]
```

**Options:**
- `--host <HOST>` - Host (default: 0.0.0.0)
- `--port <PORT>` - Port (default: 8000)

### `myquery server`

Start MCP server.

```bash
myquery server start [OPTIONS]
```

**Options:**
- `--host <HOST>` - Host (default: 0.0.0.0)
- `--port <PORT>` - Port (default: 7766)

## Examples

```bash
# Chat mode
myquery chat start

# Single query
myquery query execute "Show top 10 customers"

# Export
myquery export query "Sales data" --format excel

# Visualize
myquery visualize chart "Revenue by month" --type line

# Multi-database
myquery multidb add prod --type postgresql --name proddb
myquery multidb query "SELECT COUNT(*) FROM users"

# Web UI
myquery web start --port 3000

# MCP Server
myquery server start --port 7766
```

## Environment Variables

Configure defaults in `.env`:

```env
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4-turbo-preview
DB_TYPE=postgresql
DB_NAME=mydb
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
MCP_PORT=7766
LOG_LEVEL=INFO
```

---

[← Back to Documentation](../README.md)

