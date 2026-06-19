import sys
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
            # Phase 1: Extraction & Saving Raw JSON
            print(f" [1/3] Extracting raw data from cloud API...")
            raw_payload = fetch_daily_stock(ticker)
            
            if raw_payload and "Time Series (Daily)" in raw_payload:
                save_raw_json(ticker, raw_payload)
            else:
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
            
        except Exception as e:
            print(f"[CRITICAL FAILURE] Pipeline broke for asset {ticker}: {e}")
            continue
            
    print("\n" + "=" * 60)
    print(f"Pipeline Execution Summary: {success_count}/{len(TICKERS)} Assets Successfully Processed.")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()