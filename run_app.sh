#!/bin/bash

# Data Quality Scanner - Launch Script
# This script sets up the environment and launches the Streamlit application

echo "Data Quality Scanner"
echo "======================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if requirements.txt is newer than last install
if [ requirements.txt -nt venv/.installed ] || [ ! -f venv/.installed ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Launch Streamlit app
echo "Launching Data Quality Scanner..."
echo "The application will open in your default web browser."
echo "If it doesn't open automatically, go to: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

streamlit run app.py
