import os
import pandas as pd
import sqlite3

# Paths
DATA_DIR = "./data"
CSV_FILE_PATH = os.path.join(DATA_DIR, "population_USA.csv")
XLSX_FILE_PATH = os.path.join(DATA_DIR, "unemployed_reates_USA.xlsx")
DB_FILE_PATH = os.path.join(DATA_DIR, "USAdatabase.db")

# Generate mock data
def generate_mock_population_data(file_path):
    print(f"File {file_path} is missing. Generating mock data...")
    data = [
        {"NAME": "Alabama", "POPESTIMATE2020": 4903185, "POPESTIMATE2021": 5024279, "POPESTIMATE2022": 5039877, "POPESTIMATE2023": 5054742},
        {"NAME": "Alaska", "POPESTIMATE2020": 731545, "POPESTIMATE2021": 731158, "POPESTIMATE2022": 732673, "POPESTIMATE2023": 735132},
    ]
    pd.DataFrame(data).to_csv(file_path, index=False)

def generate_mock_unemployment_data(file_path):
    print(f"File {file_path} is missing. Generating mock data...")
    data = {
        "state": ["Alabama", "Alaska"],
        "rate_2023": [3.5, 4.0],
        "rate_2022": [3.7, 4.1],
        "rate_2021": [3.8, 4.3],
        "rate_2020": [4.2, 4.5],
    }
    pd.DataFrame(data).to_excel(file_path, index=False)

def load_population_data(file_path):
    if not os.path.exists(file_path):
        generate_mock_population_data(file_path)
    df = pd.read_csv(file_path)
    return df

def load_unemployment_data(file_path):
    if not os.path.exists(file_path):
        generate_mock_unemployment_data(file_path)
    df = pd.read_excel(file_path)
    return df

def save_to_db(df, table_name, db_path):
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

def main():
    print("Processing population data...")
    population_df = load_population_data(CSV_FILE_PATH)
    save_to_db(population_df, "population_usa_2020_2023", DB_FILE_PATH)

    print("Processing unemployment data...")
    unemployment_df = load_unemployment_data(XLSX_FILE_PATH)
    save_to_db(unemployment_df, "unemployment_rates_usa_2020_2023", DB_FILE_PATH)

    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()
