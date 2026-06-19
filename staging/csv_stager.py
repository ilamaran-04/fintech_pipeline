import os
import json
import csv
from datetime import datetime
from config.config import RAW_DATA_DIR, STAGING_DATA_DIR, TICKERS

print("Starting FinFlow Staging Engine Transformation Module...")

def stage_raw_json_to_csv(ticker: str) -> str:
    date_str = datetime.now().strftime("%Y%m%d")
    json_filename = f"{ticker}_{date_str}.json"
    json_filepath = os.path.join(RAW_DATA_DIR, json_filename)
    
    csv_filename = f"{ticker}_staged.csv"
    csv_filepath = os.path.join(STAGING_DATA_DIR, csv_filename)
    
    if not os.path.exists(json_filepath):
        print(f" [ERROR] Raw file not found at: {json_filepath}")
        return ""
        
    try:
        with open(json_filepath, "r") as json_file:
            payload = json.load(json_file)
            
        time_series = payload.get("Time Series (Daily)", {})
        if not time_series:
            print(f" [ERROR] 'Time Series (Daily)' key missing in JSON structure.")
            return ""
            
        fieldnames = ["ticker", "trade_date", "open_price", "high_price", "low_price", "close_price", "volume"]
        
        with open(csv_filepath, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            
            for trade_date, daily_metrics in time_series.items():
                writer.writerow({
                    "ticker": ticker,
                    "trade_date": trade_date,
                    "open_price": daily_metrics.get("1. open"),
                    "high_price": daily_metrics.get("2. high"),
                    "low_price": daily_metrics.get("3. low"),
                    "close_price": daily_metrics.get("4. close"),
                    "volume": daily_metrics.get("5. volume")
                })
                
        print(f" [SUCCESS] Flattened rows successfully written to staging: {csv_filepath}")
        return csv_filepath
    except Exception as e:
        print(f" [ERROR] Staging processing failed: {e}")
        return ""

if __name__ == "__main__":
    print("\n--- Running Staging Engine Unit Test In Standalone Mode ---")
    stage_raw_json_to_csv(TICKERS[0])