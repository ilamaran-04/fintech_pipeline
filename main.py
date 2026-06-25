import sys
import time
from config.config import TICKERS

# Explicitly importing your verified pipeline modules
from extract.api_extractor import fetch_daily_stock, save_raw_json
from staging.csv_stager import stage_raw_json_to_csv
from database.db_loader import load_staged_csv_to_postgres

def run_pipeline():
    print("=" * 60)
    print("      FINFLOW END-TO-END DATA WAREHOUSE PIPELINE      ")
    print("=" * 60)
    print(f"Target Portfolio Tickers: {TICKERS}\n")
    
    success_count = 0
    
    for ticker in TICKERS:
        print(f"\nKicking off ETL Pipeline for Asset: [{ticker}]")
        print("-" * 40)
        
        try:
            # Phase 1: Extraction
            print(f" [1/3] Extracting raw data from cloud API...")
            raw_payload = fetch_daily_stock(ticker)
            
            # Save whatever the API returned immediately so we can inspect it!
            save_raw_json(ticker, raw_payload)
            
            # Now validate if it has the data we want
            if not raw_payload or "Time Series (Daily)" not in raw_payload:
                raise ValueError(f"API payload missing expected time-series keys for {ticker}.")
            
            # Phase 2: Transformation & Staging
            print(f" [2/3] Transforming raw records into staged CSV schema...")
            csv_path = stage_raw_json_to_csv(ticker)
            
            if not csv_path:
                raise FileNotFoundError(f"Staging failed to generate valid CSV for {ticker}.")
            
            # Phase 3: Database Loading
            print(f" [3/3] Streaming staged CSV lines into PostgreSQL OLTP...")
            load_staged_csv_to_postgres(ticker)
            
            print(f"[COMPLETED] Full ETL cycle successful for {ticker}!")
            success_count += 1
            
            # Enforce breathing room after a successful run
            print(f" [INFO] Pausing for 15 seconds to respect API limits...")
            time.sleep(15)
            
        except Exception as e:
            print(f"[CRITICAL FAILURE] Pipeline broke for asset {ticker}: {e}")
            # Enforce breathing room even if it fails!
            print(f" [INFO] Pausing for 15 seconds before moving to next asset...")
            time.sleep(15)
            continue
            
    print("\n" + "=" * 60)
    print(f"Pipeline Execution Summary: {success_count}/{len(TICKERS)} Assets Successfully Processed.")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()