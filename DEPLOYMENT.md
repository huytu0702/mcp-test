# Hướng Dẫn Triển Khai lên Replit

## Bước 1: Chuẩn bị Tài khoản Replit

1. Truy cập [Replit.com](https://replit.com)
2. Đăng ký hoặc đăng nhập tài khoản
3. Xác minh email của bạn

## Bước 2: Tạo Repl Mới

### Cách 1: Import từ GitHub (Khuyến nghị)

1. **Push code lên GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Exchange Rates MCP Server"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Import vào Replit**
   - Nhấp "Create Repl"
   - Chọn "Import from GitHub"
   - Dán URL repository của bạn
   - Nhấp "Import from GitHub"

### Cách 2: Upload trực tiếp

1. Nhấp "Create Repl"
2. Chọn "Python" template
3. Đặt tên cho Repl (ví dụ: "exchange-rates-mcp")
4. Upload tất cả các file vào Repl

## Bước 3: Cấu hình Environment Variables

1. Trong Repl editor, nhấp vào icon **🔒 Secrets** ở sidebar trái
2. Thêm secret mới:
   - **Key**: `EXCHANGE_RATES_API_KEY`
   - **Value**: `XcYKZNK5zwVVGGdnGA6Ye5MsdDEVrrgk`
3. Nhấp "Add new secret"

## Bước 4: Cài đặt Dependencies

Replit sẽ tự động cài đặt dependencies từ `requirements.txt`. Nếu không, chạy:

```bash
pip install -r requirements.txt
```

## Bước 5: Chạy Server

1. Nhấp nút **Run** ở trên cùng
2. Server sẽ khởi động và bạn sẽ thấy output trong console
3. Replit sẽ cung cấp URL cho server của bạn

## Bước 6: Test Server

Chạy file test để kiểm tra:

```bash
python test_server.py
```

Hoặc sử dụng shell trong Replit:

```bash
python server.py
```

## Bước 7: Deployment (Production)

### Option 1: Autoscale Deployment (Khuyến nghị cho API)

1. Nhấp nút **Deploy** ở trên cùng
2. Chọn **Autoscale Deployment**
3. Điền thông tin:
   - **Name**: exchange-rates-mcp
   - **Description**: MCP Server for Exchange Rates API
4. Thêm Environment Variables trong deployment settings
5. Nhấp **Deploy**

### Option 2: Reserved VM Deployment (Always On)

1. Nhấp **Deploy** > **Reserved VM Deployment**
2. Chọn VM size (Basic hoặc Pro)
3. Cấu hình và Deploy

### Option 3: Static Deployment (Không phù hợp cho API server)

Không sử dụng cho MCP server vì cần xử lý động.

## Bước 8: Kết nối với Claude Desktop

### Cấu hình Local Development

Chỉnh sửa file cấu hình Claude:

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
%APPDATA%\Claude\claude_desktop_config.json
```

**Nội dung:**
```json
{
  "mcpServers": {
    "exchange-rates": {
      "command": "python",
      "args": ["F:/mcp-test/server.py"],
      "env": {
        "EXCHANGE_RATES_API_KEY": "XcYKZNK5zwVVGGdnGA6Ye5MsdDEVrrgk"
      }
    }
  }
}
```

### Cấu hình với Replit (SSE Transport)

Nếu đã deploy lên Replit:

```json
{
  "mcpServers": {
    "exchange-rates": {
      "url": "https://exchange-rates-mcp.your-username.repl.co",
      "transport": "sse"
    }
  }
}
```

## Bước 9: Verify Deployment

1. **Kiểm tra URL**
   - Truy cập URL Replit cung cấp
   - Kiểm tra server đang chạy

2. **Test với Claude**
   - Khởi động lại Claude Desktop
   - Thử câu lệnh: "What currencies are available?"
   - Thử: "Convert 100 USD to EUR"

## Troubleshooting

### Lỗi: API Key không hoạt động

- Kiểm tra Secrets trong Replit
- Đảm bảo key name chính xác: `EXCHANGE_RATES_API_KEY`
- Restart server sau khi thêm secret

### Lỗi: Dependencies không cài đặt

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Lỗi: Server không khởi động

1. Kiểm tra logs trong Console
2. Verify Python version (cần Python 3.11+)
3. Kiểm tra file `.replit` configuration

### Lỗi: Rate Limit (429)

- Free plan chỉ có 100 requests/tháng
- Nâng cấp plan tại [apilayer.com](https://apilayer.com)

## Monitoring

### Kiểm tra logs

Trong Replit console, bạn sẽ thấy:
- Server startup messages
- Request logs
- Error messages

### Analytics (Sau khi deploy)

1. Vào Deployments tab
2. Xem Analytics:
   - Request count
   - Response times
   - Error rates

## Pricing

### Replit Pricing

- **Free**: Basic hosting, server ngủ sau không hoạt động
- **Autoscale**: Pay per use, ~$0.000007/request
- **Reserved VM**: $7-25/tháng cho always-on

### API Pricing

- **Free**: 100 requests/tháng
- **Starter**: $14.99/tháng - 10,000 requests
- **Pro**: $59.99/tháng - 100,000 requests

## Best Practices

1. **Sử dụng Environment Variables** cho API keys
2. **Enable caching** nếu làm nhiều requests giống nhau
3. **Monitor usage** để tránh vượt quá giới hạn
4. **Set up error handling** cho production
5. **Use Autoscale** deployment cho cost optimization

## Next Steps

1. ✅ Test tất cả endpoints
2. ✅ Deploy lên Replit
3. ✅ Kết nối với Claude Desktop
4. 📊 Monitor usage và performance
5. 🔄 Optimize dựa trên usage patterns

## Resources

- [Replit Docs](https://docs.replit.com)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP Specification](https://modelcontextprotocol.io)
- [Exchange Rates API Docs](https://apilayer.com/marketplace/exchangerates_data-api)

