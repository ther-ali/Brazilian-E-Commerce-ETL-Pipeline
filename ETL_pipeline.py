import pandas as pd
from pathlib import Path
import glob
import sqlite3
import logging
import os


# Changing directory
os.chdir('/home/thar/Desktop/Earthlink_assi/')

# Setup logging
log_path_file = ("/home/thar/Desktop/Earthlink_assi/ETL_log.log")

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_path_file, mode="a"),
        logging.StreamHandler()
        ]
)
logger = logging.getLogger(__name__)

# Insert function
def insert_dataframe(conn, table, df, conflict='IGNORE'):

    if df is None or df.empty:
        logger.info(f"No data to insert into {table}")
        return 0

    # Align columns
    df.columns = [c.strip().lower() for c in df.columns]

    # Get db table columns
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table})")
    db_cols = [row[1].lower() for row in cur.fetchall()]

    # Keep matching columns
    df = df[[c for c in df.columns if c in db_cols]]

    if df.empty:
        logger.warning(f"No matching columns between dataFrame and {table}")
        return 0

    # SQL query
    placeholders = ','.join(['?'] * len(df.columns))
    col_list = ','.join([f'"{c}"' for c in df.columns])
    sql = f"INSERT OR {conflict} INTO {table} ({col_list}) VALUES ({placeholders})"

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

# Load CSV files
all_files = glob.glob('dataset/*.csv')
logger.info(f"Found CSVs: {all_files}")

table_names = [Path(path).stem.removesuffix('_dataset') for path in all_files]
logger.info(f"Target tables: {table_names}")

# Read CSV files
df_list = [pd.read_csv(file) for file in all_files]


# Connect to SQLite
conn = sqlite3.connect('olist_db')


# Insert each DataFrame
for table, df in zip(table_names, df_list):
    insert_dataframe(conn, table, df)

conn.close()
logger.info("------ All tables inserted successfully! ------")