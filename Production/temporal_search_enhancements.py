#!/usr/bin/env python3
"""
Temporal Search Enhancements - Address Date Filtering Limitations
================================================================

Adds date filtering capabilities and tracks recent regulatory changes.
Addresses limitation: "Could not filter for most recent regulatory changes"
"""

from typing import Dict, List, Optional
import requests
import json
from datetime import datetime, timedelta

class TemporalSearchEnhancements:
    """Enhanced search with temporal filtering and change tracking"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
    
    def search_by_date_range(self, search_query: str, 
                           start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None,
                           limit: int = 5) -> Dict:
        """
        Search with date filtering capabilities.
        Addresses limitation: "No Date Filtering"
        """
        # Convert dates to Unix timestamps for the API
        date_filters = {}
        
        if start_date:
            date_filters['min_publication_date'] = int(start_date.timestamp())
        
        if end_date:
            date_filters['max_publication_date'] = int(end_date.timestamp())
        
        # Enhanced query payload with date filtering
        payload = {
            "search_query": search_query,
            "limit": limit,
            **date_filters
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/search/discovery_search",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                # Add temporal analysis to results
                self._add_temporal_analysis(data)
                return data
            
        except Exception as e:
            print(f"Error in temporal search: {e}")
        
        return {'entries': [], 'temporal_analysis': 'unavailable'}
    
    def get_recent_changes(self, topic: str, months_back: int = 12) -> Dict:
        """
        Find recent regulatory changes in a specific topic area.
        """
        # Calculate date range for recent changes
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months_back * 30)
        
        # Search for recent changes
        recent_results = self.search_by_date_range(
            f"{topic} regulation change amendment update",
            start_date=start_date,
            end_date=end_date,
            limit=10
        )
        
        # Analyze for regulatory changes
        changes_analysis = {
            'topic': topic,
            'date_range': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'recent_changes': [],
            'regulatory_updates': [],
            'trend_analysis': {}
        }
        
        for entry in recent_results.get('entries', []):
            fields = entry.get('fields', {})
            pub_date = fields.get('publication_date', 0)
            
            if pub_date > start_date.timestamp():
                change_info = {
                    'title': fields.get('title', 'Unknown'),
                    'publication_date': datetime.fromtimestamp(pub_date).isoformat(),
                    'document_type': fields.get('document_type', 'unknown'),
                    'jurisdiction': fields.get('jurisdiction', 'unknown'),
                    'summary': fields.get('executive_summary', '')[:200] + '...',
                    'key_changes': self._extract_change_indicators(fields)
                }
                changes_analysis['recent_changes'].append(change_info)
        
        # Sort by publication date (most recent first)
        changes_analysis['recent_changes'].sort(
            key=lambda x: x['publication_date'], 
            reverse=True
        )
        
        return changes_analysis
    
    def track_regulatory_timeline(self, topic: str, years_back: int = 5) -> Dict:
        """
        Create a timeline of regulatory changes over time.
        """
        timeline = {
            'topic': topic,
            'timeline_years': years_back,
            'regulatory_timeline': [],
            'trend_summary': {}
        }
        
        # Search by year to create timeline
        current_year = datetime.now().year
        
        for year in range(current_year - years_back, current_year + 1):
            year_start = datetime(year, 1, 1)
            year_end = datetime(year, 12, 31)
            
            year_results = self.search_by_date_range(
                f"{topic} regulation statute amendment",
                start_date=year_start,
                end_date=year_end,
                limit=5
            )
            
            year_info = {
                'year': year,
                'document_count': len(year_results.get('entries', [])),
                'major_changes': [],
                'document_types': {}
            }
            
            for entry in year_results.get('entries', []):
                fields = entry.get('fields', {})
                doc_type = fields.get('document_type', 'unknown')
                
                # Count document types
                year_info['document_types'][doc_type] = year_info['document_types'].get(doc_type, 0) + 1
                
                # Extract major changes
                if self._is_major_change(fields):
                    year_info['major_changes'].append({
                        'title': fields.get('title', 'Unknown'),
                        'type': doc_type,
                        'impact': self._assess_change_impact(fields)
                    })
            
            timeline['regulatory_timeline'].append(year_info)
        
        return timeline
    
    def _add_temporal_analysis(self, data: Dict) -> None:
        """Add temporal analysis to search results"""
        entries = data.get('entries', [])
        if not entries:
            return
        
        # Calculate temporal metrics
        pub_dates = []
        for entry in entries:
            pub_date = entry.get('fields', {}).get('publication_date', 0)
            if pub_date > 0:
                pub_dates.append(pub_date)
        
        if pub_dates:
            pub_dates.sort()
            temporal_analysis = {
                'earliest_document': datetime.fromtimestamp(pub_dates[0]).isoformat(),
                'latest_document': datetime.fromtimestamp(pub_dates[-1]).isoformat(),
                'total_timespan_days': int((pub_dates[-1] - pub_dates[0]) / 86400),
                'documents_by_year': self._group_by_year(pub_dates)
            }
            data['temporal_analysis'] = temporal_analysis
    
    def _group_by_year(self, timestamps: List[int]) -> Dict[str, int]:
        """Group timestamps by year"""
        year_counts = {}
        for timestamp in timestamps:
            year = datetime.fromtimestamp(timestamp).year
            year_counts[str(year)] = year_counts.get(str(year), 0) + 1
        return year_counts
    
    def _extract_change_indicators(self, fields: Dict) -> List[str]:
        """Extract indicators of regulatory changes from document fields"""
        change_indicators = []
        
        # Check key findings for change language
        key_findings = fields.get('key_findings', '')
        change_words = ['amend', 'modify', 'update', 'revise', 'change', 'new requirement', 'effective']
        
        for word in change_words:
            if word in key_findings.lower():
                # Extract sentence containing the change word
                sentences = key_findings.split('. ')
                for sentence in sentences:
                    if word in sentence.lower():
                        change_indicators.append(sentence.strip())
                        break
        
        return change_indicators[:3]  # Limit to top 3 indicators
    
    def _is_major_change(self, fields: Dict) -> bool:
        """Determine if a document represents a major regulatory change"""
        title = fields.get('title', '').lower()
        key_findings = fields.get('key_findings', '').lower()
        
        major_change_indicators = [
            'amendment', 'revision', 'new law', 'effective date',
            'substantially modify', 'major change', 'significant update'
        ]
        
        return any(indicator in title or indicator in key_findings 
                  for indicator in major_change_indicators)
    
    def _assess_change_impact(self, fields: Dict) -> str:
        """Assess the potential impact of a regulatory change"""
        key_takeaways = fields.get('key_takeaways', '').lower()
        
        if any(word in key_takeaways for word in ['billion', 'million', 'significant financial']):
            return 'high_financial_impact'
        elif any(word in key_takeaways for word in ['provider', 'hospital', 'physician']):
            return 'practitioner_impact'
        elif any(word in key_takeaways for word in ['patient', 'consumer', 'public']):
            return 'consumer_impact'
        else:
            return 'general_impact'

# Usage example
def temporal_search_example():
    """
    Example showing temporal search capabilities
    """
    temporal_search = TemporalSearchEnhancements()
    
    print("=== RECENT CHANGES (Last 12 months) ===")
    recent_changes = temporal_search.get_recent_changes("medical malpractice", months_back=12)
    
    print(f"Recent changes for: {recent_changes['topic']}")
    print(f"Date range: {recent_changes['date_range']['start'][:10]} to {recent_changes['date_range']['end'][:10]}")
    
    for change in recent_changes['recent_changes'][:3]:
        print(f"\n• {change['title']}")
        print(f"  Date: {change['publication_date'][:10]}")
        print(f"  Type: {change['document_type']}")
        print(f"  Summary: {change['summary']}")
        
        if change['key_changes']:
            print("  Key Changes:")
            for key_change in change['key_changes'][:2]:
                print(f"    - {key_change}")
    
    print("\n=== REGULATORY TIMELINE (5 years) ===")
    timeline = temporal_search.track_regulatory_timeline("medical malpractice", years_back=5)
    
    for year_data in timeline['regulatory_timeline'][-3:]:  # Show last 3 years
        print(f"\n{year_data['year']}: {year_data['document_count']} documents")
        if year_data['major_changes']:
            print("  Major Changes:")
            for change in year_data['major_changes'][:2]:
                print(f"    • {change['title']} ({change['impact']})")

if __name__ == "__main__":
    temporal_search_example()