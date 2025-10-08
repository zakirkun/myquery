# Query Optimization

Get AI-powered suggestions to improve your SQL query performance.

## Overview

myquery analyzes your queries and provides:
- Static code analysis (10+ checks)
- AI-powered optimization suggestions
- Index recommendations
- Query rewrite suggestions
- Complexity scoring

## Quick Start

```python
from core.agent import QueryAgent

agent = QueryAgent()
agent.connect_database(...)

# Get optimization suggestions
optimization = agent.optimize_query(
    "SELECT * FROM users WHERE UPPER(email) = 'JOHN@EXAMPLE.COM'"
)

print(optimization)
```

## Static Analysis Checks

### 1. SELECT * Usage
**Issue:** Retrieving unnecessary columns  
**Suggestion:** Specify only needed columns

### 2. Missing WHERE Clause
**Issue:** May return entire table  
**Suggestion:** Add filtering or LIMIT

### 3. OR in WHERE
**Issue:** Can prevent index usage  
**Suggestion:** Use UNION or IN clause

### 4. NOT IN with Subquery
**Issue:** Can be slow  
**Suggestion:** Use NOT EXISTS or LEFT JOIN

### 5. Function on Indexed Column
**Issue:** Prevents index usage  
**Suggestion:** Use functional indexes or restructure

### 6. Implicit Type Conversion
**Issue:** Comparing different types  
**Suggestion:** Use proper data types

### 7. Multiple JOINs without WHERE
**Issue:** Large intermediate results  
**Suggestion:** Add filtering

### 8. Leading Wildcard (LIKE '%...')
**Issue:** Cannot use index  
**Suggestion:** Use full-text search

### 9. DISTINCT with ORDER BY
**Issue:** Extra sorting overhead  
**Suggestion:** Optimize column selection

## Example Output

```
🔍 Query Optimization Analysis

Query:
SELECT * FROM users WHERE UPPER(email) = 'JOHN@EXAMPLE.COM'

⚠️  Potential Issues Detected:

1. SELECT *: Using SELECT * can be inefficient
   💡 Suggestion: Specify only the columns you need

2. Function on column: Functions on columns in WHERE prevent index usage
   💡 Suggestion: Consider functional indexes or restructuring query

🧠 AI-Powered Suggestions:

- Create a functional index on LOWER(email) for case-insensitive searches
- Alternative query: Use email = 'john@example.com' if email is stored lowercase
- Add LIMIT clause if you only need a few results
- Estimated improvement: 50-70% faster with proper indexing

📚 General Best Practices:

- Use specific column names instead of SELECT *
- Add indexes on frequently queried columns
- Use WHERE clauses to filter early
- Consider using LIMIT for large result sets
- Use EXPLAIN/EXPLAIN ANALYZE to check execution plan
```

## Complexity Scoring

```python
metrics = agent.query_optimization_tool.get_query_complexity_score(
    "SELECT * FROM orders o JOIN users u ON o.user_id = u.id WHERE o.status = 'pending'"
)

print(metrics)
```

**Output:**
```python
{
    'join_count': 1,
    'subquery_count': 0,
    'aggregate_count': 0,
    'has_group_by': False,
    'has_having': False,
    'has_order_by': False,
    'has_distinct': False,
    'complexity_score': 15,
    'complexity_level': 'Simple'
}
```

**Complexity Levels:**
- **Simple** - Score < 20
- **Moderate** - Score 20-39
- **Complex** - Score 40-59
- **Very Complex** - Score 60+

## Programmatic Usage

### Basic Optimization

```python
from core.agent import QueryAgent

agent = QueryAgent()
agent.connect_database(...)

# Analyze query
optimization = agent.optimize_query(
    "SELECT * FROM users WHERE status = 'active'"
)

print(optimization)
```

### In Query Flow

```python
# Execute with optimization enabled
results = agent.execute_query_flow(
    "Show all active users",
    optimize=True
)

# Access optimization suggestions
if results.get("optimization"):
    print(results["optimization"])
```

## Use Cases

### 1. Performance Tuning
```python
# Before deploying to production
optimization = agent.optimize_query(production_query)
# Review and apply suggestions
```

### 2. Learning SQL Best Practices
```python
# Get feedback on your queries
for query in my_queries:
    optimization = agent.optimize_query(query)
    print(optimization)
```

### 3. Code Review
```python
# Analyze queries in codebase
if "⚠️" in optimization:
    print(f"Issues found in: {query}")
```

## Best Practices

1. **Run optimization on all production queries**
2. **Review AI suggestions even if no static issues**
3. **Use complexity scoring to prioritize**
4. **Test optimized queries before deployment**
5. **Monitor performance improvements**

## Tips

- Static analysis is instant, AI analysis requires API call
- Optimization suggestions are recommendations, not requirements
- Test suggested changes in development first
- Use EXPLAIN ANALYZE to verify improvements
- Consider your specific database and workload

## Next Steps

- [Natural Language Queries](natural-language-queries.md) - Generate queries
- [CLI Reference](../cli/commands.md) - Command reference
- [Programmatic Usage](../api/programmatic-usage.md) - API docs

---

[← Back to Documentation](../README.md)

