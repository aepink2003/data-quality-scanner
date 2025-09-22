"""
Data Quality Scanner - A tool for detecting common data issues in CSV files.

This package provides functionality to scan CSV files for:
- Missing values
- Duplicate rows
- Schema validation issues
- Data drift detection
"""

__version__ = "1.0.0"
__author__ = "Data Quality Scanner Team"

from .checks import DataQualityChecker
from .reporting import ReportGenerator

__all__ = ["DataQualityChecker", "ReportGenerator"]

