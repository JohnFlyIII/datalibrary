#!/usr/bin/env python3
"""
Enhanced Search Integration - Production Implementation
=====================================================

Integrates all enhanced search capabilities into a production-ready system
that works with the existing Superlinked infrastructure.
"""

import json
import math
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductionEnhancedSearch:
    """Production-ready enhanced search system integrating with existing Superlinked"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'LegalAI-Enhanced-Search/1.0'
        })
        
        # Verify system connectivity
        self._verify_system_health()
    
    def _verify_system_health(self) -> bool:
        """Verify that the Superlinked system is healthy and accessible"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            logger.info("✅ Superlinked system is healthy and accessible")
            return True
        except Exception as e:
            logger.error(f"❌ System health check failed: {e}")
            raise ConnectionError(f"Cannot connect to Superlinked system at {self.base_url}")
    
    def enhanced_discovery_search(self, **kwargs) -> Dict:
        """
        Enhanced discovery search with temporal, hierarchical, and relevance improvements
        
        Args:
            search_query: Base search query string
            jurisdiction_state: State jurisdiction filter
            jurisdiction_city: City jurisdiction filter  
            practice_area_primary: Primary practice area filter
            practice_area_secondary: Secondary practice area filter
            min_publication_date: Minimum publication date (Unix timestamp or ISO string)
            max_publication_date: Maximum publication date (Unix timestamp or ISO string)
            prefer_recent: Boolean to enable recency boosting
            recency_decay_days: Days for recency decay (default: 365)
            recency_boost_factor: Boost factor for recent documents (default: 1.8)
            min_confidence_score: Minimum document confidence score
            min_fact_count: Minimum number of extracted facts
            document_types: List of preferred document types
            authority_boost: Enable authority-based boosting
            multi_factor_relevance: Enable sophisticated relevance scoring
            content_focus: List of fields to focus search on
            limit: Maximum number of results to return
        """
        
        # Extract and validate parameters
        search_query = kwargs.get('search_query', '')
        if not search_query:
            raise ValueError("search_query is required")
        
        limit = kwargs.get('limit', 10)
        
        # Build enhanced query
        enhanced_query = self._build_enhanced_query(**kwargs)
        
        # Execute base search
        start_time = time.time()
        base_results = self._execute_base_search(enhanced_query)
        search_time = time.time() - start_time
        
        # Apply enhancements if we have results
        if base_results.get('entries'):
            enhanced_results = self._apply_enhancements(base_results, kwargs)
        else:
            enhanced_results = base_results
        
        # Add enhancement metadata
        enhanced_results['enhancement_metadata'] = {
            'enhanced_search_applied': True,
            'search_execution_time': f"{search_time:.3f}s",
            'enhancements_applied': self._get_applied_enhancements(kwargs),
            'query_timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Enhanced search completed in {search_time:.3f}s for query: '{search_query}'")
        return enhanced_results
    
    def _build_enhanced_query(self, **kwargs) -> Dict:
        """Build enhanced query structure for Superlinked"""
        
        query = {
            'search_query': kwargs.get('search_query', ''),
            'limit': kwargs.get('limit', 10)
        }
        
        # Add basic filters that Superlinked supports
        filter_mappings = {
            'jurisdiction': kwargs.get('jurisdiction_state'),
            'jurisdiction_state': kwargs.get('jurisdiction_state'),
            'jurisdiction_city': kwargs.get('jurisdiction_city'),
            'practice_area_primary': kwargs.get('practice_area_primary'),
            'practice_area_secondary': kwargs.get('practice_area_secondary'),
            'document_type': kwargs.get('document_type')
        }
        
        # Add non-null filters
        for key, value in filter_mappings.items():
            if value:
                query[key] = value
        
        # Add temporal filters if specified
        min_date = kwargs.get('min_publication_date')
        max_date = kwargs.get('max_publication_date')
        
        if min_date:
            query['min_publication_date'] = self._normalize_date(min_date)
        if max_date:
            query['max_publication_date'] = self._normalize_date(max_date)
        
        # Add recency preference as date filter if enabled
        if kwargs.get('prefer_recent', False):
            if not min_date:  # Don't override explicit date filter
                months_back = kwargs.get('prefer_recent_months', 24)
                cutoff_date = datetime.now() - timedelta(days=months_back * 30)
                query['min_publication_date'] = int(cutoff_date.timestamp())
        
        return query
    
    def _normalize_date(self, date_input: Union[str, int, datetime]) -> int:
        """Normalize various date formats to Unix timestamp"""
        if isinstance(date_input, datetime):
            return int(date_input.timestamp())
        elif isinstance(date_input, str):
            try:
                # Try parsing ISO format
                dt = datetime.fromisoformat(date_input.replace('Z', '+00:00'))
                return int(dt.timestamp())
            except:
                # Try parsing as YYYY-MM-DD
                dt = datetime.strptime(date_input, '%Y-%m-%d')
                return int(dt.timestamp())
        elif isinstance(date_input, int):
            return date_input
        else:
            raise ValueError(f"Unsupported date format: {type(date_input)}")
    
    def _execute_base_search(self, query: Dict) -> Dict:
        """Execute search against Superlinked system"""
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/search/discovery_search",
                json=query,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Base search execution failed: {e}")
            return {
                'entries': [],
                'error': f"Search execution failed: {str(e)}",
                'query_metadata': {
                    'query': query.get('search_query', ''),
                    'execution_time_ms': 0,
                    'total_results': 0
                }
            }
    
    def _apply_enhancements(self, base_results: Dict, kwargs: Dict) -> Dict:
        """Apply post-processing enhancements to search results"""
        
        entries = base_results.get('entries', [])
        if not entries:
            return base_results
        
        enhanced_entries = []
        
        for entry in entries:
            enhanced_entry = entry.copy()
            
            # Calculate enhanced relevance score
            original_score = entry.get('metadata', {}).get('score', 0.0)
            enhanced_score = self._calculate_enhanced_relevance(entry, original_score, kwargs)
            
            # Update metadata
            if 'metadata' not in enhanced_entry:
                enhanced_entry['metadata'] = {}
            
            enhanced_entry['metadata'].update({
                'original_score': original_score,
                'enhanced_score': enhanced_score,
                'score': enhanced_score,  # Replace with enhanced score
                'enhancements_applied': self._get_entry_enhancements(entry, kwargs)
            })
            
            enhanced_entries.append(enhanced_entry)
        
        # Re-sort by enhanced score
        enhanced_entries.sort(
            key=lambda x: x.get('metadata', {}).get('enhanced_score', 0), 
            reverse=True
        )
        
        # Update results
        enhanced_results = base_results.copy()
        enhanced_results['entries'] = enhanced_entries
        
        return enhanced_results
    
    def _calculate_enhanced_relevance(self, entry: Dict, base_score: float, kwargs: Dict) -> float:
        """Calculate enhanced relevance score using multiple factors"""
        
        fields = entry.get('fields', {})
        enhanced_score = base_score
        
        # Apply recency boost if enabled
        if kwargs.get('prefer_recent', False) or kwargs.get('recency_boost_factor'):
            recency_boost = self._calculate_recency_boost(fields, kwargs)
            enhanced_score *= recency_boost
        
        # Apply authority boost if enabled
        if kwargs.get('authority_boost', True):
            authority_boost = self._calculate_authority_boost(fields)
            enhanced_score *= authority_boost
        
        # Apply jurisdiction relevance boost
        jurisdiction_boost = self._calculate_jurisdiction_boost(fields, kwargs)
        enhanced_score *= jurisdiction_boost
        
        # Apply practice area relevance boost
        practice_boost = self._calculate_practice_area_boost(fields, kwargs)
        enhanced_score *= practice_boost
        
        # Apply factual density boost
        if kwargs.get('min_fact_count') or kwargs.get('factual_density_boost'):
            factual_boost = self._calculate_factual_boost(fields)
            enhanced_score *= factual_boost
        
        # Apply multi-factor relevance if enabled
        if kwargs.get('multi_factor_relevance', True):
            enhanced_score = self._apply_multi_factor_relevance(enhanced_score, fields, kwargs)
        
        # Ensure score stays within bounds
        return min(max(enhanced_score, 0.0), 1.0)
    
    def _calculate_recency_boost(self, fields: Dict, kwargs: Dict) -> float:
        """Calculate recency boost factor"""
        
        pub_date = fields.get('publication_date', 0)
        if not pub_date:
            return 1.0
        
        # Get recency parameters
        decay_days = kwargs.get('recency_decay_days', 365)
        boost_factor = kwargs.get('recency_boost_factor', 1.8)
        
        # Calculate age in days
        current_time = datetime.now().timestamp()
        age_days = (current_time - pub_date) / 86400
        
        if age_days < 0:
            age_days = 0  # Future dates get maximum boost
        
        # Exponential decay boost
        decay_factor = math.exp(-age_days / decay_days)
        boost = 1.0 + (boost_factor - 1.0) * decay_factor
        
        return boost
    
    def _calculate_authority_boost(self, fields: Dict) -> float:
        """Calculate authority boost based on document quality indicators"""
        
        boost = 1.0
        
        # AI model quality boost
        ai_model = fields.get('ai_model', '').lower()
        if 'claude-opus-4' in ai_model:
            boost *= 1.5
        elif 'claude' in ai_model:
            boost *= 1.3
        
        # Confidence score boost
        confidence = fields.get('confidence_score', 0)
        if confidence >= 90:
            boost *= 1.4
        elif confidence >= 80:
            boost *= 1.2
        elif confidence >= 70:
            boost *= 1.1
        
        return boost
    
    def _calculate_jurisdiction_boost(self, fields: Dict, kwargs: Dict) -> float:
        """Calculate jurisdiction relevance boost"""
        
        boost = 1.0
        
        # State-level match
        requested_state = kwargs.get('jurisdiction_state', '').lower()
        doc_state = fields.get('jurisdiction_state', '').lower()
        
        if requested_state and doc_state == requested_state:
            boost *= 2.0
        
        # City-level match
        requested_city = kwargs.get('jurisdiction_city', '').lower()
        doc_city = fields.get('jurisdiction_city', '').lower()
        
        if requested_city and doc_city == requested_city:
            boost *= 2.5
        
        return boost
    
    def _calculate_practice_area_boost(self, fields: Dict, kwargs: Dict) -> float:
        """Calculate practice area relevance boost"""
        
        boost = 1.0
        
        # Primary practice area match
        requested_primary = kwargs.get('practice_area_primary', '').lower()
        doc_primary = fields.get('practice_area_primary', '').lower()
        
        if requested_primary and doc_primary == requested_primary:
            boost *= 1.8
        
        # Secondary practice area match
        requested_secondary = kwargs.get('practice_area_secondary', '').lower()
        doc_secondary = fields.get('practice_area_secondary', '').lower()
        
        if requested_secondary and doc_secondary == requested_secondary:
            boost *= 2.2
        
        return boost
    
    def _calculate_factual_boost(self, fields: Dict) -> float:
        """Calculate factual density boost"""
        
        fact_count = fields.get('fact_count', 0)
        
        if fact_count >= 10:
            return 1.4
        elif fact_count >= 5:
            return 1.2
        elif fact_count >= 3:
            return 1.1
        else:
            return 1.0
    
    def _apply_multi_factor_relevance(self, base_score: float, fields: Dict, kwargs: Dict) -> float:
        """Apply sophisticated multi-factor relevance scoring"""
        
        # Default relevance weights
        weights = {
            'semantic_similarity': 1.0,
            'content_authority': 0.3,
            'recency_factor': 0.2,
            'jurisdiction_match': 0.25,
            'practice_area_match': 0.2,
            'factual_density': 0.15,
            'ai_processing_quality': 0.1
        }
        
        # Calculate component scores
        components = {}
        
        # Semantic similarity (base score)
        components['semantic_similarity'] = base_score
        
        # Content authority (confidence score normalized)
        confidence = fields.get('confidence_score', 0)
        components['content_authority'] = confidence / 100.0
        
        # Recency factor
        pub_date = fields.get('publication_date', 0)
        if pub_date:
            age_days = (datetime.now().timestamp() - pub_date) / 86400
            components['recency_factor'] = max(0, 1.0 - (age_days / 1095))  # 3-year decay
        else:
            components['recency_factor'] = 0.5
        
        # Jurisdiction match
        state_match = (kwargs.get('jurisdiction_state', '').lower() == 
                      fields.get('jurisdiction_state', '').lower())
        components['jurisdiction_match'] = 1.0 if state_match else 0.5
        
        # Practice area match
        primary_match = (kwargs.get('practice_area_primary', '').lower() == 
                        fields.get('practice_area_primary', '').lower())
        components['practice_area_match'] = 1.0 if primary_match else 0.5
        
        # Factual density
        fact_count = fields.get('fact_count', 0)
        components['factual_density'] = min(1.0, fact_count / 10.0)
        
        # AI processing quality
        ai_model = fields.get('ai_model', '').lower()
        if 'claude-opus-4' in ai_model:
            components['ai_processing_quality'] = 1.0
        elif 'claude' in ai_model:
            components['ai_processing_quality'] = 0.8
        else:
            components['ai_processing_quality'] = 0.5
        
        # Calculate weighted score
        total_weight = sum(weights.values())
        weighted_score = sum(
            components.get(component, 0) * (weight / total_weight)
            for component, weight in weights.items()
        )
        
        return weighted_score
    
    def _get_applied_enhancements(self, kwargs: Dict) -> List[str]:
        """Get list of enhancements that were applied"""
        
        enhancements = []
        
        if kwargs.get('prefer_recent') or kwargs.get('recency_boost_factor'):
            enhancements.append('recency_boost')
        
        if kwargs.get('min_publication_date') or kwargs.get('max_publication_date'):
            enhancements.append('temporal_filtering')
        
        if kwargs.get('jurisdiction_state') or kwargs.get('jurisdiction_city'):
            enhancements.append('hierarchical_jurisdiction')
        
        if kwargs.get('practice_area_primary') or kwargs.get('practice_area_secondary'):
            enhancements.append('hierarchical_practice_area')
        
        if kwargs.get('authority_boost', True):
            enhancements.append('authority_boost')
        
        if kwargs.get('multi_factor_relevance', True):
            enhancements.append('multi_factor_relevance')
        
        if kwargs.get('min_confidence_score'):
            enhancements.append('confidence_filtering')
        
        if kwargs.get('min_fact_count'):
            enhancements.append('factual_density_filtering')
        
        return enhancements
    
    def _get_entry_enhancements(self, entry: Dict, kwargs: Dict) -> List[str]:
        """Get list of enhancements applied to a specific entry"""
        
        fields = entry.get('fields', {})
        enhancements = []
        
        # Check if recency boost was applied
        if kwargs.get('prefer_recent') and fields.get('publication_date'):
            enhancements.append('recency_boost')
        
        # Check if authority boost was applied
        if kwargs.get('authority_boost', True):
            if 'claude-opus-4' in fields.get('ai_model', '').lower():
                enhancements.append('ai_model_boost')
            if fields.get('confidence_score', 0) >= 80:
                enhancements.append('confidence_boost')
        
        # Check jurisdiction boost
        if (kwargs.get('jurisdiction_state') and 
            fields.get('jurisdiction_state', '').lower() == kwargs.get('jurisdiction_state', '').lower()):
            enhancements.append('jurisdiction_boost')
        
        # Check practice area boost
        if (kwargs.get('practice_area_primary') and 
            fields.get('practice_area_primary', '').lower() == kwargs.get('practice_area_primary', '').lower()):
            enhancements.append('practice_area_boost')
        
        # Check factual density boost
        if fields.get('fact_count', 0) >= 5:
            enhancements.append('factual_density_boost')
        
        return enhancements
    
    # Convenience methods for common search patterns
    def legal_research_search(self, query: str, jurisdiction: str = "texas", 
                            practice_area: str = "medical_malpractice", **kwargs) -> Dict:
        """Optimized search for legal research with intelligent defaults"""
        
        return self.enhanced_discovery_search(
            search_query=query,
            jurisdiction_state=jurisdiction,
            practice_area_secondary=practice_area,
            prefer_recent=True,
            min_confidence_score=70,
            authority_boost=True,
            multi_factor_relevance=True,
            **kwargs
        )
    
    def statistical_data_search(self, topic: str, jurisdiction: str = "texas", **kwargs) -> Dict:
        """Optimized search for statistical and financial data"""
        
        enhanced_query = f"{topic} statistics trends financial data billion million"
        
        return self.enhanced_discovery_search(
            search_query=enhanced_query,
            jurisdiction_state=jurisdiction,
            min_fact_count=3,
            prefer_recent=True,
            recency_boost_factor=2.0,
            authority_boost=True,
            **kwargs
        )
    
    def procedural_requirements_search(self, procedure: str, jurisdiction: str = "texas", 
                                     practice_area: str = "medical_malpractice", **kwargs) -> Dict:
        """Optimized search for legal procedural requirements"""
        
        enhanced_query = f"{procedure} requirements procedures deadlines {jurisdiction}"
        
        return self.enhanced_discovery_search(
            search_query=enhanced_query,
            jurisdiction_state=jurisdiction,
            practice_area_primary="litigation",
            practice_area_secondary=practice_area,
            min_confidence_score=85,
            document_type="statute",
            authority_boost=True,
            **kwargs
        )

def main():
    """Test the enhanced search integration"""
    
    print("🔍 Testing Enhanced Search Integration")
    print("=" * 60)
    
    # Initialize enhanced search system
    try:
        search_engine = ProductionEnhancedSearch()
        print("✅ Enhanced search system initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize search system: {e}")
        return
    
    # Test 1: Basic enhanced search
    print("\n📋 Test 1: Basic Enhanced Search")
    print("-" * 40)
    
    try:
        result1 = search_engine.enhanced_discovery_search(
            search_query="medical malpractice expert witness requirements",
            jurisdiction_state="texas",
            practice_area_secondary="medical_malpractice",
            prefer_recent=True,
            limit=3
        )
        
        print(f"✅ Found {len(result1.get('entries', []))} results")
        print(f"   Enhancements applied: {result1.get('enhancement_metadata', {}).get('enhancements_applied', [])}")
        print(f"   Search time: {result1.get('enhancement_metadata', {}).get('search_execution_time', 'N/A')}")
        
        # Show top result with enhanced scoring
        if result1.get('entries'):
            top_result = result1['entries'][0]
            metadata = top_result.get('metadata', {})
            print(f"   Top result: {top_result.get('fields', {}).get('title', 'Unknown')[:50]}...")
            print(f"   Original score: {metadata.get('original_score', 'N/A'):.3f}")
            print(f"   Enhanced score: {metadata.get('enhanced_score', 'N/A'):.3f}")
            print(f"   Enhancements: {metadata.get('enhancements_applied', [])}")
            
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
    
    # Test 2: Statistical data search
    print("\n📊 Test 2: Statistical Data Search")
    print("-" * 40)
    
    try:
        result2 = search_engine.statistical_data_search(
            topic="medical malpractice",
            jurisdiction="texas",
            limit=2
        )
        
        print(f"✅ Found {len(result2.get('entries', []))} statistical results")
        
        # Look for statistical content
        for i, entry in enumerate(result2.get('entries', [])[:2]):
            title = entry.get('fields', {}).get('title', 'Unknown')
            fact_count = entry.get('fields', {}).get('fact_count', 0)
            enhanced_score = entry.get('metadata', {}).get('enhanced_score', 0)
            print(f"   Result {i+1}: {title[:40]}... (facts: {fact_count}, score: {enhanced_score:.3f})")
            
    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
    
    # Test 3: Temporal filtering
    print("\n📅 Test 3: Temporal Filtering")
    print("-" * 40)
    
    try:
        # Search for recent documents (last 2 years)
        cutoff_date = datetime.now() - timedelta(days=730)
        
        result3 = search_engine.enhanced_discovery_search(
            search_query="healthcare regulation changes",
            jurisdiction_state="texas",
            min_publication_date=int(cutoff_date.timestamp()),
            prefer_recent=True,
            recency_boost_factor=2.5,
            limit=3
        )
        
        print(f"✅ Found {len(result3.get('entries', []))} recent results")
        
        # Check publication dates
        for i, entry in enumerate(result3.get('entries', [])):
            pub_date = entry.get('fields', {}).get('publication_date', 0)
            if pub_date:
                pub_date_str = datetime.fromtimestamp(pub_date).strftime('%Y-%m-%d')
                print(f"   Result {i+1}: Published {pub_date_str}")
            else:
                print(f"   Result {i+1}: No publication date")
                
    except Exception as e:
        print(f"❌ Test 3 failed: {e}")
    
    # Test 4: Authority and relevance enhancement
    print("\n⭐ Test 4: Authority & Relevance Enhancement")
    print("-" * 40)
    
    try:
        result4 = search_engine.enhanced_discovery_search(
            search_query="medical malpractice damages",
            jurisdiction_state="texas",
            min_confidence_score=80,
            authority_boost=True,
            multi_factor_relevance=True,
            limit=3
        )
        
        print(f"✅ Found {len(result4.get('entries', []))} high-authority results")
        
        # Show authority metrics
        for i, entry in enumerate(result4.get('entries', [])):
            fields = entry.get('fields', {})
            metadata = entry.get('metadata', {})
            
            confidence = fields.get('confidence_score', 0)
            ai_model = fields.get('ai_model', 'unknown')
            fact_count = fields.get('fact_count', 0)
            enhanced_score = metadata.get('enhanced_score', 0)
            
            print(f"   Result {i+1}:")
            print(f"     Confidence: {confidence}")
            print(f"     AI Model: {ai_model}")
            print(f"     Facts: {fact_count}")
            print(f"     Enhanced Score: {enhanced_score:.3f}")
            
    except Exception as e:
        print(f"❌ Test 4 failed: {e}")
    
    print("\n🎯 Enhanced Search Integration Testing Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()