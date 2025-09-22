"""
Core data quality checks for CSV files.

This module provides functions to detect common data quality issues
including missing values, duplicates, and schema inconsistencies.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
import re
from datetime import datetime


class DataQualityChecker:
    """Main class for performing data quality checks on CSV files."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with a pandas DataFrame."""
        self.df = df
        self.results = {}
        
    def check_missing_values(self) -> Dict[str, Any]:
        """
        Check for missing values in each column.
        
        Returns:
            Dict containing missing value statistics per column
        """
        missing_stats = {}
        total_rows = len(self.df)
        
        for column in self.df.columns:
            missing_count = self.df[column].isnull().sum()
            missing_percentage = (missing_count / total_rows) * 100
            
            missing_stats[column] = {
                'count': int(missing_count),
                'percentage': round(missing_percentage, 2),
                'has_missing': missing_count > 0
            }
            
        self.results['missing_values'] = missing_stats
        return missing_stats
    
    def check_duplicates(self) -> Dict[str, Any]:
        """
        Check for duplicate rows in the dataset.
        
        Returns:
            Dict containing duplicate row statistics
        """
        duplicate_count = self.df.duplicated().sum()
        total_rows = len(self.df)
        duplicate_percentage = (duplicate_count / total_rows) * 100
        
        duplicate_stats = {
            'count': int(duplicate_count),
            'percentage': round(duplicate_percentage, 2),
            'has_duplicates': duplicate_count > 0,
            'duplicate_rows': self.df[self.df.duplicated(keep=False)].index.tolist() if duplicate_count > 0 else []
        }
        
        self.results['duplicates'] = duplicate_stats
        return duplicate_stats
    
    def check_schema_validation(self) -> Dict[str, Any]:
        """
        Check for schema inconsistencies in each column.
        
        Returns:
            Dict containing schema validation results per column
        """
        schema_issues = {}
        
        for column in self.df.columns:
            column_data = self.df[column].dropna()
            if len(column_data) == 0:
                continue
                
            issues = self._detect_column_issues(column, column_data)
            if issues:
                schema_issues[column] = issues
                
        self.results['schema_issues'] = schema_issues
        return schema_issues
    
    def _detect_column_issues(self, column_name: str, column_data: pd.Series) -> Dict[str, Any]:
        """
        Detect specific issues in a column.
        
        Args:
            column_name: Name of the column
            column_data: Non-null data in the column
            
        Returns:
            Dict containing detected issues
        """
        issues = {}
        
        # Check for mixed data types
        data_types = set(type(val).__name__ for val in column_data)
        if len(data_types) > 1:
            issues['mixed_types'] = {
                'detected_types': list(data_types),
                'count': len(column_data)
            }
        
        # Check for date format inconsistencies
        if self._looks_like_date_column(column_name, column_data):
            date_issues = self._check_date_formats(column_data)
            if date_issues:
                issues['date_formats'] = date_issues
        
        # Check for numeric inconsistencies
        if self._looks_like_numeric_column(column_name, column_data):
            numeric_issues = self._check_numeric_consistency(column_data)
            if numeric_issues:
                issues['numeric_issues'] = numeric_issues
        
        # Check for string inconsistencies (length, patterns)
        if column_data.dtype == 'object':
            string_issues = self._check_string_consistency(column_data)
            if string_issues:
                issues['string_issues'] = string_issues
        
        return issues
    
    def _looks_like_date_column(self, column_name: str, column_data: pd.Series) -> bool:
        """Check if a column likely contains dates."""
        date_keywords = ['date', 'time', 'created', 'updated', 'timestamp']
        return any(keyword in column_name.lower() for keyword in date_keywords)
    
    def _looks_like_numeric_column(self, column_name: str, column_data: pd.Series) -> bool:
        """Check if a column likely contains numeric data."""
        numeric_keywords = ['id', 'count', 'amount', 'price', 'quantity', 'number', 'total']
        return any(keyword in column_name.lower() for keyword in numeric_keywords)
    
    def _check_date_formats(self, column_data: pd.Series) -> Dict[str, Any]:
        """Check for date format inconsistencies."""
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{2}-\d{2}-\d{4}',  # MM-DD-YYYY
            r'\d{4}/\d{2}/\d{2}',  # YYYY/MM/DD
        ]
        
        format_counts = {}
        for pattern in date_patterns:
            matches = column_data.astype(str).str.match(pattern, na=False).sum()
            if matches > 0:
                format_counts[pattern] = int(matches)
        
        if len(format_counts) > 1:
            return {
                'multiple_formats': True,
                'format_distribution': format_counts,
                'total_records': len(column_data)
            }
        
        return {}
    
    def _check_numeric_consistency(self, column_data: pd.Series) -> Dict[str, Any]:
        """Check for numeric data inconsistencies."""
        issues = {}
        
        # Try to convert to numeric
        numeric_data = pd.to_numeric(column_data, errors='coerce')
        non_numeric_count = numeric_data.isnull().sum() - column_data.isnull().sum()
        
        if non_numeric_count > 0:
            issues['non_numeric_values'] = {
                'count': int(non_numeric_count),
                'percentage': round((non_numeric_count / len(column_data)) * 100, 2)
            }
        
        # Check for outliers using IQR method
        if len(numeric_data.dropna()) > 0:
            Q1 = numeric_data.quantile(0.25)
            Q3 = numeric_data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = numeric_data[(numeric_data < lower_bound) | (numeric_data > upper_bound)]
            if len(outliers) > 0:
                issues['outliers'] = {
                    'count': len(outliers),
                    'percentage': round((len(outliers) / len(numeric_data.dropna())) * 100, 2),
                    'values': outliers.dropna().tolist()
                }
        
        return issues
    
    def _check_string_consistency(self, column_data: pd.Series) -> Dict[str, Any]:
        """Check for string data inconsistencies."""
        issues = {}
        
        # Check for length inconsistencies
        lengths = column_data.str.len()
        if lengths.std() > lengths.mean() * 0.5:  # High variance in length
            issues['length_inconsistency'] = {
                'mean_length': round(lengths.mean(), 2),
                'std_length': round(lengths.std(), 2),
                'min_length': int(lengths.min()),
                'max_length': int(lengths.max())
            }
        
        # Check for pattern inconsistencies (basic email, phone patterns)
        if 'email' in column_data.name.lower():
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            valid_emails = column_data.str.match(email_pattern, na=False).sum()
            if valid_emails < len(column_data) * 0.8:  # Less than 80% valid
                issues['email_format'] = {
                    'valid_count': int(valid_emails),
                    'invalid_count': int(len(column_data) - valid_emails),
                    'valid_percentage': round((valid_emails / len(column_data)) * 100, 2)
                }
        
        return issues
    
    def run_all_checks(self) -> Dict[str, Any]:
        """
        Run all data quality checks.
        
        Returns:
            Complete results from all checks
        """
        self.check_missing_values()
        self.check_duplicates()
        self.check_schema_validation()
        
        # Generate summary
        total_issues = 0
        if self.results.get('missing_values'):
            total_issues += sum(1 for col in self.results['missing_values'].values() if col['has_missing'])
        
        if self.results.get('duplicates', {}).get('has_duplicates'):
            total_issues += 1
            
        if self.results.get('schema_issues'):
            total_issues += len(self.results['schema_issues'])
        
        self.results['summary'] = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'total_issues': total_issues,
            'data_quality_score': max(0, 100 - (total_issues * 10))  # Simple scoring
        }
        
        return self.results
