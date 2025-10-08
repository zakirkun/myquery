"""Demo script with SQLite database."""
import sqlite3
import os
from core.agent import QueryAgent


def create_demo_database():
    """Create a demo SQLite database with sample data."""
    db_path = "demo.db"
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Create database and tables
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            country TEXT,
            created_at TEXT
        )
    """)
    
    # Create products table
    cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            stock INTEGER
        )
    """)
    
    # Create orders table
    cursor.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            total_amount REAL,
            order_date TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    
    # Insert sample customers
    customers = [
        (1, "John Doe", "john@example.com", "USA", "2024-01-15"),
        (2, "Jane Smith", "jane@example.com", "UK", "2024-02-20"),
        (3, "Bob Johnson", "bob@example.com", "Canada", "2024-03-10"),
        (4, "Alice Williams", "alice@example.com", "USA", "2024-04-05"),
        (5, "Charlie Brown", "charlie@example.com", "Australia", "2024-05-12"),
    ]
    cursor.executemany(
        "INSERT INTO customers VALUES (?, ?, ?, ?, ?)",
        customers
    )
    
    # Insert sample products
    products = [
        (1, "Laptop", "Electronics", 999.99, 50),
        (2, "Mouse", "Electronics", 29.99, 200),
        (3, "Keyboard", "Electronics", 79.99, 150),
        (4, "Monitor", "Electronics", 299.99, 75),
        (5, "Desk Chair", "Furniture", 199.99, 30),
    ]
    cursor.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?, ?)",
        products
    )
    
    # Insert sample orders
    orders = [
        (1, 1, 1, 2, 1999.98, "2024-06-01"),
        (2, 2, 2, 1, 29.99, "2024-06-02"),
        (3, 1, 3, 1, 79.99, "2024-06-03"),
        (4, 3, 4, 3, 899.97, "2024-06-04"),
        (5, 4, 5, 1, 199.99, "2024-06-05"),
        (6, 2, 1, 1, 999.99, "2024-06-06"),
        (7, 5, 2, 5, 149.95, "2024-06-07"),
        (8, 1, 4, 1, 299.99, "2024-06-08"),
    ]
    cursor.executemany(
        "INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)",
        orders
    )
    
    conn.commit()
    conn.close()
    
    print(f"✅ Demo database created: {db_path}")
    print("📊 Tables: customers, products, orders")
    print("📝 Sample data inserted")
    return db_path


def run_demo():
    """Run the demo."""
    print("🚀 myquery Demo with SQLite\n")
    
    # Create demo database
    db_path = create_demo_database()
    print()
    
    # Initialize agent
    print("🤖 Initializing myquery agent...")
    agent = QueryAgent()
    print()
    
    # Connect to database
    print("🔌 Connecting to demo database...")
    result = agent.connect_database(
        db_type="sqlite",
        db_name=db_path,
    )
    print(result)
    print()
    
    # Example queries
    queries = [
        "Show me all tables",
        "List the top 3 customers by total spending",
        "What products are low on stock (less than 100 units)?",
        "Show total revenue by product category",
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*60}")
        print(f"Query {i}: {query}")
        print('='*60)
        
        results = agent.execute_query_flow(
            user_prompt=query,
            debug=True,
        )
        
        if results.get("analysis"):
            print(f"\n💡 Analysis:")
            print(results["analysis"])
        
        input("\nPress Enter for next query...")
    
    print("\n\n✅ Demo completed!")
    print(f"📁 Demo database saved as: {db_path}")
    print("🎯 You can now try: python -m cli.main chat start")


if __name__ == "__main__":
    # Make sure to set your OpenAI API key first!
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set!")
        print("Please set it in your .env file or environment variables.")
        print()
    
    run_demo()

