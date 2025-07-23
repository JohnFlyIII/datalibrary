#!/usr/bin/env python3
"""
Ingest Enriched Legal Documents to Superlinked
Combines processed metadata (facts, summaries) with original PDFs for comprehensive ingestion
"""
import json
import requests
import time
import argparse
from pathlib import Path
from datetime import datetime
import uuid
from typing import List, Dict, Iterator
import re
import pdfplumber

def chunked_batches(iterable, batch_size: int) -> Iterator[List]:
    """Split an iterable into batches of specified size"""
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

def extract_pdf_text(pdf_path: str) -> str:
    """Extract full text from PDF"""
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return None

def create_enhanced_chunks(text: str, metadata: Dict, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Dict]:
    """
    Create text chunks enhanced with metadata from preprocessing
    """
    chunks = []
    
    # Split by sentence boundaries for better chunk quality
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    current_chunk = ""
    current_start = 0
    current_pos = 0
    
    for sentence in sentences:
        # If adding this sentence would exceed chunk size, finalize current chunk
        if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
            # Find relevant facts for this chunk
            chunk_facts = []
            for fact in metadata.get('extracted_facts', []):
                # Simple check if fact location might be in this chunk
                if any(word in current_chunk for word in fact.get('context', [])):
                    chunk_facts.append(fact)
            
            chunks.append({
                'text': current_chunk.strip(),
                'start_char': current_start,
                'end_char': current_pos,
                'facts': chunk_facts,
                'metadata_id': metadata.get('id')
            })
            
            # Start new chunk with overlap
            overlap_text = current_chunk[-chunk_overlap:] if len(current_chunk) > chunk_overlap else current_chunk
            current_chunk = overlap_text + " " + sentence
            current_start = current_pos - len(overlap_text)
        else:
            # Add sentence to current chunk
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence
                current_start = current_pos
        
        current_pos += len(sentence) + 1
    
    # Add final chunk
    if current_chunk:
        chunk_facts = []
        for fact in metadata.get('extracted_facts', []):
            if any(word in current_chunk for word in fact.get('context', [])):
                chunk_facts.append(fact)
        
        chunks.append({
            'text': current_chunk.strip(),
            'start_char': current_start,
            'end_char': current_pos,
            'facts': chunk_facts,
            'metadata_id': metadata.get('id')
        })
    
    return chunks

def ingest_enriched_document(pdf_path: Path, metadata: Dict, superlinked_url: str) -> bool:
    """
    Ingest a document with all enriched metadata, facts, and summaries
    """
    print(f"\n📄 Processing: {metadata.get('title', pdf_path.stem)}")
    
    # Extract full text
    full_text = extract_pdf_text(pdf_path)
    if not full_text:
        print(f"❌ Failed to extract text from {pdf_path}")
        return False
    
    print(f"   ✓ Extracted {len(full_text)} characters")
    print(f"   ✓ Found {metadata.get('fact_count', 0)} facts")
    print(f"   ✓ Has executive summary: {'Yes' if metadata.get('executive_summary') else 'No'}")
    
    # Create parent document ID
    parent_doc_id = metadata.get('id', str(uuid.uuid4()))
    
    # Base document data with all enriched fields
    base_document_data = {
        # Core fields
        "practice_areas": ["civil_law"],  # TODO: Extract from metadata
        "legal_topics": metadata.get('key_findings', [])[:3],  # Use first 3 key findings as topics
        "jurisdiction": metadata.get('jurisdiction_state', 'texas'),
        "authority_level": "primary",
        "document_type": metadata.get('content_type', 'statute'),
        "publication_date": int(datetime.fromisoformat(metadata.get('processed_date', datetime.now().isoformat())).timestamp()),
        "author": "Texas Legislature",  # TODO: Extract from metadata
        
        # Enriched fields from preprocessing
        "citations": json.dumps([fact['citation'] for fact in metadata.get('extracted_facts', [])]),
        "keywords": json.dumps(metadata.get('key_takeaways', [])),
        "summary": metadata.get('executive_summary', ''),
        "bullet_points": json.dumps(metadata.get('summary_bullet_points', [])),
        "key_findings": json.dumps(metadata.get('key_findings', [])),
        "fact_count": metadata.get('fact_count', 0),
        
        # Scoring
        "authority_score": 0.9,
        "relevance_score": 0.8,
        "citation_count": len(metadata.get('extracted_facts', [])),
        
        # Source info
        "source_url": "",
        "pdf_path": str(pdf_path),
        "word_count": len(full_text.split()),
        
        # Optional fields (empty for now)
        "injury_type": "",
        "injury_severity": "",
        "medical_specialty": "",
        "liability_theory": "",
        "medical_treatment": "",
        "trial_readiness": "",
        "case_number": ""
    }
    
    # Create and ingest chunks
    print("   📦 Creating enhanced chunks...")
    chunks = create_enhanced_chunks(full_text, metadata)
    print(f"   ✓ Created {len(chunks)} chunks")
    
    chunk_successes = 0
    failed_chunks = []
    
    # Process chunks in batches
    for batch_num, batch in enumerate(chunked_batches(enumerate(chunks), 10)):
        print(f"   🔄 Processing batch {batch_num + 1}/{(len(chunks) + 9) // 10}")
        
        for i, chunk in batch:
            # Prepare chunk data with enhanced metadata
            chunk_data = {
                "id": str(uuid.uuid4()),
                "title": f"{metadata.get('title', pdf_path.stem)} - Part {i+1}",
                "content_text": chunk['text'],
                "parent_document_id": parent_doc_id,
                "chunk_index": i,
                "start_char": chunk['start_char'],
                "end_char": chunk['end_char'],
                "is_chunk": "true",
                
                # Include facts relevant to this chunk
                "chunk_facts": json.dumps([{
                    'fact': f['fact'],
                    'citation': f['citation']
                } for f in chunk.get('facts', [])]),
                
                # Include all base document data
                **base_document_data
            }
            
            # Attempt ingestion
            if ingest_single_document(chunk_data, superlinked_url):
                chunk_successes += 1
            else:
                failed_chunks.append(i)
            
            time.sleep(0.05)  # Small delay between chunks
        
        # Pause between batches
        time.sleep(1)
    
    print(f"   ✅ Successfully ingested {chunk_successes}/{len(chunks)} chunks")
    if failed_chunks:
        print(f"   ⚠️  Failed chunks: {failed_chunks[:10]}{'...' if len(failed_chunks) > 10 else ''}")
    
    # Also ingest a master document record with summary only (no full text to avoid timeouts)
    master_doc_data = {
        "id": parent_doc_id,
        "title": metadata.get('title', pdf_path.stem),
        "content_text": metadata.get('executive_summary', '')[:1000],  # Just summary
        "is_master": "true",
        "total_chunks": len(chunks),
        "extracted_facts": json.dumps(metadata.get('extracted_facts', [])),
        **base_document_data
    }
    
    print("   📋 Ingesting master document record...")
    if ingest_single_document(master_doc_data, superlinked_url):
        print("   ✅ Master document ingested")
    else:
        print("   ⚠️  Failed to ingest master document")
    
    return chunk_successes > 0

def ingest_single_document(document_data: Dict, superlinked_url: str) -> bool:
    """Ingest a single document to Superlinked"""
    try:
        url = f"{superlinked_url}/api/v1/ingest/legal_document"
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, json=document_data, headers=headers, timeout=30)
        
        if response.status_code in [200, 202]:
            return True
        else:
            print(f"      ❌ Failed: {response.status_code} - {response.text[:100]}")
            return False
            
    except Exception as e:
        print(f"      ❌ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Ingest enriched legal documents to Superlinked')
    parser.add_argument('--output-dir', required=True, help='Path to output directory with metadata')
    parser.add_argument('--pdf-dir', required=True, help='Path to directory with original PDFs')
    parser.add_argument('--superlinked-url', default='http://localhost:8080', help='Superlinked server URL')
    parser.add_argument('--limit', type=int, help='Limit number of documents to process')
    
    args = parser.parse_args()
    
    output_path = Path(args.output_dir)
    pdf_path = Path(args.pdf_dir)
    
    # Find all metadata files
    metadata_files = list(output_path.glob('metadata/*_metadata.json'))
    
    if args.limit:
        metadata_files = metadata_files[:args.limit]
    
    print(f"🚀 Starting enriched document ingestion")
    print(f"📁 Output directory: {output_path}")
    print(f"📁 PDF directory: {pdf_path}")
    print(f"🌐 Superlinked URL: {args.superlinked_url}")
    print(f"📄 Found {len(metadata_files)} documents to process")
    
    successful = 0
    failed = []
    
    for metadata_file in metadata_files:
        # Load metadata
        with open(metadata_file) as f:
            metadata = json.load(f)
        
        # Find corresponding PDF
        pdf_filename = metadata.get('source_filename')
        if not pdf_filename:
            print(f"⚠️  No source filename in metadata: {metadata_file}")
            continue
        
        pdf_file = pdf_path / pdf_filename
        if not pdf_file.exists():
            print(f"⚠️  PDF not found: {pdf_file}")
            failed.append(str(metadata_file))
            continue
        
        # Ingest document with enriched metadata
        if ingest_enriched_document(pdf_file, metadata, args.superlinked_url):
            successful += 1
        else:
            failed.append(str(pdf_file))
        
        # Small delay between documents
        time.sleep(2)
    
    print(f"\n🏁 Ingestion complete!")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {len(failed)}")
    
    if failed:
        print("\nFailed documents:")
        for f in failed[:10]:
            print(f"  - {f}")
        if len(failed) > 10:
            print(f"  ... and {len(failed) - 10} more")

if __name__ == "__main__":
    main()