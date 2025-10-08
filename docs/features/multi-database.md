# Multi-Database Operations

Query, compare, and merge data from multiple databases simultaneously.

## Overview

myquery's multi-database feature allows you to:
- Connect to multiple databases at once
- Execute queries across all databases
- Compare data between environments
- Merge results from different sources
- Join data by common keys

Perfect for comparing production vs staging, consolidating regional data, or cross-database analysis.

## Quick Start

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

## Managing Connections

### Add Connection

```bash
myquery multidb add <name> [options]
```

**Examples:**

```bash
# PostgreSQL
myquery multidb add prod \
  --type postgresql \
  --name proddb \
  --host prod.example.com \
  --port 5432 \
  --user admin

# MySQL
myquery multidb add analytics \
  --type mysql \
  --name analytics_db \
  --host analytics.example.com \
  --port 3306 \
  --user readonly

# SQLite
myquery multidb add local \
  --type sqlite \
  --name ./data/local.db
```

### List Connections

```bash
myquery multidb list
```

**Output:**
```
📋 Multi-Database Connections:

  prod (postgresql)
  ├─ Database: proddb
  ├─ Host: prod.example.com:5432
  └─ Status: ✅ Connected

  staging (postgresql)
  ├─ Database: stagingdb
  ├─ Host: staging.example.com:5432
  └─ Status: ✅ Connected

  local (sqlite)
  ├─ Database: ./data/local.db
  └─ Status: ✅ Connected

Total: 3 connection(s)
```

### Remove Connection

```bash
myquery multidb remove <name>
```

**Example:**
```bash
myquery multidb remove staging
```

### Compare Schemas

```bash
myquery multidb compare
```

Shows schema differences between databases.

## Querying Multiple Databases

### Basic Query (Separate Results)

```bash
myquery multidb query "SELECT COUNT(*) FROM users"
```

**Output:**
```json
{
  "prod": {
    "success": true,
    "data": [{"count": 15420}],
    "row_count": 1
  },
  "staging": {
    "success": true,
    "data": [{"count": 8932}],
    "row_count": 1
  }
}
```

### Query Specific Databases

```bash
myquery multidb query "SELECT * FROM products" \
  --connections prod,staging
```

Only queries specified databases.

## Merging Data

### Union Merge (Stack Rows)

Combines rows from all databases vertically.

```bash
myquery multidb query "SELECT * FROM products" \
  --merge \
  --merge-type union
```

**Result:**

| _source_db | id | name | price |
|------------|-----|------|-------|
| prod | 1 | Laptop | 1000 |
| prod | 2 | Mouse | 25 |
| staging | 1 | Laptop | 950 |
| staging | 3 | Keyboard | 75 |

**Features:**
- Adds `_source_db` column to track origin
- Handles missing columns (fills with NULL)
- Preserves all data from all sources

**Use Cases:**
- Consolidate regional databases
- Merge historical data
- Combine development environments

### Join Merge (By Key)

Merges data horizontally by common key column.

```bash
myquery multidb query "SELECT user_id, total_orders FROM user_stats" \
  --merge \
  --merge-type join \
  --merge-key user_id
```

**Result:**

| user_id | total_orders_prod | total_orders_staging |
|---------|-------------------|----------------------|
| 1 | 15 | 12 |
| 2 | 23 | 25 |
| 3 | NULL | 8 |

**Features:**
- OUTER JOIN semantics (includes all rows)
- Column suffixing (`column_dbname`)
- NULL for missing data
- Automatic schema alignment

**Use Cases:**
- Compare metrics across environments
- Reconcile data differences
- Cross-database validation

## Merge Options

### `--merge`

Enable merging of results.

```bash
myquery multidb query "..." --merge
```

### `--merge-type <type>`

Merge strategy:
- `union` - Stack rows (default)
- `join` - Merge by key

```bash
myquery multidb query "..." --merge --merge-type union
myquery multidb query "..." --merge --merge-type join --merge-key id
```

### `--merge-key <column>`

Column to use for join operations (required for join mode).

```bash
myquery multidb query "..." \
  --merge \
  --merge-type join \
  --merge-key user_id
```

## Use Cases

### 1. Environment Comparison

Compare production vs staging:

```bash
# Add connections
myquery multidb add prod --type postgresql --name proddb
myquery multidb add staging --type postgresql --name stagingdb

# Compare user counts
myquery multidb query "SELECT COUNT(*) as user_count FROM users"

# Compare with join
myquery multidb query "SELECT status, COUNT(*) as count FROM users GROUP BY status" \
  --merge --merge-type join --merge-key status
```

### 2. Regional Data Consolidation

Merge data from regional databases:

```bash
# Add regional databases
myquery multidb add us_west --type postgresql --name sales_us_west
myquery multidb add us_east --type postgresql --name sales_us_east
myquery multidb add europe --type postgresql --name sales_europe

# Consolidate all sales data
myquery multidb query "SELECT * FROM sales WHERE date >= '2024-01-01'" \
  --merge --merge-type union

# Export consolidated data
myquery export query "..." --format csv
```

### 3. Data Migration Validation

Verify data after migration:

```bash
# Add old and new databases
myquery multidb add old_db --type mysql --name legacy_db
myquery multidb add new_db --type postgresql --name new_db

# Compare record counts
myquery multidb query "SELECT COUNT(*) FROM customers"

# Compare by key
myquery multidb query "SELECT customer_id, COUNT(*) as order_count FROM orders GROUP BY customer_id" \
  --merge --merge-type join --merge-key customer_id
```

### 4. Cross-Database Analytics

Analyze data across different systems:

```bash
# Add different data sources
myquery multidb add crm --type postgresql --name crm_db
myquery multidb add analytics --type postgresql --name analytics_db

# Join user data
myquery multidb query "SELECT user_id, metric_value FROM user_metrics" \
  --merge --merge-type join --merge-key user_id
```

## Programmatic Usage

```python
from core.agent import QueryAgent

agent = QueryAgent()

# Add connections
agent.multi_db_manager.add_connection(
    "prod",
    db_type="postgresql",
    db_name="proddb",
    db_host="prod.example.com",
    db_user="admin",
    db_password="password"
)

agent.multi_db_manager.add_connection(
    "staging",
    db_type="postgresql",
    db_name="stagingdb",
    db_host="staging.example.com",
    db_user="admin",
    db_password="password"
)

# Execute multi-DB query
result = agent.multi_db_query_tool._run(
    query="SELECT * FROM products",
    connections="all",
    merge_results=True,
    merge_type="union"
)

print(result)
```

### Merge Methods

```python
# Union merge
result = agent.multi_db_query_tool._run(
    query="SELECT * FROM products",
    merge_results=True,
    merge_type="union"
)

# Join merge
result = agent.multi_db_query_tool._run(
    query="SELECT id, revenue FROM sales",
    merge_results=True,
    merge_type="join",
    merge_key="id"
)
```

## Merge Metadata

Merged results include metadata:

```json
{
  "success": true,
  "merge_type": "union",
  "source_databases": ["prod", "staging"],
  "columns": ["_source_db", "id", "name", "price"],
  "data": [...],
  "row_count": 150,
  "metadata": {
    "total_rows": 150,
    "source_count": 2,
    "rows_per_source": {
      "prod": 100,
      "staging": 50
    }
  }
}
```

## Best Practices

### 1. Use Consistent Schemas

Ensure similar column names and types across databases for easier merging.

### 2. Filter Data Early

Apply WHERE clauses to reduce data volume:

```bash
myquery multidb query "SELECT * FROM orders WHERE date >= '2024-01-01'" \
  --merge --merge-type union
```

### 3. Test on Small Datasets First

Verify merge logic with limited data:

```bash
myquery multidb query "SELECT * FROM users LIMIT 10" \
  --merge --merge-type union
```

### 4. Use Meaningful Connection Names

✅ Good: `prod`, `staging`, `us_west`  
❌ Bad: `db1`, `db2`, `test`

### 5. Export Merged Results

```bash
# Merge and export
myquery multidb query "..." --merge --merge-type union > results.json

# Or use export command
myquery export query "..." --format csv
```

## Limitations

### Current Limitations

1. **Same Query** - All databases execute the same SQL
2. **Schema Alignment** - Manual handling of column differences
3. **Performance** - Sequential execution (not parallel yet)
4. **Connection Limit** - Practical limit of ~10 connections

### Workarounds

**Different queries per database?**
- Execute separately and merge programmatically

**Schema mismatch?**
- Use SQL aliases to standardize column names

**Performance issues?**
- Filter data with WHERE clauses
- Query specific databases only

## Troubleshooting

### Connection Failed

```bash
# Test individual connection
myquery connect db --db-type postgresql --db-name proddb --db-host prod.example.com

# Check connection status
myquery multidb list
```

### Merge Key Not Found

```
Error: Merge key 'user_id' not found in database 'staging'
```

**Solution:** Ensure key column exists in all databases

### Schema Conflicts

```
Warning: Column 'price' has different types across databases
```

**Solution:** Use CAST in query to standardize types

## Next Steps

- [Data Export](data-export.md) - Export merged results
- [Natural Language Queries](natural-language-queries.md) - Generate queries
- [CLI Reference](../cli/commands.md#multidb-commands) - Full command docs

---

[← Back to Documentation](../README.md)

