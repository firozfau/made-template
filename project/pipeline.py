import os
import pandas as pd
import sqlite3
from kaggle.api.kaggle_api_extended import KaggleApi

DATA_DIR = "./data"

# Database paths set
CLIMATE_DB_PATH = os.path.join(DATA_DIR, "climate_data.db")
SALES_DB_PATH = os.path.join(DATA_DIR, "sales_data.db")

# Kaggle dataset initialize
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
    df.dropna(inplace=True)  #delete rows when get missing data
    df.drop_duplicates(inplace=True)  # delete rows when get duplicate data
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]  # rename of column   name
    return df

def save_to_sqlite(df, db_path, table_name):
   
    if df.empty:
        print(f"No data to save for {table_name}.")
        return

    print(f"Saving {table_name} to {db_path}...")
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

 
    for key, value in DATASETS.items(): 
        download_dataset(value["kaggle_id"], value["file_name"])
 
        df = load_data(os.path.join(DATA_DIR, value["file_name"]))
 
        df = transform_data(df)
 
        save_to_sqlite(df, value["db_path"], value["table_name"])

    print("Congratualtion, Data pipeline is successfully completed !")

if __name__ == "__main__":
    main()
