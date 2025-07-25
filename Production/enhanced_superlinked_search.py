#!/usr/bin/env python3
"""
Enhanced Superlinked Search Implementation
=========================================

Leverages the full 82+ field legal document structure for sophisticated search capabilities:
1. Temporal/Recency filtering and boost
2. Hierarchical structure awareness
3. Multi-factor relevance scoring
4. Advanced query parsing and filtering

Addresses current limitations in discovery_search and other endpoints.
"""

from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
import json
import math

class EnhancedLegalSearchQuery:
    """Enhanced query builder leveraging full legal document structure"""
    
    def __init__(self):
        self.base_query = ""
        self.filters = {}
        self.boost_factors = {}
        self.sort_criteria = []
        self.temporal_criteria = {}
        self.relevance_weights = {}
        
    # TEMPORAL/RECENCY ENHANCEMENTS
    def with_publication_date_range(self, start_date: Union[datetime, str, int] = None, 
                                  end_date: Union[datetime, str, int] = None):
        """Add publication date filtering"""
        if start_date:
            self.temporal_criteria['min_publication_date'] = self._normalize_date(start_date)
        if end_date:
            self.temporal_criteria['max_publication_date'] = self._normalize_date(end_date)
        return self
    
    def with_recency_boost(self, decay_days: int = 365, boost_factor: float = 2.0):
        """Boost newer documents with exponential decay"""
        self.boost_factors['recency'] = {
            'decay_days': decay_days,
            'boost_factor': boost_factor,
            'reference_date': datetime.now().timestamp()
        }
        return self
    
    def prefer_recent(self, months_back: int = 12):
        """Prefer documents from last N months"""
        cutoff_date = datetime.now() - timedelta(days=months_back * 30)
        return self.with_publication_date_range(start_date=cutoff_date)
    
    # HIERARCHICAL STRUCTURE LEVERAGE
    def with_jurisdiction_hierarchy(self, country: str = None, state: str = None, 
                                  city: str = None, exact_match: bool = False):
        """Leverage jurisdiction hierarchy for filtering"""
        if country:
            self.filters['jurisdiction_country'] = country
        if state:
            self.filters['jurisdiction_state'] = state
        if city:
            self.filters['jurisdiction_city'] = city
        
        # If not exact match, also search broader jurisdictions
        if not exact_match and state:
            self.boost_factors['jurisdiction_relevance'] = {
                'state_boost': 2.0,
                'city_boost': 3.0 if city else 1.0
            }
        return self
    
    def with_practice_area_hierarchy(self, primary: str = None, secondary: str = None, 
                                   specific: str = None):
        """Leverage practice area hierarchy"""
        if primary:
            self.filters['practice_area_primary'] = primary
        if secondary:
            self.filters['practice_area_secondary'] = secondary
        if specific:
            self.filters['practice_area_specific'] = specific
        return self
    
    def with_document_authority(self, min_confidence: int = 70, 
                              prefer_ai_model: str = "claude-opus-4-20250514"):
        """Filter by document authority and AI processing quality"""
        self.filters['min_confidence_score'] = min_confidence
        if prefer_ai_model:
            self.boost_factors['ai_model'] = {
                'preferred_model': prefer_ai_model,
                'boost_factor': 1.5
            }
        return self
    
    # ADVANCED QUERY CAPABILITIES
    def with_content_focus(self, focus_fields: List[str], weights: Dict[str, float] = None):
        """Focus search on specific content fields with weights"""
        default_weights = {
            'title': 3.0,
            'executive_summary': 2.0,
            'key_findings': 2.5,
            'key_takeaways': 1.5,
            'legal_topics': 2.0,
            'keywords': 1.8,
            'content': 1.0
        }
        
        self.relevance_weights = weights or default_weights
        self.filters['focus_fields'] = focus_fields
        return self
    
    def with_document_types(self, doc_types: List[str], preference_order: List[str] = None):
        """Filter and optionally rank by document types"""
        self.filters['document_types'] = doc_types
        if preference_order:
            self.boost_factors['document_type_preference'] = {
                type_name: len(preference_order) - idx 
                for idx, type_name in enumerate(preference_order)
            }
        return self
    
    def with_factual_density(self, min_fact_count: int = 3, boost_high_density: bool = True):
        """Prefer documents with more extracted facts"""
        self.filters['min_fact_count'] = min_fact_count
        if boost_high_density:
            self.boost_factors['factual_density'] = {'enabled': True}
        return self
    
    # RELEVANCE ENHANCEMENT
    def with_multi_factor_relevance(self, enable_all: bool = True):
        """Enable sophisticated relevance scoring"""
        if enable_all:
            self.relevance_weights.update({
                'semantic_similarity': 1.0,      # Base similarity score
                'content_authority': 0.3,        # Based on confidence_score
                'recency_factor': 0.2,          # Time decay
                'jurisdiction_match': 0.25,      # Jurisdiction relevance
                'practice_area_match': 0.2,     # Practice area alignment
                'factual_density': 0.15,        # Number of extracted facts
                'ai_processing_quality': 0.1    # AI model quality
            })
        return self
    
    def with_client_relevance_boost(self, min_client_score: int = 60):
        """Boost documents with high client relevance scores"""
        self.filters['min_client_relevance_score'] = min_client_score
        self.boost_factors['client_relevance'] = {'enabled': True}
        return self
    
    # QUERY BUILDING METHODS
    def _normalize_date(self, date_input: Union[datetime, str, int]) -> int:
        """Normalize various date formats to Unix timestamp"""
        if isinstance(date_input, datetime):
            return int(date_input.timestamp())
        elif isinstance(date_input, str):
            # Parse ISO format
            return int(datetime.fromisoformat(date_input.replace('Z', '+00:00')).timestamp())
        elif isinstance(date_input, int):
            return date_input
        else:
            raise ValueError(f"Unsupported date format: {type(date_input)}")
    
    def build_superlinked_query(self) -> Dict:
        """Build the final query for Superlinked API"""
        query = {
            'search_query': self.base_query,
            'filters': self.filters,
            'boost_factors': self.boost_factors,
            'sort_criteria': self.sort_criteria,
            'temporal_criteria': self.temporal_criteria,
            'relevance_weights': self.relevance_weights
        }
        
        # Remove empty sections
        return {k: v for k, v in query.items() if v}

class EnhancedDiscoverySearch:
    """Enhanced discovery search leveraging full legal document structure"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
    
    def legal_research_discovery(self, 
                               query: str,
                               jurisdiction: str = "texas",
                               practice_area: str = None,
                               prefer_recent: bool = True,
                               min_authority: int = 70,
                               limit: int = 5) -> Dict:
        """
        Enhanced discovery search for legal research with intelligent defaults
        """
        
        # Build enhanced query
        search_query = EnhancedLegalSearchQuery()
        search_query.base_query = query
        
        # Apply jurisdiction intelligence
        if jurisdiction:
            # Intelligent jurisdiction parsing
            if jurisdiction.lower() in ['texas', 'tx']:
                search_query.with_jurisdiction_hierarchy(
                    country='united_states', 
                    state='texas'
                )
            elif jurisdiction.lower() in ['california', 'ca']:
                search_query.with_jurisdiction_hierarchy(
                    country='united_states', 
                    state='california'
                )
        
        # Apply practice area filtering
        if practice_area:
            if 'medical_malpractice' in practice_area.lower():
                search_query.with_practice_area_hierarchy(
                    primary='litigation',
                    secondary='medical_malpractice'
                )
            elif 'healthcare' in practice_area.lower():
                search_query.with_practice_area_hierarchy(
                    primary='healthcare'
                )
        
        # Apply recency preferences
        if prefer_recent:
            search_query.with_recency_boost(decay_days=730, boost_factor=1.8)
            search_query.prefer_recent(months_back=24)  # Prefer last 2 years
        
        # Apply authority filtering
        search_query.with_document_authority(
            min_confidence=min_authority,
            prefer_ai_model="claude-opus-4-20250514"
        )
        
        # Enable multi-factor relevance
        search_query.with_multi_factor_relevance()
        
        # Focus on key content fields for legal research
        search_query.with_content_focus([
            'title', 'executive_summary', 'key_findings', 
            'key_takeaways', 'legal_topics'
        ])
        
        # Prefer high-quality document types
        search_query.with_document_types(
            ['statute', 'regulation', 'case'],
            preference_order=['statute', 'regulation', 'case']
        )
        
        # Build final query
        enhanced_query = search_query.build_superlinked_query()
        enhanced_query['limit'] = limit
        
        return self._execute_enhanced_search(enhanced_query)
    
    def statistical_research_discovery(self,
                                     topic: str,
                                     jurisdiction: str = "texas", 
                                     require_financial_data: bool = True,
                                     limit: int = 3) -> Dict:
        """
        Specialized discovery for statistical/financial legal data
        """
        
        # Build query focused on statistical content
        search_query = EnhancedLegalSearchQuery()
        search_query.base_query = f"{topic} statistics trends financial data billion million"
        
        # Jurisdiction filtering
        if jurisdiction:
            search_query.with_jurisdiction_hierarchy(state=jurisdiction)
        
        # Focus on statistical content
        search_query.with_content_focus([
            'title', 'executive_summary', 'key_findings', 'extracted_facts'
        ], weights={
            'title': 2.0,           # Statistical reports often have descriptive titles
            'executive_summary': 3.0, # Summary likely contains key statistics
            'key_findings': 2.5,    # Findings contain statistical analysis
            'extracted_facts': 4.0  # Facts likely contain specific numbers
        })
        
        # Prefer documents with high factual density
        search_query.with_factual_density(min_fact_count=5, boost_high_density=True)
        
        # Prefer regulation type documents (often contain statistical reports)
        search_query.with_document_types(
            ['regulation', 'statute'],
            preference_order=['regulation', 'statute']
        )
        
        # Boost recent data
        search_query.with_recency_boost(decay_days=365, boost_factor=2.5)
        
        # Multi-factor relevance with emphasis on factual content
        search_query.with_multi_factor_relevance()
        search_query.relevance_weights['factual_density'] = 0.4  # Higher weight for stats
        
        enhanced_query = search_query.build_superlinked_query()
        enhanced_query['limit'] = limit
        
        return self._execute_enhanced_search(enhanced_query)
    
    def procedural_requirements_discovery(self,
                                        procedure_type: str,
                                        jurisdiction: str = "texas",
                                        practice_area: str = "medical_malpractice",
                                        limit: int = 5) -> Dict:
        """
        Specialized discovery for legal procedural requirements
        """
        
        search_query = EnhancedLegalSearchQuery()
        search_query.base_query = f"{procedure_type} requirements deadlines procedures {jurisdiction}"
        
        # Jurisdiction and practice area filtering
        search_query.with_jurisdiction_hierarchy(state=jurisdiction)
        search_query.with_practice_area_hierarchy(primary='litigation', secondary=practice_area)
        
        # Focus on procedural content fields
        search_query.with_content_focus([
            'compliance_requirements', 'deadlines_timeframes', 
            'key_provisions', 'practical_implications'
        ], weights={
            'compliance_requirements': 4.0,  # Primary field for requirements
            'deadlines_timeframes': 3.5,     # Critical for procedural info
            'key_provisions': 3.0,           # Legal provisions
            'practical_implications': 2.5    # Real-world guidance
        })
        
        # Prefer authoritative sources
        search_query.with_document_types(
            ['statute', 'regulation'],
            preference_order=['statute', 'regulation']
        )
        
        # High authority threshold for procedural requirements
        search_query.with_document_authority(min_confidence=85)
        
        # Client relevance boost
        search_query.with_client_relevance_boost(min_client_score=70)
        
        enhanced_query = search_query.build_superlinked_query()
        enhanced_query['limit'] = limit
        
        return self._execute_enhanced_search(enhanced_query)
    
    def _execute_enhanced_search(self, enhanced_query: Dict) -> Dict:
        """
        Execute the enhanced search query
        (This would integrate with your actual Superlinked implementation)
        """
        
        # For now, this is a framework - you would integrate with actual Superlinked API
        # The enhanced_query contains all the sophisticated filtering and boosting logic
        
        print("Enhanced Query Structure:")
        print(json.dumps(enhanced_query, indent=2))
        
        # Placeholder response structure
        return {
            "enhanced_query": enhanced_query,
            "execution_notes": [
                "Multi-factor relevance scoring applied",
                "Temporal boosting configured", 
                "Hierarchical filtering enabled",
                "Authority thresholds applied"
            ],
            "search_strategy": self._analyze_search_strategy(enhanced_query)
        }
    
    def _analyze_search_strategy(self, query: Dict) -> Dict:
        """Analyze the search strategy for debugging/optimization"""
        strategy = {
            "temporal_strategy": "none",
            "authority_filtering": False,
            "hierarchical_filtering": False,
            "relevance_factors": [],
            "content_focus": []
        }
        
        if query.get('temporal_criteria'):
            strategy["temporal_strategy"] = "date_range_filtering"
        if query.get('boost_factors', {}).get('recency'):
            strategy["temporal_strategy"] = "recency_boosted"
            
        if query.get('filters', {}).get('min_confidence_score'):
            strategy["authority_filtering"] = True
            
        if any(key.startswith('jurisdiction_') or key.startswith('practice_area_') 
               for key in query.get('filters', {})):
            strategy["hierarchical_filtering"] = True
            
        strategy["relevance_factors"] = list(query.get('relevance_weights', {}).keys())
        strategy["content_focus"] = query.get('filters', {}).get('focus_fields', [])
        
        return strategy

# EXAMPLE USAGE PATTERNS
def example_enhanced_searches():
    """Examples showing enhanced search capabilities"""
    
    search_engine = EnhancedDiscoverySearch()
    
    print("=== EXAMPLE 1: COMPREHENSIVE LEGAL RESEARCH ===")
    result1 = search_engine.legal_research_discovery(
        query="medical malpractice expert witness requirements",
        jurisdiction="texas",
        practice_area="medical_malpractice",
        prefer_recent=True,
        min_authority=80,
        limit=5
    )
    
    print("\n=== EXAMPLE 2: STATISTICAL DATA RESEARCH ===")
    result2 = search_engine.statistical_research_discovery(
        topic="medical malpractice",
        jurisdiction="texas",
        require_financial_data=True,
        limit=3
    )
    
    print("\n=== EXAMPLE 3: PROCEDURAL REQUIREMENTS ===")
    result3 = search_engine.procedural_requirements_discovery(
        procedure_type="expert witness",
        jurisdiction="texas",
        practice_area="medical_malpractice",
        limit=5
    )
    
    return result1, result2, result3

if __name__ == "__main__":
    example_enhanced_searches()