"""Example usage of MCP client."""
from mcp.client import MCPClient


def main():
    """Example MCP client usage."""
    
    # Create client
    print("🌐 Connecting to MCP server...")
    client = MCPClient("http://localhost:7766")
    
    # Connect to database
    print("\n🔌 Connecting to database...")
    response = client.connect_db(
        db_type="sqlite",
        db_name="example.db",
    )
    
    print(f"Success: {response.success}")
    print(f"Session ID: {response.session_id}")
    
    if response.success:
        # Get schema
        print("\n📊 Getting schema...")
        schema_response = client.get_schema()
        
        if schema_response.success:
            print(f"Tables: {schema_response.context.get('table_names', [])}")
        
        # Execute query
        print("\n🔍 Executing query...")
        query_response = client.execute_query(
            prompt="Show all records from the first table",
            debug=True,
        )
        
        if query_response.success:
            print("✅ Query executed successfully")
            print(f"Results: {query_response.data}")
        
        # Chat
        print("\n💬 Chat interaction...")
        chat_response = client.chat("What tables do we have?")
        
        if chat_response.success:
            print(f"Response: {chat_response.data['response']}")
        
        # Get context
        print("\n📋 Getting context...")
        context = client.get_context()
        print(f"Context: {context}")
        
        # Cleanup
        print("\n🧹 Cleaning up...")
        client.delete_session()
        print("Session deleted")


if __name__ == "__main__":
    main()

