# 🔧 **LEGAL AI SYSTEM: TECHNICAL DEVELOPER GUIDE**
## **API Documentation, Data Types, and Implementation Details**

---

## 👥 **TARGET AUDIENCE**

**Primary Users**: Software Engineers, API Developers, DevOps Engineers, Technical Architects  
**Technical Focus**: API integration, data structures, error handling, performance optimization, system architecture  

---

## ⚡ **SYSTEM ARCHITECTURE OVERVIEW**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Legal AI System Architecture                  │
├─────────────────────────────────────────────────────────────────┤
│  Client Applications                                            │
│  ├── Web Dashboard                                              │
│  ├── API Clients                                               │
│  └── Mobile Apps                                               │
├─────────────────────────────────────────────────────────────────┤
│  API Gateway (http://localhost:8080)                           │
│  ├── /api/v1/search/discovery_search                          │
│  ├── /api/v1/search/exploration_search                        │
│  ├── /api/v1/search/deep_dive_precise                         │
│  └── /health                                                  │
├─────────────────────────────────────────────────────────────────┤
│  Superlinked Vector Database                                   │
│  ├── Document Embeddings (30+ vector spaces)                  │
│  ├── Chunk Embeddings (sentence-transformers)                 │
│  └── Metadata Index (82+ fields)                              │
├─────────────────────────────────────────────────────────────────┤
│  Data Processing Pipeline                                       │
│  ├── Claude Opus 4 AI Processing                              │
│  ├── PDF Extraction & Chunking                                │
│  └── Metadata Enrichment                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

# 🛠️ **API ENDPOINTS SPECIFICATION**

## **Base Configuration**
```bash
BASE_URL="http://localhost:8080"
API_VERSION="v1"
TIMEOUT=30  # seconds
RATE_LIMIT=100  # requests per minute
```

## **Health Check Endpoint**

### **GET /health**

**Description**: System health and readiness check  
**Authentication**: None required  
**Rate Limit**: Unlimited  

**Response Format:**
```typescript
interface HealthResponse {
  status: "healthy" | "degraded" | "unhealthy";
  timestamp: string;  // ISO 8601
  version: string;
  components: {
    database: "up" | "down";
    search_engine: "up" | "down";
    ai_processing: "up" | "down";
  };
  performance_metrics?: {
    avg_response_time_ms: number;
    active_connections: number;
    memory_usage_percent: number;
  };
}
```

**Example Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-07-25T01:30:00.000Z",
  "version": "1.2.0",
  "components": {
    "database": "up",
    "search_engine": "up", 
    "ai_processing": "up"
  },
  "performance_metrics": {
    "avg_response_time_ms": 245,
    "active_connections": 12,
    "memory_usage_percent": 68
  }
}
```

---

# 🔍 **SEARCH ENDPOINTS**

## **Discovery Search Endpoint**

### **POST /api/v1/search/discovery_search**

**Description**: High-level document discovery with AI-processed metadata  
**Use Case**: Initial exploration, blog research, broad topic investigation  
**Performance**: ~200-400ms response time  

### **Request Schema:**
```typescript
interface DiscoverySearchRequest {
  search_query: string;                    // Required. Natural language query
  limit?: number;                         // Optional. Default: 10, Max: 50
  jurisdiction?: string;                  // Optional. Filter by jurisdiction
  document_type?: 'statute' | 'case' | 'regulation' | 'other';
  min_publication_date?: number;          // Optional. Unix timestamp
  max_publication_date?: number;          // Optional. Unix timestamp
  include_chunks?: boolean;               // Optional. Include detailed chunk content
}
```

### **Response Schema:**
```typescript
interface DiscoverySearchResponse {
  entries: DocumentEntry[];
  query_metadata: {
    query: string;
    limit: number;
    execution_time_ms: number;
    total_results: number;
  };
  temporal_analysis?: TemporalAnalysis;
}

interface DocumentEntry {
  id: string;                            // Unique document identifier
  fields: DocumentFields;
  metadata: SearchMetadata;
  detailed_chunks?: ChunkContent[];      // If include_chunks=true
}

interface DocumentFields {
  // Core Fields
  title: string;
  content: string;                       // Rich AI-processed content
  document_type: 'statute' | 'case' | 'regulation' | 'other';
  jurisdiction: string;
  
  // AI-Processed Intelligence Fields  
  executive_summary: string;             // Claude Opus 4 summary
  key_findings: string;                  // Semicolon-separated findings
  key_takeaways: string;                // Plain-language explanations
  extracted_facts: string;              // JSON array of fact objects
  
  // Hierarchical Classification
  jurisdiction_state: string;
  jurisdiction_city: string;
  practice_area_primary: string;
  practice_area_secondary: string;
  
  // Enhanced Content Fields
  legal_topics: string;                  // Comma-separated topics
  keywords: string;                      // Search-optimized keywords
  
  // Temporal Fields
  publication_date: number;              // Unix timestamp
  confidence_score: number;              // 0-100 content quality score
  
  // Document Metadata
  source_filename: string;
  file_size_bytes: number;
  total_pages: number;
  total_chars: number;
  fact_count: number;
  
  // Processing Metadata
  ai_model: string;                      // "claude-opus-4-20250514"
  preprocessing_version: string;
  
  // Phase 1B Legal Practice Intelligence
  compliance_requirements: string;        // Regulatory mandates
  deadlines_timeframes: string;          // Time-sensitive information
  parties_affected: string;              // Stakeholders impacted
  penalties_consequences: string;        // Enforcement implications
  practical_implications: string;        // Real-world impact
  
  // Additional Schema Fields (82+ total)
  // ... (see full schema in load_real_data.py)
}

interface SearchMetadata {
  score: number;                         // Relevance score 0.0-1.0
  partial_scores: number[];              // Component similarity scores
  vector_parts: string[];                // Vector space contributions
}

interface ChunkContent {
  chunk_id: string;
  content: string;                       // Full chunk text
  chunk_index: number;
  start_char: number;
  end_char: number;
  relevance_score: number;
  context: string;
}
```

### **Example Request:**
```bash
curl -X POST "http://localhost:8080/api/v1/search/discovery_search" \
  -H "Content-Type: application/json" \
  -d '{
    "search_query": "medical malpractice expert witness requirements texas",
    "limit": 5,
    "jurisdiction": "texas",
    "document_type": "statute",
    "include_chunks": true
  }'
```

### **Example Response:**
```json
{
  "entries": [
    {
      "id": "8ff804f5a956",
      "fields": {
        "title": "Liability In Tort Medical C74",
        "content": "SUMMARY: This comprehensive Texas Civil Practice and Remedies Code document establishes the legal framework for medical liability claims...",
        "document_type": "statute",
        "jurisdiction": "texas",
        "executive_summary": "This comprehensive Texas Civil Practice and Remedies Code document establishes the legal framework for medical liability claims in Texas, including detailed expert witness requirements...",
        "key_findings": "Texas medical liability law requires expert witnesses to be board-certified or have substantial training in relevant medical areas and be actively practicing medicine. Expert reports must be filed within 120 days of filing suit...",
        "key_takeaways": "Medical malpractice cases in Texas require qualified expert witnesses who are actively practicing in relevant medical fields. Expert reports must be filed within 120 days...",
        "extracted_facts": "[{\"fact\": \"Expert witnesses must be board-certified or have substantial training in relevant medical area\", \"confidence\": 1.0, \"location\": \"Section 74.401\"}]",
        "jurisdiction_state": "texas",
        "practice_area_primary": "litigation",
        "practice_area_secondary": "medical_malpractice",
        "legal_topics": "medical malpractice, expert witness, tort liability",
        "keywords": "texas, medical, malpractice, expert, witness, board, certified",
        "publication_date": 1753324478,
        "confidence_score": 95,
        "source_filename": "texas_civil_practice_code.pdf", 
        "total_pages": 45,
        "fact_count": 12,
        "ai_model": "claude-opus-4-20250514",
        "compliance_requirements": "Expert witnesses must be board-certified and actively practicing in relevant medical field",
        "deadlines_timeframes": "Expert report must be filed within 120 days of lawsuit filing",
        "parties_affected": "Healthcare providers, medical practitioners, patients, legal counsel",
        "penalties_consequences": "Case dismissal possible if expert witness requirements not met",
        "practical_implications": "Medical malpractice cases require substantial upfront investment in qualified expert witnesses"
      },
      "metadata": {
        "score": 0.89234,
        "partial_scores": [0.92, 0.87, 0.88],
        "vector_parts": ["content_embedding", "topic_embedding", "legal_concept_embedding"] 
      },
      "detailed_chunks": [
        {
          "chunk_id": "8ff804f5a956_chunk_12",
          "content": "Sec. 74.401. QUALIFICATIONS OF EXPERT WITNESS IN SUIT AGAINST PHYSICIAN. (a) In a suit involving a health care liability claim against a physician for injury to or death of a patient, a person may qualify as an expert witness on the issue of whether the physician departed from accepted standards of medical care only if the person is: (1) board certified or has other substantial training or experience in an area of medical practice relevant to the claim; and (2) actively practicing medicine in rendering medical care services relevant to the claim.",
          "chunk_index": 12,
          "start_char": 15420,
          "end_char": 15892,
          "relevance_score": 0.94,
          "context": "Expert witness qualification requirements for medical malpractice cases"
        }
      ]
    }
  ],
  "query_metadata": {
    "query": "medical malpractice expert witness requirements texas",
    "limit": 5,
    "execution_time_ms": 287,
    "total_results": 1
  }
}
```

---

## **Exploration Search Endpoint**

### **POST /api/v1/search/exploration_search**

**Description**: Focused search with enhanced relevance filtering  
**Use Case**: Specific legal research, case preparation, detailed analysis  
**Performance**: ~300-500ms response time  

### **Request Schema:**
```typescript
interface ExplorationSearchRequest extends DiscoverySearchRequest {
  practice_area?: string;                // Filter by practice area
  min_confidence_score?: number;        // Minimum quality threshold
  sort_by?: 'relevance' | 'date' | 'confidence';
}
```

### **Response Schema:**
Same as DiscoverySearchResponse with additional filtering applied.

---

## **Deep Dive Precise Endpoint**

### **POST /api/v1/search/deep_dive_precise**

**Description**: Chunk-level search for specific legal text  
**Use Case**: Statutory language, precise citations, detailed legal analysis  
**Performance**: ~400-600ms response time  

### **Request Schema:**
```typescript
interface DeepDiveSearchRequest {
  search_query: string;
  limit?: number;                        // Default: 20 for chunk search
  document_id?: string;                  // Search within specific document
  chunk_context?: boolean;               // Include surrounding context
  min_relevance_score?: number;          // Minimum chunk relevance
}
```

### **Response Schema:**
```typescript
interface DeepDiveSearchResponse {
  entries: ChunkEntry[];
  query_metadata: QueryMetadata;
}

interface ChunkEntry {
  id: string;                           // Chunk ID
  fields: ChunkFields;
  metadata: SearchMetadata;
}

interface ChunkFields {
  content: string;                      // Full chunk content
  parent_document_id: string;           // Source document ID
  chunk_index: number;
  start_char: number;
  end_char: number;
  chunk_context: string;                // Surrounding context if requested
  document_title: string;               // Source document title
  document_type: string;
  jurisdiction: string;
}
```

---

# 📊 **DATA TYPES REFERENCE**

## **Core Data Types**

### **Jurisdiction Values:**
```typescript
type Jurisdiction = 
  | 'texas' 
  | 'california' 
  | 'new_york' 
  | 'federal' 
  | 'multi_state';
```

### **Document Types:**
```typescript
type DocumentType = 
  | 'statute'      // Legislative statutes and codes
  | 'case'         // Court decisions and case law
  | 'regulation'   // Administrative regulations
  | 'other';       // Contracts, guidelines, etc.
```

### **Practice Areas:**
```typescript
type PracticeAreaPrimary = 
  | 'litigation'
  | 'healthcare' 
  | 'regulatory'
  | 'corporate'
  | 'employment';

type PracticeAreaSecondary = 
  | 'medical_malpractice'
  | 'personal_injury'
  | 'healthcare_compliance'
  | 'data_privacy'
  | 'general_litigation';
```

### **Extracted Fact Object:**
```typescript
interface ExtractedFact {
  fact: string;                         // The extracted fact statement
  location: string;                     // Page/section reference
  citation: string;                     // Full citation information
  context: string[];                    // Related context terms
  confidence: number;                   // AI confidence score 0.0-1.0
}
```

### **Temporal Analysis:**
```typescript
interface TemporalAnalysis {
  earliest_document: string;            // ISO 8601 date
  latest_document: string;              // ISO 8601 date  
  total_timespan_days: number;
  documents_by_year: Record<string, number>;
}
```

---

# 🔧 **CLIENT IMPLEMENTATION PATTERNS**

## **Basic Client Setup**

### **Python Client:**
```python
import requests
import json
from typing import Dict, List, Optional
from datetime import datetime

class LegalAIClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'LegalAI-Client/1.0'
        })
    
    def health_check(self) -> Dict:
        """Check system health"""
        response = self.session.get(f"{self.base_url}/health", timeout=5)
        response.raise_for_status()
        return response.json()
    
    def discovery_search(self, query: str, **kwargs) -> Dict:
        """Perform discovery search with optional parameters"""
        payload = {"search_query": query, **kwargs}
        response = self.session.post(
            f"{self.base_url}/api/v1/search/discovery_search",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    def get_statistical_data(self, topic: str, jurisdiction: str = "texas") -> List[Dict]:
        """Extract statistical data for blog content"""
        results = self.discovery_search(
            f"{topic} statistics financial data {jurisdiction}",
            limit=3,
            jurisdiction=jurisdiction
        )
        
        statistical_facts = []
        for entry in results.get('entries', []):
            facts = json.loads(entry['fields'].get('extracted_facts', '[]'))
            for fact in facts:
                if any(indicator in fact['fact'].lower() 
                      for indicator in ['billion', 'million', '$', '%', 'annual']):
                    statistical_facts.append({
                        'fact': fact['fact'],
                        'confidence': fact['confidence'],
                        'source': entry['fields']['title'],
                        'document_id': entry['id']
                    })
        
        return statistical_facts
```

### **JavaScript/TypeScript Client:**
```typescript
interface LegalAIClientConfig {
  baseUrl?: string;
  timeout?: number;
  apiKey?: string;
}

class LegalAIClient {
  private baseUrl: string;
  private timeout: number;
  
  constructor(config: LegalAIClientConfig = {}) {
    this.baseUrl = config.baseUrl || 'http://localhost:8080';
    this.timeout = config.timeout || 30000;
  }
  
  async discoverySearch(request: DiscoverySearchRequest): Promise<DiscoverySearchResponse> {
    const response = await fetch(`${this.baseUrl}/api/v1/search/discovery_search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
      signal: AbortSignal.timeout(this.timeout)
    });
    
    if (!response.ok) {
      throw new Error(`Search failed: ${response.status} ${response.statusText}`);
    }
    
    return response.json();
  }
  
  async extractFinancialData(topic: string, jurisdiction: string = 'texas'): Promise<ExtractedFact[]> {
    const results = await this.discoverySearch({
      search_query: `${topic} financial statistics billion million`,
      jurisdiction,
      limit: 5
    });
    
    const financialFacts: ExtractedFact[] = [];
    
    for (const entry of results.entries) {
      const facts: ExtractedFact[] = JSON.parse(entry.fields.extracted_facts || '[]');
      const financial = facts.filter(fact => 
        /(\$|billion|million|percent|annual)/i.test(fact.fact)
      );
      financialFacts.push(...financial);
    }
    
    return financialFacts.sort((a, b) => b.confidence - a.confidence);
  }
}
```

---

# ⚡ **PERFORMANCE OPTIMIZATION**

## **Caching Strategy**

### **Client-Side Caching:**
```python
from functools import lru_cache
import hashlib

class CachedLegalAIClient(LegalAIClient):
    @lru_cache(maxsize=128)
    def _cached_discovery_search(self, query_hash: str, **kwargs) -> Dict:
        return super().discovery_search(kwargs['query'], **{k:v for k,v in kwargs.items() if k != 'query'})
    
    def discovery_search(self, query: str, **kwargs) -> Dict:
        # Create cache key from query and parameters
        cache_key = hashlib.md5(
            f"{query}:{json.dumps(sorted(kwargs.items()), sort_keys=True)}".encode()
        ).hexdigest()
        
        return self._cached_discovery_search(
            cache_key, 
            query=query, 
            **kwargs
        )
```

### **Response Time Optimization:**
```python
import asyncio
import aiohttp
from typing import List

class AsyncLegalAIClient:
    async def batch_discovery_search(self, queries: List[str]) -> List[Dict]:
        """Execute multiple searches concurrently"""
        async with aiohttp.ClientSession() as session:
            tasks = [
                self._async_discovery_search(session, query) 
                for query in queries
            ]
            return await asyncio.gather(*tasks)
    
    async def _async_discovery_search(self, session: aiohttp.ClientSession, query: str) -> Dict:
        async with session.post(
            f"{self.base_url}/api/v1/search/discovery_search",
            json={"search_query": query, "limit": 5},
            timeout=aiohttp.ClientTimeout(total=30)
        ) as response:
            return await response.json()
```

---

# 🚨 **ERROR HANDLING**

## **HTTP Status Codes**

| Code | Meaning | Client Action |
|------|---------|---------------|
| `200` | Success | Process response data |
| `400` | Bad Request | Check request format and required fields |
| `429` | Rate Limited | Implement exponential backoff |
| `500` | Server Error | Retry with exponential backoff |
| `503` | Service Unavailable | Check system health, wait and retry |

## **Error Response Format:**
```typescript
interface ErrorResponse {
  error: {
    code: string;                       // Error code identifier
    message: string;                    // Human-readable error message
    details?: any;                      // Additional error context
    request_id?: string;                // For support debugging
  };
  timestamp: string;                    // ISO 8601 timestamp
}
```

## **Robust Error Handling:**
```python
import time
import random
from requests.exceptions import RequestException, Timeout, ConnectionError

class ResilientLegalAIClient(LegalAIClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_retries = 3
        self.base_delay = 1.0
    
    def discovery_search_with_retry(self, query: str, **kwargs) -> Dict:
        """Discovery search with exponential backoff retry logic"""
        for attempt in range(self.max_retries):
            try:
                return self.discovery_search(query, **kwargs)
                
            except Timeout:
                if attempt == self.max_retries - 1:
                    raise
                delay = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
                time.sleep(delay)
                
            except ConnectionError:
                if attempt == self.max_retries - 1:
                    raise
                # Check health before retrying
                try:
                    health = self.health_check()
                    if health['status'] != 'healthy':
                        time.sleep(5)  # Wait longer if system unhealthy
                except:
                    time.sleep(10)  # Fallback delay
                    
            except RequestException as e:
                if hasattr(e, 'response') and e.response.status_code == 429:
                    # Rate limited - exponential backoff
                    delay = self.base_delay * (2 ** attempt)
                    time.sleep(delay)
                else:
                    raise
        
        raise Exception(f"Failed after {self.max_retries} attempts")
```

---

# 📊 **MONITORING AND OBSERVABILITY**

## **Client-Side Metrics Collection:**
```python
import time
from dataclasses import dataclass
from typing import Dict, List
import logging

@dataclass
class SearchMetrics:
    query: str
    response_time_ms: int
    result_count: int
    success: bool
    error_code: str = None

class InstrumentedLegalAIClient(LegalAIClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics: List[SearchMetrics] = []
        self.logger = logging.getLogger(__name__)
    
    def discovery_search(self, query: str, **kwargs) -> Dict:
        start_time = time.perf_counter()
        
        try:
            result = super().discovery_search(query, **kwargs)
            response_time = int((time.perf_counter() - start_time) * 1000)
            
            # Log successful search
            self.metrics.append(SearchMetrics(
                query=query,
                response_time_ms=response_time,
                result_count=len(result.get('entries', [])),
                success=True
            ))
            
            self.logger.info(
                f"Search successful: query='{query}' "
                f"results={len(result.get('entries', []))} "
                f"time={response_time}ms"
            )
            
            return result
            
        except Exception as e:
            response_time = int((time.perf_counter() - start_time) * 1000)
            
            # Log failed search
            self.metrics.append(SearchMetrics(
                query=query,
                response_time_ms=response_time,
                result_count=0,
                success=False,
                error_code=type(e).__name__
            ))
            
            self.logger.error(
                f"Search failed: query='{query}' "
                f"error={type(e).__name__} "
                f"time={response_time}ms"
            )
            
            raise
    
    def get_performance_report(self) -> Dict:
        """Generate client performance report"""
        if not self.metrics:
            return {"message": "No metrics collected"}
        
        successful_searches = [m for m in self.metrics if m.success]
        failed_searches = [m for m in self.metrics if not m.success]
        
        return {
            "total_searches": len(self.metrics),
            "successful_searches": len(successful_searches),
            "failed_searches": len(failed_searches),
            "success_rate": len(successful_searches) / len(self.metrics) * 100,
            "avg_response_time_ms": sum(m.response_time_ms for m in successful_searches) / len(successful_searches) if successful_searches else 0,
            "avg_results_per_search": sum(m.result_count for m in successful_searches) / len(successful_searches) if successful_searches else 0,
            "common_errors": {
                error: len([m for m in failed_searches if m.error_code == error])
                for error in set(m.error_code for m in failed_searches)
            }
        }
```

---

# 🔒 **SECURITY CONSIDERATIONS**

## **API Security Best Practices:**

### **Input Validation:**
```python
import re
from typing import Any

class SecureLegalAIClient(LegalAIClient):
    MAX_QUERY_LENGTH = 1000
    ALLOWED_CHARS = re.compile(r'^[a-zA-Z0-9\s\-_.,()]+$')
    
    def _validate_query(self, query: str) -> str:
        """Validate and sanitize search query"""
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
        
        if len(query) > self.MAX_QUERY_LENGTH:
            raise ValueError(f"Query too long: {len(query)} > {self.MAX_QUERY_LENGTH}")
        
        if not self.ALLOWED_CHARS.match(query):
            raise ValueError("Query contains invalid characters")
        
        return query.strip()
    
    def _validate_limit(self, limit: int) -> int:
        """Validate result limit parameter"""
        if limit < 1 or limit > 50:
            raise ValueError("Limit must be between 1 and 50")
        return limit
    
    def discovery_search(self, query: str, **kwargs) -> Dict:
        # Validate all inputs
        validated_query = self._validate_query(query)
        
        if 'limit' in kwargs:
            kwargs['limit'] = self._validate_limit(kwargs['limit'])
        
        return super().discovery_search(validated_query, **kwargs)
```

### **Request Logging for Audit:**
```python
import json
import hashlib
from datetime import datetime

class AuditedLegalAIClient(LegalAIClient):
    def __init__(self, *args, audit_log_path: str = "legal_ai_audit.log", **kwargs):
        super().__init__(*args, **kwargs)
        self.audit_log = audit_log_path
        
    def _log_request(self, endpoint: str, payload: Dict, response_data: Dict = None, error: str = None):
        """Log all API requests for audit purposes"""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint": endpoint,
            "request_hash": hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest(),
            "query": payload.get('search_query', 'N/A'),
            "success": error is None,
            "result_count": len(response_data.get('entries', [])) if response_data else 0,
            "error": error
        }
        
        with open(self.audit_log, 'a') as f:
            f.write(json.dumps(audit_entry) + '\n')
    
    def discovery_search(self, query: str, **kwargs) -> Dict:
        payload = {"search_query": query, **kwargs}
        
        try:
            result = super().discovery_search(query, **kwargs)
            self._log_request("discovery_search", payload, result)
            return result
        except Exception as e:
            self._log_request("discovery_search", payload, error=str(e))
            raise
```

---

# 🧪 **TESTING FRAMEWORK**

## **Unit Testing Examples:**
```python
import unittest
from unittest.mock import Mock, patch
import json

class TestLegalAIClient(unittest.TestCase):
    def setUp(self):
        self.client = LegalAIClient("http://test-server:8080")
    
    @patch('requests.Session.post')
    def test_discovery_search_success(self, mock_post):
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "entries": [
                {
                    "id": "test-doc-1",
                    "fields": {
                        "title": "Test Medical Malpractice Statute",
                        "document_type": "statute",
                        "executive_summary": "Test summary..."
                    },
                    "metadata": {"score": 0.85}
                }
            ],
            "query_metadata": {
                "execution_time_ms": 250,
                "total_results": 1
            }
        }
        mock_post.return_value = mock_response
        
        # Test the search
        result = self.client.discovery_search("medical malpractice texas")
        
        # Assertions
        self.assertEqual(len(result['entries']), 1)
        self.assertEqual(result['entries'][0]['fields']['title'], "Test Medical Malpractice Statute")
        self.assertEqual(result['query_metadata']['total_results'], 1)
        
        # Verify API call
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[1]['json']['search_query'], "medical malpractice texas")
    
    @patch('requests.Session.post')
    def test_discovery_search_error_handling(self, mock_post):
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.RequestException("Server Error")
        mock_post.return_value = mock_response
        
        # Test error handling
        with self.assertRaises(requests.RequestException):
            self.client.discovery_search("test query")
    
    def test_query_validation(self):
        secure_client = SecureLegalAIClient("http://test-server:8080")
        
        # Test empty query
        with self.assertRaises(ValueError):
            secure_client._validate_query("")
        
        # Test query too long
        with self.assertRaises(ValueError):
            secure_client._validate_query("a" * 1001)
        
        # Test invalid characters
        with self.assertRaises(ValueError):
            secure_client._validate_query("test; DROP TABLE users;")
        
        # Test valid query
        valid_query = secure_client._validate_query("medical malpractice texas")
        self.assertEqual(valid_query, "medical malpractice texas")

if __name__ == '__main__':
    unittest.main()
```

## **Integration Testing:**
```python
class TestLegalAIIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure test server is running
        cls.client = LegalAIClient("http://localhost:8080")
        
        # Wait for server to be ready
        max_retries = 30
        for _ in range(max_retries):
            try:
                health = cls.client.health_check()
                if health['status'] == 'healthy':
                    break
                time.sleep(1)
            except:
                time.sleep(1)
        else:
            raise Exception("Test server not available")
    
    def test_full_blog_research_workflow(self):
        """Test complete blog research workflow"""
        
        # Phase 1: Discovery
        discovery_results = self.client.discovery_search(
            "medical malpractice statistics texas", 
            limit=3
        )
        
        self.assertGreater(len(discovery_results['entries']), 0)
        self.assertIn('query_metadata', discovery_results)
        
        # Phase 2: Statistical extraction
        statistical_facts = self.client.get_statistical_data("medical malpractice", "texas")
        
        self.assertGreater(len(statistical_facts), 0)
        
        # Verify statistical data has required fields
        for fact in statistical_facts[:3]:
            self.assertIn('fact', fact)
            self.assertIn('confidence', fact)
            self.assertIn('source', fact)
            self.assertTrue(0.0 <= fact['confidence'] <= 1.0)
        
        # Phase 3: Content validation
        top_result = discovery_results['entries'][0]
        required_fields = [
            'title', 'executive_summary', 'key_findings', 
            'key_takeaways', 'jurisdiction', 'document_type'
        ]
        
        for field in required_fields:
            self.assertIn(field, top_result['fields'])
            self.assertIsNotNone(top_result['fields'][field])
    
    def test_performance_requirements(self):
        """Test that API meets performance requirements"""
        import time
        
        start_time = time.perf_counter()
        result = self.client.discovery_search("medical malpractice", limit=5)
        end_time = time.perf_counter()
        
        response_time_ms = (end_time - start_time) * 1000
        
        # Should respond within 1 second for discovery search
        self.assertLess(response_time_ms, 1000)
        
        # Should return results
        self.assertGreater(len(result['entries']), 0)
        
        # Verify response time is reported
        self.assertIn('query_metadata', result)
        self.assertIn('execution_time_ms', result['query_metadata'])
```

---

# 📚 **SDK AND TOOLING**

## **Code Generation from OpenAPI Spec:**
```bash
# Generate client from OpenAPI specification
npx @openapitools/openapi-generator-cli generate \
  -i http://localhost:8080/openapi.json \
  -g typescript-fetch \
  -o ./generated-client

# Python client generation  
openapi-generator generate \
  -i http://localhost:8080/openapi.json \
  -g python \
  -o ./python-client
```

## **CLI Tool for Testing:**
```bash
#!/bin/bash
# legal-ai-cli - Command line tool for testing

LEGAL_AI_BASE_URL=${LEGAL_AI_BASE_URL:-"http://localhost:8080"}

function health_check() {
    curl -s "$LEGAL_AI_BASE_URL/health" | jq .
}

function discovery_search() {
    local query="$1"
    local limit="${2:-5}"
    
    curl -s -X POST "$LEGAL_AI_BASE_URL/api/v1/search/discovery_search" \
        -H "Content-Type: application/json" \
        -d "{\"search_query\": \"$query\", \"limit\": $limit}" | jq .
}

function extract_statistics() {
    local topic="$1"
    local jurisdiction="${2:-texas}"
    
    discovery_search "$topic statistics financial data $jurisdiction" 3 | \
        jq '.entries[].fields.extracted_facts | fromjson | .[] | select(.fact | test("billion|million|\\$|%"))'
}

case "$1" in
    "health")
        health_check
        ;;
    "search")
        discovery_search "$2" "$3"
        ;;
    "stats")
        extract_statistics "$2" "$3"
        ;;
    *)
        echo "Usage: $0 {health|search <query> [limit]|stats <topic> [jurisdiction]}"
        exit 1
        ;;
esac
```

---

# 🔄 **DEPLOYMENT AND DEVOPS**

## **Docker Client Configuration:**
```dockerfile
# Dockerfile for client applications
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy application code
COPY . .

# Environment configuration
ENV LEGAL_AI_BASE_URL=http://legal-ai-api:8080
ENV NODE_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

EXPOSE 3000

CMD ["npm", "start"]
```

## **Environment Configuration:**
```bash
# .env.production
LEGAL_AI_BASE_URL=https://api.legalai.company.com
LEGAL_AI_TIMEOUT=30000
LEGAL_AI_RATE_LIMIT=100
LEGAL_AI_CACHE_TTL=300

# Monitoring
METRICS_ENDPOINT=https://metrics.company.com
LOG_LEVEL=info

# Security
ENABLE_REQUEST_LOGGING=true
AUDIT_LOG_PATH=/var/log/legal-ai/audit.log
```

---

**🎯 TECHNICAL SUMMARY**: This guide provides complete API documentation, robust client implementation patterns, comprehensive error handling, and production-ready deployment configurations for the Legal AI System.

**⚡ PERFORMANCE TARGETS**: <1000ms response times, 99.9% uptime, 100 requests/minute rate limits, with comprehensive monitoring and observability built-in.