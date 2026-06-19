-- 1. Portfolio Analytics: Daily Volume Ranking, 7-Day Moving Averages, and Asset Returns [cite: 342, 343, 344]

SELECT
    i.ticker,
    p.trade_date,
    p.volume,
    -- Rank stocks by daily trading volume (RANK + PARTITION) [cite: 342]
    RANK() OVER (
        PARTITION BY p.trade_date
        ORDER BY p.volume DESC
    ) AS volume_rank,
    
    -- 7-day Moving Average of the closing price (ROWS BETWEEN) [cite: 343]
    ROUND(AVG(p.close_price) OVER (
        PARTITION BY i.ticker
        ORDER BY p.trade_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ), 4) AS moving_avg_7d,
    
    -- Capture previous day close price (LAG) [cite: 343]
    LAG(p.close_price, 1) OVER (
        PARTITION BY i.ticker
        ORDER BY p.trade_date
    ) AS prev_close,
    
    -- Calculate daily asset percentage change [cite: 343, 344]
    ROUND(
        (p.close_price - LAG(p.close_price, 1) OVER (
            PARTITION BY i.ticker ORDER BY p.trade_date
        )) / NULLIF(LAG(p.close_price, 1) OVER (
            PARTITION BY i.ticker ORDER BY p.trade_date
        ), 0) * 100, 2
    ) AS daily_pct_change

FROM daily_stock_prices p
JOIN instruments i ON i.ticker = p.ticker
ORDER BY p.trade_date DESC, volume_rank;