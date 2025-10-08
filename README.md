# Exchange Rates Data API MCP Server

This is a Model Context Protocol (MCP) server that provides access to the Exchange Rates Data API from APILayer. It allows AI assistants to access real-time and historical currency exchange rates, perform currency conversions, and retrieve currency information.

## Features

- **Real-time Exchange Rates**: Get current exchange rates for any currency pair
- **Historical Data**: Access historical exchange rates for specific dates
- **Currency Conversion**: Convert amounts between currencies
- **Time Series Data**: Get exchange rate trends over time periods
- **Currency Symbols**: List all available currencies and their names
- **Fluctuation Analysis**: Analyze exchange rate changes between dates

## Available Tools

### `get_currency_symbols()`
Returns all available currency symbols and their descriptions.

### `get_latest_rates(base_currency="USD", symbols=None)`
Gets the latest exchange rates for currencies.

**Parameters:**
- `base_currency`: The base currency (default: USD)
- `symbols`: Comma-separated list of currency codes (optional)

### `convert_currency(from_currency, to_currency, amount, date=None)`
Converts an amount from one currency to another.

**Parameters:**
- `from_currency`: Source currency code
- `to_currency`: Target currency code
- `amount`: Amount to convert
- `date`: Specific date for historical conversion (YYYY-MM-DD format, optional)

### `get_historical_rates(date, base_currency="USD", symbols=None)`
Gets historical exchange rates for a specific date.

**Parameters:**
- `date`: Date in YYYY-MM-DD format
- `base_currency`: Base currency (default: USD)
- `symbols`: Comma-separated list of currency codes (optional)

### `get_time_series_rates(start_date, end_date, base_currency="USD", symbols=None)`
Gets time series exchange rates between two dates.

**Parameters:**
- `start_date`: Start date in YYYY-MM-DD format
- `end_date`: End date in YYYY-MM-DD format
- `base_currency`: Base currency (default: USD)
- `symbols`: Comma-separated list of currency codes (optional)

### `get_fluctuation_data(start_date, end_date, base_currency="USD", symbols=None)`
Gets fluctuation data between two dates.

**Parameters:**
- `start_date`: Start date in YYYY-MM-DD format
- `end_date`: End date in YYYY-MM-DD format
- `base_currency`: Base currency (default: USD)
- `symbols`: Comma-separated list of currency codes (optional)

## Available Resources

### `currency-symbols`
Provides all available currency symbols as a resource.

### `latest-rates`
Provides the latest exchange rates with USD as base currency.

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Locally

To run the MCP server locally:

```bash
python main.py
```

The server will start and be available for MCP clients to connect.

## Deployment on Replit

This project is configured for deployment on Replit:

1. Import this project into Replit
2. The `.replit` file configures the deployment settings
3. The `replit.nix` file sets up the Python environment
4. Once deployed, your MCP server will be available at the provided Replit URL

## OpenAI MCP Integration

To integrate with OpenAI's MCP platform:

1. Deploy this server on Replit
2. Copy the deployment URL
3. In OpenAI's platform, add the MCP server using the deployment URL
4. The AI assistant will then have access to all the exchange rate tools and resources

## API Key

The API key for Exchange Rates Data API is already configured in the code:
```
API_KEY = "XcYKZNK5zwVVGGdnGA6Ye5MsdDEVrrgk"
```

## Example Usage

Here's an example of how an AI assistant might use these tools:

1. **Get available currencies:**
   ```
   User: What currencies are available?
   Assistant: I'll check the currency symbols...
   ```

2. **Convert currency:**
   ```
   User: Convert 100 USD to EUR
   Assistant: I'll convert that for you...
   ```

3. **Get exchange rate trends:**
   ```
   User: How has the EUR/USD rate changed over the last month?
   Assistant: I'll get the time series data...
   ```

## Error Handling

The server includes comprehensive error handling for:
- API request failures
- Invalid parameters
- Network issues
- Rate limiting

All responses include proper error messages and status indicators.

## License

This project is provided as-is for educational and development purposes.
