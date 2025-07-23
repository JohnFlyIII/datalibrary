#!/bin/bash

echo "Testing Search Quality with Real Legal Documents"
echo "==============================================="

echo -e "\n1. Health check..."
curl -s http://localhost:8080/health | jq '.'

echo -e "\n2. Testing searches with real content..."

echo -e "\n--- Search for medical malpractice statistics ---"
curl -s -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "medical malpractice statistics trends",
    "title_query": "",
    "document_type": "",
    "jurisdiction": "texas",
    "limit": 5
  }' | jq '.entries[] | {id: .id, score: .metadata.score}' | head -5

echo -e "\n--- Search for healthcare workforce information ---"
curl -s -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "healthcare practitioners workforce analysis",
    "title_query": "",
    "document_type": "",
    "jurisdiction": "",
    "limit": 5  
  }' | jq '.entries[] | {id: .id, score: .metadata.score}' | head -5

echo -e "\n--- Search for crime and assault data ---"
curl -s -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "sexual assault crime statistics",
    "title_query": "",
    "document_type": "statute",
    "jurisdiction": "texas",
    "limit": 3
  }' | jq '.entries[] | {id: .id, score: .metadata.score}' | head -5

echo -e "\n--- Search for Texas regulations specifically ---"
curl -s -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "",
    "title_query": "",
    "document_type": "regulation",
    "jurisdiction": "texas",
    "limit": 5
  }' | jq '.entries[] | {id: .id, score: .metadata.score}' | head -5

echo -e "\n--- General search about healthcare in Texas ---"
curl -s -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "healthcare Texas",
    "title_query": "",
    "document_type": "",
    "jurisdiction": "",
    "limit": 5
  }' | jq '.entries[] | {id: .id, score: .metadata.score}' | head -5

echo -e "\nReal data search testing complete!"