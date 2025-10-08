"""Example usage of myquery programmatically."""
from core.agent import QueryAgent
import os

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "your-api-key-here"


def main():
    """Example usage."""
    
    # Initialize agent
    print("🤖 Initializing myquery agent...")
    agent = QueryAgent()
    
    # Connect to SQLite database (example)
    print("\n🔌 Connecting to database...")
    result = agent.connect_database(
        db_type="sqlite",
        db_name="example.db",  # or ":memory:" for in-memory
    )
    print(result)
    
    # Get database schema
    print("\n📊 Getting database schema...")
    schema = agent.get_schema()
    print(f"Tables: {agent.get_table_list()}")
    
    # Execute a natural language query
    print("\n🔍 Executing query...")
    results = agent.execute_query_flow(
        user_prompt="Show me all records from the first table",
        debug=True,
    )
    
    if results.get("error"):
        print(f"❌ Error: {results['error']}")
    else:
        print(f"✅ Query executed successfully")
        print(f"\n💡 Analysis:\n{results['analysis']}")
    
    # Chat interaction
    print("\n💬 Chat interaction...")
    response = agent.chat("What tables are available?")
    print(f"Response: {response}")


if __name__ == "__main__":
    main()

