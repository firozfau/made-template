import os
import pandas as pd
import sqlite3
from kaggle.api.kaggle_api_extended import KaggleApi

DATA_DIR = "./data"

# Database name  set
CLIMATE_DB_PATH = os.path.join(DATA_DIR, "climate_data.db")
SALES_DB_PATH = os.path.join(DATA_DIR, "sales_data.db")
MAIN_DB_PATH = os.path.join(DATA_DIR, "mainDatabase.db") # climate and sales both  data here.

# dataset initialize (kaggle)
DATASETS = {
    "us_climate_regions": {
        "kaggle_id": "zeeniye/us-climate-regions",
        "file_name": "us_climate_regions.csv",
        "db_path": CLIMATE_DB_PATH,
        "table_name": "climate_regions"
    },
    "us_regional_sales_data": {
        "kaggle_id": "talhabu/us-regional-sales-data",
        "file_name": "US_Regional_Sales_Data.csv",
        "db_path": SALES_DB_PATH,
        "table_name": "regional_sales"
    }
}

def download_dataset(kaggle_id, file_name):
    api = KaggleApi()
    api.authenticate()
    print(f"Downloading {file_name} from Kaggle...")
    try:
        api.dataset_download_files(kaggle_id, path=DATA_DIR, unzip=True)
        print(f"Successfully downloaded {file_name}")
    except Exception as e:
        print(f"Error downloading {file_name}: {e}")

def load_data(file_path):
    print(f"Loading data from {file_path}...")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print(f"File {file_path} not found.")
        return pd.DataFrame()

def transform_data(df):
    if df.empty:
        print("No data to transform.")
        return df

    print("Transforming data...")
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    return df

def create_main_database():
    print(f"Creating main database at {MAIN_DB_PATH}...")
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(MAIN_DB_PATH):
        try:
            with sqlite3.connect(MAIN_DB_PATH) as conn:
                conn.execute("CREATE TABLE IF NOT EXISTS dummy (id INTEGER);")
                print("mainDatabase.db successfully created.")
        except Exception as e:
            print(f"Error creating main database: {e}")

def save_to_sqlite(df, db_path, table_name):
    if df.empty:
        print(f"No data to save for {table_name}.")
        return


    print(f"Saving {table_name} to {db_path}...")
    try:
        conn = sqlite3.connect(db_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
    except Exception as e:
        print(f"Error saving to {db_path}: {e}")

    # Main database
    print(f"Saving {table_name} to mainDatabase.db...")
    try:
        with sqlite3.connect(MAIN_DB_PATH) as conn_main:
            df.to_sql(table_name, conn_main, if_exists='replace', index=False)
        print(f"Successfully saved {table_name} to mainDatabase.db")
    except Exception as e:
        print(f"Error saving {table_name} to mainDatabase.db: {e}")

def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    create_main_database()
    
    for key, value in DATASETS.items():
        download_dataset(value["kaggle_id"], value["file_name"])
        
        df = load_data(os.path.join(DATA_DIR, value["file_name"]))
        
        df = transform_data(df)
        
        save_to_sqlite(df, value["db_path"], value["table_name"])

    print("Congratulations, Data pipeline is successfully completed!")

if __name__ == "__main__":
    main()
