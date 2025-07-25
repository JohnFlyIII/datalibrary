#!/usr/bin/env python3
"""
Specialized Legal Endpoints - Address Procedure-Specific Query Limitations
=========================================================================

Adds domain-specific endpoints for common legal research patterns like
expert witness requirements, damages calculations, and procedural deadlines.
"""

from typing import Dict, List, Optional
import requests
import json
from datetime import datetime

class SpecializedLegalSearch:
    """Specialized search endpoints for common legal research patterns"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
    
    def expert_witness_requirements(self, jurisdiction: str = "texas", 
                                  practice_area: str = "medical_malpractice") -> Dict:
        """
        Specialized endpoint for expert witness requirements.
        Addresses limitation: "No Procedure-Specific Queries"
        """
        # Multi-query approach for comprehensive expert witness info
        queries = [
            f"expert witness qualifications {jurisdiction} {practice_area}",
            f"expert witness requirements board certified {jurisdiction}",
            f"expert report deadline days {jurisdiction}",
            f"expert witness testimony standards {jurisdiction}"
        ]
        
        combined_results = {
            'jurisdiction': jurisdiction,
            'practice_area': practice_area,
            'expert_requirements': [],
            'qualification_standards': [],
            'procedural_deadlines': [],
            'testimony_rules': []
        }
        
        for query in queries:
            try:
                response = requests.post(
                    f"{self.base_url}/api/v1/search/discovery_search",
                    json={"search_query": query, "limit": 3},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self._extract_expert_witness_data(data, combined_results, query)
                    
            except Exception as e:
                print(f"Error in expert witness query '{query}': {e}")
        
        return combined_results
    
    def damages_calculation_framework(self, jurisdiction: str = "texas",
                                    case_type: str = "medical_malpractice") -> Dict:
        """
        Specialized endpoint for damages calculation information.
        """
        queries = [
            f"damages economic noneconomic {jurisdiction} {case_type}",
            f"damages cap limitation {jurisdiction}",
            f"exemplary punitive damages {jurisdiction}",
            f"mental anguish damages {jurisdiction}"
        ]
        
        damages_info = {
            'jurisdiction': jurisdiction,
            'case_type': case_type,
            'economic_damages': [],
            'noneconomic_damages': [],
            'damage_caps': [],
            'exemplary_damages': []
        }
        
        for query in queries:
            try:
                response = requests.post(
                    f"{self.base_url}/api/v1/search/discovery_search",
                    json={"search_query": query, "limit": 2},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self._extract_damages_data(data, damages_info, query)
                    
            except Exception as e:
                print(f"Error in damages query '{query}': {e}")
        
        return damages_info
    
    def procedural_deadlines(self, jurisdiction: str = "texas",
                           case_type: str = "medical_malpractice") -> Dict:
        """
        Specialized endpoint for procedural deadlines and timeframes.
        """
        queries = [
            f"statute of limitations {jurisdiction} {case_type}",
            f"expert report deadline {jurisdiction}",
            f"discovery deadlines {jurisdiction}",
            f"filing requirements timeline {jurisdiction}"
        ]
        
        deadline_info = {
            'jurisdiction': jurisdiction,
            'case_type': case_type,
            'statute_of_limitations': [],
            'expert_report_deadlines': [],
            'discovery_deadlines': [],
            'filing_requirements': []
        }
        
        for query in queries:
            try:
                response = requests.post(
                    f"{self.base_url}/api/v1/search/discovery_search",
                    json={"search_query": query, "limit": 2},
                    timeout=30
                )
                
                if response.status_code == 20:
                    data = response.json()
                    self._extract_deadline_data(data, deadline_info, query)
                    
            except Exception as e:
                print(f"Error in deadline query '{query}': {e}")
        
        return deadline_info
    
    def _extract_expert_witness_data(self, data: Dict, results: Dict, query_type: str) -> None:
        """Extract and categorize expert witness information"""
        for entry in data.get('entries', []):
            fields = entry.get('fields', {})
            
            # Extract based on query type
            if 'qualifications' in query_type or 'requirements' in query_type:
                if fields.get('key_findings'):
                    for finding in fields['key_findings'].split('. '):
                        if any(term in finding.lower() for term in ['board', 'certified', 'qualified', 'training']):
                            results['qualification_standards'].append({
                                'requirement': finding.strip(),
                                'source': fields.get('title', 'Unknown'),
                                'document_id': entry.get('id')
                            })
            
            elif 'deadline' in query_type or 'days' in query_type:
                if fields.get('key_takeaways'):
                    for takeaway in fields['key_takeaways'].split('. '):
                        if any(term in takeaway.lower() for term in ['120', 'days', 'deadline', 'report']):
                            results['procedural_deadlines'].append({
                                'deadline': takeaway.strip(),
                                'source': fields.get('title', 'Unknown'),
                                'document_id': entry.get('id')
                            })
    
    def _extract_damages_data(self, data: Dict, results: Dict, query_type: str) -> None:
        """Extract and categorize damages information"""
        for entry in data.get('entries', []):
            fields = entry.get('fields', {})
            
            if 'economic' in query_type:
                if fields.get('key_findings'):
                    for finding in fields['key_findings'].split('. '):
                        if any(term in finding.lower() for term in ['economic', 'actual', 'medical expenses', 'lost wages']):
                            results['economic_damages'].append({
                                'type': finding.strip(),
                                'source': fields.get('title', 'Unknown'),
                                'document_id': entry.get('id')
                            })
            
            elif 'cap' in query_type or 'limitation' in query_type:
                if fields.get('key_findings'):
                    for finding in fields['key_findings'].split('. '):
                        if any(term in finding.lower() for term in ['cap', 'limit', 'maximum', 'non-economic']):
                            results['damage_caps'].append({
                                'limitation': finding.strip(),
                                'source': fields.get('title', 'Unknown'),
                                'document_id': entry.get('id')
                            })
    
    def _extract_deadline_data(self, data: Dict, results: Dict, query_type: str) -> None:
        """Extract and categorize deadline information"""
        for entry in data.get('entries', []):
            fields = entry.get('fields', {})
            
            if 'statute' in query_type:
                if fields.get('key_takeaways'):
                    for takeaway in fields['key_takeaways'].split('. '):
                        if any(term in takeaway.lower() for term in ['year', 'statute', 'limitation', 'file']):
                            results['statute_of_limitations'].append({
                                'timeframe': takeaway.strip(),
                                'source': fields.get('title', 'Unknown'),
                                'document_id': entry.get('id')
                            })

# Usage example
def comprehensive_legal_research_example():
    """
    Example showing specialized endpoints for comprehensive legal research
    """
    legal_search = SpecializedLegalSearch()
    
    print("=== EXPERT WITNESS REQUIREMENTS ===")
    expert_info = legal_search.expert_witness_requirements("texas", "medical_malpractice")
    
    print("Qualification Standards:")
    for qual in expert_info['qualification_standards'][:3]:
        print(f"  • {qual['requirement']}")
        print(f"    Source: {qual['source']}")
    
    print("\nProcedural Deadlines:")
    for deadline in expert_info['procedural_deadlines'][:3]:
        print(f"  • {deadline['deadline']}")
        print(f"    Source: {deadline['source']}")
    
    print("\n=== DAMAGES FRAMEWORK ===")
    damages_info = legal_search.damages_calculation_framework("texas", "medical_malpractice")
    
    print("Economic Damages:")
    for damage in damages_info['economic_damages'][:2]:
        print(f"  • {damage['type']}")
    
    print("Damage Caps:")
    for cap in damages_info['damage_caps'][:2]:
        print(f"  • {cap['limitation']}")

if __name__ == "__main__":
    comprehensive_legal_research_example()