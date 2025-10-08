"""
Exchange Rates Data API MCP Server

This MCP server provides access to the Exchange Rates Data API from APILayer
through Model Context Protocol for integration with AI assistants.
"""

import os
import json
from datetime import datetime, date
from typing import Dict, List, Optional, Any
import requests
from fastmcp import FastMCP
from pydantic import BaseModel, Field

# Initialize FastMCP server
mcp = FastMCP("Exchange Rates Data API")

# API Configuration
API_KEY = "XcYKZNK5zwVVGGdnGA6Ye5MsdDEVrrgk"
BASE_URL = "https://api.apilayer.com/exchangerates_data"


class ExchangeRateResponse(BaseModel):
    """Response model for exchange rate data"""

    success: bool
    timestamp: int
    base: str
    date: str
    rates: Dict[str, float]


class SymbolResponse(BaseModel):
    """Response model for currency symbols"""

    success: bool
    symbols: Dict[str, str]


class ConvertResponse(BaseModel):
    """Response model for currency conversion"""

    success: bool
    query: Dict[str, Any]
    info: Dict[str, Any]
    result: float


class HistoricalResponse(BaseModel):
    """Response model for historical exchange rates"""

    success: bool
    historical: bool
    date: str
    timestamp: int
    base: str
    rates: Dict[str, float]


class TimeSeriesResponse(BaseModel):
    """Response model for time series data"""

    success: bool
    timeseries: bool
    start_date: str
    end_date: str
    base: str
    rates: Dict[str, Dict[str, float]]


class FluctuationResponse(BaseModel):
    """Response model for fluctuation data"""

    success: bool
    fluctuation: bool
    start_date: str
    end_date: str
    base: str
    rates: Dict[str, Dict[str, float]]


def make_api_request(endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Make a request to the Exchange Rates Data API"""
    url = f"{BASE_URL}{endpoint}"
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")


@mcp.tool()
def get_currency_symbols() -> str:
    """
    Get all available currency symbols and their descriptions.

    Returns:
        JSON string containing all available currencies and their names
    """
    try:
        data = make_api_request("/symbols")
        symbols = SymbolResponse(**data)

        if not symbols.success:
            return json.dumps({"error": "Failed to retrieve currency symbols"})

        # Format the response for better readability
        formatted_symbols = []
        for code, name in symbols.symbols.items():
            formatted_symbols.append(f"{code}: {name}")

        return json.dumps(
            {
                "success": True,
                "symbols": symbols.symbols,
                "formatted_list": formatted_symbols,
                "total_currencies": len(symbols.symbols),
            },
            indent=2,
        )

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def get_latest_rates(base_currency: str = "USD", symbols: str = None) -> str:
    """
    Get the latest exchange rates for currencies.

    Args:
        base_currency: The base currency to get rates for (default: USD)
        symbols: Comma-separated list of currency codes to get rates for (optional)

    Returns:
        JSON string containing latest exchange rates
    """
    try:
        params = {"base": base_currency}
        if symbols:
            params["symbols"] = symbols

        data = make_api_request("/latest", params)
        rates = ExchangeRateResponse(**data)

        if not rates.success:
            return json.dumps({"error": "Failed to retrieve latest rates"})

        # Format response for better readability
        formatted_rates = []
        for currency, rate in rates.rates.items():
            formatted_rates.append(f"1 {base_currency} = {rate:.6f} {currency}")

        return json.dumps(
            {
                "success": True,
                "base_currency": rates.base,
                "date": rates.date,
                "timestamp": rates.timestamp,
                "rates": rates.rates,
                "formatted_rates": formatted_rates,
                "total_currencies": len(rates.rates),
            },
            indent=2,
        )

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def convert_currency(
    from_currency: str, to_currency: str, amount: float, date: str = None
) -> str:
    """
    Convert an amount from one currency to another.

    Args:
        from_currency: Source currency code
        to_currency: Target currency code
        amount: Amount to convert
        date: Specific date for historical conversion (YYYY-MM-DD format, optional)

    Returns:
        JSON string containing conversion result
    """
    try:
        params = {"from": from_currency, "to": to_currency, "amount": amount}

        # Use different endpoint based on whether date is provided
        if date:
            data = make_api_request(f"/{date}", params)
            # Historical conversion logic would need to be implemented
            return json.dumps(
                {"error": "Historical conversion not fully implemented in this demo"}
            )

        data = make_api_request("/convert", params)
        conversion = ConvertResponse(**data)

        if not conversion.success:
            return json.dumps({"error": "Conversion failed"})

        return json.dumps(
            {
                "success": True,
                "from_currency": from_currency,
                "to_currency": to_currency,
                "amount": amount,
                "converted_amount": conversion.result,
                "conversion_rate": conversion.result / amount,
                "query_info": conversion.query,
                "additional_info": conversion.info,
            },
            indent=2,
        )

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def get_historical_rates(
    date: str, base_currency: str = "USD", symbols: str = None
) -> str:
    """
    Get historical exchange rates for a specific date.

    Args:
        date: Date in YYYY-MM-DD format
        base_currency: Base currency (default: USD)
        symbols: Comma-separated list of currency codes (optional)

    Returns:
        JSON string containing historical exchange rates
    """
    try:
        params = {"base": base_currency}
        if symbols:
            params["symbols"] = symbols

        data = make_api_request(f"/{date}", params)
        rates = HistoricalResponse(**data)

        if not rates.success:
            return json.dumps({"error": "Failed to retrieve historical rates"})

        # Format response for better readability
        formatted_rates = []
        for currency, rate in rates.rates.items():
            formatted_rates.append(
                f"1 {base_currency} = {rate:.6f} {currency} (as of {rates.date})"
            )

        return json.dumps(
            {
                "success": True,
                "date": rates.date,
                "base_currency": rates.base,
                "timestamp": rates.timestamp,
                "rates": rates.rates,
                "formatted_rates": formatted_rates,
                "total_currencies": len(rates.rates),
            },
            indent=2,
        )

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def get_time_series_rates(
    start_date: str, end_date: str, base_currency: str = "USD", symbols: str = None
) -> str:
    """
    Get time series exchange rates between two dates.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        base_currency: Base currency (default: USD)
        symbols: Comma-separated list of currency codes (optional)

    Returns:
        JSON string containing time series data
    """
    try:
        params = {"start_date": start_date, "end_date": end_date, "base": base_currency}

        if symbols:
            params["symbols"] = symbols

        data = make_api_request("/timeseries", params)
        series = TimeSeriesResponse(**data)

        if not series.success:
            return json.dumps({"error": "Failed to retrieve time series data"})

        return json.dumps(
            {
                "success": True,
                "base_currency": series.base,
                "start_date": series.start_date,
                "end_date": series.end_date,
                "rates": series.rates,
                "total_days": len(series.rates),
            },
            indent=2,
        )

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def get_fluctuation_data(
    start_date: str, end_date: str, base_currency: str = "USD", symbols: str = None
) -> str:
    """
    Get fluctuation data between two dates.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        base_currency: Base currency (default: USD)
        symbols: Comma-separated list of currency codes (optional)

    Returns:
        JSON string containing fluctuation data
    """
    try:
        params = {"start_date": start_date, "end_date": end_date, "base": base_currency}

        if symbols:
            params["symbols"] = symbols

        data = make_api_request("/fluctuation", params)
        fluctuation = FluctuationResponse(**data)

        if not fluctuation.success:
            return json.dumps({"error": "Failed to retrieve fluctuation data"})

        return json.dumps(
            {
                "success": True,
                "base_currency": fluctuation.base,
                "start_date": fluctuation.start_date,
                "end_date": fluctuation.end_date,
                "rates": fluctuation.rates,
                "total_currencies": len(fluctuation.rates),
            },
            indent=2,
        )

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
