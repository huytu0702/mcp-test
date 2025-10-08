"""
Test script for the Exchange Rates MCP Server
Run this to verify the server is working correctly
"""

import asyncio
import os
from server import (
    get_available_currencies,
    get_latest_rates,
    convert_currency,
    get_historical_rates,
    get_timeseries_data,
    get_fluctuation_data,
)


async def test_all_endpoints():
    """Test all available endpoints"""

    print("=" * 60)
    print("Testing Exchange Rates MCP Server")
    print("=" * 60)

    try:
        # Test 1: Get available currencies
        print("\n1. Testing get_available_currencies...")
        currencies = await get_available_currencies()
        if currencies.get("success"):
            print(f"✓ Found {len(currencies.get('symbols', {}))} currencies")
            # Show first 5 currencies
            symbols = list(currencies.get("symbols", {}).items())[:5]
            for code, name in symbols:
                print(f"  - {code}: {name}")
        else:
            print("✗ Failed to get currencies")

        # Test 2: Get latest rates
        print("\n2. Testing get_latest_rates (USD to EUR, GBP, JPY)...")
        latest = await get_latest_rates(base="USD", symbols="EUR,GBP,JPY")
        if latest.get("success"):
            rates = latest.get("rates", {})
            print(f"✓ Latest rates (base: {latest.get('base')}):")
            for currency, rate in rates.items():
                print(f"  - {currency}: {rate}")
        else:
            print("✗ Failed to get latest rates")

        # Test 3: Convert currency
        print("\n3. Testing convert_currency (100 USD to EUR)...")
        conversion = await convert_currency(
            from_currency="USD", to_currency="EUR", amount=100
        )
        if conversion.get("success"):
            print(f"✓ Conversion result:")
            print(
                f"  - From: {conversion.get('query', {}).get('from')} {conversion.get('query', {}).get('amount')}"
            )
            print(
                f"  - To: {conversion.get('query', {}).get('to')} {conversion.get('result')}"
            )
            print(f"  - Rate: {conversion.get('info', {}).get('rate')}")
        else:
            print("✗ Failed to convert currency")

        # Test 4: Get historical rates
        print("\n4. Testing get_historical_rates (2024-01-01)...")
        historical = await get_historical_rates(
            date="2024-01-01", base="USD", symbols="EUR,GBP"
        )
        if historical.get("success"):
            print(f"✓ Historical rates for {historical.get('date')}:")
            for currency, rate in historical.get("rates", {}).items():
                print(f"  - {currency}: {rate}")
        else:
            print("✗ Failed to get historical rates")

        # Test 5: Get timeseries data
        print("\n5. Testing get_timeseries_data (2024-01-01 to 2024-01-07)...")
        timeseries = await get_timeseries_data(
            start_date="2024-01-01", end_date="2024-01-07", base="USD", symbols="EUR"
        )
        if timeseries.get("success"):
            print(f"✓ Timeseries data:")
            rates_data = timeseries.get("rates", {})
            for date, rates in list(rates_data.items())[:3]:
                print(f"  - {date}: EUR = {rates.get('EUR')}")
            if len(rates_data) > 3:
                print(f"  ... and {len(rates_data) - 3} more days")
        else:
            print("✗ Failed to get timeseries data")

        # Test 6: Get fluctuation data
        print("\n6. Testing get_fluctuation_data (2024-01-01 to 2024-01-31)...")
        fluctuation = await get_fluctuation_data(
            start_date="2024-01-01",
            end_date="2024-01-31",
            base="USD",
            symbols="EUR,GBP",
        )
        if fluctuation.get("success"):
            print(f"✓ Fluctuation data:")
            for currency, data in fluctuation.get("rates", {}).items():
                print(f"  - {currency}:")
                print(f"    Start: {data.get('start_rate')}")
                print(f"    End: {data.get('end_rate')}")
                print(f"    Change: {data.get('change')}")
                print(f"    Change %: {data.get('change_pct')}%")
        else:
            print("✗ Failed to get fluctuation data")

        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # Check if API key is set
    api_key = os.getenv("EXCHANGE_RATES_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("⚠️  Warning: EXCHANGE_RATES_API_KEY not set properly")
        print("Please set the environment variable or update the .env file")
        print()

    # Run tests
    asyncio.run(test_all_endpoints())
