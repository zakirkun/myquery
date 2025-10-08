# Programmatic Usage

Use myquery in your Python applications.

## Quick Start

```python
from core.agent import QueryAgent

# Initialize agent
agent = QueryAgent()

# Connect to database
agent.connect_database(
    db_type="postgresql",
    db_name="mydb",
    db_user="postgres",
    db_password="password",
    db_host="localhost",
    db_port=5432
)

# Execute query
results = agent.execute_query_flow(
    user_prompt="Show top 10 customers by revenue"
)

# Access results
print(results["sql_query"])
print(results["analysis"])
print(results["formatted_output"])
```

## QueryAgent API

### Initialization

```python
from core.agent import QueryAgent

# Default (uses .env)
agent = QueryAgent()

# Custom API key and model
agent = QueryAgent(
    api_key="your-openai-key",
    model="gpt-4-turbo-preview"
)
```

### Database Connection

```python
# Connect
agent.connect_database(
    db_type="postgresql",  # or "mysql", "sqlite"
    db_name="mydb",
    db_host="localhost",
    db_port=5432,
    db_user="postgres",
    db_password="password"
)

# Check connection
if agent.is_connected():
    print("Connected!")

# Get tables
tables = agent.get_table_list()
print(tables)
```

### Query Execution

```python
# Execute query flow
results = agent.execute_query_flow(
    user_prompt="Show all active users",
    debug=True,              # Show SQL
    auto_visualize=True,     # Create charts
    optimize=True            # Get optimization suggestions
)

# Access results
sql = results["sql_query"]
data = results["execution_result"]
analysis = results["analysis"]
viz = results["visualization"]
optimization = results["optimization"]
```

### Individual Operations

```python
# Get schema
schema = agent.get_schema(include_sample_data=True)

# Analyze schema
analysis = agent.analyze_schema()

# Generate SQL only
from tools import GenerateQueryTool
tool = GenerateQueryTool()
tool.llm = agent.llm
sql = tool._run(
    user_prompt="Show all users",
    schema_json=schema
)
```

### Data Export

```python
# Export results
export_msg = agent.export_results(
    query_result_json=results["execution_result"],
    format="excel",
    filename="my_export",
    output_dir="exports"
)
print(export_msg)
```

### Query Optimization

```python
# Get optimization suggestions
optimization = agent.optimize_query(
    "SELECT * FROM users WHERE UPPER(email) = 'JOHN@EXAMPLE.COM'"
)
print(optimization)
```

### Chat Interface

```python
# Interactive chat
response = agent.chat("Show all products")
print(response)

# Clear history
agent.clear_history()
```

## Tools API

### Using Individual Tools

```python
from tools import (
    ConnectDBTool,
    ExecuteQueryTool,
    ExportDataTool,
    VisualizeDataTool
)

# Connect tool
connect_tool = ConnectDBTool()
result = connect_tool._run(
    db_type="postgresql",
    db_name="mydb",
    db_user="postgres"
)

# Execute tool
exec_tool = ExecuteQueryTool()
result = exec_tool._run(
    sql_query="SELECT * FROM users LIMIT 10"
)

# Export tool
export_tool = ExportDataTool()
result = export_tool._run(
    query_result_json=result,
    format="csv",
    filename="users"
)
```

## Multi-Database

```python
# Add connections
agent.multi_db_manager.add_connection(
    "prod",
    db_type="postgresql",
    db_name="proddb",
    db_user="admin",
    db_password="password"
)

agent.multi_db_manager.add_connection(
    "staging",
    db_type="postgresql",
    db_name="stagingdb",
    db_user="admin",
    db_password="password"
)

# Query with merge
result = agent.multi_db_query_tool._run(
    query="SELECT * FROM products",
    connections="all",
    merge_results=True,
    merge_type="union"
)
```

## Error Handling

```python
try:
    results = agent.execute_query_flow("Show users")
    
    if results.get("error"):
        print(f"Query failed: {results['error']}")
    else:
        print(results["analysis"])
        
except Exception as e:
    print(f"Error: {str(e)}")
```

## Advanced Usage

### Custom Configuration

```python
from config.settings import settings

# Access settings
api_key = settings.openai_api_key
model = settings.openai_model
db_type = settings.db_type
```

### Direct Tool Access

```python
# Access specific tools
query_tool = agent.generate_query_tool
exec_tool = agent.execute_query_tool
viz_tool = agent.visualize_data_tool

# Use directly
sql = query_tool._run(
    user_prompt="Show products",
    schema_json=schema
)
```

## Complete Example

```python
from core.agent import QueryAgent
import json

# Initialize
agent = QueryAgent()

# Connect
agent.connect_database(
    db_type="postgresql",
    db_name="sales_db",
    db_user="analyst",
    db_password="password"
)

# Execute query with all features
results = agent.execute_query_flow(
    user_prompt="Show top 10 products by revenue with a bar chart",
    debug=True,
    auto_visualize=True,
    optimize=True
)

# Display results
print("SQL Generated:")
print(results["sql_query"])

print("\nAnalysis:")
print(results["analysis"])

if results.get("visualization"):
    print(f"\nChart created: {results['visualization']}")

if results.get("optimization"):
    print("\nOptimization Suggestions:")
    print(results["optimization"])

# Export
export_msg = agent.export_results(
    query_result_json=results["execution_result"],
    format="all",
    filename="top_products"
)
print(f"\n{export_msg}")
```

## Next Steps

- [MCP Client](mcp-client.md) - REST API client
- [Custom Tools](../advanced/custom-tools.md) - Extend myquery
- [CLI Reference](../cli/commands.md) - CLI commands

---

[← Back to Documentation](../README.md)

