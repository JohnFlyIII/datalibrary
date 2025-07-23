"""
Utilities Module

This module provides common utilities for the Legal Knowledge Platform:
- Logging configuration and helpers
- Error handling utilities
- Configuration management
"""

from .logging import get_logger, setup_logging
from .errors import SpaceInitializationError, ConfigurationError, handle_space_error, with_error_handling
from .config import Config, ModelConfig, get_config

__all__ = [
    'get_logger',
    'setup_logging',
    'SpaceInitializationError',
    'ConfigurationError',
    'handle_space_error',
    'with_error_handling',
    'Config',
    'ModelConfig',
    'get_config'
]