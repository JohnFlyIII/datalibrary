#!/usr/bin/env python3
"""
Robust Legal Document Ingester with Setup Checking
Handles all the setup verification and initialization before ingestion
"""
import json
import requests
import time
import argparse
from pathlib import Path
from datetime import datetime
import uuid
from typing import List, Dict, Iterator, Optional, Tuple
import re
import pdfplumber
import sys

# ANSI color codes for pretty output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_status(message: str, status: str = "info"):
    """Print colored status messages"""
    if status == "success":
        print(f"{GREEN}✓ {message}{RESET}")
    elif status == "error":
        print(f"{RED}✗ {message}{RESET}")
    elif status == "warning":
        print(f"{YELLOW}⚠ {message}{RESET}")
    elif status == "info":
        print(f"{BLUE}ℹ {message}{RESET}")

def check_service_health(url: str, service_name: str) -> bool:
    """Check if a service is healthy"""
    try:
        response = requests.get(f"{url}/health", timeout=5)
        if response.status_code == 200:
            print_status(f"{service_name} is healthy at {url}", "success")
            return True
    except:
        pass
    
    # Try alternative endpoints
    try:
        response = requests.get(f"{url}/", timeout=5)
        if response.status_code in [200, 404]:  # 404 is ok, means service is responding
            print_status(f"{service_name} is responding at {url}", "success")
            return True
    except Exception as e:
        print_status(f"{service_name} is not accessible at {url}: {e}", "error")
        return False

def check_qdrant_setup(qdrant_url: str = "http://localhost:6333") -> Tuple[bool, List[str]]:
    """Check Qdrant setup and collections"""
    print_status("Checking Qdrant setup...", "info")
    
    try:
        # Get collections
        response = requests.get(f"{qdrant_url}/collections", timeout=5)
        if response.status_code != 200:
            print_status("Failed to get Qdrant collections", "error")
            return False, []
        
        data = response.json()
        collections = [col['name'] for col in data.get('result', {}).get('collections', [])]
        
        if collections:
            print_status(f"Found Qdrant collections: {', '.join(collections)}", "success")
        else:
            print_status("No collections found in Qdrant", "warning")
        
        return True, collections
        
    except Exception as e:
        print_status(f"Error checking Qdrant: {e}", "error")
        return False, []

def ensure_qdrant_collection(qdrant_url: str, collection_name: str, vector_size: int = 768) -> bool:
    """Ensure a Qdrant collection exists"""
    print_status(f"Ensuring collection '{collection_name}' exists...", "info")
    
    # Check if collection exists
    try:
        response = requests.get(f"{qdrant_url}/collections/{collection_name}", timeout=5)
        if response.status_code == 200:
            print_status(f"Collection '{collection_name}' already exists", "success")
            return True
    except:
        pass
    
    # Create collection
    try:
        create_data = {
            "vectors": {
                "size": vector_size,
                "distance": "Cosine"
            }
        }
        response = requests.put(
            f"{qdrant_url}/collections/{collection_name}",
            json=create_data,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            print_status(f"Created collection '{collection_name}' with vector size {vector_size}", "success")
            return True
        else:
            print_status(f"Failed to create collection: {response.text}", "error")
            return False
            
    except Exception as e:
        print_status(f"Error creating collection: {e}", "error")
        return False

def check_superlinked_setup(superlinked_url: str) -> Dict:
    """Check Superlinked setup and configuration"""
    print_status("Checking Superlinked setup...", "info")
    
    setup_info = {
        'healthy': False,
        'endpoints': [],
        'data_loaders': [],
        'vector_size': 768  # Default
    }
    
    # Check health
    if not check_service_health(superlinked_url, "Superlinked"):
        return setup_info
    
    setup_info['healthy'] = True
    
    # Check OpenAPI spec
    try:
        response = requests.get(f"{superlinked_url}/openapi.json", timeout=5)
        if response.status_code == 200:
            openapi = response.json()
            paths = openapi.get('paths', {})
            
            # Extract ingestion endpoints
            ingestion_endpoints = [path for path in paths.keys() if 'ingest' in path]
            setup_info['endpoints'] = ingestion_endpoints
            
            if ingestion_endpoints:
                print_status(f"Found ingestion endpoints: {', '.join(ingestion_endpoints)}", "success")
            else:
                print_status("No ingestion endpoints found", "warning")
                
    except Exception as e:
        print_status(f"Could not fetch OpenAPI spec: {e}", "warning")
    
    # Check data loaders
    try:
        response = requests.get(f"{superlinked_url}/data-loader/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            loaders = list(data.get('result', {}).keys())
            setup_info['data_loaders'] = loaders
            
            if loaders:
                print_status(f"Found data loaders: {', '.join(loaders)}", "success")
            else:
                print_status("No data loaders configured", "info")
                
    except Exception as e:
        print_status(f"Could not fetch data loaders: {e}", "warning")
    
    return setup_info

def test_ingestion_endpoint(superlinked_url: str, endpoint: str) -> bool:
    """Test if an ingestion endpoint works"""
    print_status(f"Testing endpoint {endpoint}...", "info")
    
    test_doc = {
        "id": f"test_{uuid.uuid4().hex[:8]}",
        "title": "Test Document",
        "content_text": "This is a test document for setup verification",
        "practice_areas": "civil",
        "legal_topics": "test",
        "jurisdiction": "texas",
        "authority_level": "primary",
        "document_type": "statute",
        "publication_date": int(datetime.now().timestamp()),
        "author": "Test"
    }
    
    try:
        response = requests.post(
            f"{superlinked_url}{endpoint}",
            json=test_doc,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code in [200, 201, 202]:
            print_status(f"Endpoint {endpoint} is working", "success")
            return True
        else:
            print_status(f"Endpoint returned {response.status_code}: {response.text[:100]}", "error")
            return False
            
    except Exception as e:
        print_status(f"Error testing endpoint: {e}", "error")
        return False

def setup_check_and_fix(superlinked_url: str, qdrant_url: str) -> Tuple[bool, str]:
    """
    Comprehensive setup check and fix
    Returns: (success, ingestion_endpoint)
    """
    print("\n" + "="*60)
    print_status("SETUP VERIFICATION AND INITIALIZATION", "info")
    print("="*60 + "\n")
    
    # 1. Check Qdrant
    qdrant_ok, collections = check_qdrant_setup(qdrant_url)
    if not qdrant_ok:
        print_status("Qdrant is not accessible. Please ensure it's running.", "error")
        return False, ""
    
    # 2. Check Superlinked
    superlinked_info = check_superlinked_setup(superlinked_url)
    if not superlinked_info['healthy']:
        print_status("Superlinked is not accessible. Please ensure it's running.", "error")
        return False, ""
    
    # 3. Determine collection name from endpoints
    collection_names = ['default', 'legal_document']  # Possible collection names
    
    # Extract collection names from endpoints
    for endpoint in superlinked_info['endpoints']:
        match = re.search(r'/ingest/(\w+)$', endpoint)
        if match:
            collection_names.append(match.group(1))
    
    # 4. Ensure required collections exist
    for collection_name in set(collection_names):
        if collection_name not in collections:
            print_status(f"Collection '{collection_name}' not found in Qdrant", "warning")
            if not ensure_qdrant_collection(qdrant_url, collection_name, superlinked_info['vector_size']):
                print_status(f"Failed to create collection '{collection_name}'", "error")
    
    # 5. Test ingestion endpoints
    working_endpoint = None
    for endpoint in superlinked_info['endpoints']:
        if test_ingestion_endpoint(superlinked_url, endpoint):
            working_endpoint = endpoint
            break
    
    if not working_endpoint:
        print_status("No working ingestion endpoint found", "error")
        return False, ""
    
    print("\n" + "="*60)
    print_status("SETUP VERIFICATION COMPLETE", "success")
    print(f"Using endpoint: {working_endpoint}")
    print("="*60 + "\n")
    
    return True, working_endpoint

# Import the ingestion functions from the complete script
from ingest_enriched_complete import (
    chunked_batches, extract_pdf_text, determine_practice_areas,
    extract_legal_topics, create_enhanced_chunks, format_citations
)

def ingest_single_document_with_retry(document_data: Dict, superlinked_url: str, endpoint: str, timeout: int = 300) -> bool:
    """Ingest a single document with proper endpoint and retry logic"""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            url = f"{superlinked_url}{endpoint}"
            headers = {
                'Accept': '*/*',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, json=document_data, headers=headers, timeout=timeout)
            
            if response.status_code in [200, 201, 202]:
                return True
            elif response.status_code == 404:
                print(f"      ❌ Endpoint not found: {endpoint}")
                return False
            elif response.status_code == 504:
                print(f"      ⏰ Timeout on attempt {attempt + 1}, retrying...")
                timeout = timeout * 2
                time.sleep(5)
                continue
            else:
                print(f"      ❌ Failed: {response.status_code} - {response.text[:100]}")
                return False
                
        except requests.exceptions.Timeout:
            print(f"      ⏰ Request timeout on attempt {attempt + 1}/{max_retries} (waited {timeout}s)")
            if attempt < max_retries - 1:
                timeout = timeout * 2
                time.sleep(5)
                continue
            return False
        except requests.exceptions.ConnectionError:
            print(f"      🔌 Connection error - is Superlinked running?")
            return False
        except Exception as e:
            print(f"      ❌ Error: {e}")
            return False
    
    return False

def main():
    parser = argparse.ArgumentParser(description='Ingest enriched legal documents with setup verification')
    parser.add_argument('--output-dir', required=True, help='Path to output directory with metadata')
    parser.add_argument('--pdf-dir', required=True, help='Path to directory with original PDFs')
    parser.add_argument('--superlinked-url', default='http://localhost:8080', help='Superlinked server URL')
    parser.add_argument('--qdrant-url', default='http://localhost:6333', help='Qdrant server URL')
    parser.add_argument('--limit', type=int, help='Limit number of documents to process')
    parser.add_argument('--skip-setup-check', action='store_true', help='Skip setup verification')
    
    args = parser.parse_args()
    
    # Run setup check unless skipped
    if not args.skip_setup_check:
        setup_ok, ingestion_endpoint = setup_check_and_fix(args.superlinked_url, args.qdrant_url)
        if not setup_ok:
            print_status("Setup verification failed. Please fix the issues and try again.", "error")
            sys.exit(1)
    else:
        # Assume default endpoint if skipping setup
        ingestion_endpoint = "/api/v1/ingest/legal_document"
        print_status("Skipping setup check, using default endpoint", "warning")
    
    output_path = Path(args.output_dir)
    pdf_path = Path(args.pdf_dir)
    
    # Find all metadata files
    metadata_files = list(output_path.glob('metadata/*_metadata.json'))
    
    if args.limit:
        metadata_files = metadata_files[:args.limit]
    
    print(f"\n🚀 Starting enriched document ingestion")
    print(f"📁 Output directory: {output_path}")
    print(f"📁 PDF directory: {pdf_path}")
    print(f"🌐 Superlinked URL: {args.superlinked_url}")
    print(f"🎯 Ingestion endpoint: {ingestion_endpoint}")
    print(f"📄 Found {len(metadata_files)} documents to process")
    
    successful = 0
    failed = []
    
    for idx, metadata_file in enumerate(metadata_files, 1):
        print(f"\n[{idx}/{len(metadata_files)}] Processing {metadata_file.name}")
        
        # Load metadata
        with open(metadata_file) as f:
            metadata = json.load(f)
        
        # Find corresponding PDF
        pdf_filename = metadata.get('source_filename')
        if not pdf_filename:
            print_status(f"No source filename in metadata", "error")
            continue
        
        pdf_file = pdf_path / pdf_filename
        if not pdf_file.exists():
            print_status(f"PDF not found: {pdf_file}", "error")
            failed.append(str(metadata_file))
            continue
        
        # Process document (simplified version for this script)
        try:
            # Extract text
            full_text = extract_pdf_text(pdf_file)
            if not full_text:
                print_status("Failed to extract text", "error")
                failed.append(str(pdf_file))
                continue
            
            print_status(f"Extracted {len(full_text)} characters", "success")
            
            # Prepare document data (simplified for testing)
            doc_data = {
                "id": metadata.get('id', str(uuid.uuid4())),
                "title": metadata.get('title', pdf_file.stem),
                "content_text": metadata.get('executive_summary', full_text[:1000]),
                "practice_areas": "civil,medical_malpractice",
                "legal_topics": ','.join(extract_legal_topics(metadata)[:3]),
                "jurisdiction": metadata.get('jurisdiction_state', 'texas'),
                "authority_level": "primary",
                "document_type": metadata.get('content_type', 'statute'),
                "publication_date": int(datetime.now().timestamp()),
                "author": "Texas Legislature",
                "summary": metadata.get('executive_summary', ''),
                "fact_count": metadata.get('fact_count', 0),
                "keywords": json.dumps(metadata.get('key_takeaways', [])),
                "pdf_path": str(pdf_file),
                "word_count": len(full_text.split())
            }
            
            # Ingest document
            if ingest_single_document_with_retry(doc_data, args.superlinked_url, ingestion_endpoint):
                print_status("Document ingested successfully", "success")
                successful += 1
            else:
                print_status("Failed to ingest document", "error")
                failed.append(str(pdf_file))
                
        except Exception as e:
            print_status(f"Error processing document: {e}", "error")
            failed.append(str(pdf_file))
        
        # Small delay between documents
        time.sleep(1)
    
    print(f"\n{'='*60}")
    print(f"🏁 Ingestion complete!")
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
    print(f"   - Check Qdrant at {args.qdrant_url}/dashboard")
    print(f"   - Try queries like: 'medical malpractice statute of limitations'")

if __name__ == "__main__":
    main()