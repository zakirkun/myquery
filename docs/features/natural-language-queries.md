# Natural Language Queries

Query your database using plain English instead of SQL. myquery uses AI to understand your questions and generate accurate SQL queries.

## Overview

Natural language querying is the core feature of myquery. Simply ask questions as you would to a colleague, and myquery:

1. Analyzes your database schema
2. Generates optimized SQL
3. Executes the query safely
4. Displays formatted results
5. Provides AI-powered insights

## Basic Usage

### Interactive Chat Mode

```bash
myquery chat start
```

Then ask questions naturally:

```
You: show me all tables
You: list all customers
You: find orders from last month
You: what are the top 10 products by revenue?
```

### Single Queries

```bash
myquery query execute "Show all active users"
myquery query execute "Find customers who ordered in the last 30 days"
myquery query execute "What's the average order value?"
```

## Examples

### Data Exploration

```
"What tables do we have?"
"Show me the columns in the users table"
"Give me a sample of the products table"
"How many rows are in the orders table?"
```

### Filtering

```
"Show all orders where status is 'pending'"
"Find users created after January 1st 2024"
"List products with price greater than 100"
"Show customers from California"
```

### Aggregation

```
"What's the total revenue?"
"Count the number of orders by status"
"Show average order value by month"
"Sum of sales by region"
```

### Sorting & Limiting

```
"Top 10 customers by total spent"
"Show latest 20 orders"
"Products sorted by price descending"
"First 5 users by registration date"
```

### Joins & Relationships

```
"Show customers with their orders"
"List products with their categories"
"Orders with customer names"
"Users with their total order count"
```

### Time-Based Queries

```
"Orders from last week"
"Sales for this month"
"Users who signed up yesterday"
"Revenue by day for the last 30 days"
```

### Complex Queries

```
"Show top 10 customers by revenue who ordered in the last 90 days"
"Products that have never been ordered"
"Customers with more than 5 orders and total spent over $1000"
"Monthly revenue growth rate for this year"
```

## Features

### Schema Awareness

myquery automatically:
- Loads your database schema
- Understands table relationships
- Detects foreign keys
- Recognizes column types

This enables accurate query generation even for complex databases.

### Context Memory

In chat mode, myquery remembers:
- Previous questions
- Database structure
- Recent queries
- User preferences

Build on previous questions:

```
You: "Show all customers"
You: "Now filter those from California"
You: "And sort by total orders"
```

### Debug Mode

See the generated SQL:

```bash
myquery chat start --debug
```

Or for single queries:

```bash
myquery query execute "Show top products" --debug
```

Output:
```
🔍 User Query: Show top products
🔍 Generated SQL:
SELECT product_name, SUM(quantity * price) as total_revenue
FROM products p
JOIN order_items oi ON p.id = oi.product_id
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 10;
```

### Bilingual Support

myquery understands both English and Indonesian:

**English:**
```
"Show me all customers"
"List top products"
"Find orders from last month"
```

**Indonesian:**
```
"Tampilkan semua pelanggan"
"Daftar produk teratas"
"Cari pesanan dari bulan lalu"
```

## Query Types

### SELECT Queries

✅ **Supported** - Read data from database

```
"Show all users"
"Get product details"
"List orders"
```

### Aggregations

✅ **Supported** - COUNT, SUM, AVG, MAX, MIN

```
"Count total orders"
"Sum of revenue"
"Average order value"
```

### JOINS

✅ **Supported** - Automatic join detection

```
"Customers with their orders"
"Products with category names"
```

### Subqueries

✅ **Supported** - Complex nested queries

```
"Customers who spent more than average"
"Products never ordered"
```

### Destructive Queries

❌ **Blocked by default** - For safety

- DELETE
- UPDATE
- DROP
- TRUNCATE
- ALTER

These are blocked to prevent accidental data loss.

## Best Practices

### 1. Be Specific

✅ Good: "Show top 10 customers by total revenue"  
❌ Vague: "Show customers"

### 2. Use Natural Language

✅ Good: "Find orders from last week"  
❌ Technical: "SELECT * FROM orders WHERE created_at > ..."

### 3. Build Incrementally

Start simple, then add complexity:

```
"Show all products"
"Now filter products with price > 100"
"Sort them by price descending"
"Only show top 10"
```

### 4. Leverage Context

In chat mode, reference previous queries:

```
"Show customers"
"Filter those from New York"
"Sort by total orders"
```

### 5. Use Debug Mode

When learning or troubleshooting:

```bash
myquery chat start --debug
```

## Limitations

### Current Limitations

1. **Read-Only** - Destructive operations blocked by default
2. **Single Database** - One database per session (use multidb for multiple)
3. **SQL Dialects** - Optimized for PostgreSQL, MySQL, SQLite

### Workarounds

**Need to update data?**
- Use raw SQL mode: `myquery query sql "UPDATE ..."`
- Or disable safety checks (not recommended)

**Need multiple databases?**
- Use `myquery multidb` commands
- See [Multi-Database Documentation](multi-database.md)

## Advanced

### Custom Prompts

Add context to your questions:

```
"Show revenue by month, but only for products in the Electronics category"
"List customers sorted by lifetime value, excluding those with status='inactive'"
```

### Schema Hints

Help myquery understand your schema:

```
"Join users and orders using user_id"
"Group by the product category field"
```

### Output Formatting

Request specific formats:

```
"Show revenue rounded to 2 decimals"
"Format dates as YYYY-MM-DD"
"Display prices with currency symbols"
```

## Troubleshooting

### Query Not Working?

1. **Check Schema** - `"What tables do we have?"`
2. **Use Debug Mode** - Add `--debug` flag
3. **Be More Specific** - Add more details to your question
4. **Check Column Names** - `"Show columns in users table"`

### Incorrect Results?

1. **Verify Generated SQL** - Use debug mode
2. **Check Data** - `"Show sample data from table"`
3. **Rephrase Question** - Try different wording

### Timeout Errors?

1. **Limit Results** - Add "LIMIT 100" or "top 100"
2. **Add Filters** - Narrow down the query
3. **Use Indexes** - See [Query Optimization](query-optimization.md)

## Next Steps

- [Data Export](data-export.md) - Export query results
- [Visualizations](visualizations.md) - Create charts from queries
- [Query Optimization](query-optimization.md) - Improve performance
- [CLI Reference](../cli/commands.md) - All query commands

---

[← Back to Documentation](../README.md)

