#!/usr/bin/env python3
"""Test Superlinked connection and API endpoints"""
import requests
import json

def test_superlinked(url="http://localhost:8080"):
    print(f"Testing Superlinked at {url}")
    
    # Test 1: Basic health check
    try:
        response = requests.get(f"{url}/docs", timeout=5)
        print(f"✓ Docs endpoint: {response.status_code}")
    except Exception as e:
        print(f"✗ Docs endpoint failed: {e}")
    
    # Test 2: Check API endpoints
    try:
        response = requests.get(f"{url}/api/v1/", timeout=5)
        print(f"✓ API root: {response.status_code}")
    except Exception as e:
        print(f"✗ API root failed: {e}")
    
    # Test 3: Try a minimal ingestion
    try:
        test_doc = {
            "id": "test123",
            "title": "Test Document",
            "content_text": "This is a test",
            "practice_areas": "civil",
            "legal_topics": "test",
            "jurisdiction": "texas",
            "authority_level": "primary",
            "document_type": "statute",
            "publication_date": 1737536400
        }
        
        response = requests.post(
            f"{url}/api/v1/ingest/legal_document",
            json=test_doc,
            headers={'Content-Type': 'application/json'},
            timeout=60  # Give it more time
        )
        print(f"✓ Test ingestion: {response.status_code}")
        if response.status_code != 200:
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"✗ Test ingestion failed: {e}")

if __name__ == "__main__":
    test_superlinked()