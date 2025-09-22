"""
Report generation for data quality analysis results.

This module provides functionality to generate visual and text reports
from data quality check results.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, Any, List
import io
import base64


class ReportGenerator:
    """Generate reports and visualizations from data quality results."""
    
    def __init__(self, results: Dict[str, Any], df: pd.DataFrame):
        """Initialize with quality check results and original DataFrame."""
        self.results = results
        self.df = df
    
    def generate_summary_stats(self) -> Dict[str, Any]:
        """Generate summary statistics for the dashboard."""
        summary = self.results.get('summary', {})
        missing_values = self.results.get('missing_values', {})
        duplicates = self.results.get('duplicates', {})
        schema_issues = self.results.get('schema_issues', {})
        
        # Calculate key metrics
        columns_with_missing = sum(1 for col in missing_values.values() if col['has_missing'])
        total_missing_cells = sum(col['count'] for col in missing_values.values())
        
        return {
            'total_rows': summary.get('total_rows', 0),
            'total_columns': summary.get('total_columns', 0),
            'data_quality_score': summary.get('data_quality_score', 0),
            'columns_with_missing': columns_with_missing,
            'total_missing_cells': total_missing_cells,
            'duplicate_rows': duplicates.get('count', 0),
            'schema_issues_count': len(schema_issues),
            'has_issues': summary.get('total_issues', 0) > 0
        }
    
    def create_missing_values_chart(self) -> go.Figure:
        """Create a bar chart showing missing values by column."""
        missing_values = self.results.get('missing_values', {})
        
        if not missing_values:
            return self._create_empty_chart("No missing value data available")
        
        columns = list(missing_values.keys())
        percentages = [missing_values[col]['percentage'] for col in columns]
        
        fig = go.Figure(data=[
            go.Bar(
                x=columns,
                y=percentages,
                marker_color=['#ff7f7f' if p > 0 else '#90EE90' for p in percentages],
                text=[f"{p}%" for p in percentages],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title="Missing Values by Column (%)",
            xaxis_title="Columns",
            yaxis_title="Missing Percentage (%)",
            height=400,
            showlegend=False
        )
        
        return fig
    
    def create_duplicate_visualization(self) -> go.Figure:
        """Create visualization for duplicate analysis."""
        duplicates = self.results.get('duplicates', {})
        
        if not duplicates.get('has_duplicates'):
            return self._create_empty_chart("No duplicates found")
        
        duplicate_count = duplicates.get('count', 0)
        total_rows = self.results.get('summary', {}).get('total_rows', 1)
        unique_rows = total_rows - duplicate_count
        
        fig = go.Figure(data=[
            go.Pie(
                labels=['Unique Rows', 'Duplicate Rows'],
                values=[unique_rows, duplicate_count],
                marker_colors=['#90EE90', '#ff7f7f']
            )
        ])
        
        fig.update_layout(
            title=f"Duplicate Analysis: {duplicate_count} duplicates found",
            height=400
        )
        
        return fig
    
    def create_data_types_chart(self) -> go.Figure:
        """Create a chart showing data types distribution."""
        data_types = self.df.dtypes.value_counts()
        
        fig = go.Figure(data=[
            go.Bar(
                x=data_types.index.astype(str),
                y=data_types.values,
                marker_color='#87CEEB',
                text=data_types.values,
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title="Data Types Distribution",
            xaxis_title="Data Types",
            yaxis_title="Number of Columns",
            height=400,
            showlegend=False
        )
        
        return fig
    
    def create_schema_issues_chart(self) -> go.Figure:
        """Create visualization for schema issues."""
        schema_issues = self.results.get('schema_issues', {})
        
        if not schema_issues:
            return self._create_empty_chart("No schema issues detected")
        
        columns = list(schema_issues.keys())
        issue_counts = [len(issues) for issues in schema_issues.values()]
        
        fig = go.Figure(data=[
            go.Bar(
                x=columns,
                y=issue_counts,
                marker_color='#ffa500',
                text=issue_counts,
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title="Schema Issues by Column",
            xaxis_title="Columns",
            yaxis_title="Number of Issues",
            height=400,
            showlegend=False
        )
        
        return fig
    
    def create_data_quality_score_gauge(self) -> go.Figure:
        """Create a gauge chart for overall data quality score."""
        score = self.results.get('summary', {}).get('data_quality_score', 0)
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Data Quality Score"},
            delta = {'reference': 100},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=400)
        return fig
    
    def generate_text_report(self) -> str:
        """Generate a text summary report."""
        stats = self.generate_summary_stats()
        missing_values = self.results.get('missing_values', {})
        duplicates = self.results.get('duplicates', {})
        schema_issues = self.results.get('schema_issues', {})
        
        report = []
        report.append("=" * 50)
        report.append("DATA QUALITY ANALYSIS REPORT")
        report.append("=" * 50)
        report.append("")
        
        # Summary
        report.append("SUMMARY:")
        report.append(f"  Total Rows: {stats['total_rows']:,}")
        report.append(f"  Total Columns: {stats['total_columns']}")
        report.append(f"  Data Quality Score: {stats['data_quality_score']}/100")
        report.append("")
        
        # Missing Values
        if stats['columns_with_missing'] > 0:
            report.append("MISSING VALUES:")
            for col, data in missing_values.items():
                if data['has_missing']:
                    report.append(f"  {col}: {data['count']} missing ({data['percentage']}%)")
            report.append("")
        
        # Duplicates
        if stats['duplicate_rows'] > 0:
            report.append("DUPLICATES:")
            report.append(f"  {stats['duplicate_rows']} duplicate rows found")
            report.append("")
        
        # Schema Issues
        if stats['schema_issues_count'] > 0:
            report.append("SCHEMA ISSUES:")
            for col, issues in schema_issues.items():
                report.append(f"  {col}:")
                for issue_type, details in issues.items():
                    report.append(f"    - {issue_type}: {details}")
            report.append("")
        
        # Recommendations
        report.append("RECOMMENDATIONS:")
        if stats['data_quality_score'] < 70:
            report.append("  WARNING: Data quality is poor. Immediate attention required.")
        elif stats['data_quality_score'] < 90:
            report.append("  WARNING: Data quality is fair. Consider addressing identified issues.")
        else:
            report.append("  SUCCESS: Data quality is good. Minor improvements recommended.")
        
        if stats['columns_with_missing'] > 0:
            report.append("  - Address missing values in affected columns")
        if stats['duplicate_rows'] > 0:
            report.append("  - Remove or investigate duplicate rows")
        if stats['schema_issues_count'] > 0:
            report.append("  - Standardize data formats in affected columns")
        
        return "\n".join(report)
    
    def _create_empty_chart(self, message: str) -> go.Figure:
        """Create an empty chart with a message."""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font_size=16
        )
        fig.update_layout(
            height=400,
            xaxis={'visible': False},
            yaxis={'visible': False}
        )
        return fig
    
    def get_issue_summary_table(self) -> pd.DataFrame:
        """Create a summary table of all issues found."""
        issues = []
        
        # Missing value issues
        missing_values = self.results.get('missing_values', {})
        for col, data in missing_values.items():
            if data['has_missing']:
                issues.append({
                    'Type': 'Missing Values',
                    'Column': col,
                    'Severity': 'High' if data['percentage'] > 10 else 'Medium',
                    'Details': f"{data['count']} missing ({data['percentage']}%)"
                })
        
        # Duplicate issues
        duplicates = self.results.get('duplicates', {})
        if duplicates.get('has_duplicates'):
            issues.append({
                'Type': 'Duplicates',
                'Column': 'All',
                'Severity': 'Medium',
                'Details': f"{duplicates['count']} duplicate rows"
            })
        
        # Schema issues
        schema_issues = self.results.get('schema_issues', {})
        for col, col_issues in schema_issues.items():
            for issue_type, details in col_issues.items():
                severity = 'High' if 'mixed_types' in issue_type else 'Medium'
                issues.append({
                    'Type': f'Schema Issue: {issue_type}',
                    'Column': col,
                    'Severity': severity,
                    'Details': str(details)
                })
        
        return pd.DataFrame(issues)
