#!/usr/bin/env python3
"""
Binance Data Fetcher Starter
Allows user to configure runtime and save intervals for continuous data fetching
"""

import sys
import os

# Add the binance_data_fetcher directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'binance_data_fetcher'))

try:
    from fetch_data import start_fetcher
except ImportError as e:
    print("Error: Could not import the fetcher module.")
    print(f"Make sure 'binance_data_fetcher/fetch_data.py' exists in the project directory.")
    print(f"Error details: {e}")
    sys.exit(1)

def get_user_input():
    """Get runtime and save interval from user"""
    print("=" * 60)
    print("         BINANCE DATA FETCHER CONFIGURATION")
    print("=" * 60)

    # Get runtime hours
    while True:
        try:
            runtime_input = input("\n1. How many hours should the program run continuously? ")
            runtime_hours = float(runtime_input)
            if runtime_hours <= 0:
                print("   Error: Please enter a positive number.")
                continue
            break
        except ValueError:
            print("   Error: Please enter a valid number.")

    # Get save interval
    while True:
        try:
            interval_input = input("\n2. What is the save interval in minutes? ")
            save_interval_minutes = float(interval_input)
            if save_interval_minutes <= 0:
                print("   Error: Please enter a positive number.")
                continue
            break
        except ValueError:
            print("   Error: Please enter a valid number.")

    return runtime_hours, save_interval_minutes

def display_summary(runtime_hours, save_interval_minutes):
    """Display configuration summary and ask for confirmation"""
    print("\n" + "=" * 60)
    print("                CONFIGURATION SUMMARY")
    print("=" * 60)
    print(f"Runtime Duration:    {runtime_hours} hours")
    print(f"Save Interval:       {save_interval_minutes} minutes")

    # Calculate estimated number of fetches
    total_minutes = runtime_hours * 60
    estimated_fetches = int(total_minutes / save_interval_minutes) + 1
    print(f"Estimated Fetches:   ~{estimated_fetches} times")

    # Calculate estimated number of files
    files_per_fetch = 6  # Number of different data types fetched
    estimated_total_files = estimated_fetches * files_per_fetch
    print(f"Estimated Files:     ~{estimated_total_files} JSON files")

    print("\nFile Naming:")
    print("✓ All files saved with unique timestamps")
    print("✓ No files will be overwritten")
    print("✓ Format: [data_type]_YYYYMMDD_HHMMSS.json")

    print("=" * 60)

    while True:
        confirm = input("\nProceed with this configuration? (y/n): ").lower().strip()
        if confirm in ['y', 'yes']:
            return True
        elif confirm in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def main():
    """Main function"""
    try:
        print("Welcome to Binance Data Fetcher!")

        while True:
            # Get user configuration
            runtime_hours, save_interval_minutes = get_user_input()

            # Display summary and get confirmation
            if display_summary(runtime_hours, save_interval_minutes):
                break
            else:
                print("\nLet's reconfigure...")

        print("\nStarting Binance Data Fetcher...")
        print("Press Ctrl+C to stop the program early if needed.")

        # Show example of files that will be created
        from datetime import datetime
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"\nExample files that will be created:")
        print(f"  • exchange_info_{current_time}.json")
        print(f"  • ticker_24hr_all_{current_time}.json")
        print(f"  • ticker_price_all_{current_time}.json")
        print(f"  • orderbook_BTCUSDT_{current_time}.json")
        print(f"  • trades_BTCUSDT_{current_time}.json")
        print(f"  • klines_BTCUSDT_1h_{current_time}.json")
        print(f"\nAll files will be saved in: binance_data/ folder")
        print("Each fetch creates 6 files with unique timestamps.\n")

        # Start the fetcher with user configuration
        start_fetcher(runtime_hours, save_interval_minutes)

        print("\nProgram completed successfully!")

    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
        print("Data fetcher stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
