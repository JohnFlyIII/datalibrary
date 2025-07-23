#!/bin/bash

echo "Testing Complete Metadata Filtering (Type + Jurisdiction + Recency)"
echo "=================================================================="

echo -e "\n1. Checking health..."
curl -s http://localhost:8080/health | jq '.'

# Calculate timestamps for testing
current_timestamp=$(date +%s)
one_week_ago=$((current_timestamp - 604800))
one_month_ago=$((current_timestamp - 2592000))
one_year_ago=$((current_timestamp - 31536000))

echo -e "\n2. Ingesting documents with complete metadata..."
curl -X POST http://localhost:8080/api/v1/ingest/legal_document \
  -H "Content-Type: application/json" \
  -d "[
    {
      \"id\": \"recent_tx_case\",
      \"title\": \"Recent Texas Medical Case\",
      \"content\": \"A recent Texas Supreme Court case on medical malpractice liability.\",
      \"document_type\": \"case\",
      \"jurisdiction\": \"texas\",
      \"publication_date\": $current_timestamp
    },
    {
      \"id\": \"old_tx_case\", 
      \"title\": \"Old Texas Medical Case\",
      \"content\": \"An older Texas case from last year on medical malpractice.\",
      \"document_type\": \"case\",
      \"jurisdiction\": \"texas\",
      \"publication_date\": $one_year_ago
    },
    {
      \"id\": \"recent_ca_statute\",
      \"title\": \"Recent California Privacy Law\",
      \"content\": \"New California legislation on consumer privacy rights.\",
      \"document_type\": \"statute\",
      \"jurisdiction\": \"california\",
      \"publication_date\": $one_week_ago
    },
    {
      \"id\": \"old_ca_statute\",
      \"title\": \"Old California Privacy Law\",
      \"content\": \"Previous California privacy statute from last year.\",
      \"document_type\": \"statute\",
      \"jurisdiction\": \"california\",
      \"publication_date\": $one_year_ago
    },
    {
      \"id\": \"recent_fed_reg\",
      \"title\": \"Recent Federal Healthcare Regulation\",
      \"content\": \"New federal regulation on healthcare data protection.\",
      \"document_type\": \"regulation\",
      \"jurisdiction\": \"federal\",
      \"publication_date\": $one_month_ago
    },
    {
      \"id\": \"old_fed_reg\",
      \"title\": \"Old Federal Healthcare Regulation\",
      \"content\": \"Previous federal healthcare regulation from last year.\",
      \"document_type\": \"regulation\",
      \"jurisdiction\": \"federal\",
      \"publication_date\": $one_year_ago
    }
  ]"

echo -e "\n\nData ingested. Waiting 5 seconds for indexing..."
sleep 5

echo -e "\n3. Testing complete metadata searches..."

echo -e "\n--- Recent Texas cases (medical) ---"
curl -s -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "medical",
    "title_query": "",
    "document_type": "case",
    "jurisdiction": "texas",
    "recency_weight": 1.0,
    "limit": 5
  }' | jq '.entries[] | {id: .id, score: .metadata.score}' | head -10

echo -e "\n--- California statutes (any recency) ---"
curl -s -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "privacy",
    "title_query": "",
    "document_type": "statute",
    "jurisdiction": "california",
    "recency_weight": 0.0,
    "limit": 5
  }' | jq '.entries[] | {id: .id, score: .metadata.score}' | head -10

echo -e "\n--- Recent federal regulations ---"
curl -s -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "healthcare",
    "title_query": "",
    "document_type": "regulation",
    "jurisdiction": "federal",
    "recency_weight": 1.0,
    "limit": 5
  }' | jq '.entries[] | {id: .id, score: .metadata.score}' | head -10

echo -e "\n--- All documents about privacy (no filters) ---"  
curl -s -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "privacy",
    "title_query": "",
    "document_type": "",
    "jurisdiction": "",
    "recency_weight": 0.5,
    "limit": 10
  }' | jq '.entries[] | {id: .id, score: .metadata.score}' | head -10

echo -e "\nComplete metadata test finished!"