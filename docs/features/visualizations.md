# Smart Visualizations

Auto-generate interactive charts from your query results using natural language.

## Overview

myquery automatically creates visualizations when you ask for them. Just mention "chart", "graph", or "visualize" in your question.

**Supported chart types:**
- Bar charts
- Line charts
- Pie charts
- Scatter plots
- Interactive tables

## Quick Start

```bash
myquery chat start

You: "Show me a chart of sales by month"
→ Generates line chart + opens in browser

You: "Bar chart of top 10 products by revenue"
→ Creates bar chart automatically

You: "Visualize category distribution"
→ Auto-detects and creates appropriate chart
```

## Chart Types

### Auto-Detection

Let myquery choose the best chart:

```
"Show me a chart of revenue by region"
→ Detects categorical data → Bar chart

"Visualize sales trends over time"
→ Detects time series → Line chart

"Graph of product category distribution"
→ Detects proportion → Pie chart
```

### Specific Chart Types

Request exact chart type:

```
"Bar chart of top products"
"Line chart of monthly sales"
"Pie chart of market share"
"Scatter plot of price vs quantity"
```

### Keywords

**Visualization keywords:**
- English: chart, graph, plot, visualize, show, display
- Indonesian: grafik, visualisasi, tampilkan, lihat

**Chart-specific:**
- Bar: "bar chart", "bar graph", "batang"
- Line: "line chart", "trend", "tren", "grafik garis"
- Pie: "pie chart", "distribution", "proporsi", "persentase"
- Scatter: "scatter", "correlation", "korelasi", "sebaran"

## Examples

### Business Analytics

```
"Line chart of monthly revenue for this year"
"Bar chart comparing sales by region"
"Pie chart showing customer distribution by country"
"Visualize top 10 products by profit margin"
```

### Trend Analysis

```
"Show sales trend by month"
"Graph of user growth over time"
"Visualize daily active users for the last 30 days"
```

### Comparisons

```
"Bar chart comparing product categories"
"Graph of revenue: this year vs last year"
"Show performance metrics across teams"
```

### Distributions

```
"Pie chart of order status distribution"
"Show percentage breakdown by category"
"Visualize market share by product"
```

## Using Visualizations

### In Chat Mode

```bash
myquery chat start

You: "Show me sales by region"
→ Displays table + analysis

You: "Now show that as a bar chart"
→ Creates chart from last query
```

### Direct Command

```bash
myquery visualize chart "Sales by month" --type line
myquery visualize chart "Product distribution" --type pie
myquery visualize chart "Revenue trends" --type auto
```

### Bilingual Support

**English:**
```
"Show me a chart of sales by month"
"Visualize revenue trends"
```

**Indonesian:**
```
"Tampilkan grafik penjualan per bulan"
"Visualisasi tren revenue"
```

## Chart Features

### Interactive

- Hover for data points
- Zoom and pan
- Click to toggle series
- Export as PNG

### Auto-Formatting

- Auto-adjusted axes
- Smart labeling
- Color schemes
- Responsive layout

### Output

Charts are:
- Saved to `outputs/visualizations/`
- Auto-opened in browser
- Self-contained HTML files
- Shareable and embeddable

## Output Example

```
✅ Visualization Created
📊 Chart type: bar
📈 Data points: 12
📁 File: outputs/visualizations/chart_abc123.html
[Opens automatically in browser]
```

## Programmatic Usage

```python
from core.agent import QueryAgent

agent = QueryAgent()
agent.connect_database(...)

# Execute with auto-visualization
results = agent.execute_query_flow(
    "Show sales by month",
    auto_visualize=True  # Default is True
)

# Access visualization
if results.get("visualization"):
    print(results["visualization"])
    print(f"Chart type: {results['visualization_type']}")
```

## Best Practices

1. **Be Specific** - "Bar chart of top 10 products" vs "show products"
2. **Choose Right Type** - Line for trends, Bar for comparisons, Pie for proportions
3. **Limit Data** - Use "top 10" or LIMIT for better charts
4. **Add Context** - "by month", "by region", "by category"

## Tips

- Use "chart" or "graph" to trigger visualization
- Let AI auto-detect chart type when unsure
- Charts open automatically in browser
- Find saved charts in `outputs/visualizations/`

## Next Steps

- [Natural Language Queries](natural-language-queries.md) - Generate data to visualize
- [Data Export](data-export.md) - Export chart data
- [CLI Reference](../cli/commands.md#visualization-commands) - Full command docs

---

[← Back to Documentation](../README.md)

