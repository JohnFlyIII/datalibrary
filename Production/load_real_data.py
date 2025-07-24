#!/usr/bin/env python3
"""
Load Real Legal Documents into Superlinked
==========================================

Reads the processed JSON metadata files and ingests them into our Superlinked system.
Uses the rich AI-processed content including summaries, facts, and classifications.
"""

import json
import requests
from pathlib import Path
from typing import Dict, List
import click
from tqdm import tqdm

class SuperlinkedDataLoader:
    """Load processed legal documents into Superlinked"""
    
    def __init__(self, superlinked_url: str = "http://localhost:8080"):
        self.base_url = superlinked_url
        self.metadata_dir = Path("output/metadata")
        self.chunks_dir = Path("output/chunks")
        
    def map_content_type(self, content_type: str) -> str:
        """Map processing code content types to our schema"""
        mapping = {
            'statute': 'statute',
            'case_law': 'case', 
            'regulation': 'regulation',
            'contract': 'other',
            'unknown': 'other'
        }
        return mapping.get(content_type, 'other')
        
    def map_jurisdiction(self, jurisdiction_state: str) -> str:
        """Map jurisdiction state to our categories"""
        if not jurisdiction_state:
            return 'federal'  # Default assumption
        return jurisdiction_state
    
    def extract_city_from_title(self, title: str) -> str:
        """Extract city name from document title"""
        title_lower = title.lower()
        cities = ['houston', 'dallas', 'austin', 'san_antonio', 'los_angeles', 'san_francisco', 'chicago', 'new_york']
        for city in cities:
            if city.replace('_', ' ') in title_lower or city in title_lower:
                return city
        return ''
    
    def infer_primary_practice_area(self, metadata: Dict) -> str:
        """Infer primary practice area from content"""
        title = metadata.get('title', '').lower()
        content_type = metadata.get('content_type', '').lower()
        
        if any(term in title for term in ['malpractice', 'injury', 'assault', 'tort', 'liability']):
            return 'litigation'
        elif any(term in title for term in ['hospital', 'medical', 'healthcare']):
            return 'healthcare'
        elif content_type in ['statute', 'regulation']:
            return 'regulatory'
        else:
            return 'litigation'  # default
    
    def infer_secondary_practice_area(self, metadata: Dict) -> str:
        """Infer secondary practice area from content"""
        title = metadata.get('title', '').lower()
        
        if 'medical' in title and 'malpractice' in title:
            return 'medical_malpractice'
        elif any(term in title for term in ['assault', 'abuse', 'survivor']):
            return 'personal_injury'
        elif 'hospital' in title:
            return 'healthcare_compliance'
        elif 'privacy' in title:
            return 'data_privacy'
        else:
            return 'general_litigation'
    
    def extract_legal_topics(self, metadata: Dict) -> str:
        """Extract legal topics from metadata"""
        topics = []
        title = metadata.get('title', '').lower()
        
        # Extract key legal concepts
        if 'malpractice' in title:
            topics.append('medical malpractice')
        if 'liability' in title:
            topics.append('tort liability')
        if 'hospital' in title:
            topics.append('hospital law')
        if 'privacy' in title:
            topics.append('medical privacy')
        if 'assault' in title:
            topics.append('sexual assault')
        if 'statistics' in title:
            topics.append('legal statistics')
            
        return ', '.join(topics) if topics else 'general legal'
    
    def extract_keywords(self, metadata: Dict) -> str:
        """Extract search keywords from metadata"""
        keywords = []
        title = metadata.get('title', '').lower()
        
        # Add key terms for search
        key_terms = ['texas', 'medical', 'malpractice', 'hospital', 'liability', 'assault', 'privacy', 'statistics', 'houston']
        for term in key_terms:
            if term in title:
                keywords.append(term)
                
        return ', '.join(keywords) if keywords else 'legal document'
    
    def extract_publication_date(self, metadata: Dict) -> int:
        """Extract publication date as Unix timestamp"""
        from datetime import datetime
        
        # Try to get processed_date from metadata
        if metadata.get('processed_date'):
            try:
                # Parse ISO format date
                dt = datetime.fromisoformat(metadata['processed_date'].replace('Z', '+00:00'))
                return int(dt.timestamp())
            except:
                pass
        
        # Try to infer from filename or content
        title = metadata.get('title', '').lower()
        
        # Look for year in title
        import re
        year_match = re.search(r'20(\d{2})', title)
        if year_match:
            try:
                year = int('20' + year_match.group(1))
                # Create date for January 1st of that year
                dt = datetime(year, 1, 1)
                return int(dt.timestamp())
            except:
                pass
        
        # Default to current processing time
        return int(datetime.now().timestamp())
    
    def calculate_confidence_score(self, metadata: Dict) -> int:
        """Calculate overall confidence score (0-100) based on data quality"""
        score = 0
        
        # Base score for having metadata
        score += 20
        
        # Add points for AI-processed content
        if metadata.get('executive_summary'):
            score += 15
        if metadata.get('key_findings'):
            score += 15
        if metadata.get('extracted_facts'):
            score += 20
            
        # Add points for data richness
        if metadata.get('fact_count', 0) > 5:
            score += 10
        if metadata.get('total_pages', 0) > 2:
            score += 10
            
        # Add points for clear content type classification
        if metadata.get('content_type') in ['statute', 'case_law', 'regulation']:
            score += 10
            
        # Ensure score is within 0-100 range
        return min(100, max(0, score))
        
    def build_rich_content(self, metadata: Dict) -> str:
        """Build rich content from AI-processed fields"""
        content_parts = []
        
        # Executive summary (main content)
        if metadata.get('executive_summary'):
            content_parts.append(f"SUMMARY: {metadata['executive_summary']}")
            
        # Key findings
        if metadata.get('key_findings'):
            findings_text = ". ".join(metadata['key_findings'])
            content_parts.append(f"KEY FINDINGS: {findings_text}")
            
        # Key takeaways (plain language)
        if metadata.get('key_takeaways'):
            takeaways_text = ". ".join(metadata['key_takeaways'])
            content_parts.append(f"KEY TAKEAWAYS: {takeaways_text}")
            
        # Extracted facts (first 3 most confident)
        if metadata.get('extracted_facts'):
            facts = sorted(metadata['extracted_facts'], 
                         key=lambda x: x.get('confidence', 0), reverse=True)[:3]
            fact_texts = [f"{fact['fact']} ({fact.get('location', 'Unknown location')})" 
                         for fact in facts]
            if fact_texts:
                content_parts.append(f"KEY FACTS: {'. '.join(fact_texts)}")
        
        return "\n\n".join(content_parts)
        
    def load_document(self, metadata_file: Path) -> Dict:
        """Load a single document from metadata file"""
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
            
        # Map to our schema (PHASE 1: Expanded with new fields)
        document = {
            # Core fields
            'id': metadata['id'],
            'title': metadata['title'],
            'content': self.build_rich_content(metadata),
            'document_type': self.map_content_type(metadata.get('content_type', 'unknown')),
            'jurisdiction': self.map_jurisdiction(metadata.get('jurisdiction_state')),
            
            # PHASE 1: AI Preprocessing Fields
            'extracted_facts': json.dumps(metadata.get('extracted_facts', [])),
            'executive_summary': metadata.get('executive_summary', ''),
            'key_findings': '. '.join(metadata.get('key_findings', [])),
            'key_takeaways': '. '.join(metadata.get('key_takeaways', [])),
            
            # PHASE 1: Hierarchical Fields
            'jurisdiction_state': metadata.get('jurisdiction_state', ''),
            'jurisdiction_city': self.extract_city_from_title(metadata.get('title', '')),
            'practice_area_primary': self.infer_primary_practice_area(metadata),
            'practice_area_secondary': self.infer_secondary_practice_area(metadata),
            
            # PHASE 1: Content Enhancement
            'legal_topics': self.extract_legal_topics(metadata),
            'keywords': self.extract_keywords(metadata),
            
            # PHASE 2: Testing new datatypes
            'publication_date': self.extract_publication_date(metadata),
            'confidence_score': self.calculate_confidence_score(metadata),
            
            # PHASE 1A: Document Metadata Fields (ready-to-use)
            'source_filename': metadata.get('source_filename', ''),
            'file_size_bytes': metadata.get('file_size_bytes', 0),
            'total_pages': metadata.get('total_pages', 0),
            'total_chars': metadata.get('total_chars', 0),
            'fact_count': metadata.get('fact_count', 0),
            
            # PHASE 1A: Enhanced Content Fields (ready-to-use)
            'summary_bullet_points': '\n'.join(metadata.get('summary_bullet_points', [])),
            'summary_conclusion': metadata.get('summary_conclusion', ''),
            
            # PHASE 1A: Processing Metadata Fields (ready-to-use)
            'ai_model': metadata.get('ai_model', ''),
            'preprocessing_version': metadata.get('preprocessing_version', ''),
        }
        
        return document, metadata
        
    def ingest_document(self, document: Dict) -> bool:
        """Ingest document to Superlinked"""
        url = f"{self.base_url}/api/v1/ingest/legal_document"
        
        try:
            response = requests.post(url, json=[document], timeout=30)
            return response.status_code == 202
        except Exception as e:
            print(f"Error ingesting {document['id']}: {e}")
            return False
            
    def load_batch(self, limit: int = None) -> Dict:
        """Load a batch of documents"""
        metadata_files = list(self.metadata_dir.glob("*_metadata.json"))
        
        if limit:
            metadata_files = metadata_files[:limit]
            
        results = {
            'success': [],
            'failed': [],
            'stats': {
                'total': len(metadata_files),
                'by_type': {},
                'by_jurisdiction': {}
            }
        }
        
        print(f"Loading {len(metadata_files)} documents...")
        
        for metadata_file in tqdm(metadata_files):
            try:
                document, original_metadata = self.load_document(metadata_file)
                
                # Track stats
                doc_type = document['document_type']
                jurisdiction = document['jurisdiction']
                
                results['stats']['by_type'][doc_type] = results['stats']['by_type'].get(doc_type, 0) + 1
                results['stats']['by_jurisdiction'][jurisdiction] = results['stats']['by_jurisdiction'].get(jurisdiction, 0) + 1
                
                # Ingest document
                if self.ingest_document(document):
                    results['success'].append({
                        'id': document['id'],
                        'title': document['title'],
                        'type': document['document_type'],
                        'jurisdiction': document['jurisdiction']
                    })
                else:
                    results['failed'].append(document['id'])
                    
            except Exception as e:
                print(f"Error processing {metadata_file}: {e}")
                results['failed'].append(str(metadata_file))
                
        return results

@click.command()
@click.option('--limit', '-l', type=int, help='Limit number of documents to load')
@click.option('--url', '-u', default='http://localhost:8080', help='Superlinked server URL')
def main(limit, url):
    """Load real legal documents into Superlinked"""
    
    # Check if server is running
    try:
        response = requests.get(f"{url}/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ Superlinked server not healthy at {url}")
            return
    except:
        print(f"❌ Cannot connect to Superlinked server at {url}")
        return
        
    print(f"✅ Connected to Superlinked server at {url}")
    
    # Load documents
    loader = SuperlinkedDataLoader(url)
    results = loader.load_batch(limit)
    
    # Print results
    print(f"\n📊 Loading Results:")
    print(f"✅ Successfully loaded: {len(results['success'])} documents")
    print(f"❌ Failed to load: {len(results['failed'])} documents")
    
    if results['stats']['by_type']:
        print(f"\n📋 By Document Type:")
        for doc_type, count in results['stats']['by_type'].items():
            print(f"  {doc_type}: {count}")
            
    if results['stats']['by_jurisdiction']:
        print(f"\n🗺️ By Jurisdiction:")
        for jurisdiction, count in results['stats']['by_jurisdiction'].items():
            print(f"  {jurisdiction or 'unknown'}: {count}")
            
    # Show sample loaded documents
    print(f"\n📑 Sample Loaded Documents:")
    for doc in results['success'][:5]:
        print(f"  • {doc['title'][:50]}... ({doc['type']}, {doc['jurisdiction']})")
        
    if results['failed']:
        print(f"\n❌ Failed Documents: {results['failed'][:5]}")

if __name__ == "__main__":
    main()