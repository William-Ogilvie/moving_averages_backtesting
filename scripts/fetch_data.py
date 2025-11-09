"""
fetch_data.py
==============
This module querries the Alpha Vantage API (https://www.alphavantage.co) for open, high,
low, close and volume for a series of tickers on a daily time scale going back 20+ years.

It cleans the data and then saves it as a csv into the data directory.
"""


# Using alpha vantage to get financial data
# https://www.alphavantage.co/documentation/
import requests
import pandas as pd
from dotenv import load_dotenv
import os
from ma_backtesting import load_config

# Get Alpha Vantage api key
load_dotenv() # loads .env file
api_key = os.getenv("ALPHAVANTAGE_API_KEY")

# Load config
config, PROJECT_ROOT = load_config()

# Constants
DATA_DIR = PROJECT_ROOT / config["dir_paths"]["data"]

# Choose which stocks to look at, IBM, Apple, S&P 500, Microsoft, Nvidia
stocks = config["basic_settings"]["stocks"]

def query_stock(ticker: str) -> dict:
    """ Function querries the Alpha Vantage stock market API https://www.alphavantage.co/ for the requested stock

    Args:
        ticker (str): ticker for requested stock 

    Returns:
        dict: returned dictionary of data + meta data
    """    
    
    # Full 20+ years of daily OHLCV data
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey=L0BEQZ1GS5G1KJQT"
    r = requests.get(url)

    # Check API call return
    print("Response status code:", r.status_code)
    
    return r.json()

# Loop through the stocks, query the api, clean the data and save to a csv
for ticker in stocks:

    # Get data
    data = query_stock(ticker)

    # Print keys
    print(data.keys())

    # Extract keys
    meta_data_key = list(data.keys())[0]
    time_series_key = list(data.keys())[1]

    # Separate time series data from meta data
    meta_data = data[meta_data_key]
    time_series = data[time_series_key]

    # Print meta data and time series
    print(meta_data)
    print(time_series)

    # Convert time series to data frame
    ts_df = pd.DataFrame.from_dict(time_series, orient = "index")

    print(ts_df.head())
    print(ts_df.columns)

    # It is worth changing the column names from "1. open" to just "open"
    ts_df.columns = [col.split('. ')[-1] for col in ts_df.columns]

    print(ts_df.columns)
    print(ts_df["open"].dtype)

    # Check for null values it seems there are none which is handy
    print(ts_df.isnull().sum())

    # If there were any null values it would be worth using linear interpolation to try and fill them
    # this obviously isn't perfect but as we don't anticipate any null values to begin with it could be a good
    # safe check just in case one or two slip in

    # First convert open, high, low, close to floats, then convert volumne to an integer
    float_cols = ["open", "high", "low", "close"]
    int_cols = ["volume"]

    ts_df[float_cols] = ts_df[float_cols].astype("float64")
    ts_df[int_cols] = ts_df[int_cols].astype("int64")

    ts_df.interpolate(method = "linear", inplace = True)

    # Check data still looks ok, that we don't have any null values and that types converted properly
    print(ts_df.head())
    print(ts_df.isnull().sum())
    print(ts_df["open"].dtype)
    print(ts_df["volume"].dtype)

    # Export data to csv
    ts_df.to_csv(DATA_DIR / f"{ticker}_OHLCV.csv")



"""
Linear interpolation exple
df_exple = pd.DataFrame({
    "col_1": [0, None, None, 3]
})

df_exple.interpolate(method="linear", inplace = True)
print(df_exple.head())
"""
