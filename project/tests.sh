#!/bin/bash

# input and existing files set
DB_FILE="./data/USAdatabase.db"
CSV_INPUT="./data/population_USA.csv"
XLSX_INPUT="./data/unemployed_reates_USA.xlsx"

# Run the pipeline
echo "Load and Executing pipeline.py"
python3 pipeline.py

# validation
if [ $? -ne 0 ]; then
    echo "Failed to execute pipeline.py file"
    exit 1
fi

# Validate input files exist
echo "Checking input files..."
if [ ! -f "$CSV_INPUT" ]; then
    echo "Failed: $CSV_INPUT file does-not exist."
    exit 1
fi
if [ ! -f "$XLSX_INPUT" ]; then
    echo "Failed: $XLSX_INPUT file does not exist."
    exit 1
fi

# Check for database existence
echo "Final check"
if [ -f "$DB_FILE" ]; then
    echo "Database file exists."
else
    echo "Test failed: Database file is missing."
    exit 1
fi

# Validate database tables
echo "Check database tables..."
TABLES=$(sqlite3 "$DB_FILE" ".tables")

# Check for population table
if [[ "$TABLES" == *"population_usa_2020_2023"* ]]; then
    echo "Test passed: 'population_usa_2020_2023' table exists."
else
    echo "Test failed: 'population_usa_2020_2023' table is missing."
    exit 1
fi

# Check for unemployment table
if [[ "$TABLES" == *"unemployment_rates_usa_2020_2023"* ]]; then
    echo "Test passed: 'unemployment_rates_usa_2020_2023' table exists."
else
    echo "Test failed: 'unemployment_rates_usa_2020_2023' table is missing."
    exit 1
fi

echo "All system-level tests passed successfully."
