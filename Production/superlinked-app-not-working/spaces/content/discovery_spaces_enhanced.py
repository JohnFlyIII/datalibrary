"""
Discovery Layer Content Spaces - Enhanced with Error Handling and Configuration

Purpose:
- Enable broad exploration and initial discovery
- Support high-level topic identification
- Facilitate quick relevance assessment

Usage:
- First-pass searches across entire corpus
- High-level summaries and overviews
- Client-friendly takeaways
- Initial topic exploration

Human Note: Discovery spaces are optimized for breadth over depth
AI Agent Note: Use high weights on these spaces for initial exploration
"""

from superlinked import framework as sl
from typing import Optional

from schema.base.legal_document import LegalDocument
from utils import get_logger, get_config, handle_space_error, with_error_handling
from utils.errors import SpaceInitializationError

# Import coverage_scope_space to avoid duplication
from ..categorical.legal_taxonomy_spaces import coverage_scope_space

# Initialize logger and configuration
logger = get_logger(__name__)
config = get_config()

# Initialize the legal document schema
legal_document = LegalDocument()

# Create spaces with error handling
@with_error_handling(error_class=SpaceInitializationError)
def create_discovery_summary_space() -> Optional[sl.TextSimilaritySpace]:
    """Create discovery summary space with error handling"""
    try:
        model = config.models.get_model_for_space('discovery')
        logger.info(f"Creating discovery_summary_space with model: {model}")
        
        space = sl.TextSimilaritySpace(
            text=legal_document.summary,
            model=model
        )
        
        logger.info("Successfully created discovery_summary_space")
        return space
        
    except Exception as e:
        return handle_space_error(
            "discovery_summary_space",
            e,
            fallback=None,
            reraise=True
        )

@with_error_handling(error_class=SpaceInitializationError)
def create_discovery_topics_space() -> Optional[sl.TextSimilaritySpace]:
    """Create discovery topics space with error handling"""
    try:
        model = config.models.get_model_for_space('discovery')
        logger.info(f"Creating discovery_topics_space with model: {model}")
        
        space = sl.TextSimilaritySpace(
            text=legal_document.broad_topics,
            model=model
        )
        
        logger.info("Successfully created discovery_topics_space")
        return space
        
    except Exception as e:
        return handle_space_error(
            "discovery_topics_space",
            e,
            fallback=None,
            reraise=True
        )

@with_error_handling(error_class=SpaceInitializationError)
def create_content_density_space() -> Optional[sl.NumberSpace]:
    """Create content density space with error handling"""
    try:
        logger.info("Creating content_density_space")
        
        space = sl.NumberSpace(
            number=legal_document.content_density,
            min_value=0,
            max_value=100,
            mode=sl.Mode.MAXIMUM  # Changed from SIMILAR - requires .similar() in queries
        )
        
        logger.info("Successfully created content_density_space")
        return space
        
    except Exception as e:
        return handle_space_error(
            "content_density_space",
            e,
            fallback=None,
            reraise=True
        )

@with_error_handling(error_class=SpaceInitializationError)
def create_client_takeaways_space() -> Optional[sl.TextSimilaritySpace]:
    """Create client takeaways space with error handling"""
    try:
        model = config.models.get_model_for_space('discovery')
        logger.info(f"Creating client_takeaways_space with model: {model}")
        
        space = sl.TextSimilaritySpace(
            text=legal_document.key_takeaways,
            model=model
        )
        
        logger.info("Successfully created client_takeaways_space")
        return space
        
    except Exception as e:
        return handle_space_error(
            "client_takeaways_space",
            e,
            fallback=None,
            reraise=True
        )

# Create all spaces with error handling
try:
    discovery_summary_space = create_discovery_summary_space()
    discovery_topics_space = create_discovery_topics_space()
    content_density_space = create_content_density_space()
    client_takeaways_space = create_client_takeaways_space()
    
    # Log successful initialization
    logger.info("All discovery spaces initialized successfully")
    
except SpaceInitializationError as e:
    logger.error(f"Failed to initialize discovery spaces: {e}")
    # Re-raise to stop application startup if critical spaces fail
    raise

# Discovery Space Collections
DISCOVERY_CONTENT_SPACES = [
    space for space in [
        discovery_summary_space,
        discovery_topics_space,
        client_takeaways_space
    ] if space is not None
]

DISCOVERY_METADATA_SPACES = [
    space for space in [
        content_density_space,
        coverage_scope_space
    ] if space is not None
]

ALL_DISCOVERY_SPACES = DISCOVERY_CONTENT_SPACES + DISCOVERY_METADATA_SPACES

# Log space collection summary
logger.info(
    "Discovery spaces loaded",
    extra={
        'content_spaces': len(DISCOVERY_CONTENT_SPACES),
        'metadata_spaces': len(DISCOVERY_METADATA_SPACES),
        'total_spaces': len(ALL_DISCOVERY_SPACES)
    }
)

# Export spaces
__all__ = [
    'discovery_summary_space',
    'discovery_topics_space',
    'content_density_space',
    'client_takeaways_space',
    'DISCOVERY_CONTENT_SPACES',
    'DISCOVERY_METADATA_SPACES',
    'ALL_DISCOVERY_SPACES'
]

# Usage Examples with Error Handling:
"""
Discovery Query Patterns with Error Handling:

1. Basic Discovery with Error Recovery:
   from utils.errors import QueryExecutionError
   
   try:
       results = query_with_spaces(
           query="Texas employment law overview",
           spaces={
               discovery_summary_space: 3.0,
               discovery_topics_space: 2.0,
               client_takeaways_space: 1.5
           }
       )
   except QueryExecutionError as e:
       logger.error(f"Query failed: {e}")
       # Fallback to simpler query
       results = simple_text_search(query)

2. Configurable Model Selection:
   from utils import get_config
   
   config = get_config()
   fast_model = config.models.fast_model
   
   # Create fast discovery space for quick searches
   fast_discovery_space = sl.TextSimilaritySpace(
       text=legal_document.summary,
       model=fast_model
   )

3. Logged Query Execution:
   from utils.logging import log_query_execution
   import time
   
   start_time = time.time()
   results = execute_discovery_query(query_text)
   execution_time = time.time() - start_time
   
   log_query_execution(
       logger,
       query_type="discovery",
       query_text=query_text,
       num_results=len(results),
       execution_time=execution_time
   )
"""