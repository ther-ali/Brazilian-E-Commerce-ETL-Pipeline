import pandas as pd
from pathlib import Path
import glob
import sqlite3
import logging
import os

# --- Dynamic Path Configuration ---
# Get the directory where this script is located (e.g., .../project/python/)
SCRIPT_DIR = Path(__file__).resolve().parent

# Define the Project Root (one level up from python/ folder)
PROJECT_ROOT = SCRIPT_DIR.parent

# Define specific paths relative to Project Root
DATASET_DIR = PROJECT_ROOT / 'dataset'
LOG_FILE = PROJECT_ROOT / 'ETL_log.log'
DB_FILE = PROJECT_ROOT / 'olist_db'

# Ensure we are working from the project root
os.chdir(PROJECT_ROOT)

# --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Insert Function ---
def insert_dataframe(conn, table, df, conflict='IGNORE'):
    """
    Inserts a pandas DataFrame into a SQLite table.
    """
    if df is None or df.empty:
        logger.info(f"No data to insert into {table}")
        return 0

    # Align columns: strip whitespace and lowercase
    df.columns = [c.strip().lower() for c in df.columns]

    # Get existing db table columns to ensure matching
    cur = conn.cursor()
    try:
        cur.execute(f"PRAGMA table_info({table})")
        db_cols = [row[1].lower() for row in cur.fetchall()]
    except Exception as e:
        logger.error(f"Error fetching table info for {table}: {e}")
        return 0

    # Keep only matching columns
    df = df[[c for c in df.columns if c in db_cols]]

    if df.empty:
        logger.warning(f"No matching columns between DataFrame and table {table}")
        return 0

    # Prepare SQL Query
    placeholders = ','.join(['?'] * len(df.columns))
    col_list = ','.join([f'"{c}"' for c in df.columns])
    sql = f"INSERT OR {conflict} INTO {table} ({col_list}) VALUES ({placeholders})"

    # Convert DataFrame to list of tuples
    values = [tuple(row) for row in df.itertuples(index=False, name=None)]

    inserted = 0
    try:
        cur.executemany(sql, values)
        conn.commit()
        inserted = cur.rowcount
        logger.info(f"--- Inserted {len(values)} rows into {table} (conflict={conflict}) ---")
    except Exception as e:
        conn.rollback()
        logger.exception(f"------ Error inserting into {table}: {e}\nSQL: {sql} ------")
    
    return inserted

# --- Main Execution ---
if __name__ == "__main__":
    logger.info("Starting ETL Pipeline...")

    # Find all CSV files in the dataset directory
    # Using str(DATASET_DIR) to ensure compatibility with glob
    csv_pattern = str(DATASET_DIR / '*.csv')
    all_files = glob.glob(csv_pattern)
    
    if not all_files:
        logger.error(f"No CSV files found in {DATASET_DIR}")
        exit()

    logger.info(f"Found {len(all_files)} CSVs: {[Path(p).name for p in all_files]}")

    # Extract table names from filenames
    # Example: 'dataset/olist_orders_dataset.csv' -> 'olist_orders'
    table_names = [Path(path).stem.removesuffix('_dataset') for path in all_files]
    logger.info(f"Target tables: {table_names}")

    # Read CSV files into DataFrames
    try:
        df_list = [pd.read_csv(file) for file in all_files]
    except Exception as e:
        logger.critical(f"Failed to read CSV files: {e}")
        exit()

    # Connect to SQLite Database
    logger.info(f"Connecting to database at {DB_FILE}...")
    conn = sqlite3.connect(DB_FILE)

    # Insert each DataFrame into its corresponding table
    for table, df in zip(table_names, df_list):
        insert_dataframe(conn, table, df)

    conn.close()
    logger.info("------ All tables inserted successfully! ------")
