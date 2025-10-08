# Exchange Rates MCP Server

A Model Context Protocol (MCP) server that provides access to real-time and historical exchange rate data for 170+ world currencies using the [Exchange Rates Data API](https://apilayer.com/marketplace/exchangerates_data-api).

## Features

This MCP server exposes the following tools:

### 🔧 Available Tools

1. **get_available_currencies**
   - Get all available currency symbols and their names
   - Returns 170+ supported currencies

2. **get_latest_rates**
   - Get real-time exchange rates
   - Parameters:
     - `base`: Base currency (default: USD)
     - `symbols`: Comma-separated currency codes (optional)

3. **convert_currency**
   - Convert amounts between currencies
   - Parameters:
     - `from_currency`: Source currency code
     - `to_currency`: Target currency code
     - `amount`: Amount to convert
     - `date`: Optional date for historical conversion (YYYY-MM-DD)

4. **get_historical_rates**
   - Get exchange rates for a specific date
   - Parameters:
     - `date`: Date in YYYY-MM-DD format
     - `base`: Base currency (default: USD)
     - `symbols`: Comma-separated currency codes (optional)

5. **get_timeseries_data**
   - Get daily historical rates between two dates
   - Parameters:
     - `start_date`: Start date (YYYY-MM-DD)
     - `end_date`: End date (YYYY-MM-DD)
     - `base`: Base currency (default: USD)
     - `symbols`: Comma-separated currency codes (optional)

6. **get_fluctuation_data**
   - Get currency fluctuation statistics
   - Parameters:
     - `start_date`: Start date (YYYY-MM-DD)
     - `end_date`: End date (YYYY-MM-DD)
     - `base`: Base currency (default: USD)
     - `symbols`: Comma-separated currency codes (optional)

### 📚 Resources

- `exchangerates://info` - Information about the API and available tools

## Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd mcp-test
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file or set the environment variable:
   ```bash
   export EXCHANGE_RATES_API_KEY=your_api_key_here
   ```

4. **Run the server**
   ```bash
   python server.py
   ```

### Replit Deployment

1. **Import to Replit**
   - Go to [Replit](https://replit.com)
   - Click "Create Repl" > "Import from GitHub"
   - Paste your repository URL

2. **Set Environment Variables**
   - In Replit, go to "Secrets" (lock icon in left sidebar)
   - Add secret:
     - Key: `EXCHANGE_RATES_API_KEY`
     - Value: Your API key from apilayer.com

3. **Run the server**
   - Click the "Run" button
   - Your MCP server will start and be accessible

4. **Deploy (Optional)**
   - Click "Deploy" at the top
   - Choose "Autoscale Deployment" for production use
   - Follow the prompts to publish your server

## Using with Claude Desktop

To connect this MCP server to Claude Desktop, add it to your Claude configuration:

### Local Connection

Edit your Claude configuration file:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add the server configuration:

```json
{
  "mcpServers": {
    "exchange-rates": {
      "command": "python",
      "args": ["/path/to/mcp-test/server.py"],
      "env": {
        "EXCHANGE_RATES_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Replit Connection (SSE)

If deployed on Replit, you can connect via SSE:

```json
{
  "mcpServers": {
    "exchange-rates": {
      "url": "https://your-repl-name.your-username.repl.co",
      "transport": "sse"
    }
  }
}
```

## Example Usage

Once connected to Claude, you can use natural language to interact with the exchange rates API:

- "What currencies are available?"
- "What's the current exchange rate from USD to EUR?"
- "Convert 100 USD to GBP"
- "What was the EUR/USD exchange rate on 2024-01-15?"
- "Show me the EUR fluctuation against USD from 2024-01-01 to 2024-01-31"

## API Rate Limits

The free plan includes:
- 100 requests per month
- Daily rate updates
- Access to all endpoints

For higher usage, consider upgrading to a paid plan at [apilayer.com](https://apilayer.com/marketplace/exchangerates_data-api).

## Technical Details

- **Framework**: FastMCP (Model Context Protocol implementation)
- **API Client**: httpx (async HTTP client)
- **Data Source**: apilayer Exchange Rates Data API
- **Supported Currencies**: 170+ world currencies
- **Update Frequency**: Real-time (depending on plan)

## File Structure

```
mcp-test/
├── server.py           # Main MCP server implementation
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .replit            # Replit configuration
└── replit.nix         # Nix environment configuration
```

## Resources

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [Exchange Rates API Documentation](https://apilayer.com/marketplace/exchangerates_data-api#documentation-tab)
- [Replit Deployment Guide](https://docs.replit.com/category/replit-deployments)

## License

MIT License - feel free to use this server in your projects.

## Support

For issues with:
- The MCP server: Open an issue in this repository
- The Exchange Rates API: Contact [apilayer support](https://apilayer.com)
- Replit hosting: Check [Replit documentation](https://docs.replit.com)

