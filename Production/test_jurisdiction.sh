#!/bin/bash

echo "Testing Jurisdiction Filtering"
echo "============================="

echo -e "\n1. Checking health..."
curl -s http://localhost:8080/health | jq '.'

echo -e "\n2. Ingesting documents with jurisdictions..."
curl -X POST http://localhost:8080/api/v1/ingest/legal_document \
  -H "Content-Type: application/json" \
  -d '[
    {
      "id": "tx1",
      "title": "Texas Medical Malpractice Act",
      "content": "Texas statute governing medical malpractice claims and damages.",
      "document_type": "statute",
      "jurisdiction": "texas"
    },
    {
      "id": "ca1", 
      "title": "California Consumer Privacy Act",
      "content": "California law protecting consumer privacy and data rights.",
      "document_type": "statute",
      "jurisdiction": "california"
    },
    {
      "id": "fed1",
      "title": "Federal Rules of Civil Procedure",
      "content": "National rules governing civil litigation procedures.",
      "document_type": "rule",
      "jurisdiction": "federal"
    },
    {
      "id": "tx2",
      "title": "Smith v. Houston Medical Center",
      "content": "Texas Supreme Court case on hospital liability standards.",
      "document_type": "case",
      "jurisdiction": "texas"
    },
    {
      "id": "ca2",
      "title": "Jones v. Tech Corp",
      "content": "California appellate court ruling on data breach liability.",
      "document_type": "case", 
      "jurisdiction": "california"
    },
    {
      "id": "fed2",
      "title": "HIPAA Privacy Rule",
      "content": "Federal regulation protecting health information privacy.",
      "document_type": "regulation",
      "jurisdiction": "federal"
    }
  ]'

echo -e "\n\nData ingested. Waiting 5 seconds for indexing..."
sleep 5

echo -e "\n3. Testing jurisdiction searches..."

echo -e "\n--- All Texas documents ---"
curl -s -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "",
    "title_query": "",
    "document_type": "",
    "jurisdiction": "texas",
    "limit": 10
  }' | jq '.entries[] | {id: .id, score: .metadata.score}'

echo -e "\n--- California statutes only ---"
curl -s -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "",
    "title_query": "",
    "document_type": "statute",
    "jurisdiction": "california",
    "limit": 5
  }' | jq '.entries[] | {id: .id, score: .metadata.score}'

echo -e "\n--- Federal regulations about privacy ---"
curl -s -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "privacy",
    "title_query": "",
    "document_type": "regulation",
    "jurisdiction": "federal",
    "limit": 5
  }' | jq '.entries[] | {id: .id, score: .metadata.score}'

echo -e "\n--- Medical cases in Texas ---"
curl -s -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "medical",
    "title_query": "",
    "document_type": "case",
    "jurisdiction": "texas",
    "limit": 5
  }' | jq '.entries[] | {id: .id, score: .metadata.score}'

echo -e "\nJurisdiction test complete!"