# Changelog

All notable changes to myquery will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-10-08

### Added - Major Features 🎉

#### 📊 Data Visualization
- **VisualizeDataTool** - Plotly-based interactive chart generation
- **CLI command** `myquery visualize chart` for creating visualizations
- Support for 5 chart types: bar, line, scatter, pie, table
- Auto-detection of best chart type based on data
- Interactive HTML output with browser auto-open
- Charts saved in `outputs/visualizations/` directory

#### 🗄️  Multi-Database Support
- **MultiDBManager** - Manage multiple database connections simultaneously
- **MultiDBQueryTool** - Execute queries across multiple databases
- **CLI commands** under `myquery multidb`:
  - `add` - Add database connection
  - `list` - List all connections
  - `remove` - Remove connection
  - `query` - Execute query on all/selected databases
  - `compare` - Compare schemas across databases
- Aggregate and compare results from different databases

#### 🌐 Web UI
- **FastAPI web server** with full REST API
- **WebSocket support** for real-time chat
- **Embedded HTML interface** (no separate frontend build needed)
- Interactive query interface
- Visual schema explorer
- Connection management UI
- Data visualization dashboard
- **CLI command** `myquery web start` to launch server
- API endpoints:
  - `POST /api/connect` - Connect to database
  - `POST /api/query` - Execute natural language query
  - `POST /api/sql` - Execute raw SQL
  - `GET /api/schema` - Get database schema
  - `GET /api/tables` - List tables
  - `WS /ws/chat` - WebSocket chat

#### 🔄 Auto-Connect Feature
- All commands now support auto-connect from `.env`
- No need to manually connect before running queries
- `--auto/--no-auto` flag for control
- Supports .env → saved session → prompt user fallback
- Applied to: `chat`, `query execute`, `query sql`, `visualize`

### Enhanced
- **QueryAgent** - Integrated visualization and multi-DB tools
- **CLI** - Added 3 new command groups: `visualize`, `multidb`, `web`
- **Documentation** - Comprehensive guides for all new features
- **Examples** - Added `full_features_demo.py` showcasing all features

### Dependencies Added
- `plotly>=5.18.0` - Interactive visualizations
- `matplotlib>=3.8.0` - Chart generation fallback
- `pandas>=2.1.0` - Data manipulation
- `jinja2>=3.1.3` - Template rendering
- `websockets>=12.0` - WebSocket support

### Fixed
- Pydantic warnings for `schema_json` field names
- Auto-connect indentation and error handling
- SQL text() wrapper for SQLAlchemy 2.0 compatibility

## [0.1.0] - 2025-10-08

### Added - Initial Release 🎉

#### Core Features
- 🗣️ **Natural Language Queries** - Convert English to SQL using OpenAI
- 🔌 **Multi-Database Support** - PostgreSQL, MySQL, SQLite
- 🧠 **AI-Powered Analysis** - Automatic insights from query results
- 💬 **Interactive Chat Mode** - Conversational database interface
- 🔍 **Schema Discovery** - Automatic schema extraction and analysis

#### Tools Implemented
- `ConnectDBTool` - Database connection management
- `GetSchemaTool` - Schema extraction
- `AnalyzeSchemaTool` - AI-powered schema analysis
- `GenerateQueryTool` - SQL generation from natural language
- `ExecuteQueryTool` - Safe query execution
- `FormatTableTool` - Rich terminal table formatting
- `AnalyzeDataTool` - Data analysis and insights

#### CLI Commands
- `myquery connect` - Database connection management
  - `db` - Connect to database
  - `restore` - Restore saved session
  - `status` - Show connection status
- `myquery chat` - Interactive chat interface
  - `start` - Start chat session
- `myquery query` - Query execution
  - `execute` - Natural language query
  - `sql` - Raw SQL execution
- `myquery server` - MCP server management
  - `start` - Start MCP server on port 7766

#### MCP (Model Context Protocol)
- FastAPI server on port 7766
- REST API endpoints for all core actions
- Session management with context tracking
- Python client library (`mcp.client.MCPClient`)
- Support for actions:
  - `connect_db`
  - `get_schema`
  - `generate_query`
  - `execute_query`
  - `analyze_results`
  - `get_status`
  - `chat`

#### Configuration
- Pydantic-based settings management
- Environment variable support via `.env`
- Session persistence in `.myquery_session.json`
- Rich logging with configurable levels

#### Documentation
- Comprehensive README.md
- QUICKSTART.md for new users
- CONTRIBUTING.md for developers
- PROJECT_SUMMARY.md with architecture details
- FEATURES.md detailing specific features
- Example scripts and demos

#### Safety Features
- Destructive query prevention (DROP, DELETE, etc.)
- Connection validation
- Query timeout support
- Password security (not saved in session files)
- Error handling with helpful messages

## [Unreleased]

### Planned Features
- [ ] Query result export (CSV, JSON, Excel)
- [ ] Query history and favorites
- [ ] Query optimization suggestions
- [ ] Advanced chart customization options
- [ ] Multi-database data merging/joining
- [ ] Authentication for Web UI
- [ ] React/Vue frontend option
- [ ] Query templates library
- [ ] Scheduled queries and alerts
- [ ] Dashboard with multiple charts
- [ ] More database support (MongoDB, Redis, etc.)

---

## Version History

- **v0.2.0** (2025-10-08) - Major update: Visualization, Multi-DB, Web UI
- **v0.1.0** (2025-10-08) - Initial release: Core functionality

---

[0.2.0]: https://github.com/your-org/myquery/releases/tag/v0.2.0
[0.1.0]: https://github.com/your-org/myquery/releases/tag/v0.1.0
