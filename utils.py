"""
Utility functions for the Link Validator application
"""
import pandas as pd
import os


def detect_encoding(file_path):
    """
    Detect file encoding with fallback (no chardet dependency)
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Detected encoding or 'utf-8' as fallback
    """
    # Try common encodings in order
    encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'ascii']
    
    for encoding in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                # Try to read first 1000 characters
                f.read(1000)
            return encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    # If all fail, return utf-8 as fallback
    return 'utf-8'


def get_progress_interval(total):
    """
    Calculate appropriate progress reporting interval based on total items
    
    Args:
        total (int): Total number of items to process
        
    Returns:
        int: Interval for progress reporting
    """
    if total < 100:
        return 5
    elif total < 1000:
        return 25
    elif total < 10000:
        return 100
    elif total < 100000:
        return 500
    else:
        return 1000


def safe_str_conversion(value):
    """
    Safely convert any value to string for URL checking
    
    Args:
        value: Any value that might be a URL
        
    Returns:
        str: String representation or empty string if invalid
    """
    if pd.isna(value) or value is None:
        return ""
    
    # Handle numeric types that might be URLs stored as numbers
    if isinstance(value, (int, float)):
        if isinstance(value, float) and (value != value):  # NaN check
            return ""
        # Convert float to int if it's a whole number
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)
    
    # Handle other types
    return str(value).strip()


def validate_file_path(file_path):
    """
    Validate file path before processing
    
    Args:
        file_path (str): Path to validate
        
    Returns:
        bool: True if valid
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If path is invalid
    """
    if not file_path:
        raise ValueError("File path cannot be empty")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not os.path.isfile(file_path):
        raise ValueError(f"Path is not a file: {file_path}")
    
    if os.path.getsize(file_path) == 0:
        raise ValueError("File is empty")
    
    return True


def get_column_letter(col_num):
    """
    Convert column number to Excel column letter(s)
    
    Args:
        col_num (int): Column number (1-based)
        
    Returns:
        str: Column letter(s) (A, B, ..., Z, AA, AB, etc.)
    """
    result = ""
    while col_num > 0:
        col_num -= 1
        result = chr(65 + (col_num % 26)) + result
        col_num //= 26
    return result


def format_file_size(size_bytes):
    """
    Format file size in human readable format
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size (e.g., "1.5 MB")
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def is_large_file(file_path, threshold_mb=10):
    """
    Check if file is considered large
    
    Args:
        file_path (str): Path to file
        threshold_mb (int): Threshold in megabytes
        
    Returns:
        bool: True if file is larger than threshold
    """
    try:
        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024)
        return size_mb > threshold_mb
    except Exception:
        return False


def get_file_info(file_path):
    """
    Get comprehensive file information
    
    Args:
        file_path (str): Path to file
        
    Returns:
        dict: File information including size, extension, etc.
    """
    try:
        file_stats = os.stat(file_path)
        return {
            'name': os.path.basename(file_path),
            'size_bytes': file_stats.st_size,
            'size_formatted': format_file_size(file_stats.st_size),
            'extension': os.path.splitext(file_path)[1].lower(),
            'is_large': is_large_file(file_path),
            'encoding': detect_encoding(file_path) if file_path.endswith('.txt') else None
        }
    except Exception as e:
        return {
            'name': os.path.basename(file_path),
            'error': str(e)
        }


def truncate_text(text, max_length=100):
    """
    Truncate text to specified length with ellipsis
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def safe_division(numerator, denominator, default=0):
    """
    Safely divide two numbers
    
    Args:
        numerator: Number to divide
        denominator: Number to divide by
        default: Default value if division fails
        
    Returns:
        float: Result of division or default
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except Exception:
        return default