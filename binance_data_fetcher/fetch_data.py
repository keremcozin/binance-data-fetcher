#!/usr/bin/env python3
"""
Simple Binance Data Fetcher
Fetches data from Binance API and saves it as JSON files
"""

import requests
import json
import os
from datetime import datetime
import time

class BinanceDataFetcher:
    def __init__(self, runtime_hours=1, save_interval_minutes=60):
        self.base_url = "https://api.binance.com"

        # Get the correct path for binance_data folder
        # If called from root folder, save to binance_data/
        # If called from binance_data_fetcher folder, save to ../binance_data/
        current_dir = os.getcwd()
        if current_dir.endswith('binance_data_fetcher'):
            self.data_folder = "../binance_data"
        else:
            self.data_folder = "binance_data"

        self.runtime_hours = runtime_hours
        self.save_interval_minutes = save_interval_minutes

        # Create data folder if it doesn't exist
        os.makedirs(self.data_folder, exist_ok=True)
        print(f"Data will be saved to: {os.path.abspath(self.data_folder)}")

    def fetch_and_save(self, endpoint, filename_prefix):
        """Fetch data from endpoint and save to JSON file"""
        try:
            print(f"Fetching data from {endpoint}...")
            response = requests.get(f"{self.base_url}{endpoint}")
            response.raise_for_status()

            # Get current timestamp for filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename_prefix}_{timestamp}.json"
            filepath = os.path.join(self.data_folder, filename)

            # Save original JSON response
            with open(filepath, 'w') as f:
                json.dump(response.json(), f, indent=2)

            print(f"✓ Data saved to: {filepath}")
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching {endpoint}: {e}")
            return None
        except Exception as e:
            print(f"✗ Error saving data: {e}")
            return None

    def run_continuous_fetch(self):
        """Run the fetcher continuously based on specified runtime and interval"""
        runtime_seconds = self.runtime_hours * 3600
        interval_seconds = self.save_interval_minutes * 60

        start_time = time.time()
        end_time = start_time + runtime_seconds

        print(f"Starting continuous data fetch...")
        print(f"Runtime: {self.runtime_hours} hours")
        print(f"Save interval: {self.save_interval_minutes} minutes")
        print(f"Will stop at: {datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        fetch_count = 0

        while time.time() < end_time:
            fetch_count += 1
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n[{current_time}] Fetch #{fetch_count}")

            # Perform the data fetch
            self.fetch_all_data()

            # Calculate remaining time
            remaining_seconds = end_time - time.time()
            if remaining_seconds <= 0:
                break

            # Wait for the next interval (but don't exceed end time)
            sleep_time = min(interval_seconds, remaining_seconds)

            if sleep_time > 0:
                next_fetch_time = datetime.fromtimestamp(time.time() + sleep_time).strftime('%Y-%m-%d %H:%M:%S')
                print(f"Next fetch scheduled at: {next_fetch_time}")
                print(f"Sleeping for {sleep_time/60:.1f} minutes...")
                time.sleep(sleep_time)

        print("\n" + "=" * 60)
        print(f"Continuous fetch completed!")
        print(f"Total fetches performed: {fetch_count}")
        print(f"Total runtime: {(time.time() - start_time)/3600:.2f} hours")

    def fetch_all_data(self):
        """Fetch various types of data from Binance API"""

        # 1. Exchange Information
        self.fetch_and_save("/api/v3/exchangeInfo", "exchange_info")
        time.sleep(0.1)  # Small delay to be respectful to API

        # 2. 24hr Ticker Statistics (all symbols)
        self.fetch_and_save("/api/v3/ticker/24hr", "ticker_24hr_all")
        time.sleep(0.1)

        # 3. Current prices for all symbols
        self.fetch_and_save("/api/v3/ticker/price", "ticker_price_all")
        time.sleep(0.1)

        # 4. Order book for BTCUSDT (popular pair)
        self.fetch_and_save("/api/v3/depth?symbol=BTCUSDT&limit=100", "orderbook_BTCUSDT")
        time.sleep(0.1)

        # 5. Recent trades for BTCUSDT
        self.fetch_and_save("/api/v3/trades?symbol=BTCUSDT&limit=100", "trades_BTCUSDT")
        time.sleep(0.1)

        # 6. Kline/Candlestick data for BTCUSDT (1 hour intervals, last 24 hours)
        self.fetch_and_save("/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=24", "klines_BTCUSDT_1h")

def main(runtime_hours=None, save_interval_minutes=None):
    """Main function"""
    if runtime_hours is None or save_interval_minutes is None:
        # Default single fetch if no parameters provided
        fetcher = BinanceDataFetcher()
        print("Starting single Binance data fetch...")
        print("=" * 50)
        fetcher.fetch_all_data()
        print("=" * 50)
        print("Data fetch completed!")
        print(f"All files saved in: {os.path.abspath(fetcher.data_folder)}")
    else:
        # Continuous fetch with provided parameters
        fetcher = BinanceDataFetcher(runtime_hours, save_interval_minutes)
        fetcher.run_continuous_fetch()

def start_fetcher(runtime_hours, save_interval_minutes):
    """Function to be called by external programs"""
    main(runtime_hours, save_interval_minutes)

if __name__ == "__main__":
    main()
