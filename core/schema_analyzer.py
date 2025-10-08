"""Schema analysis utilities for myquery."""
from typing import Dict, List, Any, Optional
import json


class SchemaAnalyzer:
    """Utility class for analyzing database schemas."""
    
    @staticmethod
    def get_table_summary(schema_data: Dict[str, Any]) -> str:
        """
        Get a concise summary of all tables.
        
        Args:
            schema_data: Schema data dictionary
            
        Returns:
            Formatted table summary
        """
        tables = schema_data.get("tables", {})
        total_tables = schema_data.get("total_tables", 0)
        
        summary_parts = [f"📊 Database contains {total_tables} table(s):\n"]
        
        for table_name, table_info in tables.items():
            columns = table_info.get("columns", [])
            col_count = len(columns)
            
            pk = table_info.get("primary_keys", [])
            fk = table_info.get("foreign_keys", [])
            
            summary = f"  • {table_name}: {col_count} column(s)"
            
            if pk:
                summary += f" | PK: {', '.join(pk)}"
            
            if fk:
                fk_count = len(fk)
                summary += f" | {fk_count} FK(s)"
            
            summary_parts.append(summary)
        
        return "\n".join(summary_parts)
    
    @staticmethod
    def get_column_details(schema_data: Dict[str, Any], table_name: str) -> str:
        """
        Get detailed column information for a specific table.
        
        Args:
            schema_data: Schema data dictionary
            table_name: Name of the table
            
        Returns:
            Formatted column details
        """
        tables = schema_data.get("tables", {})
        
        if table_name not in tables:
            return f"❌ Table '{table_name}' not found in schema."
        
        table_info = tables[table_name]
        columns = table_info.get("columns", [])
        
        details = [f"📋 Columns in '{table_name}':\n"]
        
        for col in columns:
            col_name = col.get("name", "unknown")
            col_type = col.get("type", "unknown")
            nullable = "NULL" if col.get("nullable", True) else "NOT NULL"
            
            details.append(f"  • {col_name}: {col_type} ({nullable})")
        
        return "\n".join(details)
    
    @staticmethod
    def get_relationships(schema_data: Dict[str, Any]) -> str:
        """
        Get all foreign key relationships in the database.
        
        Args:
            schema_data: Schema data dictionary
            
        Returns:
            Formatted relationships
        """
        tables = schema_data.get("tables", {})
        relationships = []
        
        for table_name, table_info in tables.items():
            fks = table_info.get("foreign_keys", [])
            
            for fk in fks:
                source_cols = ", ".join(fk.get("columns", []))
                target_table = fk.get("refers_to_table", "unknown")
                target_cols = ", ".join(fk.get("refers_to_columns", []))
                
                relationships.append(
                    f"  • {table_name}.{source_cols} → {target_table}.{target_cols}"
                )
        
        if not relationships:
            return "ℹ️  No foreign key relationships found."
        
        result = ["🔗 Database Relationships:\n"]
        result.extend(relationships)
        
        return "\n".join(result)
    
    @staticmethod
    def find_related_tables(
        schema_data: Dict[str, Any], 
        table_name: str
    ) -> List[str]:
        """
        Find tables related to a given table through foreign keys.
        
        Args:
            schema_data: Schema data dictionary
            table_name: Name of the table
            
        Returns:
            List of related table names
        """
        tables = schema_data.get("tables", {})
        related_tables = set()
        
        if table_name not in tables:
            return []
        
        # Check foreign keys from this table
        table_info = tables[table_name]
        fks = table_info.get("foreign_keys", [])
        
        for fk in fks:
            target_table = fk.get("refers_to_table")
            if target_table:
                related_tables.add(target_table)
        
        # Check foreign keys to this table
        for other_table, other_info in tables.items():
            if other_table == table_name:
                continue
            
            other_fks = other_info.get("foreign_keys", [])
            for fk in other_fks:
                if fk.get("refers_to_table") == table_name:
                    related_tables.add(other_table)
        
        return list(related_tables)

