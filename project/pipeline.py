import os
import pandas as pd
import sqlite3

# Define paths
DATA_DIR = "./data"
MAIN_DB_PATH = os.path.join(DATA_DIR, "USAdatabase.db")
CSV_FILE_PATH = os.path.join(DATA_DIR, "population_USA.csv")
XLSX_FILE_PATH = os.path.join(DATA_DIR, "unemployed_reates_USA.xlsx")

def load_population_data(csv_file):
    """Load and process population data from CSV."""
    columns_to_use = ["NAME", "POPESTIMATE2020", "POPESTIMATE2021", "POPESTIMATE2022", "POPESTIMATE2023"]
    df = pd.read_csv(csv_file, usecols=columns_to_use, encoding='utf-8')
    
    # Rename columns
    df.rename(columns={
        "NAME": "state",
        "POPESTIMATE2020": "2020",
        "POPESTIMATE2021": "2021",
        "POPESTIMATE2022": "2022",
        "POPESTIMATE2023": "2023"
    }, inplace=True)
    
    # Drop rows with null or empty values
    df.dropna(inplace=True)
    df = df.replace("", pd.NA).dropna()
    
    return df

def load_unemployment_data(xlsx_file):
    """Load and process unemployment data from Excel."""
    # Load the Excel file without a header for manual control
    df = pd.read_excel(xlsx_file, engine='openpyxl', header=None)
    
    # Select rows A7 to A59 (index 6 to 58) and relevant columns
    df = df.iloc[6:59, [0, 1, 4, 7, 10]]
    
    # Rename columns to lowercase for consistency
    df.columns = ["state", "rate_2023", "rate_2022", "rate_2021", "rate_2020"]
    
    # Remove the first row if it contains "State" in the "state" column
    if df.iloc[0]['state'].strip().lower() == 'state':
        df = df.iloc[1:]
    
    # Convert rate columns to numeric
    rate_columns = ["rate_2023", "rate_2022", "rate_2021", "rate_2020"]
    df[rate_columns] = df[rate_columns].apply(pd.to_numeric, errors='coerce')
    
    # Drop rows with any NaN values
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    return df

def save_to_db(df, table_name, db_path):
    """Save a DataFrame to an SQLite database with UTF-8 encoding."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA encoding = 'UTF-8';")
    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Table '{table_name}' created/updated successfully.")
    except Exception as e:
        print(f"Error saving to database: {e}")
    finally:
        conn.close()

def main():
    # Step 1: Load and process the population data
    print("Processing population data...")
    population_df = load_population_data(CSV_FILE_PATH)
    save_to_db(population_df, "population_usa_2020_2023", MAIN_DB_PATH)
    
    # Step 2: Load and process the unemployment data
    print("Processing unemployment data...")
    unemployment_df = load_unemployment_data(XLSX_FILE_PATH)
    save_to_db(unemployment_df, "unemployment_rates_usa_2020_2023", MAIN_DB_PATH)
    
    print("Data pipeline completed successfully.")

if __name__ == "__main__":
    main()
