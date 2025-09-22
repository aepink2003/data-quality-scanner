#!/usr/bin/env python3
"""
Demo script for the Data Quality Scanner.

This script demonstrates the core functionality of the Data Quality Scanner
without requiring the Streamlit web interface.
"""

import pandas as pd
from scanner import DataQualityChecker, ReportGenerator


def demo_data_quality_scanner():
    """Demonstrate the Data Quality Scanner with sample data."""
    print("Data Quality Scanner Demo")
    print("=" * 50)
    
    # Create sample data with various issues
    sample_data = pd.DataFrame({
        'customer_id': [1, 2, None, 4, 1, 6, None, 8, 9, 10],
        'email': [
            'john@email.com', 'jane@email.com', 'bob@email.com', 'alice@email.com',
            'john@email.com', 'charlie@email.com', 'diana@email.com', 'eve@email.com',
            'invalid-email', 'frank@email.com'
        ],
        'purchase_date': [
            '2024-01-15', '2024-01-16', '15/01/2024', '2024-01-18',
            '2024-01-15', '2024-01-20', '20/01/2024', '2024-01-22',
            '2024-01-23', '2024-01-24'
        ],
        'amount': [100.50, 85.00, 120.75, 95.25, 100.50, 150.00, 'invalid', 75.50, 200.00, 90.00],
        'category': ['Electronics', 'Books', 'Electronics', 'Clothing', 'Electronics', 
                    'Books', 'Electronics', 'Clothing', 'Electronics', 'Books']
    })
    
    print(f"Sample Dataset: {len(sample_data)} rows, {len(sample_data.columns)} columns")
    print("\nFirst 5 rows:")
    print(sample_data.head())
    
    # Run data quality checks
    print("\nRunning Data Quality Analysis...")
    checker = DataQualityChecker(sample_data)
    results = checker.run_all_checks()
    
    # Generate report
    reporter = ReportGenerator(results, sample_data)
    
    # Display results
    print("\nData Quality Report")
    print("=" * 30)
    
    # Summary stats
    stats = reporter.generate_summary_stats()
    print(f"Data Quality Score: {stats['data_quality_score']}/100")
    print(f"Total Issues Found: {stats['columns_with_missing'] + (1 if stats['duplicate_rows'] > 0 else 0) + stats['schema_issues_count']}")
    print(f"Columns with Missing Values: {stats['columns_with_missing']}")
    print(f"Duplicate Rows: {stats['duplicate_rows']}")
    print(f"Schema Issues: {stats['schema_issues_count']}")
    
    # Missing values details
    missing_values = results.get('missing_values', {})
    if any(col['has_missing'] for col in missing_values.values()):
        print("\nMissing Values:")
        for col, data in missing_values.items():
            if data['has_missing']:
                print(f"  {col}: {data['count']} missing ({data['percentage']}%)")
    
    # Duplicates details
    duplicates = results.get('duplicates', {})
    if duplicates.get('has_duplicates'):
        print(f"\nDuplicates:")
        print(f"  {duplicates['count']} duplicate rows ({duplicates['percentage']}%)")
    
    # Schema issues details
    schema_issues = results.get('schema_issues', {})
    if schema_issues:
        print("\nSchema Issues:")
        for col, issues in schema_issues.items():
            print(f"  {col}: {len(issues)} issue(s)")
            for issue_type, details in issues.items():
                print(f"    - {issue_type}: {details}")
    
    # Generate and display text report
    print("\nDetailed Report:")
    print("-" * 30)
    text_report = reporter.generate_text_report()
    print(text_report)
    
    print("\nDemo completed successfully!")
    print("\nTo run the full web interface:")
    print("  streamlit run app.py")


if __name__ == "__main__":
    demo_data_quality_scanner()
