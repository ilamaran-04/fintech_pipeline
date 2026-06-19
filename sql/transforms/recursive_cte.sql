-- 3. Advanced Transformation: Recursive Trading Calendar Sequence Generator

WITH RECURSIVE trading_calendar AS (
    -- Anchor Member: Grab the earliest available market trade date from your database
    SELECT 
        MIN(trade_date) AS calendar_date,
        1 AS day_sequence
    FROM daily_stock_prices
    
    UNION ALL
    
    -- Recursive Member: Increment the calendar day forward by 1 step sequentially
    SELECT 
        (calendar_date + INTERVAL '1 day')::DATE,
        day_sequence + 1
    FROM trading_calendar
    -- Termination Criteria: Stop looping exactly at 14 consecutive calendar horizons
    WHERE day_sequence < 14
)

SELECT 
    day_sequence,
    calendar_date,
    TO_CHAR(calendar_date, 'Day') AS day_of_week
FROM trading_calendar
ORDER BY day_sequence ASC;