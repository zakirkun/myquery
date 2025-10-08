# MCP Client API

Python client library for the MCP (Model Context Protocol) server.

## Installation

MCP client is included with myquery:

```python
from mcp.client import MCPClient
```

## Quick Start

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

## MCPClient Methods

### Connection

```python
client = MCPClient(base_url="http://localhost:7766")
```

### connect_db()

```python
response = client.connect_db(
    db_type="postgresql",
    db_name="mydb",
    db_host="localhost",
    db_port=5432,
    db_user="postgres",
    db_password="password"
)
```

### execute_query()

```python
response = client.execute_query(
    prompt="Show all active users",
    session_id="my-session"
)
```

### get_schema()

```python
response = client.get_schema(
    session_id="my-session"
)
```

### get_status()

```python
response = client.get_status(
    session_id="my-session"
)
```

## Response Object

```python
class MCPResponse:
    success: bool
    data: dict
    session_id: str
    context: dict
    error: Optional[str]
```

## Examples

### Basic Workflow

```python
from mcp.client import MCPClient

client = MCPClient("http://localhost:7766")

# Connect
conn_response = client.connect_db(
    db_type="postgresql",
    db_name="analytics_db",
    db_user="analyst",
    db_password="password"
)

if conn_response.success:
    session_id = conn_response.session_id
    
    # Execute queries
    result = client.execute_query(
        prompt="What's the total revenue this month?",
        session_id=session_id
    )
    
    print(result.data)
```

### Error Handling

```python
try:
    response = client.execute_query(
        prompt="Show users",
        session_id="my-session"
    )
    
    if not response.success:
        print(f"Error: {response.error}")
    else:
        print(response.data)
        
except Exception as e:
    print(f"Request failed: {str(e)}")
```

### Session Management

```python
# Use consistent session ID
session_id = "analytics-session-1"

# All operations use same session
client.connect_db(..., session_id=session_id)
client.execute_query(..., session_id=session_id)
client.get_schema(session_id=session_id)
```

## Next Steps

- [Programmatic Usage](programmatic-usage.md) - Direct Python API
- [MCP Server](../features/mcp-server.md) - Server documentation

---

[← Back to Documentation](../README.md)

