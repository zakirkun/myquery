"""Main agent orchestration for myquery."""
from typing import Optional, List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage, HumanMessage
from tools import (
    ConnectDBTool,
    GetSchemaTool,
    AnalyzeSchemaTool,
    GenerateQueryTool,
    ExecuteQueryTool,
    FormatTableTool,
    AnalyzeDataTool,
    VisualizeDataTool,
    MultiDBQueryTool,
    ExportDataTool,
    QueryOptimizationTool,
)
from core.multi_db_manager import MultiDBManager
from config.logging import get_logger
from config.settings import settings

logger = get_logger(__name__)


class QueryAgent:
    """Main agent for orchestrating database query operations."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize QueryAgent.
        
        Args:
            api_key: OpenAI API key (uses settings if not provided)
            model: OpenAI model name (uses settings if not provided)
        """
        self.api_key = api_key or (settings.openai_api_key if settings else None)
        self.model = model or (settings.openai_model if settings else "gpt-4-turbo-preview")
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            api_key=self.api_key,
            model=self.model,
            temperature=0,
        )
        
        # Initialize tools
        self.connect_db_tool = ConnectDBTool()
        self.get_schema_tool = GetSchemaTool()
        self.analyze_schema_tool = AnalyzeSchemaTool()
        self.generate_query_tool = GenerateQueryTool()
        self.execute_query_tool = ExecuteQueryTool()
        self.format_table_tool = FormatTableTool()
        self.analyze_data_tool = AnalyzeDataTool()
        self.visualize_data_tool = VisualizeDataTool()
        self.multi_db_query_tool = MultiDBQueryTool()
        self.export_data_tool = ExportDataTool()
        self.query_optimization_tool = QueryOptimizationTool()
        
        # Multi-DB manager
        self.multi_db_manager = MultiDBManager()
        self.multi_db_query_tool.manager = self.multi_db_manager
        
        # Set LLM for tools that need it
        self.analyze_schema_tool.llm = self.llm
        self.generate_query_tool.llm = self.llm
        self.analyze_data_tool.llm = self.llm
        self.query_optimization_tool.llm = self.llm
        
        # Tool list
        self.tools = [
            self.connect_db_tool,
            self.get_schema_tool,
            self.analyze_schema_tool,
            self.generate_query_tool,
            self.execute_query_tool,
            self.format_table_tool,
            self.analyze_data_tool,
            self.visualize_data_tool,
            self.multi_db_query_tool,
            self.export_data_tool,
            self.query_optimization_tool,
        ]
        
        # Chat history
        self.chat_history: List[Dict[str, str]] = []
        
        logger.info("QueryAgent initialized successfully")
    
    def connect_database(
        self,
        db_type: str,
        db_name: str,
        db_host: Optional[str] = "localhost",
        db_port: Optional[int] = None,
        db_user: Optional[str] = None,
        db_password: Optional[str] = None,
    ) -> str:
        """
        Connect to a database.
        
        Args:
            db_type: Database type (postgresql, mysql, sqlite)
            db_name: Database name or file path
            db_host: Database host
            db_port: Database port
            db_user: Database username
            db_password: Database password
            
        Returns:
            Connection status message
        """
        result = self.connect_db_tool._run(
            db_type=db_type,
            db_name=db_name,
            db_host=db_host,
            db_port=db_port,
            db_user=db_user,
            db_password=db_password,
        )
        
        # Share engine with other tools
        if self.connect_db_tool.is_connected():
            engine = self.connect_db_tool.get_engine()
            self.get_schema_tool.engine = engine
            self.execute_query_tool.engine = engine
        
        return result
    
    def get_schema(self, include_sample_data: bool = False) -> str:
        """
        Get database schema.
        
        Args:
            include_sample_data: Whether to include sample data
            
        Returns:
            Schema information as JSON string
        """
        return self.get_schema_tool._run(include_sample_data=include_sample_data)
    
    def analyze_schema(self) -> str:
        """
        Analyze database schema.
        
        Returns:
            Schema analysis
        """
        schema_json = self.get_schema()
        return self.analyze_schema_tool._run(schema_json=schema_json)
    
    def execute_query_flow(
        self, 
        user_prompt: str, 
        debug: bool = False,
        auto_visualize: bool = True,
        optimize: bool = False
    ) -> Dict[str, Any]:
        """
        Execute complete query flow: generate, execute, format, analyze, visualize, and optimize.
        
        Args:
            user_prompt: User's natural language query
            debug: Enable debug mode
            auto_visualize: Auto-detect and create visualization if requested
            optimize: Show query optimization suggestions
            
        Returns:
            Dictionary with flow results
        """
        results = {
            "user_prompt": user_prompt,
            "sql_query": None,
            "execution_result": None,
            "formatted_output": None,
            "analysis": None,
            "visualization": None,
            "visualization_type": None,
            "optimization": None,
            "error": None,
        }
        
        try:
            # Get schema
            schema_json = self.get_schema()
            
            # Build chat history context
            history_context = self._build_history_context()
            
            # Generate SQL query
            if debug:
                logger.info(f"🔍 User Query: {user_prompt}")
            
            sql_query = self.generate_query_tool._run(
                user_prompt=user_prompt,
                schema_json=schema_json,
                chat_history=history_context,
            )
            
            if sql_query.startswith("❌"):
                results["error"] = sql_query
                return results
            
            results["sql_query"] = sql_query
            
            if debug:
                logger.info(f"🔍 Generated SQL:\n{sql_query}")
            
            # Execute query
            execution_result = self.execute_query_tool._run(sql_query=sql_query)
            results["execution_result"] = execution_result
            
            # Format output
            formatted = self.format_table_tool._run(
                query_result_json=execution_result,
                title=f"Results: {user_prompt[:50]}..."
            )
            results["formatted_output"] = formatted
            
            # Analyze data
            analysis = self.analyze_data_tool._run(
                query_result_json=execution_result,
                user_prompt=user_prompt
            )
            results["analysis"] = analysis
            
            # Auto-detect if visualization is requested
            if auto_visualize:
                viz_type = self._detect_visualization_request(user_prompt)
                if viz_type:
                    try:
                        visualization = self.visualize_data_tool._run(
                            query_result_json=execution_result,
                            chart_type=viz_type,
                            title=user_prompt[:100]
                        )
                        results["visualization"] = visualization
                        results["visualization_type"] = viz_type
                        logger.info(f"📊 Auto-generated {viz_type} chart")
                    except Exception as e:
                        logger.warning(f"Visualization failed: {str(e)}")
            
            # Query optimization suggestions
            if optimize:
                try:
                    schema_json = self.get_schema()
                    optimization = self.query_optimization_tool._run(
                        sql_query=sql_query,
                        schema_json=schema_json
                    )
                    results["optimization"] = optimization
                    logger.info("🔍 Query optimization analysis completed")
                except Exception as e:
                    logger.warning(f"Optimization failed: {str(e)}")
            
            # Add to chat history
            self.chat_history.append({
                "role": "user",
                "content": user_prompt,
            })
            self.chat_history.append({
                "role": "assistant",
                "content": f"SQL: {sql_query}\nAnalysis: {analysis}",
            })
            
            return results
            
        except Exception as e:
            logger.error(f"Query flow failed: {str(e)}")
            results["error"] = str(e)
            return results
    
    def chat(self, user_input: str, debug: bool = False) -> str:
        """
        Handle chat interaction with smart query detection and visualization.
        
        Args:
            user_input: User's input
            debug: Enable debug mode
            
        Returns:
            Agent's response (with embedded visualization info if applicable)
        """
        # Check if this is a query request
        query_keywords = ["show", "list", "get", "find", "select", "count", "sum", "average", "top", 
                         "tampilkan", "cari", "lihat", "berapa", "total"]
        is_query = any(keyword in user_input.lower() for keyword in query_keywords)
        
        if is_query and self.connect_db_tool.is_connected():
            # Execute query flow with auto-visualization
            results = self.execute_query_flow(user_input, debug=debug, auto_visualize=True)
            
            if results.get("error"):
                return results["error"]
            
            # Build response with analysis and visualization info
            response_parts = []
            
            # Add main analysis
            if results.get("analysis"):
                response_parts.append(results["analysis"])
            
            # Add visualization info if created
            if results.get("visualization"):
                viz_msg = f"\n\n📊 **Visualization Created**\n{results['visualization']}"
                response_parts.append(viz_msg)
            
            return "\n".join(response_parts) if response_parts else "Query completed."
        else:
            # Handle general conversation
            return self._general_chat(user_input)
    
    def _general_chat(self, user_input: str) -> str:
        """Handle general conversation."""
        try:
            messages = [
                SystemMessage(content="""You are a helpful database assistant. 
                You help users connect to databases and query them using natural language.
                You can provide guidance on database operations and SQL queries."""),
                HumanMessage(content=user_input),
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Chat failed: {str(e)}")
            return f"❌ Error: {str(e)}"
    
    def _build_history_context(self) -> str:
        """Build chat history context for query generation."""
        if not self.chat_history:
            return ""
        
        # Get last 5 exchanges
        recent_history = self.chat_history[-5:]
        context_parts = []
        
        for msg in recent_history:
            role = msg["role"].capitalize()
            content = msg["content"][:200]  # Truncate long messages
            context_parts.append(f"{role}: {content}")
        
        return "\n".join(context_parts)
    
    def _detect_visualization_request(self, user_prompt: str) -> Optional[str]:
        """
        Detect if user is requesting a visualization and determine chart type.
        
        Args:
            user_prompt: User's query
            
        Returns:
            Chart type or None if no visualization requested
        """
        prompt_lower = user_prompt.lower()
        
        # Chart type keywords
        chart_keywords = {
            "bar": ["bar chart", "bar graph", "barchart", "batang"],
            "line": ["line chart", "line graph", "trend", "time series", "tren", "grafik garis"],
            "pie": ["pie chart", "pie graph", "distribution", "proporsi", "persentase"],
            "scatter": ["scatter", "correlation", "korelasi", "sebaran"],
            "table": ["table", "tabel", "list", "daftar"],
        }
        
        # Generic visualization keywords
        viz_keywords = [
            "chart", "graph", "plot", "visualize", "visualise", "show",
            "grafik", "visualisasi", "tampilkan", "lihat", "display"
        ]
        
        # Check for specific chart types first
        for chart_type, keywords in chart_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                return chart_type
        
        # If generic visualization keywords found, use auto-detection
        if any(keyword in prompt_lower for keyword in viz_keywords):
            # Additional heuristics
            if any(word in prompt_lower for word in ["trend", "over time", "by month", "by year"]):
                return "line"
            elif any(word in prompt_lower for word in ["compare", "comparison", "vs", "versus"]):
                return "bar"
            elif any(word in prompt_lower for word in ["distribution", "share", "percentage"]):
                return "pie"
            else:
                return "auto"  # Let the tool auto-detect
        
        # Default: no visualization unless explicitly requested
        return None
    
    def get_table_list(self) -> List[str]:
        """Get list of tables in the database."""
        return self.get_schema_tool.get_table_names()
    
    def is_connected(self) -> bool:
        """Check if connected to database."""
        return self.connect_db_tool.is_connected()
    
    def clear_history(self) -> None:
        """Clear chat history."""
        self.chat_history = []
        logger.info("Chat history cleared")
    
    def export_results(
        self,
        query_result_json: str,
        format: str = "csv",
        filename: Optional[str] = None,
        output_dir: str = "outputs/exports"
    ) -> str:
        """
        Export query results to file.
        
        Args:
            query_result_json: Query results as JSON string
            format: Export format (csv, json, excel, all)
            filename: Output filename
            output_dir: Output directory
            
        Returns:
            Export status message
        """
        return self.export_data_tool._run(
            query_result_json=query_result_json,
            format=format,
            filename=filename,
            output_dir=output_dir
        )
    
    def optimize_query(self, sql_query: str) -> str:
        """
        Get optimization suggestions for SQL query.
        
        Args:
            sql_query: SQL query to optimize
            
        Returns:
            Optimization suggestions
        """
        schema_json = self.get_schema() if self.is_connected() else None
        return self.query_optimization_tool._run(
            sql_query=sql_query,
            schema_json=schema_json
        )

