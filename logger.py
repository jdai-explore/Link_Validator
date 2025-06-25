"""
Logging configuration for Link Validator application
"""
import logging
import sys
from datetime import datetime
from config import current_config


class LinkValidatorLogger:
    """Custom logger for the Link Validator application"""
    
    def __init__(self):
        self.logger = logging.getLogger('LinkValidator')
        self.setup_logger()
    
    def setup_logger(self):
        """Configure the logger based on config settings"""
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Set log level
        level = getattr(logging, current_config.LOG_LEVEL, logging.INFO)
        self.logger.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter(current_config.LOG_FORMAT)
        
        # Console handler (if enabled)
        if current_config.ENABLE_CONSOLE_LOGGING:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # Prevent propagation to root logger
        self.logger.propagate = False
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message):
        """Log critical message"""
        self.logger.critical(message)
    
    def log_file_processing_start(self, file_path, file_info):
        """Log the start of file processing"""
        self.info(f"Starting processing: {file_info.get('name', 'Unknown')} "
                 f"({file_info.get('size_formatted', 'Unknown size')})")
        self.debug(f"Full path: {file_path}")
        if file_info.get('encoding'):
            self.debug(f"Detected encoding: {file_info['encoding']}")
    
    def log_file_processing_complete(self, results, processing_time):
        """Log the completion of file processing"""
        total_links = results['valid'] + results['invalid']
        self.info(f"Processing complete in {processing_time:.1f}s - "
                 f"Total: {total_links}, Valid: {results['valid']}, "
                 f"Invalid: {results['invalid']}")
    
    def log_validation_stats(self, file_type, total_items, processing_time):
        """Log validation statistics"""
        rate = total_items / processing_time if processing_time > 0 else 0
        self.debug(f"{file_type} processing: {total_items} items in "
                  f"{processing_time:.1f}s ({rate:.0f} items/sec)")
    
    def log_error_with_context(self, error_type, error_message, context=None):
        """Log error with additional context"""
        log_msg = f"{error_type}: {error_message}"
        if context:
            log_msg += f" (Context: {context})"
        self.error(log_msg)
    
    def log_export_operation(self, file_path, record_count):
        """Log export operation"""
        self.info(f"Exported {record_count} records to {file_path}")


# Create global logger instance
logger = LinkValidatorLogger()


def get_logger():
    """Get the global logger instance"""
    return logger


def log_function_call(func_name, **kwargs):
    """Decorator-style function to log function calls"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.debug(f"Calling {func_name} with args: {args}, kwargs: {kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"{func_name} completed successfully")
                return result
            except Exception as e:
                logger.error(f"{func_name} failed: {str(e)}")
                raise
        return wrapper
    return decorator