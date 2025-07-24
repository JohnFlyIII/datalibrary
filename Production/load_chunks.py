#!/usr/bin/env python3
"""
Load Document Chunks into Superlinked
====================================

Reads chunk JSON files and loads them for precise text-segment search.
Enables finding exact passages within documents.
"""

import json
import requests
from pathlib import Path
from typing import Dict, List
import click
from tqdm import tqdm

class ChunkLoader:
    """Load document chunks into Superlinked"""
    
    def __init__(self, superlinked_url: str = "http://localhost:8080"):
        self.base_url = superlinked_url
        self.chunks_dir = Path("output/chunks")
        self.metadata_dir = Path("output/metadata")
        
    def get_document_metadata(self, doc_id: str) -> Dict:
        """Get metadata for parent document"""
        metadata_file = self.metadata_dir / f"{doc_id}_metadata.json"
        if not metadata_file.exists():
            return {}
            
        with open(metadata_file, 'r') as f:
            return json.load(f)
    
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
    
    def load_chunks_from_file(self, chunks_file: Path) -> List[Dict]:
        """Load all chunks from a chunks file"""
        with open(chunks_file, 'r') as f:
            chunk_data = json.load(f)
            
        doc_id = chunk_data['doc_id']
        
        # Get parent document metadata
        parent_metadata = self.get_document_metadata(doc_id)
        document_type = self.map_content_type(parent_metadata.get('content_type', 'unknown'))
        jurisdiction = self.map_jurisdiction(parent_metadata.get('jurisdiction_state'))
        
        # Convert chunks to our schema
        chunk_documents = []
        for chunk in chunk_data['chunks']:
            chunk_doc = {
                'id': f"{doc_id}_chunk_{chunk['chunk_index']}",
                'parent_document_id': doc_id,
                'chunk_index': chunk['chunk_index'],
                'text': chunk['text'],
                'start_char': chunk['start_char'],
                'end_char': chunk['end_char'],
                'document_type': document_type,
                'jurisdiction': jurisdiction
            }
            chunk_documents.append(chunk_doc)
            
        return chunk_documents
        
    def ingest_chunks(self, chunks: List[Dict]) -> bool:
        """Ingest chunks to Superlinked"""
        url = f"{self.base_url}/api/v1/ingest/document_chunk"
        
        try:
            response = requests.post(url, json=chunks, timeout=60)
            return response.status_code == 202
        except Exception as e:
            print(f"Error ingesting chunks: {e}")
            return False
    
    def load_batch(self, limit: int = None) -> Dict:
        """Load a batch of chunk files"""
        chunk_files = list(self.chunks_dir.glob("*_chunks.json"))
        
        if limit:
            chunk_files = chunk_files[:limit]
            
        results = {
            'success': [],
            'failed': [],
            'stats': {
                'total_files': len(chunk_files),
                'total_chunks': 0,
                'by_type': {},
                'by_jurisdiction': {}
            }
        }
        
        print(f"Loading chunks from {len(chunk_files)} files...")
        
        for chunk_file in tqdm(chunk_files):
            try:
                chunks = self.load_chunks_from_file(chunk_file)
                
                if not chunks:
                    results['failed'].append(str(chunk_file))
                    continue
                    
                # Track stats
                results['stats']['total_chunks'] += len(chunks)
                doc_type = chunks[0]['document_type']
                jurisdiction = chunks[0]['jurisdiction']
                
                results['stats']['by_type'][doc_type] = results['stats']['by_type'].get(doc_type, 0) + len(chunks)
                results['stats']['by_jurisdiction'][jurisdiction] = results['stats']['by_jurisdiction'].get(jurisdiction, 0) + len(chunks)
                
                # Ingest chunks (batch by document)
                if self.ingest_chunks(chunks):
                    results['success'].append({
                        'file': chunk_file.name,
                        'doc_id': chunks[0]['parent_document_id'],
                        'chunks': len(chunks),
                        'type': doc_type,
                        'jurisdiction': jurisdiction
                    })
                else:
                    results['failed'].append(str(chunk_file))
                    
            except Exception as e:
                print(f"Error processing {chunk_file}: {e}")
                results['failed'].append(str(chunk_file))
                
        return results

@click.command()
@click.option('--limit', '-l', type=int, help='Limit number of chunk files to load')
@click.option('--url', '-u', default='http://localhost:8080', help='Superlinked server URL')
def main(limit, url):
    """Load document chunks into Superlinked"""
    
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
    
    # Load chunks
    loader = ChunkLoader(url)
    results = loader.load_batch(limit)
    
    # Print results
    print(f"\n📊 Chunk Loading Results:")
    print(f"✅ Successfully loaded: {len(results['success'])} files")
    print(f"❌ Failed to load: {len(results['failed'])} files")
    print(f"📄 Total chunks loaded: {results['stats']['total_chunks']}")
    
    if results['stats']['by_type']:
        print(f"\n📋 Chunks by Document Type:")
        for doc_type, count in results['stats']['by_type'].items():
            print(f"  {doc_type}: {count} chunks")
            
    if results['stats']['by_jurisdiction']:
        print(f"\n🗺️ Chunks by Jurisdiction:")
        for jurisdiction, count in results['stats']['by_jurisdiction'].items():
            print(f"  {jurisdiction or 'unknown'}: {count} chunks")
            
    # Show sample loaded files
    print(f"\n📑 Sample Loaded Files:")
    for doc in results['success'][:3]:
        print(f"  • {doc['file']}: {doc['chunks']} chunks ({doc['type']}, {doc['jurisdiction']})")
        
    if results['failed']:
        print(f"\n❌ Failed Files: {results['failed'][:3]}")

if __name__ == "__main__":
    main()