"""
Configuration settings for Link Validator application
"""
import os

class Config:
    """Main configuration class for the Link Validator"""
    
    # Application Info
    APP_NAME = "Advanced Link Validator"
    APP_VERSION = "3.0"
    APP_AUTHOR = "Link Validator Team"
    
    # File Processing Limits
    MAX_EXCEL_ROWS = 50000
    MAX_EXCEL_COLS = 200
    MAX_FILE_SIZE_MB = 100
    LARGE_FILE_THRESHOLD_MB = 10
    
    # Progress Reporting Thresholds
    PROGRESS_INTERVALS = {
        'small': (100, 5),      # files < 100 items, update every 5
        'medium': (1000, 25),   # files < 1000 items, update every 25
        'large': (10000, 100),  # files < 10000 items, update every 100
        'xlarge': (100000, 500), # files < 100000 items, update every 500
        'xxlarge': (float('inf'), 1000)  # files >= 100000 items, update every 1000
    }
    
    # URL Validation Settings
    VALID_URL_SCHEMES = ['http', 'https']
    ALLOW_LOCALHOST = True
    ALLOW_IP_ADDRESSES = True
    ALLOW_INTERNAL_DOMAINS = True
    
    # Encoding Detection
    ENCODING_FALLBACKS = ['utf-8', 'latin-1', 'cp1252', 'ascii', 'utf-16']
    ENCODING_CONFIDENCE_THRESHOLD = 0.7
    
    # UI Settings
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 700
    FONT_FAMILY = 'Arial'
    MONOSPACE_FONT = 'Consolas'
    
    # Export Settings
    DEFAULT_EXPORT_FORMAT = 'csv'
    EXPORT_TIMESTAMP_FORMAT = '%Y%m%d_%H%M%S'
    MAX_URL_DISPLAY_LENGTH = 100
    
    # Logging Settings
    ENABLE_CONSOLE_LOGGING = True
    LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR
    LOG_FORMAT = '[%(asctime)s] %(levelname)s: %(message)s'
    
    # Performance Settings
    THREAD_TIMEOUT_SECONDS = 300  # 5 minutes
    UI_UPDATE_INTERVAL_MS = 100
    
    # Supported File Extensions
    SUPPORTED_EXTENSIONS = {
        '.csv': 'CSV Files',
        '.xls': 'Excel Files (Legacy)',
        '.xlsx': 'Excel Files',
        '.txt': 'Text Files',
        '.html': 'HTML Files',
        '.htm': 'HTML Files',
        '.xml': 'XML Files'
    }
    
    # File Type Processors
    FILE_PROCESSORS = {
        '.csv': 'process_csv',
        '.xls': 'process_excel',
        '.xlsx': 'process_excel',
        '.txt': 'process_text',
        '.html': 'process_html',
        '.htm': 'process_html',
        '.xml': 'process_html'  # Use HTML processor for XML
    }
    
    # Error Messages
    ERROR_MESSAGES = {
        'file_not_found': "The selected file could not be found.",
        'file_empty': "The selected file is empty.",
        'file_too_large': f"File is too large (max {MAX_FILE_SIZE_MB}MB).",
        'unsupported_format': "Unsupported file format.",
        'encoding_failed': "Could not decode file with any supported encoding.",
        'processing_failed': "An error occurred while processing the file.",
        'export_failed': "Failed to export results.",
        'no_results': "No results available to export."
    }
    
    # Success Messages
    SUCCESS_MESSAGES = {
        'processing_complete': "File processing completed successfully.",
        'export_complete': "Results exported successfully.",
        'validation_complete': "Link validation completed."
    }
    
    # UI Colors
    COLORS = {
        'background': '#f8f9fa',
        'primary': '#007acc',
        'success': '#28a745',
        'warning': '#ffc107',
        'error': '#dc3545',
        'info': '#17a2b8',
        'text': '#333333',
        'border': '#dee2e6'
    }

class DevelopmentConfig(Config):
    """Development-specific configuration"""
    ENABLE_CONSOLE_LOGGING = True
    LOG_LEVEL = 'DEBUG'
    MAX_FILE_SIZE_MB = 50  # Smaller limit for development
    
class ProductionConfig(Config):
    """Production-specific configuration"""
    ENABLE_CONSOLE_LOGGING = False
    LOG_LEVEL = 'WARNING'
    MAX_FILE_SIZE_MB = 200  # Larger limit for production

# Default configuration
current_config = Config