-- FinFlow Core OLTP Relational Database Schema Structure

-- 1. Dim/Lookup Table: Core Financial Assets Matrix
CREATE TABLE IF NOT EXISTS instruments (
    ticker VARCHAR(10) PRIMARY KEY,
    asset_class VARCHAR(20) DEFAULT 'Equity',
    currency VARCHAR(5) DEFAULT 'USD',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Transaction/Fact Table: Historical Daily Equity Market Metrics
CREATE TABLE IF NOT EXISTS daily_stock_prices (
    price_id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) REFERENCES instruments(ticker) ON DELETE CASCADE,
    trade_date DATE NOT NULL,
    open_price NUMERIC(12, 4),
    high_price NUMERIC(12, 4),
    low_price NUMERIC(12, 4),
    close_price NUMERIC(12, 4),
    volume BIGINT,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_ticker_date UNIQUE (ticker, trade_date)
);

-- Seed metadata baseline lookup arrays
INSERT INTO instruments (ticker, asset_class, currency) 
VALUES 
('AAPL', 'Equity', 'USD'),
('MSFT', 'Equity', 'USD'),
('GOOGL', 'Equity', 'USD'),
('TSLA', 'Equity', 'USD')
ON CONFLICT (ticker) DO NOTHING;