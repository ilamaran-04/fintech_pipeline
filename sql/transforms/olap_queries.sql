-- 1. Create the analytical summary table by flattening transactions and metadata
CREATE TABLE IF NOT EXISTS analytics_portfolio_summary AS
SELECT 
    i.ticker,
    i.asset_class,
    i.currency,
    DATE_TRUNC('month', p.trade_date)::DATE AS trading_month,
    p.close_price,
    p.volume
FROM daily_stock_prices p
JOIN instruments i ON i.ticker = p.ticker;

-- 2. Hierarchical portfolio analysis using ROLLUP [cite: 151, 351]
SELECT 
    asset_class,
    ticker,
    ROUND(AVG(close_price), 2) AS average_valuation,
    SUM(volume) AS total_shares_traded
FROM analytics_portfolio_summary
GROUP BY ROLLUP(asset_class, ticker)
ORDER BY asset_class NULLS LAST, ticker NULLS LAST;

-- 3. Multi-dimensional cross-aggregation using CUBE [cite: 151, 352]
SELECT 
    trading_month,
    ticker,
    SUM(volume) AS combined_volume
FROM analytics_portfolio_summary
GROUP BY CUBE(trading_month, ticker)
ORDER BY trading_month NULLS LAST, ticker NULLS LAST;