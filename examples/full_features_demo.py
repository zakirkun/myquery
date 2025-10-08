"""Complete demo of all myquery features."""
import os
import sqlite3
from core.agent import QueryAgent


def create_demo_databases():
    """Create multiple demo databases."""
    # Create sales database
    conn = sqlite3.connect("demo_sales.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY,
            product TEXT,
            amount REAL,
            month TEXT
        )
    """)
    
    cursor.executemany(
        "INSERT INTO sales VALUES (?, ?, ?, ?)",
        [
            (1, "Product A", 1000, "2024-01"),
            (2, "Product B", 1500, "2024-01"),
            (3, "Product A", 1200, "2024-02"),
            (4, "Product B", 1800, "2024-02"),
            (5, "Product C", 900, "2024-02"),
        ]
    )
    conn.commit()
    conn.close()
    print("✅ Created demo_sales.db")
    
    # Create inventory database
    conn = sqlite3.connect("demo_inventory.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            stock INTEGER,
            price REAL
        )
    """)
    
    cursor.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?)",
        [
            (1, "Product A", 50, 99.99),
            (2, "Product B", 30, 149.99),
            (3, "Product C", 75, 79.99),
        ]
    )
    conn.commit()
    conn.close()
    print("✅ Created demo_inventory.db")


def demo_visualization():
    """Demo visualization feature."""
    print("\n" + "="*60)
    print("📊 DEMO 1: DATA VISUALIZATION")
    print("="*60)
    
    agent = QueryAgent()
    agent.connect_database("sqlite", "demo_sales.db")
    
    # Execute query
    results = agent.execute_query_flow("Show all sales data")
    
    # Visualize as bar chart
    print("\n📈 Creating bar chart...")
    viz_result = agent.visualize_data_tool._run(
        query_result_json=results["execution_result"],
        chart_type="bar",
        x_column="product",
        y_column="amount",
        title="Sales by Product"
    )
    print(viz_result)
    
    # Visualize as pie chart
    print("\n🥧 Creating pie chart...")
    viz_result = agent.visualize_data_tool._run(
        query_result_json=results["execution_result"],
        chart_type="pie",
        x_column="product",
        y_column="amount",
        title="Sales Distribution"
    )
    print(viz_result)


def demo_multi_database():
    """Demo multi-database feature."""
    print("\n" + "="*60)
    print("🗄️  DEMO 2: MULTI-DATABASE QUERIES")
    print("="*60)
    
    agent = QueryAgent()
    
    # Add connections
    print("\n📌 Adding database connections...")
    agent.multi_db_manager.add_connection(
        "sales", "sqlite", "demo_sales.db"
    )
    agent.multi_db_manager.add_connection(
        "inventory", "sqlite", "demo_inventory.db"
    )
    
    # List connections
    connections = agent.multi_db_manager.list_connections()
    print(f"✅ Connected databases: {', '.join(connections)}")
    
    # Compare schemas
    print("\n📊 Comparing schemas...")
    schemas = agent.multi_db_manager.compare_schemas()
    for db_name, schema_info in schemas.items():
        print(f"  {db_name}: {schema_info.get('table_count')} table(s) - {schema_info.get('tables')}")
    
    # Query all databases (note: different tables, so this might error)
    print("\n🔍 Querying inventory database...")
    import json
    result = agent.multi_db_query_tool._run(
        query="SELECT * FROM products",
        connections="inventory"
    )
    results = json.loads(result)
    for db_name, db_result in results.items():
        if db_result.get("success"):
            print(f"  {db_name}: {db_result.get('row_count')} rows")


def demo_web_integration():
    """Demo web UI (just show how to start)."""
    print("\n" + "="*60)
    print("🌐 DEMO 3: WEB UI")
    print("="*60)
    
    print("\n📝 To start the web UI, run:")
    print("  python -m cli.main web start")
    print("\nThen open your browser at:")
    print("  http://localhost:8000")
    print("\nFeatures:")
    print("  • Interactive query interface")
    print("  • Visual schema explorer")
    print("  • Real-time chat with database")
    print("  • Data visualization")


def main():
    """Run all demos."""
    print("🚀 myquery - Complete Features Demo")
    print("="*60)
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set!")
        print("Some features may not work. Please set it in .env file.")
        print()
    
    # Create demo databases
    print("\n📦 Creating demo databases...")
    create_demo_databases()
    
    # Run demos
    try:
        demo_visualization()
    except Exception as e:
        print(f"❌ Visualization demo error: {e}")
    
    try:
        demo_multi_database()
    except Exception as e:
        print(f"❌ Multi-database demo error: {e}")
    
    demo_web_integration()
    
    print("\n" + "="*60)
    print("✅ Demo completed!")
    print("="*60)
    print("\n📁 Generated files:")
    print("  • demo_sales.db")
    print("  • demo_inventory.db")
    print("  • outputs/visualizations/*.html")
    print("\n🎯 Next steps:")
    print("  1. python -m cli.main web start")
    print("  2. python -m cli.main visualize chart 'Show sales data'")
    print("  3. python -m cli.main multidb list")


if __name__ == "__main__":
    main()

