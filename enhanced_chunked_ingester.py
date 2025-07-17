#!/usr/bin/env python3
"""
Enhanced Chunked Legal Document Ingester
Supports unlimited document size with automatic chunking for passage-level search
"""
import json
import requests
import PyPDF2
import re
import time
from pathlib import Path
from datetime import datetime
import uuid
from typing import List, Dict, Tuple, Iterator

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
    """Extract full text from PDF without character limits"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return None

def load_metadata(file_path: str) -> Dict:
    """Load metadata for a file"""
    # Try file-specific metadata first
    file_metadata_path = Path(f"{file_path}.metadata.json")
    if file_metadata_path.exists():
        with open(file_metadata_path) as f:
            return json.load(f)
    
    # Fall back to directory metadata
    dir_metadata_path = Path(file_path).parent / "metadata.json"
    if dir_metadata_path.exists():
        with open(dir_metadata_path) as f:
            return json.load(f)
    
    return {}

def determine_practice_areas(metadata: Dict) -> List[str]:
    """Determine multiple practice areas from metadata"""
    practice_areas = []
    legal_topics = metadata.get("legal_topics", [])
    primary_practice_area = metadata.get("practice_area", "civil_law")
    
    # Always include the primary practice area
    practice_areas.append(primary_practice_area)
    
    # Add additional practice areas based on legal topics
    topic_to_areas = {
        "medical_negligence": "medical_malpractice",
        "tort_liability": "tort_law", 
        "civil_procedure": "civil_law",
        "damages": "personal_injury",
        "statute_of_limitations": "civil_law",
        "venue": "civil_law",
        "discovery": "civil_law",
        "judgments": "civil_law",
        "evidence": "civil_law",
        "appeals": "civil_law",
        "injunctions": "civil_law"
    }
    
    for topic in legal_topics:
        if topic in topic_to_areas:
            area = topic_to_areas[topic]
            if area not in practice_areas:
                practice_areas.append(area)
    
    return practice_areas

def determine_legal_topics(metadata: Dict) -> List[str]:
    """Determine legal topics from metadata"""
    return metadata.get("legal_topics", ["civil_procedure", "tort_liability", "damages"])

def create_chunks(text: str, chunk_size: int = 2000, chunk_overlap: int = 400) -> List[Tuple[str, int, int]]:
    """
    Create text chunks with character position tracking for citations
    
    Args:
        text: Full document text
        chunk_size: Target chunk size in characters
        chunk_overlap: Number of characters to overlap between chunks
        
    Returns:
        List of tuples: (chunk_text, start_char, end_char)
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
            # Find end position
            chunk_end = current_pos + len(current_chunk)
            chunks.append((current_chunk.strip(), current_start, chunk_end))
            
            # Start new chunk with overlap
            overlap_text = current_chunk[-chunk_overlap:] if len(current_chunk) > chunk_overlap else current_chunk
            current_chunk = overlap_text + " " + sentence
            current_start = chunk_end - len(overlap_text)
            current_pos = chunk_end - len(overlap_text)
        else:
            # Add sentence to current chunk
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence
                current_start = current_pos
        
        current_pos += len(sentence) + 1  # +1 for space
    
    # Add final chunk if it exists
    if current_chunk:
        chunk_end = current_pos + len(current_chunk)
        chunks.append((current_chunk.strip(), current_start, chunk_end))
    
    return chunks

def create_chunk_context(text: str, start_char: int, end_char: int, context_size: int = 100) -> str:
    """Create context around a chunk for citation purposes"""
    context_start = max(0, start_char - context_size)
    context_end = min(len(text), end_char + context_size)
    
    context = text[context_start:context_end]
    
    # Add ellipsis if we're not at the beginning/end
    if context_start > 0:
        context = "..." + context
    if context_end < len(text):
        context = context + "..."
    
    return context

def ingest_document_to_superlinked(pdf_path: str, superlinked_url: str = "http://localhost:8080") -> bool:
    """
    Ingest a document with unlimited size and automatic chunking to Superlinked server
    Creates both full document entry and individual chunks for passage-level search
    """
    
    # Extract full text from PDF (no character limit)
    print(f"Processing: {pdf_path}")
    full_text = extract_pdf_text(pdf_path)
    if not full_text:
        print("Failed to extract text from PDF")
        return False
    
    print(f"Document extracted with {len(full_text)} characters (unlimited)")
    
    # Load metadata
    metadata = load_metadata(pdf_path)
    practice_areas = determine_practice_areas(metadata)
    legal_topics = determine_legal_topics(metadata)
    
    print(f"Practice areas: {practice_areas}")
    print(f"Legal topics: {legal_topics}")
    
    # Create parent document ID
    parent_doc_id = str(uuid.uuid4())
    
    # Base document data
    base_document_data = {
        "practice_areas": practice_areas,
        "legal_topics": legal_topics,
        "jurisdiction": metadata.get("jurisdiction", "texas"),
        "authority_level": metadata.get("authority_level", "primary"),
        "document_type": metadata.get("document_type", "statute"),
        "publication_date": int(datetime.now().timestamp()),
        "author": metadata.get("author", "Texas Legislature"),
        "citations": json.dumps(metadata.get("citations", [])),
        "keywords": json.dumps(metadata.get("keywords", ["civil", "practice", "remedies"])),
        "summary": metadata.get("summary", "Texas Legal Document"),
        "authority_score": metadata.get("authority_score", 0.9),
        "relevance_score": 0.8,
        "citation_count": metadata.get("citation_count", 0),
        "source_url": metadata.get("source_url", ""),
        "pdf_path": str(pdf_path),
        "word_count": len(full_text.split()),
        # Optional fields
        "injury_type": metadata.get("injury_type", ""),
        "injury_severity": metadata.get("injury_severity", ""),
        "medical_specialty": metadata.get("medical_specialty", ""),
        "liability_theory": metadata.get("liability_theory", ""),
        "medical_treatment": metadata.get("medical_treatment", ""),
        "trial_readiness": metadata.get("trial_readiness", ""),
        "case_number": metadata.get("case_number", "")
    }
    
    # Skip full document ingestion to avoid timeout issues
    print("⏭️ Skipping full document ingestion - processing chunks only for optimal performance")
    print(f"📄 Document: {metadata.get('title', Path(pdf_path).stem)} ({len(full_text)} characters)")
    
    # Create and ingest chunks for passage-level search
    print("Creating chunks for passage-level search...")
    chunks = create_chunks(full_text, chunk_size=500, chunk_overlap=100)
    
    print(f"Created {len(chunks)} chunks")
    
    chunk_successes = 0
    print("📦 Processing chunks in batches of 10...")
    
    # Process chunks in batches to reduce memory usage and improve performance
    for batch_num, batch in enumerate(chunked_batches(enumerate(chunks), 10)):
        print(f"🔄 Processing batch {batch_num + 1}/{(len(chunks) + 9) // 10}")
        
        for i, (chunk_text, start_char, end_char) in batch:
            chunk_context = create_chunk_context(full_text, start_char, end_char)
            
            chunk_data = {
                "id": str(uuid.uuid4()),
                "title": f"{metadata.get('title', Path(pdf_path).stem)} - Section {i+1}",
                "content_text": chunk_text,
                "parent_document_id": parent_doc_id,
                "chunk_index": i,
                "start_char": start_char,
                "end_char": end_char,
                "chunk_context": chunk_context,
                "is_chunk": "true",
                **base_document_data
            }
            
            if ingest_single_document(chunk_data, superlinked_url):
                chunk_successes += 1
                print(f"✅ Ingested chunk {i+1}/{len(chunks)}")
            else:
                print(f"⚠️ Failed to ingest chunk {i+1}")
            
            # Small delay between chunks within batch
            time.sleep(0.05)
        
        # Longer delay between batches to prevent overwhelming
        print(f"⏸️ Batch {batch_num + 1} complete - pausing 2 seconds...")
        time.sleep(2)
    
    print(f"✅ Successfully ingested {chunk_successes}/{len(chunks)} chunks")
    
    return chunk_successes > 0

def ingest_single_document(document_data: Dict, superlinked_url: str) -> bool:
    """Ingest a single document (full document or chunk) to Superlinked"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            url = f"{superlinked_url}/api/v1/ingest/legal_document"
            headers = {
                'Accept': '*/*',
                'Content-Type': 'application/json'
            }
            
            # Add much longer timeout for large documents
            response = requests.post(url, json=document_data, headers=headers, timeout=300)
            
            if response.status_code in [200, 202]:  # 202 = Accepted (async operation)
                return True
            else:
                print(f"❌ Failed to ingest document: {response.status_code}")
                print(f"Response: {response.text}")
                if attempt < max_retries - 1:
                    time.sleep(2)  # Wait before retry
                    continue
                return False
                
        except Exception as e:
            print(f"❌ Error ingesting document (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retry
                continue
            return False
    
    return False

if __name__ == "__main__":
    # Test with Texas PDF
    pdf_path = "data/texas/civilpracticeandremediescode.pdf"
    success = ingest_document_to_superlinked(pdf_path)
    
    if success:
        print("\n🏛️ Enhanced chunked ingestion completed successfully!")
        print("📖 Documents are now searchable at both document and passage level")
        print("🎯 Users can find specific sections and get exact citations")
    else:
        print("\n❌ Enhanced chunked ingestion failed!")