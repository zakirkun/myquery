# Web UI

Beautiful web interface for interacting with databases through your browser.

## Overview

myquery Web UI provides a modern, user-friendly interface for:
- Interactive chat with your database
- Visual schema exploration
- Real-time query results
- Data visualization dashboard
- WebSocket-based real-time updates

## Quick Start

```bash
# Start web server
myquery web start

# Access at http://localhost:8000
```

## Features

### Interactive Chat Interface
- Natural language queries
- Real-time responses
- Conversation history
- Context awareness

### Schema Explorer
- Visual table browser
- Column details
- Relationship viewer
- Sample data preview

### Query Results
- Formatted tables
- Sortable columns
- Filterable data
- Export options

### Visualization Dashboard
- Interactive charts
- Multiple chart types
- Customizable views
- Real-time updates

## Configuration

### Default Settings

```bash
# Default host and port
myquery web start

# Access at: http://localhost:8000
```

### Custom Port

```bash
myquery web start --port 3000

# Access at: http://localhost:3000
```

### Custom Host

```bash
# Allow external access
myquery web start --host 0.0.0.0 --port 8000

# Access from network: http://your-ip:8000
```

## API Endpoints

### REST API

- `POST /api/connect` - Connect to database
- `POST /api/query` - Execute natural language query
- `POST /api/sql` - Execute raw SQL
- `GET /api/schema` - Get database schema
- `GET /api/tables` - List tables
- `POST /api/visualize` - Create visualization

### WebSocket

- `WS /ws/chat` - Real-time chat connection

## Usage

### Starting the Server

```bash
# Basic start
myquery web start

# With custom settings
myquery web start --host 0.0.0.0 --port 8080 --debug
```

### Accessing the Interface

1. Open browser to `http://localhost:8000`
2. Connect to database (if not auto-connected)
3. Start querying

### Features in UI

**Chat Interface:**
- Type questions naturally
- See real-time responses
- View formatted results
- Get AI insights

**Schema Explorer:**
- Browse tables and columns
- View relationships
- See data types
- Preview sample data

**Results View:**
- Sortable columns
- Filterable rows
- Export to CSV/JSON/Excel
- Copy to clipboard

**Visualization:**
- Auto-generate charts
- Choose chart types
- Customize appearance
- Download images

## Best Practices

1. **Use for team collaboration** - No CLI knowledge needed
2. **Share connection** - Run on shared server
3. **Secure access** - Use firewall/VPN for production
4. **Monitor resources** - Watch memory usage for large results

## Security

⚠️ **Current limitations:**
- No authentication (development only)
- No encryption (use HTTPS proxy if needed)
- Read-only queries by default

**For production:**
- Use reverse proxy (nginx, Apache)
- Add authentication (basic auth, OAuth)
- Enable HTTPS
- Restrict network access

## Next Steps

- [Natural Language Queries](natural-language-queries.md) - Learn queries
- [Visualizations](visualizations.md) - Create charts
- [MCP Server](mcp-server.md) - API integration

---

[← Back to Documentation](../README.md)

