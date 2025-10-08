"""Data visualization tool for myquery."""
from typing import Optional, Type, List, Dict, Any
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from config.logging import get_logger
import json
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import tempfile

logger = get_logger(__name__)


class VisualizeDataInput(BaseModel):
    """Input schema for VisualizeDataTool."""
    model_config = {"protected_namespaces": ()}
    
    query_result_json: str = Field(description="JSON string containing query results")
    chart_type: Optional[str] = Field(
        default="auto",
        description="Chart type: auto, bar, line, scatter, pie, table"
    )
    x_column: Optional[str] = Field(
        default=None,
        description="Column for X axis (auto-detected if not provided)"
    )
    y_column: Optional[str] = Field(
        default=None,
        description="Column for Y axis (auto-detected if not provided)"
    )
    title: Optional[str] = Field(
        default="Data Visualization",
        description="Chart title"
    )


class VisualizeDataTool(BaseTool):
    """Tool for visualizing query results."""
    
    name: str = "visualize_data"
    description: str = """
    Visualize query results as charts and graphs.
    Supports bar charts, line charts, scatter plots, pie charts, and tables.
    Auto-detects the best chart type based on data if not specified.
    Use this tool to create visual representations of data.
    """
    args_schema: Type[BaseModel] = VisualizeDataInput
    
    output_dir: str = "outputs/visualizations"
    
    def __init__(self, **kwargs):
        """Initialize with output directory."""
        super().__init__(**kwargs)
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    
    def _run(
        self,
        query_result_json: str,
        chart_type: str = "auto",
        x_column: Optional[str] = None,
        y_column: Optional[str] = None,
        title: str = "Data Visualization",
    ) -> str:
        """
        Visualize query results.
        
        Args:
            query_result_json: JSON string with query results
            chart_type: Type of chart to create
            x_column: Column for X axis
            y_column: Column for Y axis
            title: Chart title
            
        Returns:
            Path to generated visualization file
        """
        try:
            logger.info(f"Creating visualization: {chart_type}")
            
            result_data = json.loads(query_result_json)
            
            # Check if query was successful
            if not result_data.get("success", False):
                return "❌ Cannot visualize: query execution failed"
            
            data = result_data.get("data", [])
            columns = result_data.get("columns", [])
            
            if not data:
                return "ℹ️  No data to visualize"
            
            # Auto-detect chart type if needed
            if chart_type == "auto":
                chart_type = self._detect_chart_type(data, columns)
            
            # Auto-detect columns if not provided
            if not x_column or not y_column:
                x_column, y_column = self._detect_columns(data, columns, chart_type)
            
            # Create visualization
            fig = self._create_chart(
                data=data,
                chart_type=chart_type,
                x_column=x_column,
                y_column=y_column,
                title=title,
            )
            
            # Save to file
            output_path = Path(self.output_dir) / f"chart_{hash(str(data))}.html"
            fig.write_html(str(output_path))
            
            logger.info(f"✅ Visualization created: {output_path}")
            
            # Also try to open in browser (non-blocking)
            try:
                fig.show()
            except:
                pass
            
            return f"✅ Visualization created: {output_path}\n\n📊 Chart type: {chart_type}\n📈 Data points: {len(data)}"
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid result JSON: {str(e)}")
            return f"❌ Invalid result JSON: {str(e)}"
        except Exception as e:
            logger.error(f"Visualization failed: {str(e)}")
            return f"❌ Failed to create visualization: {str(e)}"
    
    async def _arun(self, *args, **kwargs) -> str:
        """Async version (not implemented)."""
        return self._run(*args, **kwargs)
    
    def _detect_chart_type(self, data: List[Dict], columns: List[str]) -> str:
        """Auto-detect best chart type for the data."""
        if len(columns) <= 1:
            return "table"
        
        # Check if first column looks like categories
        first_col = columns[0]
        sample_values = [row.get(first_col) for row in data[:5]]
        
        # If numeric data in both columns, use scatter
        if len(columns) >= 2:
            try:
                float(sample_values[0])
                return "scatter"
            except:
                pass
        
        # If many unique values, use bar chart
        if len(set(str(v) for v in sample_values)) == len(sample_values):
            return "bar"
        
        # If few unique values, use pie chart
        if len(set(str(v) for v in sample_values)) <= 5:
            return "pie"
        
        # Default to bar
        return "bar"
    
    def _detect_columns(
        self,
        data: List[Dict],
        columns: List[str],
        chart_type: str,
    ) -> tuple:
        """Auto-detect X and Y columns."""
        if len(columns) == 0:
            return None, None
        
        if len(columns) == 1:
            return columns[0], columns[0]
        
        # For most charts, first column is X, second is Y
        x_col = columns[0]
        y_col = columns[1] if len(columns) > 1 else columns[0]
        
        # Try to find numeric column for Y axis
        for col in columns[1:]:
            sample_val = data[0].get(col) if data else None
            try:
                float(sample_val)
                y_col = col
                break
            except:
                continue
        
        return x_col, y_col
    
    def _create_chart(
        self,
        data: List[Dict],
        chart_type: str,
        x_column: Optional[str],
        y_column: Optional[str],
        title: str,
    ) -> go.Figure:
        """Create chart based on type."""
        
        if chart_type == "bar":
            return self._create_bar_chart(data, x_column, y_column, title)
        elif chart_type == "line":
            return self._create_line_chart(data, x_column, y_column, title)
        elif chart_type == "scatter":
            return self._create_scatter_chart(data, x_column, y_column, title)
        elif chart_type == "pie":
            return self._create_pie_chart(data, x_column, y_column, title)
        elif chart_type == "table":
            return self._create_table(data, title)
        else:
            # Default to bar
            return self._create_bar_chart(data, x_column, y_column, title)
    
    def _create_bar_chart(
        self,
        data: List[Dict],
        x_column: str,
        y_column: str,
        title: str,
    ) -> go.Figure:
        """Create bar chart."""
        x_values = [row.get(x_column) for row in data]
        y_values = [row.get(y_column) for row in data]
        
        fig = go.Figure(data=[
            go.Bar(x=x_values, y=y_values)
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title=x_column,
            yaxis_title=y_column,
            template="plotly_white",
        )
        
        return fig
    
    def _create_line_chart(
        self,
        data: List[Dict],
        x_column: str,
        y_column: str,
        title: str,
    ) -> go.Figure:
        """Create line chart."""
        x_values = [row.get(x_column) for row in data]
        y_values = [row.get(y_column) for row in data]
        
        fig = go.Figure(data=[
            go.Scatter(x=x_values, y=y_values, mode='lines+markers')
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title=x_column,
            yaxis_title=y_column,
            template="plotly_white",
        )
        
        return fig
    
    def _create_scatter_chart(
        self,
        data: List[Dict],
        x_column: str,
        y_column: str,
        title: str,
    ) -> go.Figure:
        """Create scatter plot."""
        x_values = [row.get(x_column) for row in data]
        y_values = [row.get(y_column) for row in data]
        
        fig = go.Figure(data=[
            go.Scatter(x=x_values, y=y_values, mode='markers')
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title=x_column,
            yaxis_title=y_column,
            template="plotly_white",
        )
        
        return fig
    
    def _create_pie_chart(
        self,
        data: List[Dict],
        x_column: str,
        y_column: str,
        title: str,
    ) -> go.Figure:
        """Create pie chart."""
        labels = [str(row.get(x_column)) for row in data]
        values = [row.get(y_column) for row in data]
        
        fig = go.Figure(data=[
            go.Pie(labels=labels, values=values)
        ])
        
        fig.update_layout(
            title=title,
            template="plotly_white",
        )
        
        return fig
    
    def _create_table(self, data: List[Dict], title: str) -> go.Figure:
        """Create interactive table."""
        if not data:
            return go.Figure()
        
        columns = list(data[0].keys())
        
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=columns,
                fill_color='paleturquoise',
                align='left'
            ),
            cells=dict(
                values=[[row.get(col) for row in data] for col in columns],
                fill_color='lavender',
                align='left'
            )
        )])
        
        fig.update_layout(title=title)
        
        return fig

