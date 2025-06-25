"""
Custom exceptions for Link Validator application
"""

class LinkValidatorError(Exception):
    """Base exception class for Link Validator"""
    
    def __init__(self, message, error_code=None, context=None):
        self.message = message
        self.error_code = error_code
        self.context = context or {}
        super().__init__(self.message)
    
    def __str__(self):
        return self.message


class FileProcessingError(LinkValidatorError):
    """Exception raised when file processing fails"""
    
    def __init__(self, message, file_path=None, file_type=None, **kwargs):
        self.file_path = file_path
        self.file_type = file_type
        context = {'file_path': file_path, 'file_type': file_type}
        context.update(kwargs)
        super().__init__(message, context=context)


class ValidationError(LinkValidatorError):
    """Exception raised when URL validation fails"""
    
    def __init__(self, message, url=None, validation_rule=None, **kwargs):
        self.url = url
        self.validation_rule = validation_rule
        context = {'url': url, 'validation_rule': validation_rule}
        context.update(kwargs)
        super().__init__(message, context=context)


class ExportError(LinkValidatorError):
    """Exception raised when export operations fail"""
    
    def __init__(self, message, export_path=None, export_format=None, **kwargs):
        self.export_path = export_path
        self.export_format = export_format
        context = {'export_path': export_path, 'export_format': export_format}
        context.update(kwargs)
        super().__init__(message, context=context)


class FileValidationError(FileProcessingError):
    """Exception raised when file validation fails before processing"""
    pass


class EncodingError(FileProcessingError):
    """Exception raised when file encoding cannot be determined or decoded"""
    
    def __init__(self, message, file_path=None, tried_encodings=None, **kwargs):
        self.tried_encodings = tried_encodings or []
        context = {'tried_encodings': self.tried_encodings}
        context.update(kwargs)
        super().__init__(message, file_path=file_path, context=context)


class FileSizeError(FileProcessingError):
    """Exception raised when file is too large to process"""
    
    def __init__(self, message, file_path=None, file_size=None, max_size=None, **kwargs):
        self.file_size = file_size
        self.max_size = max_size
        context = {'file_size': file_size, 'max_size': max_size}
        context.update(kwargs)
        super().__init__(message, file_path=file_path, context=context)


class UnsupportedFileFormatError(FileProcessingError):
    """Exception raised when file format is not supported"""
    
    def __init__(self, message, file_path=None, file_extension=None, **kwargs):
        self.file_extension = file_extension
        context = {'file_extension': file_extension}
        context.update(kwargs)
        super().__init__(message, file_path=file_path, context=context)


class ProcessingTimeoutError(FileProcessingError):
    """Exception raised when file processing takes too long"""
    
    def __init__(self, message, file_path=None, timeout_seconds=None, **kwargs):
        self.timeout_seconds = timeout_seconds
        context = {'timeout_seconds': timeout_seconds}
        context.update(kwargs)
        super().__init__(message, file_path=file_path, context=context)


# Exception mapping for easier error handling
ERROR_MAPPING = {
    'file_not_found': FileValidationError,
    'file_empty': FileValidationError,
    'file_too_large': FileSizeError,
    'unsupported_format': UnsupportedFileFormatError,
    'encoding_failed': EncodingError,
    'processing_failed': FileProcessingError,
    'export_failed': ExportError,
    'validation_failed': ValidationError,
    'timeout': ProcessingTimeoutError
}


def create_exception(error_type, message, **kwargs):
    """Factory function to create appropriate exception based on error type"""
    exception_class = ERROR_MAPPING.get(error_type, LinkValidatorError)
    return exception_class(message, **kwargs)


def handle_exception(exception, logger=None):
    """Handle exceptions with proper logging and user-friendly messages"""
    if logger:
        if hasattr(exception, 'context') and exception.context:
            logger.log_error_with_context(
                type(exception).__name__, 
                str(exception), 
                exception.context
            )
        else:
            logger.error(f"{type(exception).__name__}: {str(exception)}")
    
    # Return user-friendly message
    if isinstance(exception, FileValidationError):
        return "Please check that the file exists and is accessible."
    elif isinstance(exception, FileSizeError):
        return f"The file is too large to process. Maximum size allowed is {exception.max_size}MB."
    elif isinstance(exception, UnsupportedFileFormatError):
        return "This file format is not supported. Please use CSV, Excel, Text, or HTML files."
    elif isinstance(exception, EncodingError):
        return "Could not read the file. It may be corrupted or use an unsupported encoding."
    elif isinstance(exception, ProcessingTimeoutError):
        return "Processing took too long and was cancelled. Try with a smaller file."
    elif isinstance(exception, ExportError):
        return "Failed to save the results. Please check file permissions and disk space."
    else:
        return "An unexpected error occurred. Please try again."