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
            
        # Map to our schema
        document = {
            'id': metadata['id'],
            'title': metadata['title'],
            'content': self.build_rich_content(metadata),
            'document_type': self.map_content_type(metadata.get('content_type', 'unknown')),
            'jurisdiction': self.map_jurisdiction(metadata.get('jurisdiction_state'))
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