"""
Logging Configuration and Utilities

Purpose:
- Centralized logging configuration
- Structured logging with context
- Performance and error tracking

Human Note: Use structured logging for better observability
AI Agent Note: Always log errors with full context for debugging
"""

import logging
import sys
from datetime import datetime
from typing import Optional, Dict, Any
import json

# Default log format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
JSON_LOG_FORMAT = {
    'timestamp': '%(asctime)s',
    'logger': '%(name)s',
    'level': '%(levelname)s',
    'message': '%(message)s',
    'module': '%(module)s',
    'function': '%(funcName)s',
    'line': '%(lineno)d'
}

class StructuredFormatter(logging.Formatter):
    """JSON structured logging formatter"""
    
    def format(self, record):
        log_obj = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage()
        }
        
        # Add any extra fields
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'created', 'filename', 
                          'funcName', 'levelname', 'levelno', 'lineno', 
                          'module', 'msecs', 'message', 'pathname', 'process',
                          'processName', 'relativeCreated', 'thread', 'threadName']:
                log_obj[key] = value
                
        return json.dumps(log_obj)

def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    use_json: bool = False
) -> None:
    """
    Configure logging for the application
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output
        use_json: Use JSON structured logging format
    """
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # Create handlers
    handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    if use_json:
        console_handler.setFormatter(StructuredFormatter())
    else:
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    handlers.append(console_handler)
    
    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        if use_json:
            file_handler.setFormatter(StructuredFormatter())
        else:
            file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        handlers=handlers
    )
    
    # Set specific loggers
    logging.getLogger('superlinked').setLevel(log_level)
    logging.getLogger('spaces').setLevel(log_level)
    logging.getLogger('schema').setLevel(log_level)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)

class LogContext:
    """Context manager for adding context to logs"""
    
    def __init__(self, logger: logging.Logger, **kwargs):
        self.logger = logger
        self.context = kwargs
        self.old_factory = None
        
    def __enter__(self):
        self.old_factory = logging.getLogRecordFactory()
        context = self.context
        
        def record_factory(*args, **kwargs):
            record = self.old_factory(*args, **kwargs)
            for key, value in context.items():
                setattr(record, key, value)
            return record
            
        logging.setLogRecordFactory(record_factory)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.setLogRecordFactory(self.old_factory)

# Convenience functions
def log_space_creation(logger: logging.Logger, space_name: str, config: Dict[str, Any]):
    """Log space creation with configuration"""
    logger.info(
        f"Creating space: {space_name}",
        extra={
            'space_name': space_name,
            'config': config,
            'event': 'space_creation'
        }
    )

def log_query_execution(
    logger: logging.Logger, 
    query_type: str, 
    query_text: str,
    num_results: int,
    execution_time: float
):
    """Log query execution metrics"""
    logger.info(
        f"Query executed: {query_type}",
        extra={
            'query_type': query_type,
            'query_text': query_text[:100],  # Truncate long queries
            'num_results': num_results,
            'execution_time_ms': execution_time * 1000,
            'event': 'query_execution'
        }
    )

def log_error_with_context(
    logger: logging.Logger,
    error: Exception,
    context: Dict[str, Any]
):
    """Log error with full context"""
    logger.error(
        f"Error occurred: {type(error).__name__}: {str(error)}",
        extra={
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'event': 'error'
        },
        exc_info=True
    )