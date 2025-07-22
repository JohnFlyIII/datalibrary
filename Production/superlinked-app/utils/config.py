"""
Configuration Management

Purpose:
- Centralized configuration for models and settings
- Environment-based configuration
- Model configuration with fallbacks

Human Note: Update model configurations based on performance testing
AI Agent Note: Use appropriate models for different space types
"""

import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path

from .errors import ConfigurationError
from .logging import get_logger

logger = get_logger(__name__)

@dataclass
class ModelConfig:
    """Configuration for embedding models"""
    
    # Default models for different purposes
    text_similarity_model: str = "sentence-transformers/all-mpnet-base-v2"
    multilingual_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    legal_specialized_model: str = "sentence-transformers/all-mpnet-base-v2"  # Can be replaced with legal-specific model
    fast_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Model dimensions
    model_dimensions: Dict[str, int] = field(default_factory=lambda: {
        "sentence-transformers/all-mpnet-base-v2": 768,
        "sentence-transformers/paraphrase-multilingual-mpnet-base-v2": 768,
        "sentence-transformers/all-MiniLM-L6-v2": 384,
        "openai/text-embedding-ada-002": 1536,
        "cohere/embed-english-v3.0": 1024
    })
    
    # Model selection by space type
    space_type_models: Dict[str, str] = field(default_factory=lambda: {
        "discovery": "sentence-transformers/all-mpnet-base-v2",
        "exploration": "sentence-transformers/all-mpnet-base-v2",
        "deep_dive": "sentence-transformers/all-mpnet-base-v2",
        "fact_extraction": "sentence-transformers/all-mpnet-base-v2",
        "summary": "sentence-transformers/all-mpnet-base-v2",
        "multilingual": "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
        "fast_search": "sentence-transformers/all-MiniLM-L6-v2"
    })
    
    def get_model_for_space(self, space_type: str) -> str:
        """Get appropriate model for a space type"""
        return self.space_type_models.get(space_type, self.text_similarity_model)
    
    def get_model_dimension(self, model_name: str) -> int:
        """Get dimension for a model"""
        return self.model_dimensions.get(model_name, 768)  # Default to 768

@dataclass
class VectorDBConfig:
    """Configuration for vector database"""
    
    host: str = "qdrant"
    port: int = 6333
    collection_name: str = "legal_knowledge"
    timeout: int = 30
    grpc_port: Optional[int] = None
    prefer_grpc: bool = False
    
    # Collection settings
    distance_metric: str = "Cosine"
    shard_number: int = 4
    replication_factor: int = 1
    
    # Performance settings
    batch_size: int = 100
    parallel_workers: int = 4

@dataclass
class ProcessingConfig:
    """Configuration for document processing"""
    
    # Chunking settings
    chunk_size: int = 2000
    chunk_overlap: int = 200
    min_chunk_size: int = 500
    respect_sections: bool = True
    
    # AI preprocessing
    ai_provider: str = "anthropic"  # "anthropic" or "openai"
    fact_extraction_model: str = "claude-3-sonnet-20240229"
    summary_model: str = "claude-3-sonnet-20240229"
    max_facts_per_page: int = 10
    confidence_threshold: float = 0.85
    
    # Claude-specific settings
    claude_models: Dict[str, str] = field(default_factory=lambda: {
        "opus": "claude-3-opus-20240229",
        "sonnet": "claude-3-sonnet-20240229",
        "haiku": "claude-3-haiku-20240307"
    })
    
    # Processing limits
    max_document_size_mb: int = 100
    timeout_seconds: int = 300
    max_tokens_per_request: int = 4000

@dataclass
class QueryConfig:
    """Configuration for query handling"""
    
    # Default query settings
    default_limit: int = 10
    max_limit: int = 100
    score_threshold: float = 0.7
    
    # Query weights
    default_space_weight: float = 1.0
    boost_factor: float = 2.0
    
    # Performance
    enable_caching: bool = True
    cache_ttl_seconds: int = 900  # 15 minutes

class Config:
    """Main configuration class"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.models = ModelConfig()
        self.vector_db = VectorDBConfig()
        self.processing = ProcessingConfig()
        self.query = QueryConfig()
        
        # Load from environment
        self._load_from_env()
        
        # Load from file if provided
        if config_file:
            self._load_from_file(config_file)
            
        logger.info("Configuration loaded", extra={'config_file': config_file})
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        # Vector DB settings
        if os.getenv('QDRANT_HOST'):
            self.vector_db.host = os.getenv('QDRANT_HOST')
        if os.getenv('QDRANT_PORT'):
            self.vector_db.port = int(os.getenv('QDRANT_PORT'))
        if os.getenv('QDRANT_COLLECTION'):
            self.vector_db.collection_name = os.getenv('QDRANT_COLLECTION')
            
        # Model settings
        if os.getenv('DEFAULT_EMBEDDING_MODEL'):
            self.models.text_similarity_model = os.getenv('DEFAULT_EMBEDDING_MODEL')
        if os.getenv('LEGAL_EMBEDDING_MODEL'):
            self.models.legal_specialized_model = os.getenv('LEGAL_EMBEDDING_MODEL')
            
        # Processing settings
        if os.getenv('CHUNK_SIZE'):
            self.processing.chunk_size = int(os.getenv('CHUNK_SIZE'))
        if os.getenv('CHUNK_OVERLAP'):
            self.processing.chunk_overlap = int(os.getenv('CHUNK_OVERLAP'))
        if os.getenv('AI_PROVIDER'):
            self.processing.ai_provider = os.getenv('AI_PROVIDER')
        if os.getenv('CLAUDE_MODEL'):
            self.processing.fact_extraction_model = os.getenv('CLAUDE_MODEL')
            self.processing.summary_model = os.getenv('CLAUDE_MODEL')
    
    def _load_from_file(self, config_file: str):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
                
            # Update models
            if 'models' in config_data:
                for key, value in config_data['models'].items():
                    if hasattr(self.models, key):
                        setattr(self.models, key, value)
                        
            # Update vector DB
            if 'vector_db' in config_data:
                for key, value in config_data['vector_db'].items():
                    if hasattr(self.vector_db, key):
                        setattr(self.vector_db, key, value)
                        
            # Update processing
            if 'processing' in config_data:
                for key, value in config_data['processing'].items():
                    if hasattr(self.processing, key):
                        setattr(self.processing, key, value)
                        
            # Update query
            if 'query' in config_data:
                for key, value in config_data['query'].items():
                    if hasattr(self.query, key):
                        setattr(self.query, key, value)
                        
        except FileNotFoundError:
            raise ConfigurationError(
                'config_file',
                f"Configuration file not found: {config_file}"
            )
        except json.JSONDecodeError as e:
            raise ConfigurationError(
                'config_file',
                f"Invalid JSON in configuration file: {str(e)}"
            )
    
    def save_to_file(self, config_file: str):
        """Save current configuration to file"""
        config_data = {
            'models': {
                'text_similarity_model': self.models.text_similarity_model,
                'multilingual_model': self.models.multilingual_model,
                'legal_specialized_model': self.models.legal_specialized_model,
                'fast_model': self.models.fast_model,
                'space_type_models': self.models.space_type_models,
                'model_dimensions': self.models.model_dimensions
            },
            'vector_db': {
                'host': self.vector_db.host,
                'port': self.vector_db.port,
                'collection_name': self.vector_db.collection_name,
                'timeout': self.vector_db.timeout,
                'distance_metric': self.vector_db.distance_metric,
                'batch_size': self.vector_db.batch_size
            },
            'processing': {
                'chunk_size': self.processing.chunk_size,
                'chunk_overlap': self.processing.chunk_overlap,
                'fact_extraction_model': self.processing.fact_extraction_model,
                'summary_model': self.processing.summary_model,
                'confidence_threshold': self.processing.confidence_threshold
            },
            'query': {
                'default_limit': self.query.default_limit,
                'max_limit': self.query.max_limit,
                'score_threshold': self.query.score_threshold,
                'enable_caching': self.query.enable_caching
            }
        }
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
            
        logger.info(f"Configuration saved to {config_file}")

# Global configuration instance
_config: Optional[Config] = None

def get_config() -> Config:
    """Get global configuration instance"""
    global _config
    if _config is None:
        # Try to load from default location
        config_file = os.getenv('LEGAL_KNOWLEDGE_CONFIG', 'config.json')
        if Path(config_file).exists():
            _config = Config(config_file)
        else:
            _config = Config()
    return _config

def set_config(config: Config):
    """Set global configuration instance"""
    global _config
    _config = config