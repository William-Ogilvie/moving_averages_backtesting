-- Query creates moving averages for each ticker into a new table called prices_indicators
CREATE TABLE IF NOT EXISTS prices_indicators AS
SELECT
    p.id,
    p.ticker,
    p.date,
    p.open,
    p.high,
    p.low,
    p.close,
    p.volume,
    -- Moving averages
    AVG(p.close) OVER (
        PARTITION BY p.ticker
        ORDER BY p.date
        ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
    ) AS ma10,
    AVG(p.close) OVER (
        PARTITION BY p.ticker
        ORDER BY p.date
        ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
    ) AS ma20,
    AVG(p.close) OVER (
        PARTITION BY p.ticker
        ORDER BY p.date
        ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
    ) AS ma50,
    AVG(p.close) OVER (
        PARTITION BY p.ticker
        ORDER BY p.date
        ROWS BETWEEN 200 PRECEDING AND CURRENT ROW
    ) AS ma200
FROM prices p;

