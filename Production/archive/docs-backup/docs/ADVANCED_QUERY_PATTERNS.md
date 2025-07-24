# Advanced Query Patterns Documentation

## Three-Layer Query System

The legal platform implements a progressive disclosure search architecture with three distinct layers, enabling users to move from broad discovery to precise text-level search.

### Architecture Overview

```
Layer 1: DISCOVERY     →  Layer 2: EXPLORATION  →  Layer 3: DEEP DIVE
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ Broad document  │       │ Focused search  │       │ Precise chunk   │
│ search across   │  -->  │ with multiple   │  -->  │ search for      │
│ all content     │       │ filters         │       │ exact passages  │
└─────────────────┘       └─────────────────┘       └─────────────────┘
```

### Layer 1: Discovery Search

**Purpose**: Initial exploration across all documents for broad topic research.

**Endpoints**:
- `POST /api/v1/search/discovery_search` - Basic broad search
- `POST /api/v1/search/discovery_by_type` - Discovery filtered by document type  
- `POST /api/v1/search/discovery_by_jurisdiction` - Discovery filtered by jurisdiction

**Example Usage**:
```bash
# Basic discovery
curl -X POST "http://localhost:8080/api/v1/search/discovery_search" \
  -H "Content-Type: application/json" \
  -d '{
    "search_query": "medical malpractice",
    "limit": 10
  }'

# Discovery by document type
curl -X POST "http://localhost:8080/api/v1/search/discovery_by_type" \
  -H "Content-Type: application/json" \
  -d '{
    "search_query": "healthcare liability",
    "document_type": "statute",
    "limit": 10
  }'
```

**Use Cases**:
- Initial research on unfamiliar topics
- Overview of available documents
- Broad landscape analysis

### Layer 2: Exploration Search

**Purpose**: Focused investigation with multiple filter criteria for refined research.

**Endpoint**: `POST /api/v1/search/exploration_search`

**Example Usage**:
```bash
curl -X POST "http://localhost:8080/api/v1/search/exploration_search" \
  -H "Content-Type: application/json" \
  -d '{
    "search_query": "sexual assault statute of limitations",
    "document_type": "statute",
    "jurisdiction": "texas",
    "limit": 5
  }'
```

**Use Cases**:
- Targeted research within specific domains
- Cross-referencing between jurisdictions
- Focused investigation after initial discovery

### Layer 3: Deep Dive Search

**Purpose**: Precise chunk-level search for exact text passages and citations.

**Endpoints**:
- `POST /api/v1/search/deep_dive_search` - Filtered chunk search
- `POST /api/v1/search/deep_dive_precise` - Unfiltered precise search

**Example Usage**:
```bash
# Filtered deep dive
curl -X POST "http://localhost:8080/api/v1/search/deep_dive_search" \
  -H "Content-Type: application/json" \
  -d '{
    "search_query": "healthcare provider disciplinary action",
    "document_type": "regulation",
    "jurisdiction": "texas",
    "limit": 20
  }'

# Precise unfiltered search
curl -X POST "http://localhost:8080/api/v1/search/deep_dive_precise" \
  -H "Content-Type: application/json" \
  -d '{
    "search_query": "informed consent requirements",
    "limit": 10
  }'
```

**Use Cases**:
- Finding specific legal citations
- Locating exact statutory language
- Identifying precise regulatory requirements
- Quote extraction for legal documents

## Response Formats

### Document-Level Responses (Layers 1 & 2)
```json
{
  "entries": [
    {
      "id": "document_id_here",
      "fields": {
        "title": "Document Title",
        "content": "Document content...",
        "document_type": "statute",
        "jurisdiction": "texas"
      },
      "metadata": {
        "score": 0.85,
        "partial_scores": [],
        "vector_parts": []
      }
    }
  ]
}
```

### Chunk-Level Responses (Layer 3)
```json
{
  "entries": [
    {
      "id": "doc_id_chunk_0",
      "fields": {
        "parent_document_id": "doc_id",
        "chunk_index": 0,
        "text": "Specific text passage...",
        "start_char": 1200,
        "end_char": 3200,
        "document_type": "statute",
        "jurisdiction": "texas"
      },
      "metadata": {
        "score": 0.92,
        "partial_scores": [],
        "vector_parts": []
      }
    }
  ]
}
```

## Query Parameters

### Common Parameters
- `search_query` (required): The search text
- `limit` (optional): Maximum results (default varies by layer)

### Filter Parameters  
- `document_type`: Filter by document type
  - Values: `"statute"`, `"case"`, `"regulation"`, `"guidance"`, `"rule"`, `"other"`
- `jurisdiction`: Filter by jurisdiction
  - Values: `"federal"`, `"texas"`, `"california"`, `"new_york"`, `"florida"`, `"other"`

## Recommended Search Workflows

### 1. Comprehensive Legal Research
```
Step 1: Discovery Search
├── Broad search on research topic
├── Review document types and jurisdictions available
└── Identify promising documents

Step 2: Exploration Search  
├── Focus search with preferred filters
├── Cross-reference between jurisdictions
└── Narrow to most relevant documents

Step 3: Deep Dive Search
├── Extract specific citations and requirements
├── Find exact statutory language
└── Locate precise regulatory details
```

### 2. Quick Citation Lookup
```
Direct to Layer 3: Deep Dive Precise
├── Search for specific terms or phrases
├── No filtering required
└── Get immediate chunk-level results
```

### 3. Comparative Analysis
```
Step 1: Discovery by Jurisdiction (multiple calls)
├── Search same topic across jurisdictions
├── Compare document availability
└── Identify jurisdictional differences

Step 2: Deep Dive by Jurisdiction
├── Extract specific language from each jurisdiction
├── Compare regulatory approaches
└── Document jurisdictional variations
```

## Performance Characteristics

### Search Speed
- **Layer 1 (Discovery)**: Fast (~100-200ms) - searches document summaries
- **Layer 2 (Exploration)**: Medium (~200-400ms) - filtered document search  
- **Layer 3 (Deep Dive)**: Fast (~150-300ms) - searches text chunks

### Result Quality
- **Layer 1**: Good for broad overview, may include less relevant results
- **Layer 2**: Higher precision with filter constraints
- **Layer 3**: Highest precision for specific text passages

### Recommended Limits
- **Discovery**: 10-15 results for overview
- **Exploration**: 5-8 results for focused review
- **Deep Dive**: 15-25 results for comprehensive chunk analysis

## Integration Examples

### Python Client
```python
import requests

def search_legal_topic(topic, doc_type=None, jurisdiction=None):
    # Layer 1: Discovery
    discovery_results = requests.post(
        "http://localhost:8080/api/v1/search/discovery_search",
        json={"search_query": topic, "limit": 10}
    ).json()
    
    # Layer 2: Exploration (if filters provided)
    if doc_type and jurisdiction:
        exploration_results = requests.post(
            "http://localhost:8080/api/v1/search/exploration_search", 
            json={
                "search_query": topic,
                "document_type": doc_type,
                "jurisdiction": jurisdiction,
                "limit": 5
            }
        ).json()
    
    # Layer 3: Deep Dive
    deep_dive_results = requests.post(
        "http://localhost:8080/api/v1/search/deep_dive_precise",
        json={"search_query": topic, "limit": 20}
    ).json()
    
    return {
        "discovery": discovery_results,
        "exploration": exploration_results if doc_type else None,
        "deep_dive": deep_dive_results
    }
```

### JavaScript/Node.js Client
```javascript
async function layeredSearch(query, docType, jurisdiction) {
  const baseUrl = "http://localhost:8080/api/v1/search";
  
  // Layer 1: Discovery
  const discovery = await fetch(`${baseUrl}/discovery_search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ search_query: query, limit: 10 })
  }).then(r => r.json());
  
  // Layer 2: Exploration  
  const exploration = await fetch(`${baseUrl}/exploration_search`, {
    method: 'POST', 
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      search_query: query,
      document_type: docType,
      jurisdiction: jurisdiction,
      limit: 5
    })
  }).then(r => r.json());
  
  // Layer 3: Deep Dive
  const deepDive = await fetch(`${baseUrl}/deep_dive_search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      search_query: query,
      document_type: docType, 
      jurisdiction: jurisdiction,
      limit: 20
    })
  }).then(r => r.json());
  
  return { discovery, exploration, deepDive };
}
```

## Testing

Use the provided test script to validate all layers:

```bash
# Run comprehensive test
./test_layered_search.sh

# Test specific endpoints
curl -X POST "http://localhost:8080/api/v1/search/deep_dive_precise" \
  -H "Content-Type: application/json" \
  -d '{"search_query": "your search terms", "limit": 10}'
```

The three-layer system provides flexible search capabilities ranging from broad document discovery to precise text passage extraction, enabling comprehensive legal research workflows.