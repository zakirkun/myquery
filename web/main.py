"""FastAPI web application for myquery."""
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from pathlib import Path
import json

from core.agent import QueryAgent
from config import get_logger, settings

logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="myquery Web UI",
    description="AI-powered database query interface",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance
agent: Optional[QueryAgent] = None

# Request models
class ConnectRequest(BaseModel):
    db_type: str
    db_name: str
    db_host: Optional[str] = "localhost"
    db_port: Optional[int] = None
    db_user: Optional[str] = None
    db_password: Optional[str] = None


class QueryRequest(BaseModel):
    prompt: str
    debug: bool = False


class SQLRequest(BaseModel):
    query: str


# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main web UI."""
    html_file = Path(__file__).parent / "static" / "index.html"
    if html_file.exists():
        return FileResponse(html_file)
    return HTMLResponse(content=get_default_html(), status_code=200)


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "connected": agent.is_connected() if agent else False,
    }


@app.post("/api/connect")
async def connect(request: ConnectRequest):
    """Connect to a database."""
    global agent
    
    try:
        if agent is None:
            agent = QueryAgent()
        
        result = agent.connect_database(
            db_type=request.db_type,
            db_name=request.db_name,
            db_host=request.db_host,
            db_port=request.db_port,
            db_user=request.db_user,
            db_password=request.db_password,
        )
        
        # Get schema info
        schema_json = agent.get_schema()
        schema_data = json.loads(schema_json)
        
        return {
            "success": result.startswith("✅"),
            "message": result,
            "tables": list(schema_data.get("tables", {}).keys()),
            "table_count": schema_data.get("total_tables", 0),
        }
    except Exception as e:
        logger.error(f"Connection error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/schema")
async def get_schema():
    """Get database schema."""
    if not agent or not agent.is_connected():
        raise HTTPException(status_code=400, detail="Not connected to database")
    
    try:
        schema_json = agent.get_schema()
        return json.loads(schema_json)
    except Exception as e:
        logger.error(f"Schema error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/query")
async def execute_query(request: QueryRequest):
    """Execute a natural language query."""
    if not agent or not agent.is_connected():
        raise HTTPException(status_code=400, detail="Not connected to database")
    
    try:
        results = agent.execute_query_flow(
            user_prompt=request.prompt,
            debug=request.debug,
        )
        
        if results.get("error"):
            raise HTTPException(status_code=400, detail=results["error"])
        
        return {
            "success": True,
            "sql": results.get("sql_query"),
            "result": json.loads(results.get("execution_result", "{}")),
            "analysis": results.get("analysis"),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/sql")
async def execute_sql(request: SQLRequest):
    """Execute raw SQL query."""
    if not agent or not agent.is_connected():
        raise HTTPException(status_code=400, detail="Not connected to database")
    
    try:
        execution_result = agent.execute_query_tool._run(sql_query=request.query)
        result_data = json.loads(execution_result)
        
        return {
            "success": result_data.get("success", False),
            "result": result_data,
        }
    except Exception as e:
        logger.error(f"SQL error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tables")
async def get_tables():
    """Get list of tables."""
    if not agent or not agent.is_connected():
        raise HTTPException(status_code=400, detail="Not connected to database")
    
    try:
        tables = agent.get_table_list()
        return {"tables": tables}
    except Exception as e:
        logger.error(f"Tables error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time chat."""
    await websocket.accept()
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            user_message = message_data.get("message", "")
            
            if not agent or not agent.is_connected():
                await websocket.send_json({
                    "type": "error",
                    "message": "Not connected to database",
                })
                continue
            
            # Process query
            try:
                response = agent.chat(user_message, debug=False)
                
                await websocket.send_json({
                    "type": "response",
                    "message": response,
                })
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": str(e),
                })
    
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")


def get_default_html() -> str:
    """Get default HTML if static file not found."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>myquery - AI Database Assistant</title>
        
        <!-- Tailwind CSS CDN -->
        <script src="https://cdn.tailwindcss.com"></script>
        
        <!-- Custom Tailwind Config -->
        <script>
            tailwind.config = {
                theme: {
                    extend: {
                        colors: {
                            primary: '#667eea',
                            'primary-dark': '#5568d3',
                        }
                    }
                }
            }
        </script>
        
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                padding: 40px;
                max-width: 1200px;
                width: 100%;
            }
            h1 { color: #667eea; margin-bottom: 10px; }
            .subtitle { color: #666; margin-bottom: 30px; }
            .section { margin: 20px 0; }
            .btn {
                background: #667eea;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
                margin: 5px;
            }
            .btn:hover { background: #5568d3; }
            input, textarea {
                width: 100%;
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                margin: 10px 0;
                font-size: 16px;
            }
            .status {
                padding: 12px;
                border-radius: 6px;
                margin: 10px 0;
            }
            .success { background: #d4edda; color: #155724; }
            .error { background: #f8d7da; color: #721c24; }
            .info { background: #d1ecf1; color: #0c5460; }
            #response {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 6px;
                margin-top: 20px;
                overflow-x: auto;
            }
            .results-table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                background: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border-radius: 6px;
                overflow: hidden;
            }
            .results-table th {
                background: #667eea;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: 600;
                border-bottom: 2px solid #5568d3;
            }
            .results-table td {
                padding: 10px 12px;
                border-bottom: 1px solid #e0e0e0;
            }
            .results-table tr:hover {
                background: #f0f0f0;
            }
            .results-table tbody tr:nth-child(even) {
                background: #f9f9f9;
            }
            .sql-code {
                background: #2d2d2d;
                color: #f8f8f2;
                padding: 15px;
                border-radius: 6px;
                font-family: 'Courier New', monospace;
                overflow-x: auto;
                margin: 10px 0;
            }
            .analysis-box {
                background: white;
                border-left: 4px solid #667eea;
                padding: 15px;
                margin: 15px 0;
                border-radius: 4px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .tab-buttons {
                display: flex;
                gap: 10px;
                margin: 15px 0;
                flex-wrap: wrap;
            }
            .tab-btn {
                padding: 10px 20px;
                border: none;
                background: #e0e0e0;
                cursor: pointer;
                border-radius: 6px;
                transition: all 0.3s;
                font-weight: 500;
            }
            .tab-btn:hover {
                background: #d0d0d0;
            }
            .tab-btn.active {
                background: #667eea;
                color: white;
            }
            .tab-content {
                display: none;
            }
            .tab-content.active {
                display: block;
                animation: fadeIn 0.3s;
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            .stats-box {
                display: flex;
                gap: 15px;
                margin: 15px 0;
                flex-wrap: wrap;
            }
            .stat-item {
                background: white;
                padding: 20px;
                border-radius: 8px;
                flex: 1;
                min-width: 150px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                text-align: center;
            }
            .stat-label {
                color: #666;
                font-size: 14px;
                margin-bottom: 8px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .stat-value {
                font-size: 32px;
                font-weight: bold;
                color: #667eea;
            }
            .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
            @media (max-width: 768px) { 
                .grid { grid-template-columns: 1fr; }
                .stats-box { flex-direction: column; }
                .tab-buttons { flex-direction: column; }
            }
        </style>
    </head>
    <body class="gradient-bg min-h-screen flex items-center justify-center p-4 md:p-8">
        <div class="w-full max-w-7xl bg-white rounded-2xl shadow-2xl p-6 md:p-10">
            <!-- Header -->
            <div class="mb-8">
                <h1 class="text-4xl md:text-5xl font-bold text-primary mb-2">
                    🤖 myquery
                </h1>
                <p class="text-gray-600 text-lg">
                    AI-powered database query assistant
                </p>
            </div>
            
            <!-- Connection Section -->
            <div class="mb-8">
                <h2 class="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                    <span>📊</span> Connect to Database
                </h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="space-y-3">
                        <input 
                            type="text" 
                            id="dbType" 
                            placeholder="Database Type (postgresql, mysql, sqlite)" 
                            value="sqlite"
                            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-primary focus:outline-none transition"
                        >
                        <input 
                            type="text" 
                            id="dbName" 
                            placeholder="Database Name" 
                            value="test.db"
                            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-primary focus:outline-none transition"
                        >
                    </div>
                    <div class="space-y-3">
                        <input 
                            type="text" 
                            id="dbHost" 
                            placeholder="Host (optional)" 
                            value="localhost"
                            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-primary focus:outline-none transition"
                        >
                        <input 
                            type="text" 
                            id="dbUser" 
                            placeholder="Username (optional)"
                            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-primary focus:outline-none transition"
                        >
                        <input 
                            type="password" 
                            id="dbPassword" 
                            placeholder="Password (optional)"
                            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-primary focus:outline-none transition"
                        >
                    </div>
                </div>
                <button 
                    onclick="connect()" 
                    class="mt-4 bg-primary hover:bg-primary-dark text-white font-semibold px-6 py-3 rounded-lg transition duration-200 shadow-md hover:shadow-lg"
                >
                    🔌 Connect
                </button>
                <div id="connectStatus" class="mt-4"></div>
            </div>
            
            <!-- Query Section -->
            <div class="mb-8">
                <h2 class="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                    <span>💬</span> Ask a Question
                </h2>
                <textarea 
                    id="query" 
                    rows="4" 
                    class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-primary focus:outline-none transition resize-none"
                    placeholder="Enter your question in natural language... (Examples: Show me all tables | List top 10 records from users | What is the total count of orders)"
                ></textarea>
                <div class="flex flex-wrap gap-3 mt-4">
                    <button 
                        onclick="executeQuery()" 
                        class="bg-primary hover:bg-primary-dark text-white font-semibold px-6 py-3 rounded-lg transition duration-200 shadow-md hover:shadow-lg flex items-center gap-2"
                    >
                        <span>▶️</span> Execute Query
                    </button>
                    <button 
                        onclick="getTables()" 
                        class="bg-green-500 hover:bg-green-600 text-white font-semibold px-6 py-3 rounded-lg transition duration-200 shadow-md hover:shadow-lg flex items-center gap-2"
                    >
                        <span>📋</span> Show Tables
                    </button>
                    <button 
                        onclick="clearResponse()" 
                        class="bg-gray-500 hover:bg-gray-600 text-white font-semibold px-6 py-3 rounded-lg transition duration-200 shadow-md hover:shadow-lg flex items-center gap-2"
                    >
                        <span>🗑️</span> Clear
                    </button>
                </div>
                <div id="response" class="mt-6"></div>
            </div>
            
            <!-- Features Section -->
            <div class="mb-8">
                <h2 class="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                    <span>📚</span> Features
                </h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="bg-gradient-to-br from-purple-50 to-blue-50 p-6 rounded-xl shadow-md hover:shadow-lg transition">
                        <h3 class="text-xl font-bold text-primary mb-2 flex items-center gap-2">
                            <span>🎯</span> Natural Language
                        </h3>
                        <p class="text-gray-600">Ask questions in plain English and get SQL results automatically.</p>
                    </div>
                    <div class="bg-gradient-to-br from-blue-50 to-cyan-50 p-6 rounded-xl shadow-md hover:shadow-lg transition">
                        <h3 class="text-xl font-bold text-primary mb-2 flex items-center gap-2">
                            <span>📊</span> Table View
                        </h3>
                        <p class="text-gray-600">Beautiful table formatting with interactive tabs for SQL, analysis, and raw data.</p>
                    </div>
                    <div class="bg-gradient-to-br from-cyan-50 to-teal-50 p-6 rounded-xl shadow-md hover:shadow-lg transition">
                        <h3 class="text-xl font-bold text-primary mb-2 flex items-center gap-2">
                            <span>🤖</span> AI Analysis
                        </h3>
                        <p class="text-gray-600">Get intelligent insights and summaries from your query results.</p>
                    </div>
                    <div class="bg-gradient-to-br from-teal-50 to-green-50 p-6 rounded-xl shadow-md hover:shadow-lg transition">
                        <h3 class="text-xl font-bold text-primary mb-2 flex items-center gap-2">
                            <span>🔌</span> Multi-DB
                        </h3>
                        <p class="text-gray-600">Connect to PostgreSQL, MySQL, or SQLite databases.</p>
                    </div>
                </div>
                
                <!-- API Endpoints -->
                <details class="mt-6 bg-gray-50 p-4 rounded-lg">
                    <summary class="cursor-pointer font-bold text-primary text-lg hover:text-primary-dark">
                        🔗 API Endpoints
                    </summary>
                    <ul class="mt-4 space-y-2 text-gray-700">
                        <li class="flex items-start gap-2">
                            <span class="text-primary">🔹</span>
                            <code class="bg-gray-200 px-2 py-1 rounded text-sm">POST /api/connect</code>
                            <span class="text-gray-600">- Connect to database</span>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-primary">🔹</span>
                            <code class="bg-gray-200 px-2 py-1 rounded text-sm">POST /api/query</code>
                            <span class="text-gray-600">- Execute natural language query</span>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-primary">🔹</span>
                            <code class="bg-gray-200 px-2 py-1 rounded text-sm">POST /api/sql</code>
                            <span class="text-gray-600">- Execute raw SQL</span>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-primary">🔹</span>
                            <code class="bg-gray-200 px-2 py-1 rounded text-sm">GET /api/schema</code>
                            <span class="text-gray-600">- Get database schema</span>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-primary">🔹</span>
                            <code class="bg-gray-200 px-2 py-1 rounded text-sm">GET /api/tables</code>
                            <span class="text-gray-600">- List tables</span>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-primary">🔹</span>
                            <code class="bg-gray-200 px-2 py-1 rounded text-sm">WS /ws/chat</code>
                            <span class="text-gray-600">- WebSocket chat</span>
                        </li>
                    </ul>
                </details>
            </div>
            
            <!-- Footer -->
            <div class="text-center text-gray-500 text-sm mt-8 pt-6 border-t border-gray-200">
                <p>Built with ❤️ using <span class="font-semibold text-primary">myquery</span></p>
                <p class="mt-1">FastAPI • OpenAI • LangChain • Tailwind CSS</p>
            </div>
        </div>
        
        <script>
            // Utility functions
            function clearResponse() {
                document.getElementById('response').innerHTML = '';
                document.getElementById('query').value = '';
            }
            
            function escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }
            
            // Connection function
            async function connect() {
                const status = document.getElementById('connectStatus');
                status.innerHTML = '<div class="bg-blue-100 border-l-4 border-blue-500 text-blue-700 p-4 rounded">⏳ Connecting...</div>';
                
                try {
                    const response = await fetch('/api/connect', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            db_type: document.getElementById('dbType').value,
                            db_name: document.getElementById('dbName').value,
                            db_host: document.getElementById('dbHost').value || null,
                            db_user: document.getElementById('dbUser').value || null,
                            db_password: document.getElementById('dbPassword').value || null,
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        status.innerHTML = `<div class="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 rounded">✅ ${data.message}<br>Found ${data.table_count} table(s)</div>`;
                    } else {
                        status.innerHTML = `<div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded">❌ ${data.message}</div>`;
                    }
                } catch (error) {
                    status.innerHTML = `<div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded">❌ Error: ${error.message}</div>`;
                }
            }
            
            async function executeQuery() {
                const query = document.getElementById('query').value;
                const response_div = document.getElementById('response');
                response_div.innerHTML = '<div class="bg-blue-100 border-l-4 border-blue-500 text-blue-700 p-4 rounded">⏳ Processing query...</div>';
                
                try {
                    const response = await fetch('/api/query', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ prompt: query, debug: true })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        response_div.innerHTML = formatQueryResponse(data);
                    } else {
                        response_div.innerHTML = `<div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded">❌ Error: ${data.detail}</div>`;
                    }
                } catch (error) {
                    response_div.innerHTML = `<div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded">❌ Error: ${error.message}</div>`;
                }
            }
            
            function formatQueryResponse(data) {
                const result = data.result;
                const rowCount = result.row_count || 0;
                const columns = result.columns || [];
                const rows = result.data || [];
                
                let html = '';
                
                // Stats
                html += '<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">';
                html += '<div class="bg-white p-6 rounded-xl shadow-md text-center border-t-4 border-primary">';
                html += '<div class="text-gray-600 text-sm font-semibold uppercase tracking-wide mb-2">Rows Returned</div>';
                html += '<div class="text-4xl font-bold text-primary">' + rowCount + '</div>';
                html += '</div>';
                html += '<div class="bg-white p-6 rounded-xl shadow-md text-center border-t-4 border-blue-500">';
                html += '<div class="text-gray-600 text-sm font-semibold uppercase tracking-wide mb-2">Columns</div>';
                html += '<div class="text-4xl font-bold text-blue-500">' + columns.length + '</div>';
                html += '</div>';
                html += '<div class="bg-white p-6 rounded-xl shadow-md text-center border-t-4 border-green-500">';
                html += '<div class="text-gray-600 text-sm font-semibold uppercase tracking-wide mb-2">Status</div>';
                html += '<div class="text-4xl">✅</div>';
                html += '</div>';
                html += '</div>';
                
                // Tabs
                html += '<div class="flex flex-wrap gap-2 mb-4">';
                html += '<button class="tab-btn active bg-primary text-white px-6 py-3 rounded-lg font-semibold transition shadow-md hover:bg-primary-dark" onclick="showTab(' + "'table'" + ')">📊 Table View</button>';
                html += '<button class="tab-btn bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-semibold transition shadow-md hover:bg-gray-300" onclick="showTab(' + "'sql'" + ')">💻 SQL Query</button>';
                html += '<button class="tab-btn bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-semibold transition shadow-md hover:bg-gray-300" onclick="showTab(' + "'analysis'" + ')">💡 AI Analysis</button>';
                html += '<button class="tab-btn bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-semibold transition shadow-md hover:bg-gray-300" onclick="showTab(' + "'json'" + ')">📋 Raw JSON</button>';
                html += '</div>';
                
                // Table View
                html += '<div id="tab-table" class="tab-content active">';
                if (rows.length > 0) {
                    html += '<div class="overflow-x-auto rounded-lg shadow-lg">';
                    html += '<table class="min-w-full bg-white">';
                    html += '<thead class="bg-primary text-white"><tr>';
                    columns.forEach(col => {
                        html += '<th class="px-6 py-3 text-left text-sm font-semibold">' + escapeHtml(col) + '</th>';
                    });
                    html += '</tr></thead><tbody class="divide-y divide-gray-200">';
                    
                    rows.forEach((row, idx) => {
                        html += '<tr class="hover:bg-gray-50 transition">';
                        columns.forEach(col => {
                            const value = row[col];
                            html += '<td class="px-6 py-4 text-sm text-gray-900">' + escapeHtml(String(value !== null && value !== undefined ? value : '')) + '</td>';
                        });
                        html += '</tr>';
                    });
                    
                    html += '</tbody></table></div>';
                    
                    if (result.truncated) {
                        html += '<div class="mt-4 bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 rounded">⚠️ Results truncated. Use LIMIT in your query for more control.</div>';
                    }
                } else {
                    html += '<div class="bg-blue-100 border-l-4 border-blue-500 text-blue-700 p-4 rounded">ℹ️ Query executed successfully but returned no results.</div>';
                }
                html += '</div>';
                
                // SQL View
                html += '<div id="tab-sql" class="tab-content">';
                html += '<div class="bg-gray-900 text-gray-100 p-6 rounded-lg overflow-x-auto shadow-lg">';
                html += '<pre class="font-mono text-sm">' + escapeHtml(data.sql) + '</pre>';
                html += '</div>';
                html += '</div>';
                
                // Analysis View
                html += '<div id="tab-analysis" class="tab-content">';
                html += '<div class="bg-white border-l-4 border-primary p-6 rounded-lg shadow-lg">';
                html += '<h3 class="text-2xl font-bold text-primary mb-4 flex items-center gap-2"><span>🤖</span> AI Analysis</h3>';
                html += '<div class="text-gray-700 leading-relaxed">' + escapeHtml(data.analysis).replace(/\\n/g, '<br>') + '</div>';
                html += '</div>';
                html += '</div>';
                
                // JSON View
                html += '<div id="tab-json" class="tab-content">';
                html += '<div class="bg-gray-50 p-6 rounded-lg overflow-x-auto shadow-lg">';
                html += '<pre class="font-mono text-sm text-gray-800">' + escapeHtml(JSON.stringify(data, null, 2)) + '</pre>';
                html += '</div>';
                html += '</div>';
                
                return html;
            }
            
            // Tab switching function
            function showTab(tabName) {
                // Hide all tabs
                document.querySelectorAll('.tab-content').forEach(tab => {
                    tab.classList.remove('active');
                });
                document.querySelectorAll('.tab-btn').forEach(btn => {
                    btn.classList.remove('active');
                    btn.classList.remove('bg-primary', 'text-white', 'hover:bg-primary-dark');
                    btn.classList.add('bg-gray-200', 'text-gray-700', 'hover:bg-gray-300');
                });
                
                // Show selected tab
                document.getElementById('tab-' + tabName).classList.add('active');
                event.target.classList.add('active', 'bg-primary', 'text-white', 'hover:bg-primary-dark');
                event.target.classList.remove('bg-gray-200', 'text-gray-700', 'hover:bg-gray-300');
            }
            
            // Get tables function
            async function getTables() {
                const response_div = document.getElementById('response');
                
                try {
                    const response = await fetch('/api/tables');
                    const data = await response.json();
                    
                    let html = '<h3 class="text-2xl font-bold text-primary mb-4 flex items-center gap-2"><span>📋</span> Available Tables</h3>';
                    html += '<div class="overflow-x-auto rounded-lg shadow-lg">';
                    html += '<table class="min-w-full bg-white">';
                    html += '<thead class="bg-primary text-white"><tr>';
                    html += '<th class="px-6 py-3 text-left text-sm font-semibold">#</th>';
                    html += '<th class="px-6 py-3 text-left text-sm font-semibold">Table Name</th>';
                    html += '</tr></thead><tbody class="divide-y divide-gray-200">';
                    
                    data.tables.forEach((table, index) => {
                        html += '<tr class="hover:bg-gray-50 transition">';
                        html += '<td class="px-6 py-4 text-sm text-gray-500">' + (index + 1) + '</td>';
                        html += '<td class="px-6 py-4 text-sm font-semibold text-gray-900">' + escapeHtml(table) + '</td>';
                        html += '</tr>';
                    });
                    
                    html += '</tbody></table></div>';
                    html += '<div class="mt-4 bg-green-100 border-l-4 border-green-500 text-green-700 p-4 rounded">✅ Found ' + data.tables.length + ' table(s)</div>';
                    
                    response_div.innerHTML = html;
                } catch (error) {
                    response_div.innerHTML = `<div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded">❌ Error: ${error.message}</div>`;
                }
            }
        </script>
    </body>
    </html>
    """


def start_web_server(host: str = "0.0.0.0", port: int = 8000):
    """Start the web server."""
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_web_server()

