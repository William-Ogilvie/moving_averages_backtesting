# Moving Averages Backtesting

## Docker commands
```bash
docker build -t ma-backtest --build-arg ENV_FILE=environment.yml .
```

```bash
docker run -it --rm --mount type=bind,src="$(pwd)",dst=/app ma-backtest
```

Will need to install python package:

```bash
pip install -e .
```


## SQLite CLI

```bash
sqlite3 data/test.db
```

## .env file for keys

You will need to create a .env file contaning your Alpha Vantage API key, store as:

```env
ALPHAVANTAGEAPIKEY=[your key]
```

### Expo of strategy
https://www.investopedia.com/ask/answers/121114/what-difference-between-golden-cross-and-death-cross-pattern.asp