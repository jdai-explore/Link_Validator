# Advanced Link Validator v3.0

A production-ready desktop application for validating URLs in various file formats including CSV, Excel, Text, and HTML files.

## 🚀 Features

### Core Functionality
- **Multi-format Support**: CSV, Excel (.xls/.xlsx), Text (.txt), HTML/XML files
- **Advanced URL Validation**: Supports localhost, IP addresses, internal domains
- **Smart Encoding Detection**: Automatically handles different file encodings
- **Progress Tracking**: Real-time progress updates with time estimation
- **Export Options**: CSV, Excel, and Text export formats
- **Cancellation Support**: Stop processing at any time

### Production Features
- **Comprehensive Logging**: Detailed logging with configurable levels
- **Error Handling**: Robust error handling with user-friendly messages
- **Performance Optimization**: Adaptive progress reporting and memory management
- **File Validation**: Pre-processing file validation and size limits
- **Threading**: Non-blocking UI with background processing
- **Configuration**: Centralized configuration management

## 📋 Requirements

- Python 3.7+
- tkinter (usually included with Python)
- pandas
- openpyxl
- beautifulsoup4
- lxml (optional, for better HTML parsing)

## 🛠️ Installation

1. **Clone or download the application files**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   python link_validator.py
   ```

## 📁 File Structure

```
link_validator/
├── link_validator.py      # Main application
├── utils.py              # Utility functions
├── config.py             # Configuration settings
├── logger.py             # Logging configuration
├── exceptions.py         # Custom exceptions
├── test_link_validator.py # Test suite
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## 🔧 Configuration

The application behavior can be customized through `config.py`:

### File Processing Limits
```python
MAX_EXCEL_ROWS = 50000      # Maximum Excel rows to process
MAX_EXCEL_COLS = 200        # Maximum Excel columns to process
MAX_FILE_SIZE_MB = 100      # Maximum file size in MB
LARGE_FILE_THRESHOLD_MB = 10 # Threshold for "large file" warning
```

### URL Validation Settings
```python
VALID_URL_SCHEMES = ['http', 'https']  # Allowed URL schemes
ALLOW_LOCALHOST = True                 # Allow localhost URLs
ALLOW_IP_ADDRESSES = True             # Allow IP address URLs
ALLOW_INTERNAL_DOMAINS = True         # Allow internal domain names
```

### UI Settings
```python
WINDOW_WIDTH = 900          # Application window width
WINDOW_HEIGHT = 700         # Application window height
FONT_FAMILY = 'Arial'       # Primary font family
MONOSPACE_FONT = 'Consolas' # Monospace font for results
```

## 📊 Supported File Formats

### CSV Files (.csv)
- Automatically detects encoding
- Processes all columns and rows
- Handles mixed data types

### Excel Files (.xls, .xlsx)
- Supports multiple worksheets
- Memory-efficient row-by-row processing
- Handles various cell data types

### Text Files (.txt)
- One URL per line
- Multiple encoding support
- Skips empty lines

### HTML/XML Files (.html, .htm, .xml)
- Extracts URLs from href and src attributes
- Supports links, images, scripts, and stylesheets
- Proper HTML parsing with BeautifulSoup

## 🎯 Usage Examples

### Basic Usage
1. **Launch the application**
2. **Click "📂 Upload File"**
3. **Select your file** (CSV, Excel, Text, or HTML)
4. **Wait for processing** to complete
5. **Review results** in the output area
6. **Export results** if needed

### URL Validation Examples

**Valid URLs:**
- `http://example.com`
- `https://www.google.com`
- `http://localhost:8080`
- `https://192.168.1.1`
- `http://internal.company.com`

**Invalid URLs:**
- `ftp://example.com` (wrong scheme)
- `www.example.com` (no scheme)
- `not-a-url` (not a URL)
- `http://` (incomplete)

## 📈 Performance

### Processing Speed
- **Small files** (< 1MB): Near instant
- **Medium files** (1-10MB): 5-30 seconds
- **Large files** (10-50MB): 1-5 minutes
- **Very large files** (> 50MB): 10+ minutes

### Memory Usage
- **Efficient streaming**: Row-by-row processing
- **Smart limits**: Configurable size constraints
- **Resource cleanup**: Automatic memory management

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_link_validator.py
```

### Test Coverage
- URL validation logic
- File processing for all formats
- Utility functions
- Exception handling
- Integration workflows

## 📝 Export Formats

### CSV Export
- Comprehensive metadata header
- Structured data with location info
- UTF-8 encoding support

### Excel Export
- Formatted headers with styling
- Auto-adjusted column widths
- Multiple data types support

### Text Export
- Human-readable format
- Summary statistics
- Complete invalid link listing

## 🚨 Error Handling

### File Validation Errors
- File not found
- File too large
- Unsupported format
- Permission issues

### Processing Errors
- Encoding problems
- Memory limitations
- Timeout issues
- Corrupted files

### User-Friendly Messages
- Clear error descriptions
- Actionable suggestions
- Detailed logging for debugging

## 🔍 Logging

### Log Levels
- **DEBUG**: Detailed processing information
- **INFO**: General application flow
- **WARNING**: Non-critical issues
- **ERROR**: Serious problems

### Log Configuration
Configure logging in `config.py`:
```python
ENABLE_CONSOLE_LOGGING = True
LOG_LEVEL = 'INFO'
LOG_FORMAT = '[%(asctime)s] %(levelname)s: %(message)s'
```

## 🛡️ Security Considerations

- **File Size Limits**: Prevents resource exhaustion
- **Input Validation**: Comprehensive file validation
- **Safe Processing**: Protected against malformed files
- **No Network Access**: Validation is syntax-only (no actual HTTP requests)

## 🚀 Advanced Features

### Cancellation Support
- Stop processing at any time
- Safe thread termination
- Resource cleanup on cancellation

### Progress Estimation
- Adaptive progress intervals
- Time remaining calculation
- Processing rate statistics

### Memory Management
- Streaming file processing
- Configurable size limits
- Automatic resource cleanup

## 🐛 Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
pip install -r requirements.txt
```

**File encoding issues:**
- Application automatically tries multiple encodings
- Check file is not corrupted
- Ensure file has proper extension

**Large file performance:**
- Increase memory if available
- Consider splitting large files
- Adjust limits in config.py

**UI freezing:**
- Processing runs in background thread
- Use Cancel button if needed
- Check system resources

### Debug Mode
Enable debug logging in `config.py`:
```python
LOG_LEVEL = 'DEBUG'
ENABLE_CONSOLE_LOGGING = True
```

## 📞 Support

For issues and questions:
1. Check this README
2. Review log output
3. Run test suite to verify installation
4. Check configuration settings

## 🔄 Version History

### v3.0 (Current)
- Production-ready stability
- Comprehensive error handling
- Advanced logging system
- Cancellation support
- Enhanced UI/UX
- Full test suite

### v2.0
- Performance optimizations
- Enhanced file support
- Better progress reporting
- Utility functions separation

### v1.0
- Basic link validation
- Multi-format support
- Simple GUI interface

## 📜 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please:
1. Run the test suite
2. Follow existing code style
3. Add tests for new features
4. Update documentation as needed