# Local vs Cloud Processing Architecture

## Current Hybrid Approach

```
Local Machine                   Cloud Services              Production AWS
┌─────────────────┐            ┌─────────────────┐        ┌─────────────────┐
│ PDF Processing  │            │ Claude API      │        │                 │
│ - Text extract  │ ─────────> │ - Fact extract  │        │ Qdrant DB       │
│ - Chunking      │ <───────── │ - Summaries     │        │ (Final home)    │
│                 │            └─────────────────┘        │                 │
│ Embeddings      │                                       │                 │
│ - Local models  │                                       │                 │
│                 │                                       │                 │
│ Package Results │ ─────────────────────────────────────>│ Import Tool     │
└─────────────────┘                                       └─────────────────┘
```

## Fully Local Approach

To process **everything** locally before AWS:

### Option 1: Local LLM for Summaries

```python
# Use local LLM like Llama 2, Mistral, or Phi-2
from transformers import pipeline

# Local summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
summary = summarizer(document_text, max_length=200)

# Local fact extraction (more limited)
qa_pipeline = pipeline("question-answering")
facts = extract_facts_locally(document_text, qa_pipeline)
```

### Option 2: Pre-process for Later Cloud Enhancement

```python
# Create metadata shells locally
metadata = {
    "id": doc_id,
    "title": extract_title(pdf),
    "text_chunks": chunks,
    "basic_metadata": {...},
    
    # Placeholders for cloud processing
    "needs_ai_processing": True,
    "extracted_facts": [],
    "executive_summary": "Pending AI processing",
    "summary_bullet_points": []
}
```

## Recommended Architecture

### Phase 1: Local Preprocessing (No External APIs)
```bash
# 1. Extract and chunk text
python scripts/local_preprocess.py raw_data output

# 2. Generate basic metadata
python scripts/extract_basic_metadata.py output

# 3. Create embeddings with local models
python scripts/generate_local_embeddings.py output

# 4. Package for cloud
./scripts/package_for_cloud.py output
```

### Phase 2: Cloud Enhancement (On AWS)
```python
# On AWS server with GPU
# 1. Load preprocessed data
# 2. Run Claude/GPT for enrichment
# 3. Update Qdrant directly
```

## Comparison

| Aspect | Current Hybrid | Fully Local | Deferred Cloud |
|--------|---------------|-------------|----------------|
| **Cost** | $10-20 now | $0 | $10-20 later |
| **Time** | 2-4 hours | 1-2 hours | 1hr + 2hr later |
| **Quality** | High (Claude) | Lower (local) | High (eventual) |
| **Privacy** | Text to Claude | Fully private | Delayed exposure |
| **Resources** | Moderate | High (GPU?) | Low initially |

## Implementation for Fully Local

### 1. Create Local Processing Script

```python
# scripts/local_only_process.py
#!/usr/bin/env python3
"""
Process documents entirely locally without external APIs
"""

import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import pdfplumber
from transformers import pipeline
import spacy
from datetime import datetime

class LocalProcessor:
    def __init__(self):
        # Local models only
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.nlp = spacy.load('en_core_web_sm')
        
    def extract_facts_locally(self, text):
        """Extract facts using spaCy and rules"""
        doc = self.nlp(text)
        facts = []
        
        # Extract entities and key sentences
        for sent in doc.sents:
            # Look for sentences with legal patterns
            if any(token.text.lower() in ['must', 'shall', 'required', 'prohibited'] 
                   for token in sent):
                facts.append({
                    'fact': sent.text,
                    'type': 'requirement',
                    'confidence': 0.7
                })
                
        return facts[:20]  # Limit to top 20
        
    def generate_summary_locally(self, text):
        """Create basic summary using extractive methods"""
        # Simple extractive summary
        sentences = text.split('.')[:5]
        return {
            'executive_summary': '. '.join(sentences[:3]) + '.',
            'key_points': sentences[:5]
        }
```

### 2. Metadata for Cloud Processing

```json
{
  "id": "doc_123",
  "local_processing": {
    "completed": true,
    "timestamp": "2024-01-17T10:00:00Z",
    "version": "1.0"
  },
  "basic_metadata": {
    "title": "Texas Civil Code",
    "pages": 150,
    "text_length": 500000
  },
  "embeddings": {
    "model": "all-MiniLM-L6-v2",
    "chunks": 75,
    "dimension": 384
  },
  "ai_processing_status": {
    "required": true,
    "completed": false,
    "fields_needed": [
      "extracted_facts",
      "executive_summary",
      "key_findings",
      "compliance_requirements"
    ]
  }
}
```

## Which Approach to Use?

### Use Current Hybrid If:
- You want high-quality summaries now
- API costs ($10-20) are acceptable
- You trust Claude with your data
- You want to deploy complete data to AWS

### Use Fully Local If:
- Data is highly sensitive
- You have GPU for local LLMs
- Lower quality summaries acceptable
- You want zero external dependencies

### Use Deferred Cloud If:
- You want to prototype quickly
- Budget is tight initially
- You'll enhance data later on AWS
- You want to batch API costs

## Next Steps

1. **Continue with current hybrid** (Recommended)
   ```bash
   ./scripts/start_processing.sh
   # Choose option 4 for full processing
   ```

2. **Switch to local-only**
   ```bash
   # Need to create new scripts
   python scripts/create_local_pipeline.py
   ```

3. **Create two-phase approach**
   ```bash
   # Phase 1: Local prep
   python scripts/local_preprocess.py
   
   # Phase 2: Cloud enhance (later)
   python scripts/cloud_enhance.py
   ```