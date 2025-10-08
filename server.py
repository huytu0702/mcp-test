import os
import httpx
from datetime import datetime
from typing import Optional
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()
# Initialize FastMCP server
mcp = FastMCP("Exchange Rates API")


# Load environment variables from .env file


# API configuration
API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data"


def get_headers():
    """Get headers for API requests"""
    return {"apikey": API_KEY}


@mcp.tool()
async def get_available_currencies() -> dict:
    """
    Get all available currency symbols and their names.

    Returns:
        Dictionary with success status and available currency symbols
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{BASE_URL}/symbols", headers=get_headers())
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_latest_rates(base: str = "USD", symbols: Optional[str] = None) -> dict:
    """
    Get the latest exchange rates for specified currencies.

    Args:
        base: Base currency code (default: USD)
        symbols: Comma-separated list of currency codes to get rates for (optional)

    Returns:
        Dictionary with latest exchange rates
    """
    params = {"base": base}
    if symbols:
        params["symbols"] = symbols

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/latest", headers=get_headers(), params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def convert_currency(
    from_currency: str, to_currency: str, amount: float, date: Optional[str] = None
) -> dict:
    """
    Convert an amount from one currency to another.

    Args:
        from_currency: Source currency code (e.g., USD)
        to_currency: Target currency code (e.g., EUR)
        amount: Amount to convert
        date: Optional date in YYYY-MM-DD format for historical conversion

    Returns:
        Dictionary with conversion result
    """
    params = {"from": from_currency, "to": to_currency, "amount": amount}

    if date:
        params["date"] = date

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/convert", headers=get_headers(), params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_historical_rates(
    date: str, base: str = "USD", symbols: Optional[str] = None
) -> dict:
    """
    Get historical exchange rates for a specific date.

    Args:
        date: Date in YYYY-MM-DD format
        base: Base currency code (default: USD)
        symbols: Comma-separated list of currency codes (optional)

    Returns:
        Dictionary with historical exchange rates
    """
    params = {"base": base}
    if symbols:
        params["symbols"] = symbols

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/{date}", headers=get_headers(), params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_timeseries_data(
    start_date: str, end_date: str, base: str = "USD", symbols: Optional[str] = None
) -> dict:
    """
    Get daily historical exchange rates between two dates.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        base: Base currency code (default: USD)
        symbols: Comma-separated list of currency codes (optional)

    Returns:
        Dictionary with timeseries exchange rate data
    """
    params = {"start_date": start_date, "end_date": end_date, "base": base}

    if symbols:
        params["symbols"] = symbols

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/timeseries", headers=get_headers(), params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_fluctuation_data(
    start_date: str, end_date: str, base: str = "USD", symbols: Optional[str] = None
) -> dict:
    """
    Get currency fluctuation data between two dates.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        base: Base currency code (default: USD)
        symbols: Comma-separated list of currency codes (optional)

    Returns:
        Dictionary with fluctuation data including change and change_pct
    """
    params = {"start_date": start_date, "end_date": end_date, "base": base}

    if symbols:
        params["symbols"] = symbols

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/fluctuation", headers=get_headers(), params=params
        )
        response.raise_for_status()
        return response.json()


# Add a resource to provide API information
@mcp.resource("exchangerates://info")
def get_api_info() -> str:
    """Get information about the Exchange Rates API"""
    return """Exchange Rates Data API
    
This MCP server provides access to real-time and historical exchange rate data for 170+ world currencies.

Available Tools:
- get_available_currencies: Get all available currency symbols
- get_latest_rates: Get real-time exchange rates
- convert_currency: Convert amounts between currencies
- get_historical_rates: Get exchange rates for a specific date
- get_timeseries_data: Get daily rates between two dates
- get_fluctuation_data: Get currency fluctuation statistics

Data Source: apilayer.com/exchangerates_data
"""


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
