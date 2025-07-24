#!/bin/bash

# Test Three-Layer Query System
# =============================
# Demonstrates progressive disclosure search patterns

BASE_URL="http://localhost:8080"
SEARCH_TERM="medical malpractice"
DOC_TYPE="other"
JURISDICTION="federal"

echo "🔍 Testing Three-Layer Query System"
echo "=================================="
echo "Search term: $SEARCH_TERM"
echo "Document type: $DOC_TYPE"  
echo "Jurisdiction: $JURISDICTION"
echo ""

# Test server connectivity
echo "📡 Checking server connectivity..."
if curl -s "$BASE_URL/health" > /dev/null; then
    echo "✅ Server is responsive"
else
    echo "❌ Server is not responding"
    exit 1
fi
echo ""

# LAYER 1: DISCOVERY
echo "🌟 LAYER 1: DISCOVERY SEARCH"
echo "----------------------------"
echo "Broad search across all documents..."

echo "1️⃣ Basic Discovery:"
curl -s "$BASE_URL/api/v1/search/discovery_search" \
  -X POST -H "Content-Type: application/json" \
  -d "{\"search_query\": \"$SEARCH_TERM\", \"limit\": 5}" | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
entries = data.get('entries', [])
print(f'Found {len(entries)} documents')
for i, entry in enumerate(entries[:3]):
    score = entry.get('metadata', {}).get('score', 'N/A')
    print(f'  • Document {i+1}: {entry.get(\"id\", \"N/A\")} (score: {score})')
"
echo ""

echo "2️⃣ Discovery by Document Type:"
curl -s "$BASE_URL/api/v1/search/discovery_by_type" \
  -X POST -H "Content-Type: application/json" \
  -d "{\"search_query\": \"$SEARCH_TERM\", \"document_type\": \"$DOC_TYPE\", \"limit\": 5}" | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
entries = data.get('entries', [])
print(f'Found {len(entries)} documents of type $DOC_TYPE')
for i, entry in enumerate(entries[:3]):
    score = entry.get('metadata', {}).get('score', 'N/A')
    print(f'  • Document {i+1}: {entry.get(\"id\", \"N/A\")} (score: {score})')
"
echo ""

# LAYER 2: EXPLORATION
echo "🎯 LAYER 2: EXPLORATION SEARCH"
echo "------------------------------"
echo "Focused search with multiple filters..."

curl -s "$BASE_URL/api/v1/search/exploration_search" \
  -X POST -H "Content-Type: application/json" \
  -d "{\"search_query\": \"$SEARCH_TERM\", \"document_type\": \"$DOC_TYPE\", \"jurisdiction\": \"$JURISDICTION\", \"limit\": 3}" | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
entries = data.get('entries', [])
print(f'Found {len(entries)} focused results')
for i, entry in enumerate(entries):
    score = entry.get('metadata', {}).get('score', 'N/A')
    print(f'  • Document {i+1}: {entry.get(\"id\", \"N/A\")} (score: {score})')
"
echo ""

# LAYER 3: DEEP DIVE
echo "🔎 LAYER 3: DEEP DIVE SEARCH"
echo "----------------------------"
echo "Precise chunk-level search for exact passages..."

echo "1️⃣ Deep Dive with Filters:"
curl -s "$BASE_URL/api/v1/search/deep_dive_search" \
  -X POST -H "Content-Type: application/json" \
  -d "{\"search_query\": \"$SEARCH_TERM\", \"document_type\": \"$DOC_TYPE\", \"jurisdiction\": \"$JURISDICTION\", \"limit\": 5}" | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
entries = data.get('entries', [])
print(f'Found {len(entries)} precise chunks')
for i, entry in enumerate(entries[:3]):
    score = entry.get('metadata', {}).get('score', 'N/A')
    chunk_id = entry.get('id', 'N/A')
    print(f'  • Chunk {i+1}: {chunk_id} (score: {score})')
"
echo ""

echo "2️⃣ Precise Deep Dive (no filters):"
curl -s "$BASE_URL/api/v1/search/deep_dive_precise" \
  -X POST -H "Content-Type: application/json" \
  -d "{\"search_query\": \"healthcare provider\", \"limit\": 3}" | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
entries = data.get('entries', [])
print(f'Found {len(entries)} precise chunks for \"healthcare provider\"')
for i, entry in enumerate(entries):
    score = entry.get('metadata', {}).get('score', 'N/A')  
    chunk_id = entry.get('id', 'N/A')
    print(f'  • Chunk {i+1}: {chunk_id} (score: {score})')
"
echo ""

echo "✅ Three-layer query system test complete!"
echo ""
echo "📋 Available endpoints:"
echo "  Discovery: /api/v1/search/discovery_search"
echo "  Discovery by Type: /api/v1/search/discovery_by_type"  
echo "  Discovery by Jurisdiction: /api/v1/search/discovery_by_jurisdiction"
echo "  Exploration: /api/v1/search/exploration_search"
echo "  Deep Dive: /api/v1/search/deep_dive_search"
echo "  Deep Dive Precise: /api/v1/search/deep_dive_precise"