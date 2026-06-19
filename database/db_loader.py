# database/db_loader.py
import os
import csv
from sqlalchemy import create_engine, text
from config.config import DB_CONFIG, STAGING_DATA_DIR, TICKERS

print("Starting FinFlow Database Loading Warehouse Module...")

def load_staged_csv_to_postgres(ticker: str):
    """
    Reads structured time-series data from data/staging/ and loads it
    into the local PostgreSQL OLTP daily_stock_prices table.
    """
    csv_filename = f"{ticker}_staged.csv"
    csv_filepath = os.path.join(STAGING_DATA_DIR, csv_filename)
    
    if not os.path.exists(csv_filepath):
        print(f" [ERROR] Target staging CSV not found at: {csv_filepath}")
        return
        
    # Build connection string from config settings
    conn_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    engine = create_engine(conn_string)
    
    insert_query = text("""
        INSERT INTO daily_stock_prices (ticker, trade_date, open_price, high_price, low_price, close_price, volume)
        VALUES (:ticker, :trade_date, :open, :high, :low, :close, :volume)
        ON CONFLICT (ticker, trade_date) DO NOTHING;
    """)
    
    records_loaded = 0
    try:
        with open(csv_filepath, mode='r') as file:
            reader = csv.DictReader(file)
            
            with engine.begin() as connection:  # Automatically manages a single transaction commit/rollback
                for row in reader:
                    connection.execute(insert_query, {
                        "ticker": row["ticker"],
                        "trade_date": row["trade_date"],
                        "open": float(row["open_price"]) if row["open_price"] else None,
                        "high": float(row["high_price"]) if row["high_price"] else None,
                        "low": float(row["low_price"]) if row["low_price"] else None,
                        "close": float(row["close_price"]) if row["close_price"] else None,
                        "volume": int(row["volume"]) if row["volume"] else None
                    })
                    records_loaded += 1
                    
        print(f" [SUCCESS] Loaded {records_loaded} market rows into PostgreSQL for asset: {ticker}")
    except Exception as e:
        print(f" [ERROR] Data warehouse loading operation failed for {ticker}: {e}")
    finally:
        engine.dispose()
        print(f" [INFO] Database pipeline connection thread pool terminated for ticker: {ticker}")

if __name__ == "__main__":
    print("\n--- Running Database Warehouse Loader Unit Test In Standalone Mode ---")
    test_ticker = TICKERS[0]  # 'AAPL'
    load_staged_csv_to_postgres(test_ticker)