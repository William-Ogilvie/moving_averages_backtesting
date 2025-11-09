# Moving Averages Backtesting

## Docker commands
```bash
docker build -t ma-backtest --build-arg ENV_FILE=environment.yml .
```

```bash
docker run -it --rm --mount type=bind,src="$(pwd)",dst=/app ma-backtest
```

