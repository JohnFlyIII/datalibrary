# Legal Knowledge System

A comprehensive legal document ingestion, vectorization, and search platform built with Superlinked, optimized for medical malpractice and multi-practice legal research.

## 🏛️ Overview

The Legal Knowledge System provides advanced vector-based search capabilities for legal documents, with specialized support for:

- **Medical Malpractice Cases** - Comprehensive schema for injury types, medical complexity, expert witnesses
- **Multi-Practice Support** - Immigration, family law, criminal law, business law, and more
- **Directory-Based Ingestion** - Automated processing of PDF, DOCX, and text files
- **Metadata Inheritance** - Directory-level defaults with file-specific overrides
- **Authority Weighting** - Prioritize primary sources and cited materials
- **Recency Scoring** - Balance historical precedent with recent developments

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.10+ 
- 8GB+ RAM recommended

### 1-Command Deployment

```bash
# Deploy and test the complete system
./deploy_and_test.sh
```

This script will:
- Start all services (Qdrant, Redis, GROBID, Superlinked, API, UI)
- Create sample medical malpractice test data
- Ingest documents and verify search functionality
- Provide usage examples and system status

### Manual Deployment

```bash
# Start all services
docker-compose -f legal-docker-compose.yml up -d

# Check service health
docker-compose -f legal-docker-compose.yml ps

# Access the system
open http://localhost:3000  # Web UI
open http://localhost:8000/docs  # API Documentation
open http://localhost:8080/docs  # Vector Search API
```

## 📁 Directory-Based Document Ingestion

### Setup for Medical Malpractice

1. **Create your document directory:**
```bash
mkdir -p medical_malpractice_docs/2024_cases
```

2. **Add directory-level metadata:**
```json
// medical_malpractice_docs/metadata.json
{
  "practice_area": "personal_injury",
  "jurisdiction": "california",
  "authority_level": "primary",
  "document_type": "case_law",
  "injury_type": "medical_malpractice",
  "liability_theory": "negligence",
  "medical_treatment": "long_term",
  "trial_readiness": "complex_litigation",
  "source_attribution": "Superior Court of California"
}
```

3. **Add file-specific metadata (optional):**
```json
// medical_malpractice_docs/case_123.pdf.metadata.json
{
  "case_number": "CV-2024-001234",
  "injury_severity": "catastrophic", 
  "body_parts_affected": ["spine", "neurological"],
  "medical_specialty": "neurosurgery",
  "expert_witnesses_needed": ["medical_expert", "economic_expert"],
  "special_damages": ["medical_bills", "lost_wages", "future_care"]
}
```

4. **Ingest documents:**
```bash
python3 legal_directory_ingester.py ingest \
  --directory medical_malpractice_docs \
  --practice-area personal_injury \
  --recursive
```

## 🔍 Search and Research

### Web Interface
Access the full-featured web interface at `http://localhost:3000`:
- **Legal Research** - Comprehensive document search
- **Authoritative Sources** - High-authority legal precedents  
- **Recent Developments** - Latest legal updates and changes

### API Examples

**Comprehensive Legal Search:**
```bash
curl -X POST http://localhost:8000/api/v1/search/legal \
  -H "Content-Type: application/json" \
  -d '{
    "query": "spinal surgery medical malpractice",
    "limit": 20,
    "authority_weight": 0.9,
    "recency_weight": 0.4
  }'
```

**Authority-Weighted Search:**
```bash
curl -X POST http://localhost:8000/api/v1/search/authority \
  -H "Content-Type: application/json" \
  -d '{
    "query": "surgical standard of care",
    "min_authority_score": 0.8
  }'
```

**Recent Developments:**
```bash
curl -X POST http://localhost:8000/api/v1/search/recent \
  -H "Content-Type: application/json" \
  -d '{
    "query": "medical malpractice legislation",
    "days_back": 90
  }'
```

## 🏗️ System Architecture

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

## 📊 Medical Malpractice Schema

The system includes comprehensive schemas for medical malpractice cases:

### Core Fields
- **Injury Classification**: Type, severity, body parts affected
- **Medical Context**: Specialty, treatment complexity, records volume
- **Liability Analysis**: Theory, causation complexity, comparative fault
- **Economic Impact**: Lost wages, earning capacity, special damages
- **Expert Requirements**: Medical experts, economic experts, life care planners
- **Case Management**: Trial readiness, statute of limitations

### Example Document Structure
```json
{
  "id": "med_mal_case_001",
  "title": "Surgical Malpractice - Spinal Procedure",
  "practice_area": "personal_injury",
  "injury_type": "medical_malpractice",
  "injury_severity": "catastrophic",
  "body_parts_affected": ["spine", "neurological"],
  "medical_specialty": "neurosurgery",
  "liability_theory": "negligence",
  "medical_treatment": "long_term",
  "expert_witnesses_needed": ["medical_expert", "economic_expert"],
  "trial_readiness": "complex_litigation"
}
```

## 🛠️ CLI Tools

### Directory Ingester
```bash
# Test connection
python3 legal_directory_ingester.py test

# Create sample metadata
python3 legal_directory_ingester.py create-samples --directory ./sample_docs

# Dry run (see what would be processed)
python3 legal_directory_ingester.py ingest --directory ./docs --dry-run

# Full ingestion
python3 legal_directory_ingester.py ingest \
  --directory ./legal_docs \
  --practice-area personal_injury \
  --recursive \
  --verbose
```

### Monitoring
```bash
# View service logs
docker-compose -f legal-docker-compose.yml logs -f legal-superlinked

# Check Qdrant collections
curl http://localhost:6333/collections

# Monitor Redis usage
docker-compose -f legal-docker-compose.yml exec redis redis-cli info memory

# System health check
curl http://localhost:8000/api/v1/health
```

## 📚 Practice Areas Supported

- **Personal Injury** (Medical Malpractice optimized)
- **Immigration Law** (K-1, H-1B, EB-5, Asylum)
- **Family Law** (Custody, Divorce, Support)
- **Criminal Law** (Defense, Appeals)
- **Business Law** (Corporate, Contract)
- **Real Estate Law** (Transactions, Disputes)
- **Employment Law** (Discrimination, Wrongful Termination)
- **Estate Planning** (Wills, Trusts, Probate)

## 🔧 Configuration

### Environment Variables
Key configuration options in `.env.legal`:

```bash
# Practice Areas
DEFAULT_PRACTICE_AREAS=personal_injury,immigration_law,family_law

# Authority Levels  
AUTHORITY_LEVELS=primary,secondary,tertiary

# Model Configuration
EMBEDDING_MODEL_PRIMARY=sentence-transformers/all-mpnet-base-v2
EMBEDDING_MODEL_SECONDARY=Alibaba-NLP/gte-large-en-v1.5

# Content Generation
BLOG_POST_MIN_AUTHORITY_SCORE=0.7
SEO_KEYWORD_EXTRACTION=true
```

### Superlinked Configuration
The system uses advanced vector spaces for legal document search:
- **Content Similarity** - Semantic matching of document text
- **Practice Area Categorization** - Legal domain classification
- **Authority Scoring** - Primary/secondary source weighting
- **Recency Weighting** - Time-based relevance scoring
- **Citation Analysis** - Reference popularity scoring

## 🚀 Production Deployment

### Scaling
```bash
# Scale Superlinked instances
docker-compose -f legal-docker-compose.yml up -d --scale legal-superlinked=3

# Increase memory limits
export GROBID_JAVA_OPTIONS="-Xmx4g"
export QDRANT_MEMORY_LIMIT="2g"
```

### Security
- PII anonymization enabled by default
- GDPR compliance features
- 7-year data retention policy
- CORS protection for web interface

## 🧪 Testing

The deployment script includes comprehensive tests:
- Service health checks
- Document ingestion verification  
- Search functionality validation
- API endpoint testing
- Sample data creation and processing

## 📖 Documentation

- **API Documentation**: `http://localhost:8000/docs`
- **Vector Search API**: `http://localhost:8080/docs` 
- **System Quickstart**: [`LEGAL_SYSTEM_QUICKSTART.md`](LEGAL_SYSTEM_QUICKSTART.md)
- **Schema Reference**: [`docs/samplesClasses.md`](docs/samplesClasses.md)

## 🐛 Troubleshooting

### Common Issues

**Superlinked Server Won't Start:**
```bash
# Check model downloads
docker-compose -f legal-docker-compose.yml exec legal-superlinked ls -la /app/model_cache/

# Verify configuration
docker-compose -f legal-docker-compose.yml exec legal-superlinked python -c "import superlinked_app.app as app"
```

**Qdrant Connection Issues:**
```bash
# Test connection
curl http://localhost:6333/collections

# Restart with fresh data
docker-compose -f legal-docker-compose.yml down qdrant
docker volume rm legal_qdrant_data
docker-compose -f legal-docker-compose.yml up -d qdrant
```

**Complete Reset:**
```bash
docker-compose -f legal-docker-compose.yml down -v
docker system prune -f
docker-compose -f legal-docker-compose.yml up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Superlinked** - Vector search framework
- **Qdrant** - Vector database
- **GROBID** - PDF text extraction
- **FastAPI** - API framework
- **React** - Web interface

---

**Ready to revolutionize legal research!** 🏛️⚖️

For support or questions, please open an issue or contact the development team.