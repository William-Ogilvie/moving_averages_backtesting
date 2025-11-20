"""
compute_ma.py
==============
This module computes several moving averages for each of the tickers (the moving averages
are described in create_indicators_table.sql) in a new table called prices_indicators.
It then creates a table called strategy_signals that contains our trading strategy, here we 
use golden cross and death cross. Golden cross is when the 50 day moving average crosses the 
200 day moving average upwards this signals a bullish market so we buy. Death cross is when the
200 day moving average crosses the 50 day moving average upwards this signals a bearish market so 
we sell. 
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
CREATE_STRATEGY_FILE_NAME = config["sql_files"]["create_strategy"]

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

# Now we will create the strategy singals table, this uses the golden cross and death cross trading 
# strategy, so BUY when ma50 cross ma200 upwards and sell when ma200 crosses ma50 upwards
create_strategy_file = Path(SQL_DIR / CREATE_STRATEGY_FILE_NAME)
query = create_strategy_file.read_text()

# Run the query on the db to create the strategy_signals db
with engine.begin() as conn:
    conn.execute(text(query))

# To test a buy look at 2009-06-24 the strategy recommends buying SPY
# we will double check that we are in a golden cross
#SELECT 
#   ticker,
#   date,
#   ma50, 
#   ma200,
#   signal
#FROM strategy_signals
#WHERE 
#   ticker = "SPY" 
#   AND (date = "2009-06-23" OR date = "2009-06-24");
#
# we get:
# SPY|2009-06-23|90.1752|90.2501990049751|HOLD
# SPY|2009-06-24|90.2906|90.079552238806|BUY
# so we see that on the 23rd the 200 day moving average was above the 50 day one
# then on the 24th the 50 day one has overtaken so we are indeed in a golden cross!

# To test a sell look at MSFT 2024-11-01 where the strategy recommends we sell
#SELECT
#   ticker,
#   date,
#   ma50,
#   ma200,
#   prev_ma50, -- just to check these work correctly
#   prev_ma200,
#   signal
#FROM strategy_signals
#WHERE 
#   ticker = "MSFT"
#   AND (date = "2024-11-01" OR date = "2024-10-31");
#
# we get:
# MSFT|2024-10-31|420.791|420.590199004975|421.1468|420.510199004975|HOLD
# MSFT|2024-11-01|420.6874|420.694179104478|420.791|420.590199004975|SELL
# first we see that prev_ma50 and prev_ma200 work correctly which is good
# secondly we note that on the 31st ma50 was ahead of ma200, then on the 1st
# ma200 overtakes ma50 so we are in a death cross!

# Finally we will check a random hold value is correct (these tests
# obviously aren't rigorous but more simple checks for a small project)
# let's do 2022-03-03 for NVDA
#SELECT 
#   ticker,
#   date,
#   ma50,
#   ma200,
#   signal
#FROM strategy_signals
#WHERE
#   ticker = "NVDA"
#   AND (date = "2022-03-03" OR date = "2022-03-02");
# 
# we get:
# NVDA|2022-03-02|259.4302|350.300099502488|HOLD
# NVDA|2022-03-03|258.6292|348.660895522388|HOLD
# so again we see that on the 2nd there is no 
# cross over as the 200 day moving average remains above the 
# 50 day one