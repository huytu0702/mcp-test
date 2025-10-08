#!/usr/bin/env node

import express from 'express';
import cors from 'cors';
import axios from 'axios';
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
    CallToolRequestSchema,
    ErrorCode,
    McpError,
    ListToolsRequestSchema,
    ListResourcesRequestSchema,
    ReadResourceRequestSchema,
    ListPromptsRequestSchema,
    GetPromptRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

// API Configuration
const API_KEY = 'XcYKZNK5zwVVGGdnGA6Ye5MsdDEVrrgk';
const BASE_URL = 'https://api.apilayer.com/exchangerates_data';

// Create Express app for HTTP transport
const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// MCP Server setup
const server = new Server(
    {
        name: 'exchange-rates-server',
        version: '1.0.0',
    },
    {
        capabilities: {
            tools: {},
            resources: {},
            prompts: {},
        },
    }
);

// Exchange Rates API helper functions
async function callExchangeRatesAPI(endpoint, params = {}) {
    try {
        const response = await axios.get(`${BASE_URL}${endpoint}`, {
            headers: {
                'apikey': API_KEY,
            },
            params,
        });
        return response.data;
    } catch (error) {
        if (error.response) {
            throw new Error(`Exchange Rates API error: ${error.response.status} - ${error.response.data.message || error.response.data}`);
        }
        throw new Error(`Network error: ${error.message}`);
    }
}

// Tool handlers
server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
        tools: [
            {
                name: 'get_symbols',
                description: 'Lấy danh sách tất cả các loại tiền tệ được hỗ trợ',
                inputSchema: {
                    type: 'object',
                    properties: {},
                },
            },
            {
                name: 'get_latest_rates',
                description: 'Lấy tỷ giá hối đoái mới nhất cho tất cả hoặc một số loại tiền tệ cụ thể',
                inputSchema: {
                    type: 'object',
                    properties: {
                        base: {
                            type: 'string',
                            description: 'Loại tiền tệ gốc (mặc định: EUR)',
                        },
                        symbols: {
                            type: 'string',
                            description: 'Danh sách các loại tiền tệ cần lấy tỷ giá (phân cách bởi dấu phẩy)',
                        },
                    },
                },
            },
            {
                name: 'convert_currency',
                description: 'Chuyển đổi một số tiền từ loại tiền tệ này sang loại tiền tệ khác',
                inputSchema: {
                    type: 'object',
                    properties: {
                        from: {
                            type: 'string',
                            description: 'Loại tiền tệ gốc',
                        },
                        to: {
                            type: 'string',
                            description: 'Loại tiền tệ đích',
                        },
                        amount: {
                            type: 'number',
                            description: 'Số tiền cần chuyển đổi',
                        },
                        date: {
                            type: 'string',
                            description: 'Ngày tỷ giá (YYYY-MM-DD, mặc định: ngày hiện tại)',
                        },
                    },
                    required: ['from', 'to', 'amount'],
                },
            },
            {
                name: 'get_historical_rates',
                description: 'Lấy tỷ giá hối đoái lịch sử cho một ngày cụ thể',
                inputSchema: {
                    type: 'object',
                    properties: {
                        date: {
                            type: 'string',
                            description: 'Ngày cần lấy tỷ giá (YYYY-MM-DD)',
                        },
                        base: {
                            type: 'string',
                            description: 'Loại tiền tệ gốc (mặc định: EUR)',
                        },
                        symbols: {
                            type: 'string',
                            description: 'Danh sách các loại tiền tệ cần lấy tỷ giá (phân cách bởi dấu phẩy)',
                        },
                    },
                    required: ['date'],
                },
            },
            {
                name: 'get_timeseries',
                description: 'Lấy dữ liệu tỷ giá lịch sử trong khoảng thời gian',
                inputSchema: {
                    type: 'object',
                    properties: {
                        start_date: {
                            type: 'string',
                            description: 'Ngày bắt đầu (YYYY-MM-DD)',
                        },
                        end_date: {
                            type: 'string',
                            description: 'Ngày kết thúc (YYYY-MM-DD)',
                        },
                        base: {
                            type: 'string',
                            description: 'Loại tiền tệ gốc (mặc định: EUR)',
                        },
                        symbols: {
                            type: 'string',
                            description: 'Danh sách các loại tiền tệ cần lấy tỷ giá (phân cách bởi dấu phẩy)',
                        },
                    },
                    required: ['start_date', 'end_date'],
                },
            },
            {
                name: 'get_fluctuation',
                description: 'Lấy dữ liệu biến động tỷ giá giữa hai ngày',
                inputSchema: {
                    type: 'object',
                    properties: {
                        start_date: {
                            type: 'string',
                            description: 'Ngày bắt đầu (YYYY-MM-DD)',
                        },
                        end_date: {
                            type: 'string',
                            description: 'Ngày kết thúc (YYYY-MM-DD)',
                        },
                        base: {
                            type: 'string',
                            description: 'Loại tiền tệ gốc (mặc định: EUR)',
                        },
                        symbols: {
                            type: 'string',
                            description: 'Danh sách các loại tiền tệ cần lấy biến động (phân cách bởi dấu phẩy)',
                        },
                    },
                    required: ['start_date', 'end_date'],
                },
            },
        ],
    };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
    try {
        const { name, arguments: args } = request.params;

        switch (name) {
            case 'get_symbols': {
                const data = await callExchangeRatesAPI('/symbols');
                return {
                    content: [
                        {
                            type: 'text',
                            text: `Danh sách các loại tiền tệ được hỗ trợ:\n${JSON.stringify(data.symbols, null, 2)}`,
                        },
                    ],
                };
            }

            case 'get_latest_rates': {
                const params = {};
                if (args.base) params.base = args.base;
                if (args.symbols) params.symbols = args.symbols;

                const data = await callExchangeRatesAPI('/latest', params);
                return {
                    content: [
                        {
                            type: 'text',
                            text: `Tỷ giá hối đoái mới nhất (${data.date}):\n${JSON.stringify(data.rates, null, 2)}`,
                        },
                    ],
                };
            }

            case 'convert_currency': {
                const params = {
                    from: args.from,
                    to: args.to,
                    amount: args.amount,
                };
                if (args.date) params.date = args.date;

                const data = await callExchangeRatesAPI('/convert', params);
                return {
                    content: [
                        {
                            type: 'text',
                            text: `Kết quả chuyển đổi: ${args.amount} ${args.from} = ${data.result} ${args.to} (tỷ giá: ${data.rate})`,
                        },
                    ],
                };
            }

            case 'get_historical_rates': {
                const endpoint = `/${args.date}`;
                const params = {};
                if (args.base) params.base = args.base;
                if (args.symbols) params.symbols = args.symbols;

                const data = await callExchangeRatesAPI(endpoint, params);
                return {
                    content: [
                        {
                            type: 'text',
                            text: `Tỷ giá lịch sử ngày ${args.date}:\n${JSON.stringify(data.rates, null, 2)}`,
                        },
                    ],
                };
            }

            case 'get_timeseries': {
                const params = {
                    start_date: args.start_date,
                    end_date: args.end_date,
                };
                if (args.base) params.base = args.base;
                if (args.symbols) params.symbols = args.symbols;

                const data = await callExchangeRatesAPI('/timeseries', params);
                return {
                    content: [
                        {
                            type: 'text',
                            text: `Dữ liệu tỷ giá từ ${args.start_date} đến ${args.end_date}:\n${JSON.stringify(data.rates, null, 2)}`,
                        },
                    ],
                };
            }

            case 'get_fluctuation': {
                const params = {
                    start_date: args.start_date,
                    end_date: args.end_date,
                };
                if (args.base) params.base = args.base;
                if (args.symbols) params.symbols = args.symbols;

                const data = await callExchangeRatesAPI('/fluctuation', params);
                return {
                    content: [
                        {
                            type: 'text',
                            text: `Biến động tỷ giá từ ${args.start_date} đến ${args.end_date}:\n${JSON.stringify(data.rates, null, 2)}`,
                        },
                    ],
                };
            }

            default:
                throw new McpError(ErrorCode.MethodNotFound, `Unknown tool: ${name}`);
        }
    } catch (error) {
        throw new McpError(ErrorCode.InternalError, `Error calling tool: ${error.message}`);
    }
});

// HTTP MCP endpoint
app.post('/mcp', async (req, res) => {
    try {
        const transport = new StdioServerTransport();
        server.connect(transport);

        // Handle MCP messages
        const message = req.body;
        const response = await server.processMessage(message);

        res.json(response);
    } catch (error) {
        console.error('MCP Error:', error);
        res.status(500).json({
            error: {
                code: ErrorCode.InternalError,
                message: error.message,
            },
        });
    }
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'Exchange Rates MCP Server' });
});

// Start server
if (process.argv[2] === '--stdio') {
    // STDIO mode for direct MCP usage
    const transport = new StdioServerTransport();
    server.connect(transport);
    console.error('Exchange Rates MCP Server running in STDIO mode');
} else {
    // HTTP server mode
    app.listen(port, () => {
        console.log(`Exchange Rates MCP Server running on port ${port}`);
        console.log(`MCP endpoint: http://localhost:${port}/mcp`);
        console.log(`Health check: http://localhost:${port}/health`);
    });
}
