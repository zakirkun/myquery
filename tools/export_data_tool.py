"""Data export tool for myquery - CSV, JSON, Excel support."""
from typing import Optional, Type, List
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from config.logging import get_logger
import json
import csv
from pathlib import Path
from datetime import datetime
import pandas as pd

logger = get_logger(__name__)


class ExportDataInput(BaseModel):
    """Input schema for ExportDataTool."""
    query_result_json: str = Field(description="JSON string containing query results")
    format: str = Field(
        default="csv",
        description="Export format: csv, json, excel, or all"
    )
    filename: Optional[str] = Field(
        default=None,
        description="Output filename (without extension, auto-generated if not provided)"
    )
    output_dir: Optional[str] = Field(
        default="outputs/exports",
        description="Output directory path"
    )


class ExportDataTool(BaseTool):
    """Tool for exporting query results to various formats."""
    
    name: str = "export_data"
    description: str = """
    Export query results to CSV, JSON, or Excel format.
    Supports single format or exporting to all formats at once.
    Files are saved to outputs/exports/ directory by default.
    Use this tool when users want to save or export query results.
    """
    args_schema: Type[BaseModel] = ExportDataInput
    
    def _run(
        self,
        query_result_json: str,
        format: str = "csv",
        filename: Optional[str] = None,
        output_dir: str = "outputs/exports",
    ) -> str:
        """
        Export query results to file(s).
        
        Args:
            query_result_json: JSON string with query results
            format: Export format (csv, json, excel, all)
            filename: Output filename without extension
            output_dir: Output directory
            
        Returns:
            Success message with file paths
        """
        try:
            logger.info(f"Exporting data to {format} format...")
            
            # Parse result data
            result_data = json.loads(query_result_json)
            
            # Check if query was successful
            if not result_data.get("success", False):
                return "❌ Cannot export: query execution failed"
            
            data = result_data.get("data", [])
            columns = result_data.get("columns", [])
            
            if not data:
                return "ℹ️  No data to export"
            
            # Create output directory
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"query_export_{timestamp}"
            
            # Export based on format
            exported_files = []
            
            if format.lower() in ["csv", "all"]:
                csv_file = self._export_csv(data, columns, output_path, filename)
                exported_files.append(csv_file)
            
            if format.lower() in ["json", "all"]:
                json_file = self._export_json(data, columns, output_path, filename)
                exported_files.append(json_file)
            
            if format.lower() in ["excel", "xlsx", "all"]:
                excel_file = self._export_excel(data, columns, output_path, filename)
                exported_files.append(excel_file)
            
            if not exported_files:
                return f"❌ Invalid format: {format}. Use csv, json, excel, or all"
            
            # Build success message
            row_count = len(data)
            col_count = len(columns)
            
            result_msg = f"✅ Data exported successfully!\n\n"
            result_msg += f"📊 Records: {row_count} rows × {col_count} columns\n\n"
            result_msg += f"📁 Exported files:\n"
            
            for file_path in exported_files:
                file_size = Path(file_path).stat().st_size
                size_kb = file_size / 1024
                result_msg += f"  • {file_path} ({size_kb:.1f} KB)\n"
            
            logger.info(f"✅ Exported {len(exported_files)} file(s)")
            return result_msg
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid result JSON: {str(e)}")
            return f"❌ Invalid result JSON: {str(e)}"
        except Exception as e:
            logger.error(f"Export failed: {str(e)}")
            return f"❌ Failed to export data: {str(e)}"
    
    async def _arun(self, *args, **kwargs) -> str:
        """Async version (not implemented)."""
        return self._run(*args, **kwargs)
    
    def _export_csv(
        self,
        data: List[dict],
        columns: List[str],
        output_path: Path,
        filename: str
    ) -> str:
        """Export data to CSV format."""
        csv_path = output_path / f"{filename}.csv"
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            if not data:
                return str(csv_path)
            
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data)
        
        logger.info(f"CSV exported: {csv_path}")
        return str(csv_path)
    
    def _export_json(
        self,
        data: List[dict],
        columns: List[str],
        output_path: Path,
        filename: str
    ) -> str:
        """Export data to JSON format."""
        json_path = output_path / f"{filename}.json"
        
        export_data = {
            "metadata": {
                "exported_at": datetime.now().isoformat(),
                "row_count": len(data),
                "columns": columns,
            },
            "data": data
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        logger.info(f"JSON exported: {json_path}")
        return str(json_path)
    
    def _export_excel(
        self,
        data: List[dict],
        columns: List[str],
        output_path: Path,
        filename: str
    ) -> str:
        """Export data to Excel format."""
        excel_path = output_path / f"{filename}.xlsx"
        
        # Create DataFrame
        df = pd.DataFrame(data, columns=columns)
        
        # Export to Excel with formatting
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Query Results', index=False)
            
            # Get workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets['Query Results']
            
            # Auto-adjust column widths
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(str(col))
                )
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[chr(65 + idx)].width = adjusted_width
        
        logger.info(f"Excel exported: {excel_path}")
        return str(excel_path)


class QuickExportMixin:
    """Mixin for quick export functionality."""
    
    @staticmethod
    def quick_export(
        data: List[dict],
        format: str = "csv",
        filename: Optional[str] = None
    ) -> str:
        """Quick export without tool wrapper."""
        export_tool = ExportDataTool()
        
        # Prepare result JSON
        result_json = json.dumps({
            "success": True,
            "data": data,
            "columns": list(data[0].keys()) if data else [],
            "row_count": len(data)
        })
        
        return export_tool._run(
            query_result_json=result_json,
            format=format,
            filename=filename
        )

