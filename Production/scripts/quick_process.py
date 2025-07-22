#!/usr/bin/env python3
"""
Quick Local Processing Script

A simplified version for quick document processing without all dependencies.
Works with basic Python libraries.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
import subprocess
import sys

def extract_text_simple(pdf_path):
    """Extract text using pdftotext (must be installed)"""
    try:
        result = subprocess.run(
            ['pdftotext', str(pdf_path), '-'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"Failed to extract text from {pdf_path}")
            return ""
    except FileNotFoundError:
        print("pdftotext not found. Install with: brew install poppler (Mac) or apt-get install poppler-utils (Linux)")
        sys.exit(1)

def create_basic_metadata(pdf_path, text):
    """Create basic metadata without AI processing"""
    doc_id = hashlib.md5(pdf_path.name.encode()).hexdigest()[:12]
    
    # Basic jurisdiction detection
    text_lower = text.lower()
    jurisdiction_state = None
    
    state_keywords = {
        'texas': ['texas', 'tex.', 'tx'],
        'california': ['california', 'cal.', 'ca'],
        'new_york': ['new york', 'n.y.', 'ny'],
        'florida': ['florida', 'fla.', 'fl'],
    }
    
    for state, keywords in state_keywords.items():
        if any(kw in text_lower[:5000] for kw in keywords):
            jurisdiction_state = state
            break
    
    # Basic content type detection
    content_type = 'unknown'
    if 'statute' in text_lower[:1000] or 'code' in text_lower[:1000]:
        content_type = 'statute'
    elif 'opinion' in text_lower[:1000] or 'court' in text_lower[:1000]:
        content_type = 'case_law'
    elif 'regulation' in text_lower[:1000] or 'rule' in text_lower[:1000]:
        content_type = 'regulation'
    
    # Extract title (first non-empty line)
    lines = text.split('\n')
    title = pdf_path.stem.replace('_', ' ').title()
    for line in lines[:20]:
        if line.strip() and len(line.strip()) > 10:
            title = line.strip()
            break
    
    return {
        'id': doc_id,
        'title': title,
        'source_filename': pdf_path.name,
        'file_size_bytes': pdf_path.stat().st_size,
        'content_type': content_type,
        'jurisdiction_country': 'united_states',
        'jurisdiction_state': jurisdiction_state,
        'processed_date': datetime.now().isoformat(),
        'preprocessing_version': 'quick_1.0',
        'requires_ai_processing': True,
        'human_reviewed': False,
        'text_length': len(text),
        'estimated_pages': text.count('\f') + 1,  # Form feed characters
        
        # Placeholder fields for AI processing
        'extracted_facts': [],
        'fact_count': 0,
        'executive_summary': 'Pending AI processing',
        'summary_bullet_points': [],
        'practice_areas': [],
        'key_provisions': [],
        'compliance_requirements': [],
        'deadlines_timeframes': []
    }

def create_chunks(text, chunk_size=2000, overlap=200):
    """Create text chunks for processing"""
    chunks = []
    start = 0
    chunk_index = 0
    
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = {
            'chunk_index': chunk_index,
            'start_char': start,
            'end_char': end,
            'text': text[start:end]
        }
        chunks.append(chunk)
        
        start = end - overlap if end < len(text) else end
        chunk_index += 1
    
    return chunks

def process_directory(input_dir, output_dir):
    """Process all PDFs in a directory"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Create output directories
    metadata_dir = output_path / 'metadata' / 'unreviewed'
    chunks_dir = output_path / 'chunks'
    logs_dir = output_path / 'logs'
    
    for dir in [metadata_dir, chunks_dir, logs_dir]:
        dir.mkdir(parents=True, exist_ok=True)
    
    # Process log
    log_file = logs_dir / f"quick_process_{datetime.now():%Y%m%d_%H%M%S}.json"
    processing_log = []
    
    # Find all PDFs
    pdf_files = list(input_path.glob('*.pdf'))
    print(f"Found {len(pdf_files)} PDF files")
    
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}] Processing: {pdf_path.name}")
        
        try:
            # Extract text
            text = extract_text_simple(pdf_path)
            if not text:
                print("  ⚠️  No text extracted")
                continue
            
            # Create metadata
            metadata = create_basic_metadata(pdf_path, text)
            print(f"  ✓ Created metadata - ID: {metadata['id']}")
            print(f"  ✓ Detected: {metadata['content_type']} - {metadata['jurisdiction_state'] or 'Unknown state'}")
            
            # Create chunks
            chunks = create_chunks(text)
            print(f"  ✓ Created {len(chunks)} chunks")
            
            # Save metadata
            metadata_file = metadata_dir / f"{metadata['id']}_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Save chunks
            chunks_file = chunks_dir / f"{metadata['id']}_chunks.json"
            chunks_data = {
                'doc_id': metadata['id'],
                'total_chunks': len(chunks),
                'chunks': chunks
            }
            with open(chunks_file, 'w') as f:
                json.dump(chunks_data, f, indent=2)
            
            # Log success
            processing_log.append({
                'timestamp': datetime.now().isoformat(),
                'filename': pdf_path.name,
                'doc_id': metadata['id'],
                'status': 'success',
                'chunks': len(chunks),
                'text_length': len(text)
            })
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            processing_log.append({
                'timestamp': datetime.now().isoformat(),
                'filename': pdf_path.name,
                'status': 'failed',
                'error': str(e)
            })
    
    # Save processing log
    with open(log_file, 'w') as f:
        json.dump(processing_log, f, indent=2)
    
    # Summary
    successful = sum(1 for entry in processing_log if entry.get('status') == 'success')
    failed = sum(1 for entry in processing_log if entry.get('status') == 'failed')
    
    print("\n" + "="*60)
    print("Processing Complete!")
    print(f"✓ Successful: {successful}")
    print(f"✗ Failed: {failed}")
    print(f"Output directory: {output_path}")
    print("\nNext steps:")
    print("1. Review metadata files in:", metadata_dir)
    print("2. Run AI processing for fact extraction and summaries")
    print("3. Have human expert review and enrich metadata")
    print("4. Generate embeddings and prepare for production import")

def main():
    """Main entry point"""
    if len(sys.argv) != 3:
        print("Usage: python quick_process.py <input_dir> <output_dir>")
        print("Example: python quick_process.py ./pdfs ./processed")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not Path(input_dir).exists():
        print(f"Error: Input directory '{input_dir}' does not exist")
        sys.exit(1)
    
    process_directory(input_dir, output_dir)

if __name__ == "__main__":
    main()