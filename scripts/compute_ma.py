"""
compute_ma.py
==============
This module computes several moving averages for each of the tickers (the moving averages
are described in create_indicators_table.sql) in a new table called prices_indicators.
"""

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

# Get the create indicators table query
create_indicators_file = Path(SQL_DIR / CREATE_INDICATORS_FILE_NAME)
query = create_indicators_file.read_text()

# Run the query on the db to create the prices_indicators table
with engine.begin() as conn:
    conn.execute(text(query))

# To test:
# SELECT * FROM prices_indicators WHERE ticker = "IBM" AND date = "2023-08-23";
# 556|IBM|2023-08-23|141.72|143.475|141.58|143.41|2559083|142.004|143.0705|138.1728|133.800655737705
# We will check the 50 day moving average 
# SELECT SUM(close) / COUNT(*) AS manual_ma50
# FROM 
# (
#   SELECT close
#   FROM prices
#   WHERE ticker = "IBM" AND date <= "2023-08-23"
#   ORDER BY date DESC
#   LIMIT 50
#);
# 138.1728 is output of above query, which matches!