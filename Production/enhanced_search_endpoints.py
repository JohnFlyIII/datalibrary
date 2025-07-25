#!/usr/bin/env python3
"""
Enhanced Search Endpoints - Address Chunk Content Limitations
============================================================

Adds specialized endpoints for retrieving full chunk content when summaries aren't sufficient.
"""

from typing import Dict, List, Optional
import requests
import json

class EnhancedSearchClient:
    """Enhanced search client with chunk content retrieval"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
    
    def discovery_with_chunks(self, search_query: str, limit: int = 5, 
                             include_chunks: bool = True) -> Dict:
        """
        Enhanced discovery search that can optionally include full chunk content
        when document summaries don't provide enough detail.
        """
        # First, do standard discovery
        discovery_results = self.discovery_search(search_query, limit)
        
        if not include_chunks:
            return discovery_results
        
        # For each document, fetch detailed chunks if available
        enhanced_results = discovery_results.copy()
        
        for i, entry in enumerate(enhanced_results.get('entries', [])):
            doc_id = entry.get('id')
            if doc_id:
                # Fetch chunks for this document
                chunks = self.get_document_chunks(doc_id, search_query)
                if chunks:
                    enhanced_results['entries'][i]['detailed_chunks'] = chunks
        
        return enhanced_results
    
    def get_document_chunks(self, document_id: str, query: str = "", 
                           max_chunks: int = 5) -> List[Dict]:
        """
        Retrieve specific chunks from a document, optionally filtered by query relevance.
        Addresses limitation: "Limited Chunk Content in summary queries"
        """
        try:
            # Use deep_dive_precise to get chunks for specific document
            response = requests.post(
                f"{self.base_url}/api/v1/search/deep_dive_precise",
                json={
                    "search_query": f"document_id:{document_id} {query}".strip(),
                    "limit": max_chunks,
                    "document_type": "",  # Allow any type
                    "jurisdiction": ""    # Allow any jurisdiction
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                chunks = []
                
                for entry in data.get('entries', []):
                    # Extract chunk content and metadata
                    chunk_info = {
                        'chunk_id': entry.get('id'),
                        'content': entry.get('fields', {}).get('content', ''),
                        'chunk_index': entry.get('fields', {}).get('chunk_index', 0),
                        'start_char': entry.get('fields', {}).get('start_char', 0),
                        'end_char': entry.get('fields', {}).get('end_char', 0),
                        'relevance_score': entry.get('metadata', {}).get('score', 0),
                        'context': entry.get('fields', {}).get('chunk_context', '')
                    }
                    chunks.append(chunk_info)
                
                # Sort by relevance score
                chunks.sort(key=lambda x: x['relevance_score'], reverse=True)
                return chunks
                
        except Exception as e:
            print(f"Error fetching chunks for document {document_id}: {e}")
        
        return []
    
    def discovery_search(self, search_query: str, limit: int = 5) -> Dict:
        """Standard discovery search"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/search/discovery_search",
                json={"search_query": search_query, "limit": limit},
                timeout=30
            )
            return response.json() if response.status_code == 200 else {}
        except:
            return {}

# Usage example for blog research
def enhanced_medical_malpractice_research():
    """
    Example showing how enhanced chunk retrieval addresses content limitations
    """
    client = EnhancedSearchClient()
    
    # Phase 1: Discovery with detailed chunks when needed
    discovery = client.discovery_with_chunks(
        "medical malpractice expert witness requirements", 
        limit=3, 
        include_chunks=True
    )
    
    # Now we have both document summaries AND detailed chunk content
    for entry in discovery.get('entries', []):
        print(f"Document: {entry.get('fields', {}).get('title', 'Unknown')}")
        print(f"Summary: {entry.get('fields', {}).get('executive_summary', 'No summary')[:200]}...")
        
        # ENHANCED: Access to detailed chunks
        if 'detailed_chunks' in entry:
            print("Detailed chunks available:")
            for chunk in entry['detailed_chunks'][:2]:  # Show top 2 chunks
                content = chunk['content'][:300] + "..." if len(chunk['content']) > 300 else chunk['content']
                print(f"  Chunk {chunk['chunk_index']}: {content}")
                print(f"  Relevance: {chunk['relevance_score']:.3f}")
        print("-" * 80)

if __name__ == "__main__":
    enhanced_medical_malpractice_research()