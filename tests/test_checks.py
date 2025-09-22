"""
Unit tests for the Data Quality Scanner checks module.
"""

import unittest
import pandas as pd
import numpy as np
from scanner.checks import DataQualityChecker


class TestDataQualityChecker(unittest.TestCase):
    """Test cases for DataQualityChecker class."""
    
    def setUp(self):
        """Set up test data."""
        self.test_data = pd.DataFrame({
            'id': [1, 2, None, 4, 1],
            'email': ['test@email.com', 'invalid-email', 'test@email.com', 'user@email.com', 'test@email.com'],
            'date': ['2024-01-01', '01/01/2024', '2024-01-03', '2024-01-04', '2024-01-01'],
            'amount': [100.50, 85.00, 'invalid', 95.25, 100.50],
            'category': ['A', 'B', 'A', 'B', 'A']
        })
        self.checker = DataQualityChecker(self.test_data)
    
    def test_missing_values_detection(self):
        """Test missing value detection."""
        results = self.checker.check_missing_values()
        
        # Check that missing values are detected
        self.assertIn('id', results)
        self.assertTrue(results['id']['has_missing'])
        self.assertEqual(results['id']['count'], 1)
        self.assertEqual(results['id']['percentage'], 20.0)
    
    def test_duplicates_detection(self):
        """Test duplicate detection."""
        results = self.checker.check_duplicates()
        
        # Check that duplicates are detected
        self.assertTrue(results['has_duplicates'])
        self.assertEqual(results['count'], 1)  # One duplicate row
        self.assertEqual(results['percentage'], 20.0)
    
    def test_schema_validation(self):
        """Test schema validation."""
        results = self.checker.check_schema_validation()
        
        # Should detect issues in date and amount columns
        self.assertIn('date', results)
        self.assertIn('amount', results)
    
    def test_run_all_checks(self):
        """Test running all checks together."""
        results = self.checker.run_all_checks()
        
        # Check that all result types are present
        self.assertIn('missing_values', results)
        self.assertIn('duplicates', results)
        self.assertIn('schema_issues', results)
        self.assertIn('summary', results)
        
        # Check summary statistics
        summary = results['summary']
        self.assertEqual(summary['total_rows'], 5)
        self.assertEqual(summary['total_columns'], 5)
        self.assertGreater(summary['total_issues'], 0)
    
    def test_data_quality_score_calculation(self):
        """Test data quality score calculation."""
        results = self.checker.run_all_checks()
        score = results['summary']['data_quality_score']
        
        # Score should be between 0 and 100
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        
        # With multiple issues, score should be lower
        self.assertLess(score, 100)


class TestCleanData(unittest.TestCase):
    """Test cases with clean data (no issues)."""
    
    def setUp(self):
        """Set up clean test data."""
        self.clean_data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'email': ['a@email.com', 'b@email.com', 'c@email.com', 'd@email.com', 'e@email.com'],
            'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
            'amount': [100.50, 85.00, 120.75, 95.25, 150.00],
            'category': ['A', 'B', 'C', 'D', 'E']
        })
        self.checker = DataQualityChecker(self.clean_data)
    
    def test_clean_data_no_issues(self):
        """Test that clean data has no issues."""
        results = self.checker.run_all_checks()
        
        # Should have high data quality score
        self.assertEqual(results['summary']['data_quality_score'], 100)
        self.assertEqual(results['summary']['total_issues'], 0)
        
        # No missing values
        missing_values = results['missing_values']
        for col_data in missing_values.values():
            self.assertFalse(col_data['has_missing'])
        
        # No duplicates
        self.assertFalse(results['duplicates']['has_duplicates'])
        
        # No schema issues
        self.assertEqual(len(results['schema_issues']), 0)


if __name__ == '__main__':
    unittest.main()
