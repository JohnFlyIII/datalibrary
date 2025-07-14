#!/usr/bin/env python3
"""
Enhanced Multi-Area Legal Document Ingester for Superlinked
Supports documents that span multiple practice areas and legal topics
"""

import json
import uuid
import requests
from pathlib import Path
from datetime import datetime
import PyPDF2
import argparse

def extract_pdf_text(pdf_path):
    """Extract text from PDF file using PyPDF2"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def load_metadata(file_path):
    """Load metadata from file-specific or directory metadata.json"""
    # Check for file-specific metadata
    file_metadata_path = Path(str(file_path) + ".metadata.json")
    if file_metadata_path.exists():
        with open(file_metadata_path) as f:
            return json.load(f)
    
    # Fall back to directory metadata
    dir_metadata_path = Path(file_path).parent / "metadata.json"
    if dir_metadata_path.exists():
        with open(dir_metadata_path) as f:
            return json.load(f)
    
    return {}

def determine_practice_areas(metadata):
    """Determine multiple practice areas from metadata"""
    practice_areas = []
    legal_topics = metadata.get("legal_topics", [])
    
    # Primary practice area
    primary_practice_area = metadata.get("practice_area", "civil_law")
    practice_areas.append(primary_practice_area)
    
    # Add additional practice areas based on legal topics
    topic_to_practice_area_map = {
        "personal_injury": "personal_injury",
        "medical_malpractice": "medical_malpractice", 
        "medical_negligence": "medical_malpractice",
        "tort_liability": "personal_injury",
        "civil_procedure": "civil_law",
        "civil_law": "civil_law",
        "immigration": "immigration_law",
        "family_law": "family_law",
        "criminal_law": "criminal_law",
        "business_law": "business_law",
        "constitutional_law": "constitutional_law",
        "administrative_law": "administrative_law"
    }
    
    for topic in legal_topics:
        mapped_area = topic_to_practice_area_map.get(topic)
        if mapped_area and mapped_area not in practice_areas:
            practice_areas.append(mapped_area)
    
    # Also check keywords for additional areas
    keywords = metadata.get("keywords", [])
    for keyword in keywords:
        if "malpractice" in keyword.lower():
            if "medical_malpractice" not in practice_areas:
                practice_areas.append("medical_malpractice")
        if "personal_injury" in keyword.lower():
            if "personal_injury" not in practice_areas:
                practice_areas.append("personal_injury")
    
    return practice_areas

def ingest_document_to_superlinked(pdf_path, superlinked_url="http://localhost:8080"):
    """Enhanced ingester for multi-area legal documents"""
    
    # Extract text from PDF
    print(f"Processing: {pdf_path}")
    text_content = extract_pdf_text(pdf_path)
    if not text_content:
        print("Failed to extract text from PDF")
        return False
    
    # Load metadata
    metadata = load_metadata(pdf_path)
    
    # Determine multiple practice areas and topics
    practice_areas = determine_practice_areas(metadata)
    legal_topics = metadata.get("legal_topics", ["civil_law"])
    
    print(f"Document prepared with {len(text_content)} characters")
    print(f"Practice areas: {practice_areas}")
    print(f"Legal topics: {legal_topics}")
    
    # Create unified document data for enhanced LegalDocument schema
    document_data = {
        "id": str(uuid.uuid4()),
        "title": metadata.get("title", Path(pdf_path).stem),
        "content_text": text_content[:50000],  # Limit for meaningful content
        "practice_areas": practice_areas,  # Multi-value StringList
        "legal_topics": legal_topics,      # Multi-value StringList
        "jurisdiction": metadata.get("jurisdiction", "texas"),
        "authority_level": metadata.get("authority_level", "primary"),
        "document_type": metadata.get("document_type", "statute"),
        "publication_date": metadata.get("publication_date", int(datetime.now().timestamp())),
        "author": metadata.get("author", "Texas Legislature"),
        "citations": json.dumps(metadata.get("citations", [])),
        "keywords": json.dumps(metadata.get("keywords", ["civil", "practice", "remedies"])),
        "summary": metadata.get("summary", "Legal document"),
        "authority_score": metadata.get("authority_score", 0.9),
        "relevance_score": metadata.get("relevance_score", 0.8),
        "citation_count": metadata.get("citation_count", 0),
        "source_url": metadata.get("source_url", ""),
        "pdf_path": str(pdf_path),
        "word_count": len(text_content.split()),
        
        # Optional specialized fields (populated if relevant)
        "injury_type": "medical_malpractice" if "medical_malpractice" in practice_areas else "",
        "injury_severity": "varied" if "personal_injury" in practice_areas else "",
        "medical_specialty": "general" if "medical_malpractice" in practice_areas else "",
        "liability_theory": "negligence" if "personal_injury" in practice_areas else "",
        "medical_treatment": "varied" if "medical_malpractice" in practice_areas else "",
        "trial_readiness": "statute_reference" if "personal_injury" in practice_areas else "",
        "case_number": metadata.get("case_number", "")
    }
    
    # Always use unified legal_document schema
    schema_name = "legal_document"
    
    print(f"Using schema: {schema_name}")
    
    # Ingest to Superlinked
    url = f"{superlinked_url}/api/v1/ingest/{schema_name}"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=document_data, headers=headers)
        if response.status_code in [200, 202]:  # 202 = Accepted (async operation)
            print("✅ Document successfully ingested to Superlinked!")
            if response.text:
                print(f"Response: {response.text}")
        else:
            print(f"❌ Failed to ingest document. Status: {response.status_code}")
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Enhanced Multi-Area Legal Document Ingester")
    parser.add_argument("--file", required=True, help="Path to PDF file to ingest")
    parser.add_argument("--superlinked-url", default="http://localhost:8080", 
                       help="Superlinked server URL")
    
    args = parser.parse_args()
    
    if ingest_document_to_superlinked(args.file, args.superlinked_url):
        print("🏛️ Multi-area ingestion completed successfully!")
    else:
        print("❌ Ingestion failed!")

if __name__ == "__main__":
    main()