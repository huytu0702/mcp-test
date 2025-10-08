# Hướng Dẫn Nhanh - Exchange Rates MCP Server

## 📋 Tổng Quan

MCP Server này cung cấp truy cập đến dữ liệu tỷ giá hối đoái thời gian thực và lịch sử cho 170+ loại tiền tệ thế giới thông qua Exchange Rates Data API.

## 🚀 Bắt Đầu Nhanh

### 1. Kiểm tra Local (Không bắt buộc)

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy test
python test_server.py

# Chạy server
python server.py
```

### 2. Deploy lên Replit

#### Bước 1: Tạo Repository GitHub
```bash
git init
git add .
git commit -m "Exchange Rates MCP Server"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

#### Bước 2: Import vào Replit
1. Truy cập [Replit.com](https://replit.com) và đăng nhập
2. Nhấp **Create Repl** → **Import from GitHub**
3. Dán URL repository của bạn
4. Nhấp **Import from GitHub**

#### Bước 3: Cấu hình API Key
1. Trong Replit, nhấp icon **🔒 Secrets** (sidebar trái)
2. Thêm secret:
   - **Key**: `EXCHANGE_RATES_API_KEY`
   - **Value**: `XcYKZNK5zwVVGGdnGA6Ye5MsdDEVrrgk`

#### Bước 4: Chạy và Deploy
1. Nhấp **Run** để test
2. Nhấp **Deploy** → chọn **Autoscale Deployment**
3. Điền thông tin và nhấp **Deploy**

### 3. Kết Nối với Claude Desktop

#### Windows
Chỉnh sửa file: `%APPDATA%\Claude\claude_desktop_config.json`

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

#### macOS
Chỉnh sửa file: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "exchange-rates": {
      "command": "python",
      "args": ["/path/to/mcp-test/server.py"],
      "env": {
        "EXCHANGE_RATES_API_KEY": "XcYKZNK5zwVVGGdnGA6Ye5MsdDEVrrgk"
      }
    }
  }
}
```

#### Kết nối qua Replit (sau khi deploy)
```json
{
  "mcpServers": {
    "exchange-rates": {
      "url": "https://your-repl.username.repl.co",
      "transport": "sse"
    }
  }
}
```

## 🛠️ Các Công Cụ Có Sẵn

### 1. `get_available_currencies`
Lấy danh sách tất cả các loại tiền tệ có sẵn

**Ví dụ với Claude:**
```
"Cho tôi biết các loại tiền tệ có sẵn"
```

### 2. `get_latest_rates`
Lấy tỷ giá hối đoái thời gian thực

**Ví dụ:**
```
"Tỷ giá USD sang EUR hiện tại là bao nhiêu?"
"Cho tôi tỷ giá của USD với EUR, GBP và JPY"
```

### 3. `convert_currency`
Chuyển đổi số tiền giữa các loại tiền tệ

**Ví dụ:**
```
"Đổi 100 USD sang EUR"
"1000 EUR bằng bao nhiêu VND?"
"Chuyển 50 GBP sang JPY"
```

### 4. `get_historical_rates`
Lấy tỷ giá lịch sử cho một ngày cụ thể

**Ví dụ:**
```
"Tỷ giá EUR/USD ngày 1/1/2024 là bao nhiêu?"
"Cho tôi tỷ giá GBP vào ngày 15/3/2024"
```

### 5. `get_timeseries_data`
Lấy dữ liệu tỷ giá hàng ngày giữa hai ngày

**Ví dụ:**
```
"Cho tôi tỷ giá EUR/USD từ 1/1/2024 đến 7/1/2024"
"Lịch sử tỷ giá GBP trong tháng 1/2024"
```

### 6. `get_fluctuation_data`
Lấy thống kê biến động giữa hai ngày

**Ví dụ:**
```
"EUR biến động như thế nào trong tháng 1/2024?"
"Thống kê biến động USD/EUR từ 1/1 đến 31/1/2024"
```

## 📊 Ví Dụ Sử Dụng

Sau khi kết nối với Claude Desktop, bạn có thể hỏi:

1. **Kiểm tra tỷ giá:**
   - "Tỷ giá USD sang VND hiện tại?"
   - "1 EUR bằng bao nhiêu USD?"

2. **Chuyển đổi tiền:**
   - "Đổi 500 USD sang EUR"
   - "100 GBP bằng bao nhiêu JPY?"

3. **Phân tích lịch sử:**
   - "EUR/USD biến động như thế nào trong quý 1/2024?"
   - "Tỷ giá cao nhất của GBP trong tháng 1/2024"

4. **So sánh:**
   - "So sánh tỷ giá EUR/USD hôm nay với tuần trước"
   - "Xu hướng của GBP trong 30 ngày qua"

## 🔍 Kiểm Tra Hoạt Động

### Test Local
```bash
python test_server.py
```

Bạn sẽ thấy output kiểm tra tất cả các endpoints:
- ✓ Found 170+ currencies
- ✓ Latest rates
- ✓ Conversion result
- ✓ Historical rates
- ✓ Timeseries data
- ✓ Fluctuation data

### Test trên Replit
1. Nhấp **Run** trong Replit
2. Xem console logs
3. Server sẽ hiển thị "MCP Server running..."

### Test với Claude
1. Khởi động lại Claude Desktop
2. Kiểm tra MCP connection trong settings
3. Thử câu lệnh đơn giản: "What currencies are available?"

## ⚙️ Cấu Hình

### Environment Variables

| Variable | Description | Value |
|----------|-------------|-------|
| `EXCHANGE_RATES_API_KEY` | API key từ apilayer.com | `XcYKZNK5zwVVGGdnGA6Ye5MsdDEVrrgk` |

### API Rate Limits

**Free Plan (Đang sử dụng):**
- 100 requests/tháng
- Cập nhật hàng ngày
- Truy cập tất cả endpoints

**Nâng cấp nếu cần:**
- Starter: $14.99/tháng - 10,000 requests
- Pro: $59.99/tháng - 100,000 requests
- Enterprise: $99.99/tháng - 500,000 requests

## 📁 Cấu Trúc File

```
mcp-test/
├── server.py              # MCP server chính
├── test_server.py         # Script kiểm tra
├── requirements.txt       # Python dependencies
├── package.json          # NPM configuration
├── README.md             # Tài liệu tiếng Anh
├── QUICKSTART_VI.md      # Hướng dẫn nhanh (file này)
├── DEPLOYMENT.md         # Hướng dẫn deployment chi tiết
├── .replit               # Replit configuration
├── replit.nix           # Nix environment
└── .gitignore           # Git ignore rules
```

## 🐛 Xử Lý Lỗi

### Server không khởi động
```bash
# Kiểm tra Python version
python --version  # Cần >= 3.11

# Cài lại dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### API không hoạt động
- Kiểm tra API key trong Secrets
- Verify network connection
- Kiểm tra API quota (100 requests/tháng cho free plan)

### Claude không kết nối được
1. Restart Claude Desktop
2. Kiểm tra đường dẫn trong config file
3. Verify server đang chạy
4. Kiểm tra logs trong terminal

## 📚 Tài Liệu Tham Khảo

- **README.md**: Tài liệu đầy đủ bằng tiếng Anh
- **DEPLOYMENT.md**: Hướng dẫn deployment chi tiết
- [FastMCP Docs](https://github.com/jlowin/fastmcp)
- [MCP Specification](https://modelcontextprotocol.io)
- [Exchange Rates API](https://apilayer.com/marketplace/exchangerates_data-api)
- [Replit Docs](https://docs.replit.com)

## 💡 Tips

1. **Tiết kiệm API calls**: Cache kết quả nếu sử dụng nhiều
2. **Monitor usage**: Theo dõi số lượng requests
3. **Use Autoscale**: Deployment option tốt nhất cho API
4. **Test local first**: Trước khi deploy lên Replit
5. **Keep API key secret**: Không commit vào Git

## ✅ Checklist Deploy

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Test local: `python test_server.py`
- [ ] Push to GitHub
- [ ] Import vào Replit
- [ ] Set API key trong Secrets
- [ ] Run và test trên Replit
- [ ] Deploy (Autoscale recommended)
- [ ] Configure Claude Desktop
- [ ] Test với Claude
- [ ] Monitor usage

## 🎯 Kết Quả Mong Đợi

Sau khi hoàn thành, bạn sẽ có:
- ✅ MCP Server chạy trên Replit
- ✅ Truy cập 170+ loại tiền tệ
- ✅ 6 công cụ exchange rate trong Claude
- ✅ Real-time và historical data
- ✅ Production-ready deployment

---

**Cần trợ giúp?**
- Kiểm tra DEPLOYMENT.md cho hướng dẫn chi tiết
- Xem README.md cho technical details
- Test với `python test_server.py`

