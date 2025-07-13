# Legal Knowledge System - Quick Start Guide

## 🚀 Quick Deployment

### Prerequisites
- Docker & Docker Compose
- 8GB+ RAM recommended
- Python 3.10+ (for development)

### 1. Start the System
```bash
# Clone or navigate to your project directory
cd /path/to/your/legal-knowledge-system

# Start all services
docker-compose -f legal-docker-compose.yml up -d

# Check service health
docker-compose -f legal-docker-compose.yml ps
```

### 2. Verify Services
```bash
# Qdrant Vector Database
curl http://localhost:6333/collections

# Superlinked Server API
curl http://localhost:8080/docs

# Legal Research API  
curl http://localhost:8000/docs

# Redis Cache
docker-compose exec redis redis-cli ping

# GROBID PDF Processing
curl http://localhost:8070/api/isalive
```

### 3. Ingest Your First Legal Document
```bash
curl -X POST "http://localhost:8080/ingest/legal_document_source" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "immigration_guide_001",
    "title": "Complete Guide to K-1 Visa Applications",
    "content_text": "The K-1 visa allows foreign nationals to enter the United States for the purpose of marrying a U.S. citizen...",
    "practice_area": "immigration_law",
    "jurisdiction": "federal", 
    "authority_level": "primary",
    "document_type": "guide",
    "publication_date": 1720656000,
    "author": "Immigration Law Center",
    "citations": ["8 CFR 214.2(k)", "INA 101(a)(15)(K)"],
    "keywords": ["K-1 visa", "fiancé visa", "immigration"],
    "summary": "Comprehensive guide for K-1 visa applications",
    "authority_score": 0.85,
    "relevance_score": 0.9,
    "citation_count": 15,
    "source_url": "https://example.com/k1-guide",
    "pdf_path": "/docs/k1_guide.pdf",
    "word_count": 3500
  }'
```

### 4. Search Legal Documents
```bash
# General legal research
curl -X POST "http://localhost:8080/query/legal_research_query" \
  -H "Content-Type: application/json" \
  -d '{
    "search_query": "K-1 visa requirements",
    "content_weight": 1.0,
    "authority_weight": 0.9,
    "recency_weight": 0.6,
    "limit": 10
  }'

# Authority-focused search
curl -X POST "http://localhost:8080/query/authority_query" \
  -H "Content-Type: application/json" \
  -d '{
    "search_query": "immigration law updates",
    "authority_weight": 1.5,
    "citation_weight": 1.2,
    "limit": 5
  }'
```

## 🎯 Available Query Types

### 1. **legal_research_query** - Comprehensive Legal Research
- Balanced weighting across content, authority, recency
- Best for general legal research

### 2. **authority_query** - Authoritative Sources Only
- Heavy weighting on authority and citations
- Best for citing reliable sources

### 3. **practice_area_query** - Quick Practice Area Search
- Fast lookup within specific legal areas
- Best for quick references

### 4. **content_gap_query** - Content Opportunity Analysis
- Identifies underrepresented topics
- Best for blog post/content planning

### 5. **recent_developments_query** - Latest Legal Updates
- Heavy recency weighting
- Best for staying current

## 📊 Service Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Legal UI      │    │   Legal API     │    │ Legal Research  │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   Database      │
│   Port: 3000    │    │   Port: 8000    │    │   (PostgreSQL)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Legal Superlinked│    │     Qdrant      │    │      Redis      │
│ Vector Search   │◄──►│ Vector Database │    │     Cache       │
│   Port: 8080    │    │   Port: 6333    │    │   Port: 6379    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │     GROBID      │
                       │ PDF Processing  │
                       │   Port: 8070    │
                       └─────────────────┘
```

## 🔧 Development Workflow

### Local Development
```bash
# Start only infrastructure services
docker-compose -f legal-docker-compose.yml up -d qdrant redis postgres grobid

# Run Superlinked locally
cd legal_superlinked_config
python -m superlinked.server

# Run API locally
cd api
uvicorn app.main:app --reload --port 8000

# Run UI locally  
cd ui
npm start
```

### Adding New Legal Documents
```python
import asyncio
from legal_api_examples import LegalKnowledgeAPI

async def add_document():
    api = LegalKnowledgeAPI()
    
    document = {
        "id": "unique_doc_id",
        "title": "Document Title",
        "content_text": "Full document content...",
        "practice_area": "immigration_law",  # See .env.legal for valid areas
        "jurisdiction": "federal",
        "authority_level": "primary",        # primary, secondary, tertiary
        "document_type": "case_law",         # case_law, statute, regulation, etc.
        "publication_date": int(datetime.now().timestamp()),
        "author": "Author Name",
        "citations": ["Citation 1", "Citation 2"],
        "keywords": ["keyword1", "keyword2"],
        "summary": "Brief summary",
        "authority_score": 0.85,             # 0.0-1.0
        "relevance_score": 0.9,              # 0.0-1.0  
        "citation_count": 25,
        "source_url": "https://source.com",
        "pdf_path": "/path/to/pdf",
        "word_count": 2500
    }
    
    result = await api.ingest_legal_document(document)
    print(f"Ingested: {result}")

# Run it
asyncio.run(add_document())
```

## 📈 Performance Optimization

### Production Settings
```bash
# Increase memory limits
export GROBID_JAVA_OPTIONS="-Xmx4g"
export QDRANT_MEMORY_LIMIT="2g"

# Scale Superlinked instances
docker-compose -f legal-docker-compose.yml up -d --scale legal-superlinked=3

# Enable model caching
export TRANSFORMERS_CACHE="/persistent/model/cache"
```

### Monitoring
```bash
# Check Qdrant collections
curl http://localhost:6333/collections

# Monitor Redis usage
docker-compose exec redis redis-cli info memory

# Check Superlinked health
curl http://localhost:8080/docs

# View service logs
docker-compose -f legal-docker-compose.yml logs -f legal-superlinked
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Superlinked Server Won't Start
```bash
# Check model downloads
docker-compose exec legal-superlinked ls -la /app/model_cache/

# Verify configuration
docker-compose exec legal-superlinked python -c "import superlinked_app.app as app"

# Check environment variables
docker-compose exec legal-superlinked env | grep QDRANT
```

#### 2. Qdrant Connection Issues
```bash
# Test Qdrant connection
curl http://localhost:6333/collections

# Check Qdrant logs
docker-compose logs qdrant

# Restart Qdrant with fresh data
docker-compose down qdrant
docker volume rm legal_qdrant_data
docker-compose up -d qdrant
```

#### 3. Model Download Issues
```bash
# Pre-download models manually
docker-compose exec legal-superlinked python -c "
from sentence_transformers import SentenceTransformer
SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
SentenceTransformer('Alibaba-NLP/gte-large-en-v1.5')
"
```

### Reset Everything
```bash
# Complete reset
docker-compose -f legal-docker-compose.yml down -v
docker system prune -f
docker-compose -f legal-docker-compose.yml up -d
```

## 📚 Next Steps

1. **Customize Schema**: Edit `legal_superlinked_config/app.py` to add legal domain-specific fields
2. **Add Data Sources**: Integrate with legal databases, case law APIs, regulation feeds
3. **Build UI**: Create React components for legal research interface
4. **Content Pipeline**: Set up automated content ingestion from legal publications
5. **SEO Integration**: Connect to content management systems for blog generation

## 🔗 Useful Links

- **Superlinked Docs**: https://docs.superlinked.com/
- **Qdrant Docs**: https://qdrant.tech/documentation/
- **API Documentation**: http://localhost:8080/docs (when running)
- **Legal System Config**: `legal_superlinked_config/app.py`
- **Docker Compose**: `legal-docker-compose.yml`

## 💡 Pro Tips

1. **Use specific practice areas** in queries for better results
2. **Combine authority and recency weights** for balanced research
3. **Monitor Qdrant dashboard** for performance insights
4. **Cache frequent queries** using Redis for faster response times
5. **Batch document ingestion** for better performance

Happy legal researching! 🏛️⚖️