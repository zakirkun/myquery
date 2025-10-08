# Custom Tools

Extend myquery with custom LangChain tools.

## Overview

myquery uses LangChain tools for all operations. You can create custom tools to add new functionality.

## Creating a Tool

### Basic Structure

```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class CustomToolInput(BaseModel):
    """Input schema for the tool."""
    param1: str = Field(description="First parameter")
    param2: int = Field(description="Second parameter")

class CustomTool(BaseTool):
    """Custom tool description."""
    
    name: str = "custom_tool"
    description: str = """
    Description of what this tool does.
    Use this when you need to...
    """
    args_schema: Type[BaseModel] = CustomToolInput
    
    def _run(self, param1: str, param2: int) -> str:
        """
        Execute the tool.
        
        Args:
            param1: Description of param1
            param2: Description of param2
            
        Returns:
            Tool result as string
        """
        # Your custom logic here
        result = f"Processed: {param1} with {param2}"
        return result
    
    async def _arun(self, *args, **kwargs) -> str:
        """Async version (optional)."""
        return self._run(*args, **kwargs)
```

## Example: Custom Export Tool

```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import pandas as pd

class CSVExportInput(BaseModel):
    data: str = Field(description="JSON data to export")
    filename: str = Field(description="Output filename")

class CSVExportTool(BaseTool):
    """Export data to CSV file."""
    
    name: str = "csv_export"
    description: str = """
    Export query results to CSV file.
    Use this when user wants to save data as CSV.
    """
    args_schema: Type[BaseModel] = CSVExportInput
    
    def _run(self, data: str, filename: str) -> str:
        import json
        
        # Parse data
        records = json.loads(data)
        
        # Create DataFrame
        df = pd.DataFrame(records)
        
        # Export to CSV
        output_path = f"exports/{filename}.csv"
        df.to_csv(output_path, index=False)
        
        return f"✅ Exported to {output_path}"
```

## Integrating with QueryAgent

### Method 1: Add to Agent

```python
from core.agent import QueryAgent
from your_module import CustomTool

agent = QueryAgent()

# Add custom tool
custom_tool = CustomTool()
agent.tools.append(custom_tool)

# Now available in agent
```

### Method 2: Modify Agent Class

Edit `core/agent.py`:

```python
class QueryAgent:
    def __init__(self, ...):
        # ... existing tools ...
        
        # Add your custom tool
        from your_module import CustomTool
        self.custom_tool = CustomTool()
        
        self.tools = [
            # ... existing tools ...
            self.custom_tool,
        ]
```

## Tool Best Practices

### 1. Clear Description

```python
description: str = """
Export query results to PDF format with custom styling.
Use this when user explicitly requests PDF export.
Input should be the query results in JSON format.
"""
```

### 2. Type Hints

```python
def _run(self, data: str, format: str) -> str:
    """Always use type hints."""
    pass
```

### 3. Error Handling

```python
def _run(self, data: str) -> str:
    try:
        # Your logic
        return "✅ Success"
    except Exception as e:
        return f"❌ Error: {str(e)}"
```

### 4. Logging

```python
from config.logging import get_logger

logger = get_logger(__name__)

def _run(self, data: str) -> str:
    logger.info("Processing data...")
    # Your logic
    logger.info("✅ Complete")
    return result
```

## Example: Database Backup Tool

```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import subprocess
from datetime import datetime

class BackupInput(BaseModel):
    table_name: str = Field(description="Table to backup")

class DatabaseBackupTool(BaseTool):
    """Backup database table to file."""
    
    name: str = "backup_table"
    description: str = """
    Create a backup of a database table.
    Use when user wants to backup or archive table data.
    """
    args_schema: Type[BaseModel] = BackupInput
    
    db_connection: str = ""  # Set from agent
    
    def _run(self, table_name: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_{table_name}_{timestamp}.sql"
        
        # Use pg_dump for PostgreSQL
        cmd = f"pg_dump -t {table_name} {self.db_connection} > {filename}"
        
        try:
            subprocess.run(cmd, shell=True, check=True)
            return f"✅ Backup created: {filename}"
        except Exception as e:
            return f"❌ Backup failed: {str(e)}"
```

## Example: Slack Notification Tool

```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import requests

class SlackNotifyInput(BaseModel):
    message: str = Field(description="Message to send")
    channel: str = Field(description="Slack channel", default="#general")

class SlackNotificationTool(BaseTool):
    """Send notifications to Slack."""
    
    name: str = "slack_notify"
    description: str = """
    Send notification to Slack channel.
    Use when user wants to share results via Slack.
    """
    args_schema: Type[BaseModel] = SlackNotifyInput
    
    webhook_url: str = ""  # Set from config
    
    def _run(self, message: str, channel: str = "#general") -> str:
        payload = {
            "channel": channel,
            "text": message
        }
        
        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            return f"✅ Sent to {channel}"
        except Exception as e:
            return f"❌ Failed to send: {str(e)}"
```

## Testing Custom Tools

```python
def test_custom_tool():
    tool = CustomTool()
    
    result = tool._run(
        param1="test",
        param2=123
    )
    
    assert "✅" in result
    print(result)

if __name__ == "__main__":
    test_custom_tool()
```

## Next Steps

- [Architecture](architecture.md) - System design
- [Development](development.md) - Contributing guide
- [Programmatic Usage](../api/programmatic-usage.md) - API docs

---

[← Back to Documentation](../README.md)

