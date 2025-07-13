#!/usr/bin/env python3
"""
Direct Superlinked Ingester
Sends data directly to Superlinked server bypassing the legal API
"""
import json
import requests
import PyPDF2
from pathlib import Path
from datetime import datetime
import uuid

def extract_pdf_text(pdf_path):
    """Extract text from PDF using PyPDF2"""
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

def load_metadata(file_path):
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

def ingest_document_to_superlinked(pdf_path, superlinked_url="http://localhost:8080"):
    """Ingest a document directly to Superlinked server using proper API endpoints"""
    
    # Extract text from PDF
    print(f"Processing: {pdf_path}")
    text_content = extract_pdf_text(pdf_path)
    if not text_content:
        print("Failed to extract text from PDF")
        return False
    
    # Load metadata
    metadata = load_metadata(pdf_path)
    practice_area = metadata.get("practice_area", "personal_injury")
    
    print(f"Document prepared with {len(text_content)} characters")
    print(f"Practice area: {practice_area}")
    
    # Create document data based on practice area
    if practice_area == "personal_injury":
        # Use PersonalInjuryDocument schema
        document_data = {
            "id": str(uuid.uuid4()),
            "title": metadata.get("title", Path(pdf_path).stem),
            "content_text": text_content[:50000],  # Increase limit for meaningful content
            "practice_area": practice_area,
            "jurisdiction": metadata.get("jurisdiction", "texas"),
            "authority_level": metadata.get("authority_level", "primary"),
            "document_type": metadata.get("document_type", "statute"),
            "publication_date": int(datetime.now().timestamp()),
            "author": metadata.get("author", "Texas Legislature"),
            "citations": json.dumps(metadata.get("citations", [])),
            "keywords": json.dumps(metadata.get("keywords", ["civil", "practice", "remedies", "medical", "malpractice"])),
            "summary": metadata.get("summary", "Texas Civil Practice and Remedies Code - Personal Injury Provisions"),
            "authority_score": metadata.get("authority_score", 0.9),
            "citation_count": metadata.get("citation_count", 0),
            "source_url": metadata.get("source_url", ""),
            "pdf_path": str(pdf_path),
            "word_count": len(text_content.split()),
            # Personal injury specific fields
            "injury_type": "medical_malpractice",
            "injury_severity": "varied",
            "medical_specialty": "general",
            "liability_theory": "negligence",
            "medical_treatment": "varied",
            "trial_readiness": "statute_reference",
            "case_number": ""
        }
        schema_name = "personal_injury_document"
    else:
        # Use general LegalDocument schema
        document_data = {
            "id": str(uuid.uuid4()),
            "title": metadata.get("title", Path(pdf_path).stem),
            "content_text": text_content[:50000],
            "practice_area": practice_area,
            "jurisdiction": metadata.get("jurisdiction", "texas"),
            "authority_level": metadata.get("authority_level", "primary"),
            "document_type": metadata.get("document_type", "statute"),
            "publication_date": int(datetime.now().timestamp()),
            "author": metadata.get("author", "Texas Legislature"),
            "citations": json.dumps(metadata.get("citations", [])),
            "keywords": json.dumps(metadata.get("keywords", ["civil", "practice", "remedies"])),
            "summary": metadata.get("summary", "Texas Civil Practice and Remedies Code"),
            "authority_score": metadata.get("authority_score", 0.9),
            "relevance_score": 0.8,
            "citation_count": metadata.get("citation_count", 0),
            "source_url": metadata.get("source_url", ""),
            "pdf_path": str(pdf_path),
            "word_count": len(text_content.split())
        }
        schema_name = "legal_document"
    
    print(f"Using schema: {schema_name}")
    
    # Send to Superlinked using the proper API endpoint from documentation
    try:
        url = f"{superlinked_url}/api/v1/ingest/{schema_name}"
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, json=document_data, headers=headers)
        
        if response.status_code in [200, 202]:  # 202 = Accepted (async operation)
            print("✅ Document successfully ingested to Superlinked!")
            print(f"Response: {response.text}")
            return True
        else:
            print(f"❌ Failed to ingest document: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error ingesting document: {e}")
        return False

if __name__ == "__main__":
    # Test with Texas PDF
    pdf_path = "data/texas/civilpracticeandremediescode.pdf"
    success = ingest_document_to_superlinked(pdf_path)
    
    if success:
        print("\n🏛️ Ingestion completed successfully!")
    else:
        print("\n❌ Ingestion failed!")