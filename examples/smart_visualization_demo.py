"""
Smart Visualization & Analysis Demo for myquery

This demo showcases the new auto-visualization feature that automatically
creates charts when users request visualizations in their queries.

Features demonstrated:
- Auto-detection of visualization requests
- Multiple chart types (bar, line, pie, scatter)
- AI-powered data analysis
- Bilingual support (English + Indonesian)
"""

import sqlite3
import os
from pathlib import Path


def create_demo_database():
    """Create a demo SQLite database with sample data."""
    db_path = Path("demo_visualization.db")
    
    # Remove if exists
    if db_path.exists():
        db_path.unlink()
    
    # Create database
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Create sales table
    cursor.execute("""
        CREATE TABLE sales (
            id INTEGER PRIMARY KEY,
            product VARCHAR(100),
            category VARCHAR(50),
            region VARCHAR(50),
            month VARCHAR(20),
            revenue DECIMAL(10, 2),
            quantity INTEGER
        )
    """)
    
    # Sample data
    data = [
        # Electronics
        (1, "Laptop Pro", "Electronics", "North", "January", 15000.00, 10),
        (2, "Laptop Pro", "Electronics", "South", "January", 18000.00, 12),
        (3, "Smartphone X", "Electronics", "East", "January", 12000.00, 20),
        (4, "Tablet Air", "Electronics", "West", "January", 8000.00, 15),
        
        (5, "Laptop Pro", "Electronics", "North", "February", 16500.00, 11),
        (6, "Smartphone X", "Electronics", "South", "February", 13500.00, 22),
        (7, "Tablet Air", "Electronics", "East", "February", 9000.00, 17),
        
        (8, "Laptop Pro", "Electronics", "North", "March", 18000.00, 12),
        (9, "Smartphone X", "Electronics", "South", "March", 15000.00, 25),
        
        # Clothing
        (10, "T-Shirt", "Clothing", "North", "January", 2000.00, 100),
        (11, "Jeans", "Clothing", "South", "January", 3500.00, 70),
        (12, "Jacket", "Clothing", "East", "January", 5000.00, 50),
        
        (13, "T-Shirt", "Clothing", "North", "February", 2200.00, 110),
        (14, "Jeans", "Clothing", "South", "February", 3800.00, 75),
        
        (15, "T-Shirt", "Clothing", "North", "March", 2500.00, 125),
        
        # Home & Garden
        (16, "Coffee Maker", "Home", "West", "January", 1500.00, 30),
        (17, "Blender", "Home", "East", "January", 800.00, 40),
        (18, "Coffee Maker", "Home", "West", "February", 1600.00, 32),
        (19, "Blender", "Home", "East", "February", 900.00, 45),
        (20, "Coffee Maker", "Home", "West", "March", 1800.00, 36),
    ]
    
    cursor.executemany(
        "INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?)",
        data
    )
    
    conn.commit()
    conn.close()
    
    print(f"✅ Demo database created: {db_path}")
    print(f"📊 20 sales records inserted")
    return str(db_path)


def print_demo_instructions(db_path):
    """Print demo instructions."""
    
    print("\n" + "="*70)
    print("🎯 SMART VISUALIZATION DEMO")
    print("="*70)
    
    print(f"""
📁 Database: {db_path}
🎨 Features: Auto-visualization + AI Analysis

🚀 HOW TO USE:

1. Connect to the demo database:
   
   myquery connect db --db-type sqlite --db-name {db_path}

2. Start interactive chat:
   
   myquery chat start

3. Try these example queries:

""")
    
    # English examples
    print("📌 ENGLISH EXAMPLES:\n")
    
    examples_en = [
        ("Basic Query (No Visualization)", 
         "Show me total revenue by category"),
        
        ("Auto Bar Chart",
         "Show me a chart of total revenue by category"),
        
        ("Line Chart (Trend)",
         "Line chart of total revenue by month"),
        
        ("Pie Chart (Distribution)",
         "Pie chart showing revenue distribution by region"),
        
        ("Top N with Bar Chart",
         "Bar chart of top 5 products by revenue"),
        
        ("Scatter Plot",
         "Scatter plot of price vs quantity"),
        
        ("Auto-Detection",
         "Visualize sales performance by region"),
    ]
    
    for title, query in examples_en:
        print(f"   • {title}:")
        print(f"     \"{query}\"\n")
    
    # Indonesian examples
    print("\n📌 INDONESIAN EXAMPLES:\n")
    
    examples_id = [
        ("Query Biasa (Tanpa Visualisasi)",
         "Tampilkan total revenue per kategori"),
        
        ("Grafik Batang Otomatis",
         "Tampilkan grafik total revenue per kategori"),
        
        ("Grafik Garis (Tren)",
         "Grafik garis revenue per bulan"),
        
        ("Diagram Pie (Distribusi)",
         "Pie chart proporsi revenue per region"),
        
        ("Top N dengan Bar Chart",
         "Bar chart 5 produk dengan revenue tertinggi"),
    ]
    
    for title, query in examples_id:
        print(f"   • {title}:")
        print(f"     \"{query}\"\n")
    
    print("\n" + "="*70)
    print("💡 TIPS:")
    print("="*70)
    print("""
✨ All queries will automatically:
   1. Generate SQL
   2. Execute query
   3. Display results in table
   4. Provide AI analysis
   5. Create visualization (if requested)

📊 Visualization Keywords:
   - chart, graph, plot, visualize (English)
   - grafik, visualisasi, tampilkan (Indonesian)

🎨 Specific Chart Types:
   - "bar chart" / "batang" → Bar chart
   - "line chart" / "tren" → Line chart
   - "pie chart" / "proporsi" → Pie chart
   - "scatter" / "korelasi" → Scatter plot

🐛 Debug Mode:
   myquery chat start --debug
   (See generated SQL and visualization decisions)

📂 Charts saved to:
   outputs/visualizations/

🌐 Charts auto-open in browser!
""")
    
    print("="*70)
    print("🎉 Happy exploring!")
    print("="*70 + "\n")


def print_sample_queries_only():
    """Just print sample queries for quick reference."""
    print("\n" + "="*70)
    print("📋 QUICK REFERENCE - SAMPLE QUERIES")
    print("="*70 + "\n")
    
    queries = {
        "Basic Queries": [
            "Show me all products",
            "List total revenue by category",
            "Find top 10 products by sales",
            "Count orders by region",
        ],
        
        "With Visualization": [
            "Show me a bar chart of revenue by category",
            "Line chart of monthly sales trends",
            "Pie chart of category distribution",
            "Visualize top products",
        ],
        
        "Advanced": [
            "Show me a trend line of revenue over time",
            "Compare revenue across regions with a chart",
            "Display scatter plot of quantity vs revenue",
        ],
        
        "Indonesian": [
            "Tampilkan grafik revenue per kategori",
            "Grafik garis penjualan per bulan",
            "Pie chart distribusi per region",
        ]
    }
    
    for category, query_list in queries.items():
        print(f"🎯 {category}:")
        for q in query_list:
            print(f"   • \"{q}\"")
        print()
    
    print("="*70 + "\n")


if __name__ == "__main__":
    print("\n🚀 Setting up Smart Visualization Demo...\n")
    
    # Create demo database
    db_path = create_demo_database()
    
    # Print instructions
    print_demo_instructions(db_path)
    
    # Print quick reference
    print_sample_queries_only()
    
    print("✅ Demo setup complete!")
    print(f"\n🎯 Next step: Run the commands above to try the visualization features!\n")

