# Troubleshooting

Common issues and solutions for myquery.

## Installation Issues

### "Module not found" Error

```
ModuleNotFoundError: No module named 'langchain'
```

**Solution:**
```bash
pip install -r requirements.txt
```

### "Python version not supported"

**Solution:** myquery requires Python 3.8+

```bash
python --version
# Should be 3.8 or higher
```

## Configuration Issues

### "OpenAI API key not found"

```
ValueError: OpenAI API key is required
```

**Solutions:**

1. Check `.env` file exists:
   ```bash
   ls -la .env
   ```

2. Verify API key is set:
   ```bash
   cat .env | grep OPENAI_API_KEY
   ```

3. Create `.env` if missing:
   ```bash
   cp .env.example .env
   # Edit .env and add your key
   ```

### Environment Variables Not Loading

**Solution:** Ensure `.env` is in project root:

```bash
pwd  # Should be in myquery directory
ls .env  # Should exist
```

## Database Connection Issues

### "Cannot connect to database"

**Solutions:**

1. **Test connection manually:**
   ```bash
   myquery connect db --db-type postgresql --db-name mydb --db-user postgres
   ```

2. **Check credentials:**
   ```bash
   cat .env | grep DB_
   ```

3. **Verify database is running:**
   ```bash
   # PostgreSQL
   psql -h localhost -U postgres -d mydb
   
   # MySQL
   mysql -h localhost -u root -p mydb
   ```

4. **Check firewall:**
   - Ensure port is open (5432 for PostgreSQL, 3306 for MySQL)

### "Access denied" Error

**Solution:** Verify username/password:

```bash
myquery connect db \
  --db-type postgresql \
  --db-name mydb \
  --db-user correct_username
# Enter correct password when prompted
```

### "Database does not exist"

**Solution:** Create database first:

```sql
-- PostgreSQL
CREATE DATABASE mydb;

-- MySQL
CREATE DATABASE mydb;
```

## Query Issues

### Query Returns No Results

**Solutions:**

1. **Check data exists:**
   ```
   You: "How many rows in users table?"
   ```

2. **Verify table name:**
   ```
   You: "What tables do we have?"
   ```

3. **Use debug mode:**
   ```bash
   myquery chat start --debug
   ```

### "SQL Syntax Error"

**Solutions:**

1. **Use debug mode** to see generated SQL
2. **Rephrase question** more clearly
3. **Check schema** for correct table/column names

### Timeout Errors

**Solutions:**

1. **Add LIMIT:**
   ```
   "Show users LIMIT 100"
   ```

2. **Add WHERE clause:**
   ```
   "Show recent orders from last week"
   ```

3. **Create indexes** on frequently queried columns

## Export Issues

### "Permission denied" When Exporting

**Solution:** Check output directory permissions:

```bash
mkdir -p outputs/exports
chmod 755 outputs/exports
```

### Export File Not Found

**Solution:** Check output location:

```bash
ls -la outputs/exports/
```

## Visualization Issues

### Chart Not Opening

**Solutions:**

1. **Check output directory:**
   ```bash
   ls outputs/visualizations/
   ```

2. **Open manually:**
   ```bash
   # Find the file
   open outputs/visualizations/chart_*.html
   ```

3. **Check browser default:**
   - Set default program for `.html` files

### "No data to visualize"

**Solution:** Ensure query returns data first:

```
You: "Show sales by month"  # Verify this returns data
You: "Now show as chart"    # Then visualize
```

## Performance Issues

### Slow Queries

**Solutions:**

1. **Use query optimization:**
   ```python
   optimization = agent.optimize_query(your_query)
   print(optimization)
   ```

2. **Add indexes:**
   ```sql
   CREATE INDEX idx_users_email ON users(email);
   ```

3. **Limit results:**
   ```
   "Show top 100 customers"
   ```

### High Memory Usage

**Solutions:**

1. **Limit result size**
2. **Close unnecessary sessions**
3. **Restart myquery periodically**

## Web UI Issues

### "Port already in use"

**Solution:** Use different port:

```bash
myquery web start --port 3000
```

### Cannot Access Web UI

**Solutions:**

1. **Check server is running:**
   ```bash
   myquery web start
   # Should show "Server running at..."
   ```

2. **Try different browser**

3. **Check firewall settings**

## MCP Server Issues

### "Connection refused"

**Solutions:**

1. **Verify server is running:**
   ```bash
   myquery server start
   ```

2. **Check port:**
   ```bash
   netstat -an | grep 7766
   ```

3. **Use correct URL:**
   ```python
   client = MCPClient("http://localhost:7766")  # Not https
   ```

## Common Error Messages

### "No module named 'tools'"

**Solution:** Run from project directory:

```bash
cd /path/to/myquery
python -m cli.main chat start
```

### "LangChain API error"

**Solution:** Check OpenAI API key:

1. Verify key is valid
2. Check API quota/billing
3. Try different model:
   ```env
   OPENAI_MODEL=gpt-3.5-turbo
   ```

### "Schema not found"

**Solution:** Ensure connected to database:

```bash
myquery connect status
# Should show "Connected: true"
```

## Getting More Help

### Enable Debug Mode

```bash
myquery chat start --debug
myquery query execute "..." --debug
```

### Check Logs

```bash
# Set log level
export LOG_LEVEL=DEBUG

# View detailed logs
myquery chat start
```

### Community Support

- [GitHub Issues](https://github.com/zakirkun/myquery/issues)
- [Discussions](https://github.com/zakirkun/myquery/discussions)
- [Documentation](README.md)

### Reporting Bugs

Include:
1. myquery version
2. Python version
3. Database type/version
4. Error message
5. Steps to reproduce
6. Debug logs (if applicable)

---

[← Back to Documentation](README.md)

