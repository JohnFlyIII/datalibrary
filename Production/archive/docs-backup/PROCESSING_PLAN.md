# Legal Document Processing Plan

This plan outlines the steps to process the PDFs in `raw_data/` through our complete metadata pipeline.

## Overview

We'll process the documents through multiple stages:
1. **Discovery** - Quick scan and categorization
2. **Basic Processing** - Extract metadata without AI
3. **AI Enhancement** - Claude-powered fact extraction
4. **Human Review** - Expert validation and enrichment
5. **Embedding Generation** - Create vector representations
6. **Production Prep** - Package for deployment

## Pre-Processing Setup

### 1. Environment Preparation

```bash
# Navigate to Production directory
cd /Users/johnfly/develop/firmpilot/dataLibrary/Production

# Activate virtual environment (create if needed)
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements-claude.txt

# Set up environment variables
cp .env.local.example .env.local
# Edit .env.local and add your ANTHROPIC_API_KEY
```

### 2. Directory Structure Check

```bash
# Verify structure
tree -L 2 .
# Expected:
# ├── raw_data/          # Source PDFs
# ├── output/            # Processing results
# │   ├── metadata/      # Document metadata
# │   ├── chunks/        # Text chunks
# │   ├── embeddings/    # Vector embeddings
# │   └── logs/          # Processing logs
# ├── scripts/           # Processing scripts
# └── exports/           # Production packages
```

## Stage 1: Discovery & Categorization

### Quick Scan (5-10 minutes)

```bash
# Count and categorize PDFs
find raw_data -name "*.pdf" -type f | wc -l

# Group by directory/type
find raw_data -name "*.pdf" -type f | sed 's|/[^/]*$||' | sort | uniq -c

# Check file sizes
du -sh raw_data/*

# Create initial inventory
python scripts/inventory_pdfs.py --input-dir raw_data --output inventory.json
```

### Create Inventory Script

```python
# scripts/inventory_pdfs.py
import os
import json
from pathlib import Path
import hashlib

def create_inventory(input_dir):
    inventory = []
    
    for pdf_path in Path(input_dir).rglob("*.pdf"):
        rel_path = pdf_path.relative_to(input_dir)
        
        # Categorize by path
        parts = rel_path.parts
        category = parts[0] if len(parts) > 1 else "uncategorized"
        
        inventory.append({
            "filename": pdf_path.name,
            "path": str(rel_path),
            "category": category,
            "size_mb": pdf_path.stat().st_size / 1024 / 1024,
            "hash": hashlib.md5(pdf_path.read_bytes()).hexdigest()[:8]
        })
    
    return sorted(inventory, key=lambda x: x['category'])
```

## Stage 2: Basic Metadata Extraction (No AI)

### Run Quick Processing (30-60 minutes)

```bash
# Process all PDFs without AI
python scripts/quick_process.py raw_data output

# Check results
ls -la output/metadata/unreviewed/ | head -10
cat output/logs/quick_process_*.json | jq '.[] | select(.status=="success")' | wc -l
```

### Expected Output
- Basic metadata for each PDF
- Text chunks for later processing
- Processing log with success/failure status

## Stage 3: AI Enhancement with Claude

### 3.1 Test Claude Integration First

```bash
# Test on one document
python scripts/test_claude_extraction.py

# Process single PDF as test
python scripts/process_single_claude.py raw_data/sample.pdf
```

### 3.2 Batch Processing Strategy

Given API costs and rate limits, process in batches:

```bash
# Small batch test (5 documents)
python scripts/process_documents_claude.py \
  --input-dir raw_data \
  --output-dir output \
  --batch-size 5 \
  --model claude-3-sonnet-20240229

# Full processing in stages
# Option 1: By category
for category in texas federal practice_guides; do
  python scripts/process_documents_claude.py \
    --input-dir raw_data/$category \
    --output-dir output \
    --batch-size 10
done

# Option 2: By priority
# Process most important documents first
python scripts/process_priority_docs.py --config priority_list.json
```

### 3.3 Cost Estimation

```
Estimated processing with Claude 3 Sonnet:
- Average document: 50 pages = ~20k tokens
- Fact extraction + summary = ~5k tokens output
- Cost per document: ~$0.10-0.15
- 100 documents = ~$10-15 total
```

## Stage 4: Human Review

### 4.1 Review Interface

```bash
# Start review process
python scripts/review_metadata.py --metadata-dir output/metadata

# Review specific categories
python scripts/review_metadata.py \
  --metadata-dir output/metadata \
  --filter-category "texas"
```

### 4.2 Review Checklist

For each document, verify/add:
- [ ] Correct jurisdiction (country/state/city)
- [ ] Accurate practice areas (primary/secondary/specific)
- [ ] Content type classification
- [ ] Key compliance requirements
- [ ] Important deadlines
- [ ] Related documents
- [ ] Special notes or warnings

### 4.3 Bulk Enrichment

```python
# scripts/bulk_enrich.py
# Add common metadata to multiple documents
python scripts/bulk_enrich.py \
  --pattern "texas_*.json" \
  --add-jurisdiction "texas" \
  --add-practice-area "medical_malpractice"
```

## Stage 5: Embedding Generation

### Generate Embeddings (1-2 hours)

```bash
# Generate embeddings for all processed documents
python scripts/generate_embeddings.py \
  --metadata-dir output/metadata/reviewed \
  --output-dir output/embeddings \
  --model sentence-transformers/all-mpnet-base-v2

# Verify embeddings
ls -la output/embeddings/ | wc -l
```

## Stage 6: Quality Assurance

### 6.1 Validation Checks

```bash
# Run QA script
python scripts/qa_check.py --output-dir output

# Expected checks:
# - All PDFs have metadata
# - All metadata has required fields
# - Embeddings match metadata files
# - No duplicate document IDs
# - Citation formats are valid
```

### 6.2 Test Queries

```python
# Test search functionality locally
python scripts/test_search.py \
  --query "medical malpractice statute limitations texas" \
  --embeddings-dir output/embeddings \
  --metadata-dir output/metadata/reviewed
```

## Stage 7: Production Preparation

### 7.1 Final Package

```bash
# Create production export
./scripts/prepare_for_production.sh

# Verify package
python scripts/verify_export.py exports/legal_docs_export_*.tar.gz
```

### 7.2 Documentation

Create deployment notes:
```bash
cat > exports/DEPLOYMENT_NOTES.md << EOF
# Deployment Notes

## Package Contents
- Documents processed: $(find output/metadata/reviewed -name "*.json" | wc -l)
- Total size: $(du -sh output | cut -f1)
- Processing date: $(date)
- Claude model used: claude-3-sonnet-20240229

## Special Considerations
- Texas documents have enhanced jurisdiction metadata
- Medical malpractice docs include expert witness requirements
- All facts include APA 7th citations

## Import Command
\`\`\`bash
python import_metadata.py --import-dir . --collection legal_knowledge
\`\`\`
EOF
```

## Execution Timeline

### Day 1 (2-3 hours)
- [ ] Environment setup (30 min)
- [ ] Discovery & categorization (30 min)
- [ ] Basic metadata extraction (1-2 hours)

### Day 2 (4-6 hours)
- [ ] Claude API setup and testing (30 min)
- [ ] AI processing in batches (3-4 hours)
- [ ] Initial review of results (1 hour)

### Day 3 (3-4 hours)
- [ ] Human review and enrichment (2-3 hours)
- [ ] Embedding generation (1 hour)

### Day 4 (2 hours)
- [ ] Quality assurance (1 hour)
- [ ] Production packaging (30 min)
- [ ] Documentation (30 min)

## Monitoring & Troubleshooting

### Progress Tracking
```bash
# Check processing progress
tail -f output/logs/processing_*.log

# Monitor Claude API usage
grep "ai_model" output/logs/*.json | wc -l
```

### Common Issues

1. **PDF extraction fails**
   ```bash
   # Try OCR for scanned PDFs
   ocrmypdf input.pdf output.pdf
   ```

2. **Claude rate limits**
   ```bash
   # Reduce batch size
   --batch-size 5
   # Add delay between requests
   export CLAUDE_DELAY=2
   ```

3. **Memory issues with embeddings**
   ```bash
   # Process in smaller batches
   python scripts/generate_embeddings.py --batch-size 50
   ```

## Success Metrics

- ✅ 95%+ PDFs successfully processed
- ✅ All documents have extracted facts
- ✅ Human review completed for high-priority docs
- ✅ Embeddings generated for all documents
- ✅ Export package < 1GB
- ✅ Test queries return relevant results

## Next Steps

After processing:
1. Transfer to production server
2. Import into Qdrant
3. Verify search functionality
4. Set up regular update pipeline