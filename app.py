"""
Data Quality Scanner - Streamlit Application

A web application for scanning CSV files and detecting common data quality issues.
"""

import streamlit as st
import pandas as pd
import numpy as np
from scanner import DataQualityChecker, ReportGenerator
import plotly.graph_objects as go
from io import StringIO
import base64
from datetime import datetime


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Data Quality Scanner",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("Data Quality Scanner")
    st.markdown("""
    Upload a CSV file to automatically detect common data quality issues including:
    - Missing values
    - Duplicate rows  
    - Schema inconsistencies
    - Data type mismatches
    """)
    
    # Sidebar for file upload
    st.sidebar.header("Upload CSV File")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a CSV file",
        type="csv",
        help="Upload a CSV file to analyze data quality"
    )
    
    # Sample data option
    if st.sidebar.button("Use Sample Data"):
        sample_data = create_sample_data()
        uploaded_file = sample_data
    
    # Main content area
    if uploaded_file is not None:
        try:
            # Load the CSV file
            if isinstance(uploaded_file, pd.DataFrame):
                df = uploaded_file
                st.success("Sample data loaded successfully!")
            else:
                df = pd.read_csv(uploaded_file)
                st.success(f"File '{uploaded_file.name}' loaded successfully!")
            
            # Display basic info
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Rows", f"{len(df):,}")
            with col2:
                st.metric("Total Columns", len(df.columns))
            with col3:
                st.metric("File Size", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
            with col4:
                st.metric("Data Types", len(df.dtypes.value_counts()))
            
            # Run data quality checks
            st.header("Data Quality Analysis")
            
            with st.spinner("Analyzing data quality..."):
                checker = DataQualityChecker(df)
                results = checker.run_all_checks()
                reporter = ReportGenerator(results, df)
            
            # Display results in tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "Overview", 
                "Missing Values", 
                "Duplicates", 
                "Schema Issues",
                "Detailed Report"
            ])
            
            with tab1:
                display_overview_tab(reporter, results)
            
            with tab2:
                display_missing_values_tab(reporter, results)
            
            with tab3:
                display_duplicates_tab(reporter, results)
            
            with tab4:
                display_schema_tab(reporter, results)
            
            with tab5:
                display_detailed_report_tab(reporter, results)
            
            # Download options
            st.header("Export Options")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Download Text Report"):
                    text_report = reporter.generate_text_report()
                    st.download_button(
                        label="Download Report",
                        data=text_report,
                        file_name=f"data_quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
            
            with col2:
                if st.button("Download Issues Summary"):
                    issues_df = reporter.get_issue_summary_table()
                    csv = issues_df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"data_quality_issues_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            
            with col3:
                if st.button("Download Data Sample"):
                    sample_df = df.head(100)  # First 100 rows
                    csv = sample_df.to_csv(index=False)
                    st.download_button(
                        label="Download Sample",
                        data=csv,
                        file_name=f"data_sample_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
        
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            st.info("Please make sure you've uploaded a valid CSV file.")
    
    else:
        # Welcome screen
        display_welcome_screen()


def display_welcome_screen():
    """Display the welcome screen when no file is uploaded."""
    st.markdown("""
    ## Welcome to Data Quality Scanner!
    
    This tool helps you identify and fix common data quality issues in your CSV files.
    
    ### What you can detect:
    - **Missing Values**: Identify columns with missing or null data
    - **Duplicates**: Find duplicate rows in your dataset
    - **Schema Issues**: Detect inconsistent data types and formats
    - **Data Anomalies**: Spot outliers and unexpected patterns
    
    ### How to get started:
    1. Upload a CSV file using the sidebar
    2. Wait for the automatic analysis
    3. Review the interactive dashboard
    4. Download reports and recommendations
    
    ### Sample Data Available:
    Click "Use Sample Data" in the sidebar to try the tool with example data containing common issues.
    """)


def display_overview_tab(reporter, results):
    """Display the overview tab with key metrics and charts."""
    stats = reporter.generate_summary_stats()
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Data Quality Score", 
            f"{stats['data_quality_score']}/100",
            delta=f"{'Excellent' if stats['data_quality_score'] >= 90 else 'Good' if stats['data_quality_score'] >= 70 else 'Needs Attention'}"
        )
    
    with col2:
        st.metric(
            "Issues Found",
            f"{stats['columns_with_missing'] + (1 if stats['duplicate_rows'] > 0 else 0) + stats['schema_issues_count']}",
            delta="Total Issues" if stats['has_issues'] else "No Issues"
        )
    
    with col3:
        st.metric(
            "Columns with Issues",
            f"{stats['columns_with_missing'] + stats['schema_issues_count']}",
            delta=f"out of {stats['total_columns']} columns"
        )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(reporter.create_data_quality_score_gauge(), use_container_width=True)
    
    with col2:
        st.plotly_chart(reporter.create_data_types_chart(), use_container_width=True)
    
    # Summary table
    if stats['has_issues']:
        st.subheader("Issue Summary")
        issues_df = reporter.get_issue_summary_table()
        st.dataframe(issues_df, use_container_width=True)
    else:
        st.success("Congratulations! No data quality issues detected in your dataset.")


def display_missing_values_tab(reporter, results):
    """Display missing values analysis."""
    st.subheader("Missing Values Analysis")
    
    missing_values = results.get('missing_values', {})
    
    if not any(col['has_missing'] for col in missing_values.values()):
        st.success("No missing values found!")
        return
    
    # Missing values chart
    st.plotly_chart(reporter.create_missing_values_chart(), use_container_width=True)
    
    # Detailed table
    st.subheader("Missing Values by Column")
    
    missing_data = []
    for col, data in missing_values.items():
        if data['has_missing']:
            missing_data.append({
                'Column': col,
                'Missing Count': data['count'],
                'Missing Percentage': f"{data['percentage']}%",
                'Status': 'Critical' if data['percentage'] > 20 else 'Warning' if data['percentage'] > 5 else 'Low'
            })
    
    if missing_data:
        missing_df = pd.DataFrame(missing_data)
        st.dataframe(missing_df, use_container_width=True)
        
        # Recommendations
        st.subheader("Recommendations")
        high_missing = [row['Column'] for row in missing_data if float(row['Missing Percentage'].rstrip('%')) > 20]
        if high_missing:
            st.warning(f"**High Priority**: Columns with >20% missing values: {', '.join(high_missing)}")
        
        medium_missing = [row['Column'] for row in missing_data if 5 < float(row['Missing Percentage'].rstrip('%')) <= 20]
        if medium_missing:
            st.info(f"**Medium Priority**: Columns with 5-20% missing values: {', '.join(medium_missing)}")


def display_duplicates_tab(reporter, results):
    """Display duplicates analysis."""
    st.subheader("Duplicates Analysis")
    
    duplicates = results.get('duplicates', {})
    
    if not duplicates.get('has_duplicates'):
        st.success("No duplicate rows found!")
        return
    
    # Duplicates chart
    st.plotly_chart(reporter.create_duplicate_visualization(), use_container_width=True)
    
    # Detailed info
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Duplicate Rows", duplicates['count'])
        st.metric("Duplicate Percentage", f"{duplicates['percentage']}%")
    
    with col2:
        st.metric("Unique Rows", results['summary']['total_rows'] - duplicates['count'])
        st.metric("Total Rows", results['summary']['total_rows'])
    
    # Show duplicate rows if not too many
    if duplicates['count'] <= 50:
        st.subheader("Duplicate Rows Preview")
        duplicate_rows = reporter.df[reporter.df.duplicated(keep=False)]
        st.dataframe(duplicate_rows, use_container_width=True)
    
    # Recommendations
    st.subheader("Recommendations")
    if duplicates['percentage'] > 10:
        st.error("**High Priority**: More than 10% of rows are duplicates. This significantly impacts data quality.")
    elif duplicates['percentage'] > 5:
        st.warning("**Medium Priority**: Some duplicate rows detected. Consider investigating the cause.")
    else:
        st.info("**Low Priority**: Few duplicate rows detected. Review and remove if necessary.")


def display_schema_tab(reporter, results):
    """Display schema issues analysis."""
    st.subheader("Schema Issues Analysis")
    
    schema_issues = results.get('schema_issues', {})
    
    if not schema_issues:
        st.success("No schema issues detected!")
        return
    
    # Schema issues chart
    st.plotly_chart(reporter.create_schema_issues_chart(), use_container_width=True)
    
    # Detailed analysis
    st.subheader("Schema Issues by Column")
    
    for column, issues in schema_issues.items():
        with st.expander(f"{column} - {len(issues)} issue(s)"):
            for issue_type, details in issues.items():
                st.write(f"**{issue_type.replace('_', ' ').title()}**:")
                st.json(details)
    
    # Recommendations
    st.subheader("Recommendations")
    st.info("""
    **Common Schema Issues & Solutions:**
    - **Mixed Types**: Standardize data types across the column
    - **Date Formats**: Use consistent date format (recommend YYYY-MM-DD)
    - **Numeric Issues**: Clean non-numeric values from numeric columns
    - **String Issues**: Standardize string lengths and formats
    """)


def display_detailed_report_tab(reporter, results):
    """Display the detailed text report."""
    st.subheader("Detailed Analysis Report")
    
    # Text report
    text_report = reporter.generate_text_report()
    st.text_area("Full Report", text_report, height=400)
    
    # Raw results (for debugging/advanced users)
    with st.expander("Raw Results (JSON)"):
        st.json(results)


def create_sample_data():
    """Create sample data with common data quality issues."""
    np.random.seed(42)
    
    # Create sample data with intentional issues
    data = {
        'customer_id': [1, 2, None, 4, 1, 6, None, 8, 9, 10, 11, 12, 13, None, 15],
        'email': [
            'john@email.com', 'jane@email.com', 'bob@email.com', 'alice@email.com',
            'john@email.com', 'charlie@email.com', 'diana@email.com', 'eve@email.com',
            'invalid-email', 'frank@email.com', 'grace@email.com', 'henry@email.com',
            'invalid-email', 'invalid@', 'iris@email.com'
        ],
        'purchase_date': [
            '2024-01-15', '2024-01-16', '15/01/2024', '2024-01-18',
            '2024-01-15', '2024-01-20', '20/01/2024', '2024-01-22',
            '2024-01-23', '2024-01-24', '24/01/2024', '2024-01-26',
            '2024-01-27', '27/01/2024', '2024-01-29'
        ],
        'amount': [100.50, 85.00, 120.75, 95.25, 100.50, 150.00, 'invalid', 75.50, 200.00, 90.00, 110.25, 85.75, 300.00, 95.50, 125.00],
        'category': ['Electronics', 'Books', 'Electronics', 'Clothing', 'Electronics', 'Books', 'Electronics', 'Clothing', 'Electronics', 'Books', 'Electronics', 'Clothing', 'Electronics', 'Books', 'Electronics']
    }
    
    df = pd.DataFrame(data)
    
    # Create a file-like object
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    return df


if __name__ == "__main__":
    main()
