# Data Quality Scanner  
### Interactive Data Validation & Profiling Tool

## TL;DR
Built an interactive data quality scanning tool that automatically detects common issues in CSV files, including missing values, duplicates, schema inconsistencies, and invalid formats.  
Provides a data quality score, issue prioritization by severity, and downloadable reports via a Streamlit dashboard.

🔗 **Live App:** https://data-quality-scanner.streamlit.app/#how-to-get-started

---

## Overview
The Data Quality Scanner is an interactive tool designed to automatically detect and summarize common data quality issues in CSV datasets. It helps data practitioners quickly assess data readiness before analysis, modeling, or pipeline ingestion.

The application transforms raw datasets into actionable diagnostics through automated checks, visual summaries, and exportable reports.

---

## Problem Statement
Poor data quality is a leading cause of unreliable analytics, failed machine learning models, and broken data pipelines. Manual data validation is time-consuming, error-prone, and difficult to scale.

### Objective
Provide an automated, easy-to-use tool that identifies data quality issues, prioritizes them by severity, and summarizes overall data health in a format accessible to both technical and non-technical users.

---

## Key Features

### Core Data Quality Checks
- Detection and quantification of missing values
- Identification of duplicate rows
- Schema validation and inconsistent data types
- Column-level data type and distribution analysis

### Analytics & Reporting
- Interactive dashboard with real-time metrics
- Overall data quality score (0–100) with breakdowns
- Issue prioritization by severity (High / Medium / Low)
- Exportable reports (TXT, CSV)

### User Experience
- Drag-and-drop CSV upload
- Built-in sample datasets for exploration
- Instant feedback on uploaded data
- Responsive UI for desktop and mobile use

---

## Approach

### Data Ingestion
- CSV file upload via Streamlit interface
- Validation of file structure and size limits

### Automated Quality Checks
- Missing value analysis across all columns
- Duplicate row detection
- Schema and data type consistency checks
- Pattern-based validation (e.g., dates, emails)

### Scoring & Prioritization
- Computation of an overall data quality score
- Classification of issues by severity thresholds
- Column-level and dataset-level summaries

### Visualization & Reporting
- Interactive charts and tables for issue exploration
- Downloadable quality reports for sharing or documentation

---

## Interpreting Results

### Data Quality Score
- **90–100:** Excellent data quality
- **70–89:** Good quality with minor issues
- **50–69:** Fair quality, attention recommended
- **0–49:** Poor quality, immediate action required

### Issue Severity Levels
- 🔴 **Critical:** Affects >20% of the dataset
- 🟡 **Warning:** Affects 5–20% of the dataset
- 🟢 **Low:** Affects <5% of the dataset

---

## Example Issues Detected (Sample Data)
- Missing customer identifiers
- Duplicate transaction records
- Inconsistent date formats
- Mixed numeric and string values in amount columns
- Invalid email address formats

---

## Tools & Libraries
- **Language:** Python  
- **Data Processing:** pandas, NumPy  
- **Visualization:** Plotly  
- **Frontend / Deployment:** Streamlit  
- **Testing:** unittest  

---

## Project Structure

### DataQualityChecker (`scanner/checks.py`)
- Executes automated data quality checks
- Computes metrics and severity levels
- Generates dataset-level summaries

### ReportGenerator (`scanner/reporting.py`)
- Builds visual and textual reports
- Handles export functionality

### Streamlit App (`app.py`)
- User interface for file upload and exploration
- Interactive dashboard for results visualization

---

## Performance
- Supports CSV files up to 50MB
- Processes datasets with 10,000+ rows in under 10 seconds
- Optimized for memory efficiency on large files

---

## Testing
Run the test suite locally to validate functionality:

```bash
python -m pytest tests/
python -m pytest tests/test_checks.py
python -m pytest tests/ -v
