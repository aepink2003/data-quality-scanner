# Data Quality Scanner

A comprehensive tool for automatically detecting common data quality issues in CSV files. Built with Python and Streamlit, this application provides an interactive dashboard to analyze data quality and generate detailed reports.

## Features

### Core Data Quality Checks
- **Missing Values Detection**: Identify and quantify missing or null values across columns
- **Duplicate Row Detection**: Find and analyze duplicate entries in your dataset
- **Schema Validation**: Detect inconsistent data types and format mismatches
- **Data Type Analysis**: Comprehensive analysis of data types and distributions

### Advanced Analytics
- **Interactive Dashboard**: Real-time visualization of data quality metrics
- **Quality Score**: Overall data quality score (0-100) with detailed breakdown
- **Issue Prioritization**: Categorize issues by severity (High/Medium/Low)
- **Export Options**: Download reports in multiple formats (TXT, CSV)

### User Experience
- **Drag & Drop Upload**: Easy CSV file upload via web interface
- **Sample Data**: Built-in sample datasets to explore functionality
- **Real-time Analysis**: Instant feedback on data quality issues
- **Mobile Responsive**: Works on desktop and mobile devices

## Screenshots

### Dashboard Overview
![Dashboard](https://via.placeholder.com/800x400/4CAF50/FFFFFF?text=Data+Quality+Dashboard)

### Missing Values Analysis
![Missing Values](https://via.placeholder.com/800x400/FF9800/FFFFFF?text=Missing+Values+Analysis)

### Schema Issues Detection
![Schema Issues](https://via.placeholder.com/800x400/F44336/FFFFFF?text=Schema+Issues+Detection)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

## Usage

Link to tool: https://data-quality-scanner.streamlit.app/#how-to-get-started

### Basic Usage

1. **Upload a CSV file** using the sidebar uploader
2. **Wait for analysis** - the tool automatically scans your data
3. **Review the dashboard** with interactive charts and metrics
4. **Download reports** for further analysis or sharing

### Sample Data

Click "Use Sample Data" to explore the tool with pre-loaded datasets containing common data quality issues:
- Missing values in customer IDs
- Duplicate purchase records
- Inconsistent date formats
- Mixed data types in amount columns
- Invalid email formats

### Understanding the Results

#### Data Quality Score
- **90-100**: Excellent data quality
- **70-89**: Good data quality with minor issues
- **50-69**: Fair data quality, attention needed
- **0-49**: Poor data quality, immediate action required

#### Issue Severity Levels
- **🔴 Critical**: Issues affecting >20% of data
- **🟡 Warning**: Issues affecting 5-20% of data
- **🟢 Low**: Issues affecting <5% of data


## Technical Details

### Technology Stack
- **Frontend**: Streamlit for interactive dashboard
- **Backend**: Python with Pandas and NumPy for data processing
- **Visualization**: Plotly for interactive charts
- **Testing**: unittest for unit testing
- **Data Processing**: Pandas for CSV handling and analysis

### Key Components

#### DataQualityChecker (`scanner/checks.py`)
- Performs comprehensive data quality analysis
- Detects missing values, duplicates, and schema issues
- Calculates data quality metrics and scores

#### ReportGenerator (`scanner/reporting.py`)
- Generates interactive visualizations
- Creates text and summary reports
- Provides export functionality

#### Streamlit App (`app.py`)
- Web interface for file upload and visualization
- Real-time data quality analysis
- Interactive dashboard with multiple views

### Performance
- Handles CSV files up to 50MB efficiently
- Processes 10,000+ rows in under 10 seconds
- Memory-optimized for large datasets

## Testing

Run the test suite to ensure everything works correctly:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_checks.py

# Run with verbose output
python -m pytest tests/ -v
```

### Test Coverage
- Missing value detection
- Duplicate row identification
- Schema validation
- Data quality scoring
- Clean data handling
- Error handling

## Use Cases

### Data Engineering Teams
- **Pre-processing validation**: Check data quality before ETL processes
- **Pipeline monitoring**: Regular data quality audits
- **Issue triage**: Prioritize data quality problems

### Data Analysts
- **Data exploration**: Understand data quality before analysis
- **Report validation**: Ensure data integrity for business reports
- **Stakeholder communication**: Generate quality reports for business users

### Data Scientists
- **Model preparation**: Clean data before machine learning
- **Feature engineering**: Identify problematic features
- **Model validation**: Ensure training data quality

### Business Intelligence
- **Dashboard validation**: Verify data quality for BI dashboards
- **Compliance reporting**: Generate data quality documentation
- **Audit preparation**: Prepare data quality evidence for audits

*Help improve data quality, one CSV at a time!*
