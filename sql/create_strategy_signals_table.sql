CREATE TABLE IF NOT EXISTS strategy_signals AS
SELECT
    ticker,
    date,
    close,
    ma50,
    ma200,

    -- Previous day's MA values to detect crossovers
    LAG(ma50) OVER (PARTITION BY ticker ORDER BY date) AS prev_ma50,
    LAG(ma200) OVER (PARTITION BY ticker ORDER BY date) AS prev_ma200,
    -- Signal logic: Golden cross is when ma50 crosses ma200 upwards, signals
    -- bullish market so buy, death cross is when ma200 crosses ma50 upwards, signals
    -- bearish market so sell
    CASE
        WHEN ma50 > ma200 AND LAG(ma50) OVER (PARTITION BY ticker ORDER BY date) <= LAG(ma200) OVER (PARTITION BY ticker ORDER BY date) 
        THEN 'BUY'
        WHEN ma50 < ma200 AND LAG(ma50) OVER (PARTITION BY ticker ORDER BY date) >= LAG(ma200) OVER (PARTITION BY ticker ORDER BY date)  
        THEN 'SELL'
        ELSE 'HOLD'
    END AS signal
FROM prices_indicators
ORDER BY ticker, date;