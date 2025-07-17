"""
Error Handling Utilities

Purpose:
- Custom exception classes for better error handling
- Error recovery strategies
- Graceful degradation support

Human Note: Always provide meaningful error messages for debugging
AI Agent Note: Include context and recovery suggestions in errors
"""

from typing import Optional, Dict, Any, Callable
import functools
from .logging import get_logger, log_error_with_context

logger = get_logger(__name__)

class LegalKnowledgeError(Exception):
    """Base exception for Legal Knowledge Platform"""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.context = context or {}

class SpaceInitializationError(LegalKnowledgeError):
    """Raised when a space fails to initialize"""
    
    def __init__(
        self, 
        space_name: str, 
        original_error: Exception,
        context: Optional[Dict[str, Any]] = None
    ):
        message = f"Failed to initialize space '{space_name}': {str(original_error)}"
        super().__init__(message, context)
        self.space_name = space_name
        self.original_error = original_error

class ConfigurationError(LegalKnowledgeError):
    """Raised when configuration is invalid"""
    
    def __init__(
        self,
        config_key: str,
        issue: str,
        context: Optional[Dict[str, Any]] = None
    ):
        message = f"Configuration error for '{config_key}': {issue}"
        super().__init__(message, context)
        self.config_key = config_key
        self.issue = issue

class SchemaValidationError(LegalKnowledgeError):
    """Raised when schema validation fails"""
    
    def __init__(
        self,
        field_name: str,
        issue: str,
        context: Optional[Dict[str, Any]] = None
    ):
        message = f"Schema validation failed for field '{field_name}': {issue}"
        super().__init__(message, context)
        self.field_name = field_name
        self.issue = issue

class QueryExecutionError(LegalKnowledgeError):
    """Raised when query execution fails"""
    
    def __init__(
        self,
        query_type: str,
        original_error: Exception,
        context: Optional[Dict[str, Any]] = None
    ):
        message = f"Query execution failed for '{query_type}': {str(original_error)}"
        super().__init__(message, context)
        self.query_type = query_type
        self.original_error = original_error

def handle_space_error(
    space_name: str,
    error: Exception,
    fallback: Optional[Any] = None,
    reraise: bool = True
) -> Optional[Any]:
    """
    Handle space initialization errors
    
    Args:
        space_name: Name of the space that failed
        error: The original exception
        fallback: Optional fallback value to return
        reraise: Whether to reraise the exception after logging
        
    Returns:
        Fallback value if provided and reraise is False
        
    Raises:
        SpaceInitializationError if reraise is True
    """
    context = {
        'space_name': space_name,
        'error_type': type(error).__name__,
        'fallback_provided': fallback is not None
    }
    
    log_error_with_context(logger, error, context)
    
    if reraise:
        raise SpaceInitializationError(space_name, error, context)
    
    if fallback is not None:
        logger.warning(f"Using fallback for space '{space_name}'")
        return fallback
    
    return None

def with_error_handling(
    error_class: type = LegalKnowledgeError,
    fallback: Optional[Any] = None,
    log_errors: bool = True
):
    """
    Decorator for error handling
    
    Args:
        error_class: Exception class to catch
        fallback: Optional fallback return value
        log_errors: Whether to log errors
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_errors:
                    context = {
                        'function': func.__name__,
                        'args': str(args)[:100],
                        'kwargs': str(kwargs)[:100]
                    }
                    log_error_with_context(logger, e, context)
                
                if isinstance(e, error_class):
                    raise
                
                # Wrap in our error class
                raise error_class(
                    f"Error in {func.__name__}: {str(e)}",
                    context={'original_error': type(e).__name__}
                )
        
        return wrapper
    return decorator

def validate_required_fields(
    data: Dict[str, Any],
    required_fields: list,
    context: str = "validation"
) -> None:
    """
    Validate that required fields are present
    
    Args:
        data: Dictionary to validate
        required_fields: List of required field names
        context: Context for error messages
        
    Raises:
        SchemaValidationError if any required field is missing
    """
    missing_fields = [
        field for field in required_fields
        if field not in data or data[field] is None
    ]
    
    if missing_fields:
        raise SchemaValidationError(
            field_name=", ".join(missing_fields),
            issue=f"Required fields missing in {context}",
            context={'missing_fields': missing_fields}
        )

# Error recovery strategies
class ErrorRecovery:
    """Strategies for recovering from errors"""
    
    @staticmethod
    def retry_with_backoff(
        func: Callable,
        max_retries: int = 3,
        backoff_factor: float = 2.0
    ) -> Callable:
        """Retry a function with exponential backoff"""
        import time
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        wait_time = backoff_factor ** attempt
                        logger.warning(
                            f"Attempt {attempt + 1} failed, retrying in {wait_time}s: {str(e)}"
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"All {max_retries} attempts failed")
            
            raise last_error
        
        return wrapper
    
    @staticmethod
    def fallback_to_default(default_value: Any):
        """Decorator to return default value on error"""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(
                        f"Function {func.__name__} failed, using default: {str(e)}"
                    )
                    return default_value
            return wrapper
        return decorator