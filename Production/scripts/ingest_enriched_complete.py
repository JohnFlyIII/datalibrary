#!/usr/bin/env python3
"""
Complete Enriched Legal Document Ingester for Superlinked
Maps all preprocessed metadata to the comprehensive schema fields
"""
import json
import requests
import time
import argparse
from pathlib import Path
from datetime import datetime
import uuid
from typing import List, Dict, Iterator, Optional
import re
import pdfplumber
from collections import defaultdict

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

def determine_practice_areas(metadata: Dict) -> Dict[str, str]:
    """
    Determine hierarchical practice areas from content
    Returns: primary, secondary, specific areas
    """
    title = metadata.get('title', '').lower()
    content_type = metadata.get('content_type', '').lower()
    
    # Keywords to practice area mapping
    if 'medical' in title or 'hospital' in title or 'health' in title:
        if 'malpractice' in title:
            return {
                'primary': 'litigation',
                'secondary': 'personal_injury', 
                'specific': 'medical_malpractice'
            }
        else:
            return {
                'primary': 'healthcare',
                'secondary': 'medical_regulation',
                'specific': 'healthcare_compliance'
            }
    elif 'sexual assault' in title or 'sex offender' in title:
        return {
            'primary': 'criminal',
            'secondary': 'violent_crimes',
            'specific': 'sexual_assault'
        }
    elif 'crime' in title or 'criminal' in title:
        return {
            'primary': 'criminal',
            'secondary': 'criminal_procedure',
            'specific': 'criminal_law'
        }
    elif 'tort' in title or 'liability' in title:
        return {
            'primary': 'litigation',
            'secondary': 'tort_law',
            'specific': 'civil_liability'
        }
    elif 'privacy' in title or 'records' in title:
        return {
            'primary': 'regulatory',
            'secondary': 'privacy_law',
            'specific': 'health_information_privacy'
        }
    else:
        # Default to civil law
        return {
            'primary': 'civil',
            'secondary': 'civil_procedure',
            'specific': 'general_civil'
        }

def extract_legal_topics(metadata: Dict) -> List[str]:
    """Extract legal topics from key findings and facts"""
    topics = set()
    
    # Extract from key findings
    for finding in metadata.get('key_findings', []):
        finding_lower = finding.lower()
        if 'medical' in finding_lower:
            topics.add('medical_law')
        if 'privacy' in finding_lower or 'hipaa' in finding_lower:
            topics.add('privacy_law')
        if 'liability' in finding_lower:
            topics.add('tort_liability')
        if 'criminal' in finding_lower:
            topics.add('criminal_law')
        if 'statute of limitations' in finding_lower:
            topics.add('statute_of_limitations')
        if 'damages' in finding_lower:
            topics.add('damages')
        if 'negligence' in finding_lower:
            topics.add('negligence')
        if 'consent' in finding_lower:
            topics.add('informed_consent')
        if 'disclosure' in finding_lower:
            topics.add('disclosure_requirements')
    
    # Extract from facts
    for fact in metadata.get('extracted_facts', []):
        for context_word in fact.get('context', []):
            if context_word.lower() in ['damages', 'liability', 'negligence', 'consent', 'privacy']:
                topics.add(context_word.lower())
    
    # Ensure we have at least some topics
    if not topics:
        topics = {'civil_procedure', 'texas_law', 'legal_requirements'}
    
    return list(topics)[:10]  # Limit to 10 topics

def create_enhanced_chunks(text: str, metadata: Dict, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Dict]:
    """Create text chunks enhanced with metadata from preprocessing"""
    chunks = []
    
    # Split by sentence boundaries
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
                # Check if fact's context words appear in this chunk
                fact_contexts = fact.get('context', [])
                if any(context.lower() in current_chunk.lower() for context in fact_contexts):
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
            if any(context.lower() in current_chunk.lower() for context in fact.get('context', [])):
                chunk_facts.append(fact)
        
        chunks.append({
            'text': current_chunk.strip(),
            'start_char': current_start,
            'end_char': current_pos,
            'facts': chunk_facts,
            'metadata_id': metadata.get('id')
        })
    
    return chunks

def format_citations(facts: List[Dict]) -> List[str]:
    """Extract and format citations from facts"""
    citations = []
    for fact in facts:
        if 'citation' in fact:
            citations.append(fact['citation'])
    return citations

def ingest_enriched_document(pdf_path: Path, metadata: Dict, superlinked_url: str) -> bool:
    """Ingest a document with all enriched metadata, facts, and summaries"""
    print(f"\n📄 Processing: {metadata.get('title', pdf_path.stem)}")
    
    # Extract full text
    full_text = extract_pdf_text(pdf_path)
    if not full_text:
        print(f"❌ Failed to extract text from {pdf_path}")
        return False
    
    print(f"   ✓ Extracted {len(full_text)} characters")
    print(f"   ✓ Found {metadata.get('fact_count', 0)} facts")
    print(f"   ✓ Has executive summary: {'Yes' if metadata.get('executive_summary') else 'No'}")
    
    # Determine practice areas and legal topics
    practice_areas = determine_practice_areas(metadata)
    legal_topics = extract_legal_topics(metadata)
    
    print(f"   ✓ Practice areas: {practice_areas['primary']} > {practice_areas['secondary']} > {practice_areas['specific']}")
    print(f"   ✓ Legal topics: {', '.join(legal_topics[:3])}...")
    
    # Create parent document ID
    parent_doc_id = metadata.get('id', str(uuid.uuid4()))
    
    # Extract all citations
    all_citations = format_citations(metadata.get('extracted_facts', []))
    
    # Determine author based on content
    author = "Texas Legislature"  # Default
    if metadata.get('content_type') == 'report':
        author = "Office of the Governor"
    elif 'guide' in metadata.get('title', '').lower():
        author = "Texas Attorney General"
    
    # Base document data with all enriched fields
    base_document_data = {
        # Core fields - using legacy format for compatibility
        "practice_areas": f"{practice_areas['primary']},{practice_areas['secondary']},{practice_areas['specific']}",
        "legal_topics": ','.join(legal_topics),
        "jurisdiction": metadata.get('jurisdiction_state', 'texas'),
        "authority_level": "primary" if metadata.get('content_type') == 'statute' else "secondary",
        "document_type": metadata.get('content_type', 'statute'),
        "publication_date": int(datetime.fromisoformat(metadata.get('processed_date', datetime.now().isoformat())).timestamp()),
        "author": author,
        
        # Hierarchical fields
        "jurisdiction_country": metadata.get('jurisdiction_country', 'united_states'),
        "jurisdiction_state": metadata.get('jurisdiction_state', 'texas'),
        "jurisdiction_city": "",  # Not in metadata
        "jurisdiction_full_path": f"{metadata.get('jurisdiction_country', 'united_states')}/{metadata.get('jurisdiction_state', 'texas')}",
        
        # Hierarchical practice areas
        "practice_area_primary": practice_areas['primary'],
        "practice_area_secondary": practice_areas['secondary'],
        "practice_area_specific": practice_areas['specific'],
        "practice_area_full_path": f"{practice_areas['primary']}/{practice_areas['secondary']}/{practice_areas['specific']}",
        
        # Preprocessing fields
        "extracted_facts": json.dumps(metadata.get('extracted_facts', [])),
        "fact_locations": json.dumps([f.get('location', '') for f in metadata.get('extracted_facts', [])]),
        "fact_count": metadata.get('fact_count', 0),
        "key_findings": json.dumps(metadata.get('key_findings', [])),
        "executive_summary": metadata.get('executive_summary', ''),
        "summary_bullet_points": json.dumps(metadata.get('summary_bullet_points', [])),
        "summary_conclusion": metadata.get('summary_conclusion', ''),
        "key_provisions": json.dumps(metadata.get('key_findings', [])),  # Using key findings
        "practical_implications": metadata.get('summary_conclusion', ''),
        
        # Citation fields
        "citations": json.dumps(all_citations),
        "citations_apa7": json.dumps(all_citations),
        "internal_citations": json.dumps([]),  # Would need deeper analysis
        "external_citations": json.dumps(all_citations),
        
        # Keywords and search
        "keywords": json.dumps(metadata.get('key_takeaways', [])),
        "summary": metadata.get('executive_summary', ''),
        "key_takeaways": json.dumps(metadata.get('key_takeaways', [])),
        
        # Scoring and metadata
        "authority_score": 0.9 if metadata.get('content_type') == 'statute' else 0.7,
        "relevance_score": 0.8,
        "citation_count": len(all_citations),
        "confidence_score": 90,  # High confidence for Claude-processed
        
        # Source info
        "source_url": "",
        "pdf_path": str(pdf_path),
        "word_count": len(full_text.split()),
        
        # Progressive disclosure
        "broad_topics": practice_areas['primary'],
        "content_density": min(100, metadata.get('fact_count', 0) * 10),  # More facts = denser
        "coverage_scope": "comprehensive" if metadata.get('fact_count', 0) > 10 else "moderate",
        "legal_concepts": ','.join(legal_topics),
        "client_relevance_score": 8,  # High for Texas law
        "complexity_level": "intermediate",
        
        # Content strategy
        "target_audience": "practitioners",
        "readability_score": 75,  # Legal documents tend to be complex
        "common_questions": json.dumps([]),  # Could extract from content
        
        # Quality fields
        "human_reviewed": "false",
        "last_verified": metadata.get('processed_date', ''),
        "preprocessing_version": metadata.get('preprocessing_version', '1.0'),
        
        # Empty fields for this document type
        "injury_type": "",
        "injury_severity": "",
        "medical_specialty": "",
        "liability_theory": "",
        "medical_treatment": "",
        "trial_readiness": "",
        "case_number": "",
        "published_date": metadata.get('processed_date', ''),
        "effective_date": "",
        "last_updated": metadata.get('processed_date', ''),
        "citation_format": all_citations[0] if all_citations else "",
        "case_precedents": json.dumps([]),
        "legislative_history": "",
        "cites_documents": json.dumps([]),
        "cited_by_documents": json.dumps([]),
        "related_documents": json.dumps([]),
        "superseded_by": "",
        "compliance_requirements": "",
        "deadlines_timeframes": "",
        "parties_affected": "",
        "penalties_consequences": "",
        "exceptions_exclusions": "",
        "synonyms": "",
        "acronyms_abbreviations": "",
        "search_weight": 5,
        "access_frequency": 0,
        "user_ratings": json.dumps([]),
        "search_performance": 0,
        "update_priority": "medium",
        "notes_comments": ""
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
                "chunk_context": chunk['text'][:200] + "...",  # First 200 chars as context
                "is_chunk": "true",
                
                # Include facts relevant to this chunk
                "extracted_facts": json.dumps(chunk.get('facts', [])),
                "fact_count": len(chunk.get('facts', [])),
                
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
    
    # Also ingest a master document record with summary only
    master_doc_data = {
        "id": parent_doc_id,
        "title": metadata.get('title', pdf_path.stem),
        "content_text": metadata.get('executive_summary', '')[:1000],  # Just summary
        "is_chunk": "false",
        "parent_document_id": "",  # Master has no parent
        "chunk_index": -1,  # Not a chunk
        "start_char": 0,
        "end_char": 0,
        "chunk_context": "",
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
    
    print(f"\n🎯 Next steps:")
    print(f"   - Test searches at {args.superlinked_url}/docs")
    print(f"   - Query for facts: 'medical malpractice statute of limitations'")
    print(f"   - Query by citation: 'Tex. Health & Safety Code § 181'")
    print(f"   - Query summaries: 'rights of sexual assault survivors'")

if __name__ == "__main__":
    main()