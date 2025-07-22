# Local Preprocessing Guide with Claude

This guide walks through preprocessing your legal documents locally, creating complete metadata files ready for AWS deployment.

## What Happens Locally

Everything runs on your machine:
1. ✅ PDF text extraction
2. ✅ Document chunking
3. ✅ Basic metadata creation
4. ✅ Claude API calls for AI enhancement
5. ✅ Embedding generation
6. ✅ Final packaging

The only external connection is to Claude's API for high-quality analysis.

## Quick Start

### 1. Setup Environment

```bash
cd /Users/johnfly/develop/firmpilot/dataLibrary/Production

# Check you have PDFs
ls -la raw_data/*.pdf | head -5

# Verify Claude API key
grep ANTHROPIC_API_KEY .env.local
```

### 2. Run Complete Local Preprocessing

```bash
# Option A: Use the interactive menu
./scripts/start_processing.sh
# Select option 8 for complete pipeline

# Option B: Run directly
python scripts/process_documents_claude.py \
  --input-dir raw_data \
  --output-dir output \
  --batch-size 10
```

## Step-by-Step Process

### Step 1: Basic Extraction (No AI)
```bash
# Extract text and create basic metadata
python scripts/quick_process.py raw_data output

# This creates:
# - output/metadata/unreviewed/*.json (basic metadata)
# - output/chunks/*.json (text chunks)
# - output/logs/quick_process_*.json (processing log)
```

### Step 2: AI Enhancement with Claude
```bash
# Enhance with Claude for facts and summaries
python scripts/process_documents_claude.py \
  --input-dir raw_data \
  --output-dir output \
  --batch-size 10 \
  --model claude-3-sonnet-20240229

# This adds to each document:
# - Extracted facts with APA citations
# - Executive summary
# - Key findings
# - Summary bullet points
# - Key takeaways
```

### Step 3: Generate Embeddings Locally
```bash
# Create vector embeddings using local model
python -c "
from sentence_transformers import SentenceTransformer
import json
from pathlib import Path
from tqdm import tqdm

# Load model
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# Process each metadata file
metadata_dir = Path('output/metadata')
embeddings_dir = Path('output/embeddings')
embeddings_dir.mkdir(exist_ok=True)

for metadata_file in tqdm(list(metadata_dir.glob('*_metadata.json'))):
    with open(metadata_file) as f:
        metadata = json.load(f)
    
    # Generate embedding for summary
    text = metadata.get('executive_summary', '') + ' ' + metadata.get('title', '')
    embedding = model.encode(text).tolist()
    
    # Save embedding
    doc_id = metadata['id']
    embedding_data = {
        'doc_id': doc_id,
        'embedding': embedding,
        'model': 'all-mpnet-base-v2',
        'text_preview': text[:200]
    }
    
    with open(embeddings_dir / f'{doc_id}_embedding.json', 'w') as f:
        json.dump(embedding_data, f)

print(f'Generated embeddings for {len(list(embeddings_dir.glob(\"*.json\")))} documents')
"
```

### Step 4: Human Review (Optional but Recommended)
```bash
# Review and enrich metadata
python scripts/review_metadata.py --metadata-dir output/metadata

# Move reviewed files to separate folder
mkdir -p output/metadata/reviewed
# After review, files are automatically moved
```

### Step 5: Package for AWS
```bash
# Create deployment package
./scripts/prepare_for_production.sh

# This creates:
# - exports/legal_docs_export_TIMESTAMP.tar.gz
# - exports/transfer_legal_docs_export_TIMESTAMP.sh
```

## What You Get

After local preprocessing, each document has:

```json
{
  "id": "a1b2c3d4e5f6",
  "title": "Texas Civil Practice and Remedies Code",
  "source_filename": "texas_civil_code.pdf",
  
  // Basic metadata (local extraction)
  "content_type": "statute",
  "jurisdiction_country": "united_states",
  "jurisdiction_state": "texas",
  "total_pages": 1500,
  
  // Claude AI enhancement
  "extracted_facts": [
    {
      "fact": "The statute of limitations for personal injury is two years",
      "location": "Page 245, Section 16.003",
      "citation": "Tex. Civ. Prac. & Rem. Code § 16.003",
      "confidence": 0.95
    }
  ],
  "fact_count": 847,
  "executive_summary": "Comprehensive Texas civil procedure code...",
  "summary_bullet_points": ["Key point 1", "Key point 2"],
  "key_findings": ["Major finding 1", "Major finding 2"],
  
  // Processing metadata
  "ai_model": "claude-3-sonnet-20240229",
  "preprocessing_timestamp": "2024-01-17T10:30:00Z",
  "human_reviewed": false
}
```

## Processing Options

### Fast Test (1-2 documents)
```bash
# Test on single PDF
python scripts/process_documents_claude.py \
  --input-dir raw_data \
  --output-dir output_test \
  --batch-size 1 \
  --model claude-3-haiku-20240307  # Cheaper model
```

### Production Run (All documents)
```bash
# Full processing with Sonnet
python scripts/process_documents_claude.py \
  --input-dir raw_data \
  --output-dir output \
  --batch-size 20 \
  --model claude-3-sonnet-20240229
```

### Cost-Optimized Approach
```bash
# Step 1: Classify with Haiku (cheap)
python scripts/classify_documents.py \
  --model claude-3-haiku-20240307

# Step 2: Process important docs with Sonnet
python scripts/process_documents_claude.py \
  --input-dir raw_data/important \
  --model claude-3-sonnet-20240229

# Step 3: Process rest with Haiku
python scripts/process_documents_claude.py \
  --input-dir raw_data/standard \
  --model claude-3-haiku-20240307
```

## Monitoring Progress

```bash
# Watch processing in real-time
tail -f output/logs/processing_*.log

# Check completion status
echo "Processed: $(ls output/metadata/*.json 2>/dev/null | wc -l) documents"
echo "With embeddings: $(ls output/embeddings/*.json 2>/dev/null | wc -l)"

# View sample metadata
cat output/metadata/*_metadata.json | head -100 | jq '.'
```

## Final Package Contents

Your export package will contain:
```
legal_docs_export_20240117_150000.tar.gz
├── metadata/
│   ├── doc1_metadata.json    # Complete metadata with AI enhancement
│   ├── doc2_metadata.json
│   └── ...
├── embeddings/
│   ├── doc1_embeddings.json  # Vector embeddings
│   ├── doc2_embeddings.json
│   └── ...
├── chunks/
│   ├── doc1_chunks.json      # Text chunks for search
│   ├── doc2_chunks.json
│   └── ...
└── manifest.json             # Package metadata
```

## Ready for AWS

After preprocessing, your data is:
- ✅ Fully processed with AI enhancement
- ✅ Vector embeddings generated
- ✅ Packaged in standard format
- ✅ Ready for Qdrant import
- ✅ No further processing needed on AWS

Just transfer and import:
```bash
# Transfer to AWS
scp exports/legal_docs_export_*.tar.gz user@aws-server:/imports/

# On AWS server
tar -xzf legal_docs_export_*.tar.gz
python import_metadata.py --import-dir . --collection legal_knowledge
```

## Total Time Estimate

For 100 documents:
- Basic extraction: 30-60 minutes
- Claude enhancement: 2-3 hours
- Embedding generation: 30 minutes
- Packaging: 5 minutes
- **Total: 3-5 hours**

All happening locally on your machine!