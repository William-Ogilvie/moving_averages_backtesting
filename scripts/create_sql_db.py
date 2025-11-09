

import pandas as pd
from sqlalchemy import Column, Date, Float, Integer, MetaData, Table, Text, create_engine, text
from ma_backtesting import load_config


config, PROJECT_ROOT = load_config()

# Constants
DATA_DIR = PROJECT_ROOT / config["dir_paths"]["data"]

# Create an engine for an sqlite db
engine = create_engine(f"sqlite:///{DATA_DIR}/test.db", future = True)
metadata = MetaData()

# Create the table in metadata
prices = Table(
    "prices",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("ticker", Text, nullable=False),
    Column("date", Date, nullable=False),
    Column("open", Float),
    Column("high", Float),
    Column("low", Float),
    Column("close", Float),
    Column("volume", Integer)
)

metadata.drop_all(engine) # reset the database
metadata.create_all(engine) # create the defined table above

# Loop through the tickers in the config
for ticker in config["basic_settings"]["stocks"]:
    # Insert from CSV into the table
    
    # Get CSV, and make a date and symbol column
    df = pd.read_csv(f"{DATA_DIR}/{ticker}_OHLCV.csv", index_col=0)
    df["date"] = df.index
    df["symbol"] = ticker
    

    # Insert the dataframe into the db 
    with engine.begin() as conn:
        # Insert statement template
        insert_stmt = text("""
            INSERT INTO prices (ticker, date, open, high, low, close, volume)
            VALUES (:ticker, :date, :open, :high, :low, :close, :volume)
        """)

        # Loop through the rows in the data frame and run the insert statement 
        for row in df.itertuples(index = False):
            conn.execute(
                insert_stmt,
                {
                    "ticker": row.symbol,
                    "date": row.date,
                    "open": row.open,
                    "high": row.high,
                    "low": row.low,
                    "close": row.close,
                    "volume": row.volume,
                }, # binding values
            )

# To use the SQLite CLI to check if we inserted properly do sqlite3 data/test.db
# then do SELECT * FROM prices LIMIT 5;
# test querries:
# SELECT open, close FROM prices WHERE ticker = 'MSFT' AND date = '2009-04-28'
# answer from csv: 20.25, 19.93
# SELECT volume FROM prices WHERE ticker = 'SPY' AND date = '2024-03-20'
# answer from csv: 69594574
# SELECT ticker, high, low FROM prices WHERE date = '2016-08-23'
# answer from csvs: 
#                   IBM  161.34 160.23
#                   AAPL 109.32 108.53
#                   SPY  219.60 218.90                     
#                   MSFT  58.18  57.85
#                   NVDA  63.32  62.73
