# Data Export

Export query results to CSV, JSON, or Excel files with a single command.

## Overview

myquery makes it easy to export your data for:
- Reports and presentations
- Data analysis in Excel/Google Sheets
- Integration with other tools
- Archiving and backup

## Supported Formats

| Format | Extension | Use Case |
|--------|-----------|----------|
| **CSV** | `.csv` | Universal compatibility, Excel/Google Sheets |
| **JSON** | `.json` | Structured data with metadata, APIs |
| **Excel** | `.xlsx` | Formatted spreadsheets with styling |
| **All** | All three | Export to all formats at once |

## Quick Start

### Export a Query

```bash
# Execute query and export to all formats
myquery export query "Show all customers" --format all

# Export to specific format
myquery export query "Top 10 products" --format csv
myquery export query "Monthly sales" --format excel
myquery export query "User data" --format json
```

### Export Raw SQL

```bash
myquery export sql "SELECT * FROM orders WHERE date > '2024-01-01'" --format csv
```

## Command Reference

### `myquery export query`

Execute natural language query and export results.

```bash
myquery export query "<question>" [options]
```

**Options:**
- `-f, --format` - Format: `csv`, `json`, `excel`, or `all` (default: `all`)
- `-n, --filename` - Custom filename without extension
- `-o, --output` - Output directory (default: `outputs/exports`)
- `--debug` - Show generated SQL
- `--auto/--no-auto` - Auto-connect from .env (default: `true`)

**Examples:**

```bash
# Basic export
myquery export query "Show revenue by region"

# Custom filename
myquery export query "Top customers" \
  --filename customer_report \
  --format excel

# Custom output directory
myquery export query "Sales data" \
  --output /path/to/reports \
  --format csv

# With debug mode
myquery export query "Product analysis" \
  --format all \
  --debug
```

### `myquery export sql`

Execute raw SQL and export results.

```bash
myquery export sql "<sql-query>" [options]
```

**Examples:**

```bash
# Export SQL query
myquery export sql "SELECT * FROM customers WHERE active = 1" \
  --format csv

# Complex query with custom filename
myquery export sql "
  SELECT 
    region,
    SUM(revenue) as total_revenue,
    COUNT(DISTINCT customer_id) as customer_count
  FROM sales
  GROUP BY region
" --filename regional_summary --format excel
```

## Export Formats

### CSV Format

**Features:**
- Universal compatibility
- Opens in Excel, Google Sheets, Numbers
- Lightweight file size
- Plain text, easy to parse

**Example Output:**

```csv
id,name,email,total_orders
1,John Doe,john@example.com,15
2,Jane Smith,jane@example.com,23
3,Bob Johnson,bob@example.com,8
```

**Use Cases:**
- Data analysis in spreadsheets
- Import into other databases
- Quick data sharing

### JSON Format

**Features:**
- Structured data with metadata
- Includes export timestamp
- Contains row count and column info
- Machine-readable

**Example Output:**

```json
{
  "metadata": {
    "exported_at": "2025-10-08T15:30:00.000Z",
    "row_count": 3,
    "columns": ["id", "name", "email", "total_orders"]
  },
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "total_orders": 15
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "email": "jane@example.com",
      "total_orders": 23
    }
  ]
}
```

**Use Cases:**
- API integration
- Data pipelines
- Programmatic processing
- Archiving with metadata

### Excel Format

**Features:**
- Formatted spreadsheet (.xlsx)
- Auto-adjusted column widths
- Header formatting
- Professional appearance

**Excel Features:**
- Sheet name: "Query Results"
- Auto-fitted columns (up to 50 chars width)
- Ready to print and share

**Use Cases:**
- Business reports
- Presentations
- Sharing with non-technical users
- Professional documentation

## Auto-Filename Generation

If you don't specify a filename, myquery generates one automatically:

**Format:** `query_export_YYYYMMDD_HHMMSS`

**Example:**
```
query_export_20251008_153045.csv
query_export_20251008_153045.json
query_export_20251008_153045.xlsx
```

**Custom Filename:**
```bash
myquery export query "..." --filename my_report
```

**Output:**
```
my_report.csv
my_report.json
my_report.xlsx
```

## Output Location

**Default Directory:** `outputs/exports/`

**Custom Directory:**
```bash
myquery export query "..." --output /path/to/directory
```

**Relative Paths:**
```bash
myquery export query "..." --output ./reports/2024
```

## File Information

After export, myquery shows:
- ✅ Success confirmation
- 📊 Row and column count
- 📁 File paths
- 💾 File sizes

**Example Output:**
```
✅ Data exported successfully!

📊 Records: 150 rows × 5 columns

📁 Exported files:
  • outputs/exports/customer_report.csv (12.3 KB)
  • outputs/exports/customer_report.json (24.5 KB)
  • outputs/exports/customer_report.xlsx (15.8 KB)
```

## Programmatic Usage

Use export in Python code:

```python
from core.agent import QueryAgent

agent = QueryAgent()
agent.connect_database(...)

# Execute query
results = agent.execute_query_flow("Show all customers")

# Export results
export_msg = agent.export_results(
    query_result_json=results["execution_result"],
    format="all",
    filename="customers_export",
    output_dir="outputs/exports"
)

print(export_msg)
```

### Export Tool Directly

```python
from tools import ExportDataTool

tool = ExportDataTool()

# Export with custom settings
result = tool._run(
    query_result_json=query_result_json,
    format="excel",
    filename="my_export",
    output_dir="./exports"
)
```

## Use Cases

### 1. Regular Reports

```bash
# Daily sales report
myquery export query "Sales for today" \
  --filename daily_sales_$(date +%Y%m%d) \
  --format excel
```

### 2. Data Analysis

```bash
# Export for analysis in Excel
myquery export query "Customer purchase patterns" \
  --format excel

# Export for Python/R analysis
myquery export query "Transaction data" \
  --format csv
```

### 3. Data Backup

```bash
# Backup critical data
myquery export sql "SELECT * FROM critical_table" \
  --format all \
  --output backups/$(date +%Y-%m-%d)
```

### 4. Sharing Results

```bash
# Generate report for stakeholders
myquery export query "Q4 revenue summary" \
  --format excel \
  --filename Q4_Revenue_Report
```

### 5. API Integration

```bash
# Export as JSON for API consumption
myquery export query "Product catalog" \
  --format json \
  --output api/data
```

## Best Practices

### 1. Use Descriptive Filenames

✅ Good: `--filename monthly_sales_2024_10`  
❌ Bad: `--filename data`

### 2. Organize by Date

```bash
--output reports/2024/october
```

### 3. Choose Right Format

- **CSV** - For data analysis
- **JSON** - For APIs and programming
- **Excel** - For business users
- **All** - When unsure or need multiple

### 4. Include Metadata

JSON format automatically includes:
- Export timestamp
- Row count
- Column names

### 5. Version Control

```bash
--filename report_v1
--filename report_v2
```

## Tips

### Large Datasets

For large exports:

```bash
# Add LIMIT to your query
myquery export query "Show customers LIMIT 10000" --format csv

# Or be more specific
myquery export query "Show active customers from 2024" --format csv
```

### Automated Exports

Create a script:

```bash
#!/bin/bash
# daily_export.sh

myquery export query "Daily summary" \
  --filename daily_$(date +%Y%m%d) \
  --format excel \
  --output reports/daily
```

Then schedule with cron or Task Scheduler.

### Combine with Other Features

```bash
# Query, visualize, AND export
myquery visualize chart "Sales trends" --type line
# Then export the data
myquery export query "Sales trends data" --format csv
```

## Troubleshooting

### "No data to export"

- Verify your query returns data
- Use `myquery query execute "..."` first to test

### "Permission denied"

- Check output directory permissions
- Use absolute path: `--output /full/path/to/directory`

### "File exists"

- Files are overwritten by default
- Use unique filenames or timestamps

### Large file warnings

- CSV and JSON are text-based (larger)
- Excel is binary (smaller but limit ~1M rows)
- Consider filtering data before export

## Next Steps

- [Natural Language Queries](natural-language-queries.md) - Generate queries to export
- [Multi-Database](multi-database.md) - Export merged data
- [CLI Reference](../cli/commands.md#export-commands) - Full command docs

---

[← Back to Documentation](../README.md)

