-- Multi-stage CTE: identify outperforming stocks based on monthly volume and close prices

WITH

-- CTE 1: Calculate average close and total volume per stock per month
monthly_avg AS (
    SELECT
        ticker,
        DATE_TRUNC('month', trade_date) AS trading_month,
        ROUND(AVG(close_price), 4) AS avg_monthly_close,
        SUM(volume) AS total_monthly_volume
    FROM daily_stock_prices
    GROUP BY ticker, DATE_TRUNC('month', trade_date)
),

-- CTE 2: Flag months where cumulative asset volume exceeded a high benchmark (e.g., 500 million)
high_volume_months AS (
    SELECT
        ma.ticker,
        ma.trading_month,
        ma.avg_monthly_close,
        ma.total_monthly_volume,
        CASE 
            WHEN ma.total_monthly_volume > 500000000 THEN 'HIGH' 
            ELSE 'NORMAL'
        END AS volume_flag
    FROM monthly_avg ma
),

-- CTE 3: Rank each stock within its respective month by its average close price
ranked_stocks AS (
    SELECT
        hvm.*,
        DENSE_RANK() OVER (
            PARTITION BY hvm.trading_month
            ORDER BY hvm.avg_monthly_close DESC
        ) AS price_rank
    FROM high_volume_months hvm
)

SELECT * FROM ranked_stocks
WHERE price_rank <= 3
ORDER BY trading_month DESC, price_rank;