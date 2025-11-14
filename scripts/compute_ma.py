

# --- Imports ---
import pandas as pd
from sqlalchemy import text, create_engine
from ma_backtesting import load_config
from pathlib import Path

# --- Config and constants ---
config, PROJECT_ROOT = load_config()

DATA_DIR = PROJECT_ROOT / config["dir_paths"]["data"]
SQL_DIR = PROJECT_ROOT / config["dir_paths"]["sql"] 
DB_NAME = config["basic_settings"]["data_base_name"]

CREATE_INDICATORS_FILE_NAME = config["sql_files"]["create_indicators"]

# --- Run SQL querries to create moving averages for all stocks ---
# Create engine
engine = create_engine(f"sqlite:///{DATA_DIR}/{DB_NAME}.db")

# Get tickers in the prices table
with engine.connect() as conn:
    result = conn.execute(text("SELECT DISTINCT ticker FROM prices"))
    tickers = [row[0] for row in result] 

# Get the create indicators table query
create_indicators_file = Path(SQL_DIR / CREATE_INDICATORS_FILE_NAME)
query = create_indicators_file.read_text()

# Run the query on the db to create the prices_indicators table
with engine.begin() as conn:
    conn.execute(text(query))