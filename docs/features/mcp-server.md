# MCP Server

REST API server for external integrations using Model Context Protocol.

## Overview

The MCP (Model Context Protocol) server exposes myquery's functionality through a REST API on port 7766.

Perfect for:
- External application integration
- Custom frontends
- Automation and scripting
- Cross-platform access

## Quick Start

```bash
# Start MCP server
myquery server start

# Access at http://localhost:7766
```

## Configuration

### Default Settings

```env
MCP_PORT=7766
MCP_HOST=0.0.0.0
```

### Custom Settings

```bash
myquery server start --port 8080 --host 127.0.0.1
```

## API Endpoints

### Execute Action

**Endpoint:** `POST /mcp/action`

```bash
curl -X POST http://localhost:7766/mcp/action \
  -H "Content-Type: application/json" \
  -d '{
    "action": "execute_query",
    "parameters": {
      "prompt": "Show top 10 customers by revenue"
    },
    "session_id": "my-session-123"
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "sql_query": "SELECT ...",
    "results": [...],
    "analysis": "..."
  },
  "session_id": "my-session-123",
  "context": {
    "connected": true,
    "db_type": "postgresql"
  }
}
```

### Available Actions

- `connect_db` - Connect to database
- `get_schema` - Get database schema
- `generate_query` - Generate SQL from natural language
- `execute_query` - Execute complete query flow
- `analyze_results` - Analyze query results
- `get_status` - Get connection status
- `chat` - Chat interaction

### Get Context

**Endpoint:** `GET /mcp/context/{session_id}`

```bash
curl http://localhost:7766/mcp/context/my-session-123
```

### List Sessions

**Endpoint:** `GET /mcp/sessions`

```bash
curl http://localhost:7766/mcp/sessions
```

### Delete Session

**Endpoint:** `DELETE /mcp/session/{session_id}`

```bash
curl -X DELETE http://localhost:7766/mcp/session/my-session-123
```

## Python Client

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

## Use Cases

### 1. Custom Web Application

```javascript
// JavaScript example
fetch('http://localhost:7766/mcp/action', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    action: 'execute_query',
    parameters: {
      prompt: 'Show total revenue'
    }
  })
})
.then(r => r.json())
.then(data => console.log(data))
```

### 2. Automation Scripts

```python
import requests

# Query database
response = requests.post(
    'http://localhost:7766/mcp/action',
    json={
        'action': 'execute_query',
        'parameters': {
            'prompt': 'Show daily sales'
        }
    }
)

data = response.json()
# Process results...
```

### 3. Integration with Other Tools

- Slack bots
- Discord bots
- Web dashboards
- Mobile apps
- Desktop applications

## Security

⚠️ **No authentication by default**

For production:
- Use API gateway with auth
- Implement JWT tokens
- Use HTTPS
- Restrict IP access
- Add rate limiting

## Next Steps

- [MCP Client API](../api/mcp-client.md) - Client library docs
- [Programmatic Usage](../api/programmatic-usage.md) - Direct Python usage

---

[← Back to Documentation](../README.md)

