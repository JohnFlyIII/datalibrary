#!/usr/bin/env python3
"""
Superlinked Integration Enhancements
===================================

Integration layer for enhanced search capabilities with existing Superlinked system.
Shows how to modify existing endpoints to leverage the full 82+ field structure.
"""

import json
import math
from datetime import datetime
from typing import Dict, List, Optional, Any
import requests

class SuperlinkedEnhancedAdapter:
    """Adapter to integrate enhanced search capabilities with existing Superlinked system"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        
    def enhanced_discovery_search(self, request_data: Dict) -> Dict:
        """
        Enhanced discovery search that processes the sophisticated query structure
        and translates it to Superlinked's native capabilities
        """
        
        # Extract components from enhanced query
        base_query = request_data.get('search_query', '')
        filters = request_data.get('filters', {})
        boost_factors = request_data.get('boost_factors', {})
        temporal_criteria = request_data.get('temporal_criteria', {})
        relevance_weights = request_data.get('relevance_weights', {})
        limit = request_data.get('limit', 10)
        
        # Build Superlinked query with enhancements
        superlinked_query = self._build_superlinked_query(
            base_query, filters, boost_factors, temporal_criteria, relevance_weights, limit
        )
        
        # Execute search
        raw_results = self._execute_superlinked_search(superlinked_query)
        
        # Post-process results with enhanced scoring
        enhanced_results = self._post_process_results(
            raw_results, boost_factors, temporal_criteria, relevance_weights
        )
        
        return enhanced_results
    
    def _build_superlinked_query(self, base_query: str, filters: Dict, 
                                boost_factors: Dict, temporal_criteria: Dict,
                                relevance_weights: Dict, limit: int) -> Dict:
        """Build query structure for Superlinked with enhancements"""
        
        # Start with base query structure
        query = {
            "search_query": base_query,
            "limit": limit
        }
        
        # TEMPORAL FILTERING INTEGRATION
        if temporal_criteria:
            # Add publication date filters
            if 'min_publication_date' in temporal_criteria:
                query['min_publication_date'] = temporal_criteria['min_publication_date']
            if 'max_publication_date' in temporal_criteria:
                query['max_publication_date'] = temporal_criteria['max_publication_date']
        
        # HIERARCHICAL FILTERING INTEGRATION
        # Jurisdiction hierarchy
        if 'jurisdiction_state' in filters:
            query['jurisdiction_state'] = filters['jurisdiction_state']
        if 'jurisdiction_city' in filters:
            query['jurisdiction_city'] = filters['jurisdiction_city']
        if 'jurisdiction_country' in filters:
            query['jurisdiction_country'] = filters['jurisdiction_country']
            
        # Practice area hierarchy
        if 'practice_area_primary' in filters:
            query['practice_area_primary'] = filters['practice_area_primary']
        if 'practice_area_secondary' in filters:
            query['practice_area_secondary'] = filters['practice_area_secondary']
        
        # DOCUMENT TYPE AND AUTHORITY FILTERING
        if 'document_types' in filters:
            query['document_type'] = filters['document_types']
        if 'min_confidence_score' in filters:
            query['min_confidence_score'] = filters['min_confidence_score']
        if 'min_fact_count' in filters:
            query['min_fact_count'] = filters['min_fact_count']
        if 'min_client_relevance_score' in filters:
            query['min_client_relevance_score'] = filters['min_client_relevance_score']
        
        # CONTENT FOCUS FIELDS
        if 'focus_fields' in filters:
            query['focus_fields'] = filters['focus_fields']
        
        # Add boost factor metadata for post-processing
        query['_boost_factors'] = boost_factors
        query['_relevance_weights'] = relevance_weights
        
        return query
    
    def _execute_superlinked_search(self, query: Dict) -> Dict:
        """Execute search against Superlinked system"""
        
        # Remove internal metadata before sending to Superlinked
        clean_query = {k: v for k, v in query.items() if not k.startswith('_')}
        
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/search/discovery_search",
                json=clean_query,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"Superlinked search error: {e}")
            return {"entries": [], "error": str(e)}
    
    def _post_process_results(self, raw_results: Dict, boost_factors: Dict,
                            temporal_criteria: Dict, relevance_weights: Dict) -> Dict:
        """Post-process results with enhanced scoring and ranking"""
        
        entries = raw_results.get('entries', [])
        if not entries:
            return raw_results
        
        # Apply enhanced scoring to each entry
        for entry in entries:
            original_score = entry.get('metadata', {}).get('score', 0.0)
            enhanced_score = self._calculate_enhanced_relevance(
                entry, original_score, boost_factors, temporal_criteria, relevance_weights
            )
            
            # Update metadata with enhanced scoring
            if 'metadata' not in entry:
                entry['metadata'] = {}
            
            entry['metadata']['original_score'] = original_score
            entry['metadata']['enhanced_score'] = enhanced_score
            entry['metadata']['score'] = enhanced_score  # Replace original score
            entry['metadata']['boost_applied'] = self._get_applied_boosts(
                entry, boost_factors, temporal_criteria
            )
        
        # Re-sort by enhanced score
        entries.sort(key=lambda x: x.get('metadata', {}).get('enhanced_score', 0), reverse=True)
        
        # Add enhancement metadata to response
        raw_results['enhancement_metadata'] = {
            'enhanced_scoring_applied': True,
            'boost_factors_used': list(boost_factors.keys()),
            'temporal_filtering_applied': bool(temporal_criteria),
            'multi_factor_relevance': bool(relevance_weights)
        }
        
        return raw_results
    
    def _calculate_enhanced_relevance(self, entry: Dict, base_score: float,
                                    boost_factors: Dict, temporal_criteria: Dict,
                                    relevance_weights: Dict) -> float:
        """Calculate enhanced relevance score using multiple factors"""
        
        fields = entry.get('fields', {})
        enhanced_score = base_score
        
        # RECENCY BOOST
        if 'recency' in boost_factors:
            recency_boost = self._calculate_recency_boost(
                fields, boost_factors['recency']
            )
            enhanced_score *= recency_boost
        
        # AUTHORITY BOOST (based on confidence score and AI model)
        authority_boost = self._calculate_authority_boost(fields, boost_factors)
        enhanced_score *= authority_boost
        
        # JURISDICTION RELEVANCE BOOST
        jurisdiction_boost = self._calculate_jurisdiction_boost(fields, boost_factors)
        enhanced_score *= jurisdiction_boost
        
        # FACTUAL DENSITY BOOST
        factual_boost = self._calculate_factual_density_boost(fields, boost_factors)
        enhanced_score *= factual_boost
        
        # CLIENT RELEVANCE BOOST
        client_boost = self._calculate_client_relevance_boost(fields, boost_factors)
        enhanced_score *= client_boost
        
        # MULTI-FACTOR RELEVANCE WEIGHTING
        if relevance_weights:
            enhanced_score = self._apply_multi_factor_weighting(
                enhanced_score, fields, relevance_weights
            )
        
        # Ensure score stays in reasonable bounds
        return min(enhanced_score, 1.0)
    
    def _calculate_recency_boost(self, fields: Dict, recency_config: Dict) -> float:
        """Calculate boost factor based on document recency"""
        
        pub_date = fields.get('publication_date', 0)
        if not pub_date:
            return 1.0  # No boost if no publication date
        
        reference_date = recency_config.get('reference_date', datetime.now().timestamp())
        decay_days = recency_config.get('decay_days', 365)
        boost_factor = recency_config.get('boost_factor', 2.0)
        
        # Calculate age in days
        age_days = (reference_date - pub_date) / 86400
        
        if age_days < 0:
            age_days = 0  # Future dates get no penalty
        
        # Exponential decay: newer documents get higher boost
        decay_factor = math.exp(-age_days / decay_days)
        boost = 1.0 + (boost_factor - 1.0) * decay_factor
        
        return boost
    
    def _calculate_authority_boost(self, fields: Dict, boost_factors: Dict) -> float:
        """Calculate boost based on document authority indicators"""
        
        boost = 1.0
        
        # AI model preference boost
        if 'ai_model' in boost_factors:
            ai_config = boost_factors['ai_model']
            preferred_model = ai_config.get('preferred_model', '')
            model_boost = ai_config.get('boost_factor', 1.5)
            
            if fields.get('ai_model', '').startswith(preferred_model):
                boost *= model_boost
        
        # Confidence score boost
        confidence_score = fields.get('confidence_score', 0)
        if confidence_score > 80:
            boost *= 1.3
        elif confidence_score > 90:
            boost *= 1.5
        
        return boost
    
    def _calculate_jurisdiction_boost(self, fields: Dict, boost_factors: Dict) -> float:
        """Calculate boost based on jurisdiction relevance"""
        
        if 'jurisdiction_relevance' not in boost_factors:
            return 1.0
        
        jur_config = boost_factors['jurisdiction_relevance']
        state_boost = jur_config.get('state_boost', 1.0)
        city_boost = jur_config.get('city_boost', 1.0)
        
        boost = 1.0
        
        # State-level match gets boost
        if fields.get('jurisdiction_state'):
            boost *= state_boost
        
        # City-level match gets additional boost
        if fields.get('jurisdiction_city'):
            boost *= city_boost
        
        return boost
    
    def _calculate_factual_density_boost(self, fields: Dict, boost_factors: Dict) -> float:
        """Calculate boost based on factual content density"""
        
        if 'factual_density' not in boost_factors:
            return 1.0
        
        fact_count = fields.get('fact_count', 0)
        total_chars = fields.get('total_chars', 1)
        
        # Calculate facts per 1000 characters
        fact_density = (fact_count / total_chars) * 1000 if total_chars > 0 else 0
        
        # Higher fact density gets boost
        if fact_density > 2.0:
            return 1.4
        elif fact_density > 1.0:
            return 1.2
        else:
            return 1.0
    
    def _calculate_client_relevance_boost(self, fields: Dict, boost_factors: Dict) -> float:
        """Calculate boost based on client relevance score"""
        
        if 'client_relevance' not in boost_factors:
            return 1.0
        
        client_score = fields.get('client_relevance_score', 0)
        
        if client_score > 80:
            return 1.3
        elif client_score > 60:
            return 1.15
        else:
            return 1.0
    
    def _apply_multi_factor_weighting(self, base_score: float, fields: Dict,
                                    relevance_weights: Dict) -> float:
        """Apply sophisticated multi-factor relevance weighting"""
        
        if not relevance_weights:
            return base_score
        
        # Calculate component scores
        components = {}
        
        # Semantic similarity (base score)
        components['semantic_similarity'] = base_score
        
        # Content authority (0-1 based on confidence score)
        confidence = fields.get('confidence_score', 0)
        components['content_authority'] = confidence / 100.0
        
        # Recency factor (0-1 based on publication date)
        pub_date = fields.get('publication_date', 0)
        if pub_date:
            age_days = (datetime.now().timestamp() - pub_date) / 86400
            components['recency_factor'] = max(0, 1.0 - (age_days / 1095))  # 3-year decay
        else:
            components['recency_factor'] = 0.5
        
        # Factual density (0-1 based on fact count)
        fact_count = fields.get('fact_count', 0)
        components['factual_density'] = min(1.0, fact_count / 10.0)
        
        # AI processing quality (0-1 based on AI model)
        ai_model = fields.get('ai_model', '')
        if 'claude-opus-4' in ai_model:
            components['ai_processing_quality'] = 1.0
        elif 'claude' in ai_model:
            components['ai_processing_quality'] = 0.8
        else:
            components['ai_processing_quality'] = 0.5
        
        # Calculate weighted average
        total_weight = sum(relevance_weights.values())
        if total_weight == 0:
            return base_score
        
        weighted_score = 0
        for component, weight in relevance_weights.items():
            if component in components:
                weighted_score += components[component] * (weight / total_weight)
        
        return weighted_score
    
    def _get_applied_boosts(self, entry: Dict, boost_factors: Dict,
                          temporal_criteria: Dict) -> List[str]:
        """Get list of boost factors that were applied to this entry"""
        
        applied_boosts = []
        fields = entry.get('fields', {})
        
        if 'recency' in boost_factors and fields.get('publication_date'):
            applied_boosts.append('recency_boost')
        
        if 'ai_model' in boost_factors:
            preferred_model = boost_factors['ai_model'].get('preferred_model', '')
            if fields.get('ai_model', '').startswith(preferred_model):
                applied_boosts.append('ai_model_preference')
        
        if 'jurisdiction_relevance' in boost_factors:
            if fields.get('jurisdiction_state') or fields.get('jurisdiction_city'):
                applied_boosts.append('jurisdiction_relevance')
        
        if 'factual_density' in boost_factors and fields.get('fact_count', 0) > 0:
            applied_boosts.append('factual_density')
        
        if 'client_relevance' in boost_factors and fields.get('client_relevance_score', 0) > 60:
            applied_boosts.append('client_relevance')
        
        return applied_boosts

class EnhancedSearchAPI:
    """Enhanced API endpoints that leverage the SuperlinkedEnhancedAdapter"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.adapter = SuperlinkedEnhancedAdapter(base_url)
    
    def discovery_search_v2(self, request_data: Dict) -> Dict:
        """
        Enhanced discovery search endpoint (v2) with sophisticated capabilities
        
        Example request:
        {
            "search_query": "medical malpractice expert witness requirements",
            "jurisdiction_state": "texas",
            "practice_area_primary": "litigation",
            "prefer_recent": true,
            "min_confidence_score": 80,
            "include_temporal_boost": true,
            "multi_factor_relevance": true,
            "limit": 5
        }
        """
        
        # Convert simplified API parameters to enhanced query structure
        enhanced_request = self._convert_to_enhanced_query(request_data)
        
        # Execute enhanced search
        return self.adapter.enhanced_discovery_search(enhanced_request)
    
    def _convert_to_enhanced_query(self, request_data: Dict) -> Dict:
        """Convert simplified API request to enhanced query structure"""
        
        enhanced_query = {
            "search_query": request_data.get("search_query", ""),
            "limit": request_data.get("limit", 10),
            "filters": {},
            "boost_factors": {},
            "temporal_criteria": {},
            "relevance_weights": {}
        }
        
        # Simple parameter mappings
        simple_filters = [
            'jurisdiction_state', 'jurisdiction_city', 'jurisdiction_country',
            'practice_area_primary', 'practice_area_secondary', 
            'document_type', 'min_confidence_score', 'min_fact_count',
            'min_client_relevance_score'
        ]
        
        for filter_name in simple_filters:
            if filter_name in request_data:
                enhanced_query["filters"][filter_name] = request_data[filter_name]
        
        # Temporal parameters
        if request_data.get("prefer_recent"):
            enhanced_query["boost_factors"]["recency"] = {
                "decay_days": request_data.get("recency_decay_days", 730),
                "boost_factor": request_data.get("recency_boost_factor", 1.8)
            }
        
        if "min_publication_date" in request_data:
            enhanced_query["temporal_criteria"]["min_publication_date"] = request_data["min_publication_date"]
        if "max_publication_date" in request_data:
            enhanced_query["temporal_criteria"]["max_publication_date"] = request_data["max_publication_date"]
        
        # Authority boosting
        if request_data.get("include_authority_boost", True):
            enhanced_query["boost_factors"]["ai_model"] = {
                "preferred_model": "claude-opus-4-20250514",
                "boost_factor": 1.5
            }
        
        # Multi-factor relevance
        if request_data.get("multi_factor_relevance", True):
            enhanced_query["relevance_weights"] = {
                "semantic_similarity": 1.0,
                "content_authority": 0.3,
                "recency_factor": 0.2,
                "jurisdiction_match": 0.25,
                "practice_area_match": 0.2,
                "factual_density": 0.15,
                "ai_processing_quality": 0.1
            }
        
        return enhanced_query

# EXAMPLE IMPLEMENTATION
def demonstrate_enhanced_integration():
    """Demonstrate the enhanced search integration"""
    
    api = EnhancedSearchAPI()
    
    # Example 1: Enhanced legal research query
    print("=== ENHANCED LEGAL RESEARCH QUERY ===")
    request = {
        "search_query": "medical malpractice expert witness requirements",
        "jurisdiction_state": "texas",
        "practice_area_primary": "litigation",
        "practice_area_secondary": "medical_malpractice",
        "prefer_recent": True,
        "min_confidence_score": 80,
        "multi_factor_relevance": True,
        "limit": 5
    }
    
    result = api.discovery_search_v2(request)
    print("Enhanced search completed with sophisticated relevance scoring")
    
    # Example 2: Statistical data query with temporal filtering
    print("\n=== STATISTICAL DATA WITH TEMPORAL FILTERING ===")
    request2 = {
        "search_query": "medical malpractice statistics billion payouts",
        "jurisdiction_state": "texas",
        "min_fact_count": 5,
        "prefer_recent": True,
        "recency_decay_days": 365,
        "include_authority_boost": True,
        "limit": 3
    }
    
    result2 = api.discovery_search_v2(request2)
    print("Statistical search with factual density and recency boosting applied")
    
    return result, result2

if __name__ == "__main__":
    demonstrate_enhanced_integration()