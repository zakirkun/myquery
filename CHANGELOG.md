# Changelog

All notable changes to myquery will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2025-10-08

### Added - Productivity Features 🚀

#### 📤 Data Export
- **ExportDataTool** - Export query results to CSV, JSON, Excel
- **Multi-format support** - Export to single format or all at once
- **CLI commands** `myquery export query` and `myquery export sql`
- **Auto-filename generation** with timestamps
- **Excel formatting** - Auto-adjusted column widths
- **JSON metadata** - Includes export timestamp, row count, columns
- **File size reporting** - Shows exported file sizes
- **Custom output directory** support

#### 🔗 Multi-Database Merge/Join
- **Enhanced MultiDBQueryTool** with data merge capabilities
- **Union merge** - Stack rows from all databases with source tracking
- **Join merge** - Merge data by common key column (outer join)
- **Schema alignment** - Auto-handle missing columns across databases
- **Source tracking** - `_source_db` column shows data origin
- **Merge metadata** - Statistics about merge operation
- **Column suffixing** - Automatic naming for joined columns
- **CLI flags**: `--merge`, `--merge-type`, `--merge-key`

#### ⚡ Query Optimization
- **QueryOptimizationTool** - AI-powered SQL optimization suggestions
- **Static analysis** - Detects 10+ common performance issues:
  - SELECT * usage
  - Missing WHERE clauses
  - OR in WHERE conditions
  - NOT IN subqueries
  - Functions on indexed columns
  - Implicit type conversions
  - Multiple JOINs without filtering
  - Leading wildcards in LIKE
  - DISTINCT with ORDER BY
- **AI-powered suggestions** - Context-aware recommendations using schema
- **Index recommendations** - Based on query patterns and schema
- **Query rewriting** - Alternative query suggestions
- **Complexity scoring** - Calculates query complexity (0-100)
- **Complexity levels** - Simple, Moderate, Complex, Very Complex
- **Best practices** - General optimization tips

### Enhanced

#### 🧠 QueryAgent Improvements
- Added `export_data_tool` and `query_optimization_tool`
- New method `export_results()` for easy data export
- New method `optimize_query()` for optimization analysis
- Enhanced `execute_query_flow()` with `optimize` parameter
- LLM integration for optimization tool

#### 💬 CLI Enhancements
- New command group `myquery export` with 2 subcommands
- Enhanced `myquery multidb query` with merge options
- Import export module in main CLI
- Auto-connect support for export commands

#### 📚 Documentation
- **NEW_FEATURES.md** - Comprehensive guide for v0.4.0 features
- Updated README with new features section
- Examples for export, merge/join, and optimization
- API reference and use cases

### Dependencies Added
- `pandas>=2.1.0` - Required for data merging and export
- `openpyxl>=3.1.0` - Required for Excel export

### Files Added
- `tools/export_data_tool.py` - Data export implementation
- `tools/query_optimization_tool.py` - Query optimization implementation
- `cli/commands/export.py` - Export CLI commands
- `NEW_FEATURES.md` - Feature documentation

### Files Modified
- `tools/multi_db_query_tool.py` - Added merge/join capabilities
- `tools/__init__.py` - Export new tools
- `core/agent.py` - Integrate new tools
- `cli/main.py` - Add export command
- `README.md` - Document new features
- `CHANGELOG.md` - This file

### Use Cases Enabled
1. **Data Export**: Export analysis results for reports and sharing
2. **Cross-Database Analysis**: Compare and merge data from multiple environments
3. **Performance Tuning**: Get AI-powered optimization suggestions
4. **Data Consolidation**: Merge regional databases into unified dataset
5. **Query Review**: Analyze queries for best practices

### Technical Improvements
- Pandas-based data manipulation for robust merging
- Type-safe export with multiple format handlers
- Modular optimization checks (easily extensible)
- Non-breaking integration (all features optional)
- Graceful error handling for merge failures

---

## [0.3.0] - 2025-10-08

### Added - Smart Visualization 🎨✨

#### 📊 Auto-Visualization in Chat
- **Smart keyword detection** - Automatically detects when users request visualizations
- **Auto-chart generation** - Creates charts directly from chat queries
- **Seamless integration** - Works within normal chat flow, no separate commands needed
- **Natural language** - Just say "show me a chart" or "visualize this data"

#### 🌍 Bilingual Support
- **English keywords**: chart, graph, plot, visualize, show, display
- **Indonesian keywords**: grafik, visualisasi, tampilkan, lihat, tabel
- **Chart-specific (both languages)**:
  - Bar: bar chart, bar graph, batang
  - Line: line chart, trend, tren, grafik garis
  - Pie: pie chart, distribution, proporsi, persentase
  - Scatter: scatter, correlation, korelasi, sebaran

#### 🎯 Intelligent Chart Type Detection
- **Auto-detection** - Analyzes data to pick best chart type
- **Contextual hints** - Recognizes time series, comparisons, distributions
- **Explicit control** - Users can specify exact chart type
- **Fallback handling** - Graceful degradation if visualization fails

#### 🔄 Enhanced Query Flow
- **Unified output** - Table + Analysis + Chart in one response
- **Progressive display** - Shows table, then analysis, then chart
- **Browser integration** - Charts auto-open in default browser
- **File persistence** - All charts saved to `outputs/visualizations/`

### Enhanced

#### 🧠 QueryAgent Improvements
- Added `_detect_visualization_request()` method
- Enhanced `execute_query_flow()` with `auto_visualize` parameter
- Improved `chat()` method to handle visualization results
- Better response formatting with visualization info

#### 💬 Chat Command Enhancements
- Direct integration with visualization flow
- Rich output for table + analysis + chart
- Better error handling for visualization failures
- Enhanced help text with visualization examples

#### 📚 Documentation
- **SMART_VISUALIZATION.md** - Comprehensive guide to auto-visualization
- Updated README with Smart Visualization section
- Added examples for English and Indonesian queries
- Keyword reference guide

#### 🎮 Examples
- **smart_visualization_demo.py** - Interactive demo with sample database
- 20+ example queries (English & Indonesian)
- Step-by-step instructions
- Quick reference guide

### New Features Breakdown

**Before (v0.2.0):**
```bash
# Had to use separate command
myquery visualize chart "Show sales by region" --type bar
```

**Now (v0.3.0):**
```bash
# Just ask in chat!
myquery chat start
You: "Show me a bar chart of sales by region"
# → Automatically generates chart + displays table + gives analysis
```

**Bilingual:**
```bash
You: "Tampilkan grafik penjualan per bulan"
# → Auto-detects Indonesian, creates chart
```

### Technical Improvements
- Keyword-based visualization detection system
- Language-agnostic chart type mapping
- Context-aware chart type heuristics
- Non-blocking visualization (failures don't break queries)
- Modular architecture for easy extension

### Use Cases Enabled
1. **Quick exploration**: "Visualize this data" → instant chart
2. **Trend analysis**: "Show sales trend by month" → line chart
3. **Comparisons**: "Compare revenue by region" → bar chart
4. **Distributions**: "Show category breakdown" → pie chart
5. **Indonesian users**: "Tampilkan grafik..." → full support

### Files Changed
- `core/agent.py` - Added visualization detection and integration
- `cli/commands/chat.py` - Enhanced display with visualization support
- `SMART_VISUALIZATION.md` - New comprehensive documentation
- `examples/smart_visualization_demo.py` - New interactive demo
- `README.md` - Added Smart Visualization section
- `CHANGELOG.md` - This file

---

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
