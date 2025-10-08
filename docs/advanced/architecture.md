# Architecture

System architecture and design of myquery.

## Overview

myquery is built with a modular architecture using:
- **LangChain** for LLM orchestration
- **OpenAI** for natural language processing
- **SQLAlchemy** for database connectivity
- **Typer** for CLI interface
- **FastAPI** for web/API server

## System Architecture

```
┌─────────────────┐
│   User Input    │
│  (CLI/Web/API)  │
└────────┬────────┘
         │
    ┌────▼────────┐
    │  QueryAgent │  ← Main orchestrator
    └────┬────────┘
         │
    ┌────▼──────────────────────┐
    │      LangChain Tools       │
    ├────────────────────────────┤
    │ • ConnectDBTool            │
    │ • GetSchemaTool            │
    │ • GenerateQueryTool (LLM)  │
    │ • ExecuteQueryTool         │
    │ • AnalyzeDataTool (LLM)    │
    │ • VisualizeDataTool        │
    │ • ExportDataTool           │
    │ • QueryOptimizationTool    │
    │ • MultiDBQueryTool         │
    └────┬───────────────────────┘
         │
    ┌────▼────────┐
    │  Database   │
    └─────────────┘
```

## Component Diagram

```
myquery/
├── cli/              # User interfaces
│   ├── main.py       # CLI entry point
│   └── commands/     # Command handlers
│
├── core/             # Business logic
│   ├── agent.py      # QueryAgent orchestrator
│   ├── query_generator.py
│   ├── schema_analyzer.py
│   ├── data_analyzer.py
│   └── multi_db_manager.py
│
├── tools/            # LangChain tools
│   ├── connect_db_tool.py
│   ├── execute_query_tool.py
│   ├── visualize_data_tool.py
│   ├── export_data_tool.py
│   └── ...
│
├── web/              # Web UI
│   └── main.py       # FastAPI server
│
├── mcp/              # MCP Protocol
│   ├── server.py     # MCP server
│   ├── protocol.py   # Protocol definitions
│   └── client.py     # Python client
│
└── config/           # Configuration
    ├── settings.py   # Pydantic settings
    └── logging.py    # Logging setup
```

## Query Flow

```
1. User Input
   "Show top 10 customers by revenue"
   
2. Schema Analysis
   - Load database schema
   - Identify relevant tables
   - Understand relationships
   
3. SQL Generation (LLM)
   - Use schema context
   - Generate optimized SQL
   - Validate syntax
   
4. Query Execution
   - Safety checks
   - Execute on database
   - Retrieve results
   
5. Data Processing
   - Format as table
   - Generate visualization (if requested)
   - AI analysis and insights
   
6. Output
   - Display results
   - Show analysis
   - Open charts (if applicable)
```

## Tool Architecture

Each tool inherits from LangChain's `BaseTool`:

```python
class ExampleTool(BaseTool):
    name: str = "example_tool"
    description: str = "Tool description"
    args_schema: Type[BaseModel] = ExampleInput
    
    def _run(self, **kwargs) -> str:
        # Tool implementation
        pass
```

Tools are stateless and composable.

## Data Flow

```
User Query
    ↓
Natural Language → LLM → SQL
    ↓
SQL → Database → Raw Results
    ↓
Raw Results → Formatter → Table
    ↓
Raw Results → LLM → Analysis
    ↓
Raw Results → Visualizer → Chart
    ↓
Output (Table + Analysis + Chart)
```

## Design Principles

1. **Modularity** - Each component is independent
2. **Composability** - Tools can be combined
3. **Safety** - Read-only by default
4. **Extensibility** - Easy to add new tools
5. **Type Safety** - Pydantic for validation

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| LLM Orchestration | LangChain | Tool coordination |
| AI Model | OpenAI GPT-4 | Natural language understanding |
| Database | SQLAlchemy | Multi-database support |
| CLI | Typer + Rich | Command-line interface |
| Web Server | FastAPI | Web UI and API |
| Visualization | Plotly | Interactive charts |
| Data Processing | Pandas | Data manipulation |
| Configuration | Pydantic | Settings management |

## Next Steps

- [Custom Tools](custom-tools.md) - Extend myquery
- [Development](development.md) - Contributing guide

---

[← Back to Documentation](../README.md)

