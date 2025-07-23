"""
Legal Knowledge Platform - Production Superlinked Application
Main package initialization for modular legal document processing system.
"""

# Import all components to ensure they're loaded
from . import index
from . import query
from . import api

__all__ = ["index", "query", "api"]