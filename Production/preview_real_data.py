#!/usr/bin/env python3
"""
Preview Real Legal Document Data
===============================

Shows what the processed data looks like when mapped to our schema.
"""

import json
from pathlib import Path
import sys
sys.path.append('.')
from load_real_data import SuperlinkedDataLoader

def preview_documents(limit=3):
    """Preview how documents will look when loaded"""
    
    loader = SuperlinkedDataLoader()
    metadata_files = list(loader.metadata_dir.glob("*_metadata.json"))[:limit]
    
    print("🔍 Preview of Real Legal Documents")
    print("=" * 50)
    
    for i, metadata_file in enumerate(metadata_files, 1):
        print(f"\n📄 Document {i}: {metadata_file.name}")
        print("-" * 40)
        
        try:
            document, original_metadata = loader.load_document(metadata_file)
            
            print(f"ID: {document['id']}")
            print(f"Title: {document['title']}")
            print(f"Type: {document['document_type']}")
            print(f"Jurisdiction: {document['jurisdiction']}")
            print(f"Content Length: {len(document['content'])} chars")
            
            # Show content preview
            print(f"\nContent Preview:")
            content_preview = document['content'][:500] + "..." if len(document['content']) > 500 else document['content']
            print(content_preview)
            
            # Show original metadata stats
            print(f"\nOriginal Metadata:")
            print(f"  Source: {original_metadata.get('source_filename')}")
            print(f"  Facts: {original_metadata.get('fact_count', 0)}")
            print(f"  Pages: {original_metadata.get('total_pages', 0)}")
            print(f"  Processing Date: {original_metadata.get('processed_date', 'Unknown')}")
            
        except Exception as e:
            print(f"❌ Error processing {metadata_file}: {e}")
            
    print(f"\n📊 Found {len(list(loader.metadata_dir.glob('*_metadata.json')))} total documents available")

if __name__ == "__main__":
    preview_documents()