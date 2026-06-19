import requests
import json
import os
from datetime import datetime
# Import our centralized system configurations
from config.config import API_KEY, BASE_URL, TICKERS, RAW_DATA_DIR

print("Starting FinFlow Extraction Engine Ingestion Module...")

def fetch_daily_stock(ticker: str) -> dict:
    """
    Fetches daily historical stock price data for a given ticker from Alpha Vantage.
    Returns the raw JSON response payload as a dictionary.
    """
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "outputsize": "compact", # Pulls the last 100 historical trading days
        "apikey": API_KEY
    }
    
    try:
        # Executing the live API network connection request
        response = requests.get(BASE_URL, params=params, timeout=15)
        response.raise_for_status() # Instantly raises HTTPError for 4xx/5xx responses
        data = response.json()
        
        # Validating API provider payload messages
        if "Error Message" in data:
            raise ValueError(f"Invalid ticker symbol or malformed request for {ticker}.")
        if "Note" in data:
            raise RuntimeError("Alpha Vantage API standard rate limit hit. Please retry in 1 minute.")
            
    except requests.exceptions.ConnectionError as e:
        print(f" [ERROR] Network connection failure for {ticker}: {e}")
        raise
    except requests.exceptions.Timeout as e:
        print(f" [ERROR] API connection timed out for {ticker}: {e}")
        raise
    except requests.exceptions.HTTPError as e:
        print(f" [ERROR] HTTP error code returned for {ticker}: {e}")
        raise
    except Exception as e:
        print(f" [ERROR] Unexpected exception occurred: {e}")
        raise
    else:
        print(f"[SUCCESS] API payload downloaded perfectly for ticker: {ticker}")
        return data
    finally:
        print(f" [INFO] Network thread call completed for {ticker} at {datetime.now()}")

def save_raw_json(ticker: str, data: dict) -> str:
    """
    Saves the fetched raw JSON dictionary payload into the data/raw storage folder.
    """
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{ticker}_{date_str}.json"
    filepath = os.path.join(RAW_DATA_DIR, filename)
    
    try:
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f" [ERROR] Failed to write file to storage disk for {ticker}: {e}")
        raise
    else:
        print(f" [SUCCESS] Immutable raw payload archived successfully at: {filepath}")
        return filepath
    finally:
        print(f" [INFO] File-system save cycle concluded for {ticker}")

# Operational unit test execution boundary
if __name__ == "__main__":
    print("\n--- Running Extraction Engine Unit Test In Standalone Mode ---")
    # Using the first ticker 'AAPL' from our config tracking matrix to verify connection
    test_ticker = TICKERS[0] 
    try:
        raw_payload = fetch_daily_stock(test_ticker)
        # Only attempt to save file if data was successfully pulled
        if raw_payload and "Time Series (Daily)" in raw_payload:
            save_raw_json(test_ticker, raw_payload)
    except Exception as error:
        print(f"\n Standalone extraction check stopped: {error}")