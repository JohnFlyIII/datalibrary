# Local Processing Quick Start Guide

Get started with local document processing in 5 minutes.

## Prerequisites

1. **Python 3.8+**
2. **PDF text extraction tool**:
   ```bash
   # macOS
   brew install poppler
   
   # Ubuntu/Debian
   sudo apt-get install poppler-utils
   
   # Test installation
   pdftotext -v
   ```

## Quick Start (No AI)

### 1. Basic Processing

Process PDFs without AI (creates basic metadata and chunks):

```bash
# Clone or navigate to the project
cd /Users/johnfly/develop/firmpilot/dataLibrary/Production

# Process PDFs
python scripts/quick_process.py ./input_pdfs ./output

# Example output:
# Found 3 PDF files
# [1/3] Processing: texas_civil_code.pdf
#   ✓ Created metadata - ID: a1b2c3d4e5f6
#   ✓ Detected: statute - texas
#   ✓ Created 750 chunks
```

### 2. Prepare for Production

Package processed files for transfer:

```bash
# Create export package
./scripts/prepare_for_production.sh

# Output:
# Export package: ./exports/legal_docs_export_20240117_150234.tar.gz
# Package size: 12M
```

### 3. Transfer to Production

```bash
# Using the generated transfer script
./exports/transfer_legal_docs_export_*.sh username production.server.com /imports

# Or manually
scp ./exports/legal_docs_export_*.tar.gz user@server:/imports/
```

## Full Processing (With AI)

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install full requirements
pip install openai sentence-transformers pdfplumber tqdm python-dotenv
```

### 2. Configure API Keys

Create `.env.local`:
```bash
OPENAI_API_KEY=sk-...your-key...
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
```

### 3. Run Full Processing

```bash
# Full processing with AI
python scripts/process_documents.py --input-dir ./input_pdfs --output-dir ./output

# Review and enrich metadata
python scripts/review_metadata.py --metadata-dir ./output/metadata

# Export for production
python scripts/export_for_production.py --output-dir ./output
```

## Folder Structure

```
Production/
├── input_pdfs/          # Place your PDFs here
├── output/
│   ├── metadata/        # Document metadata
│   │   ├── unreviewed/  # Auto-generated
│   │   └── reviewed/    # Human-reviewed
│   ├── chunks/          # Text chunks
│   ├── embeddings/      # Vector embeddings
│   └── logs/           # Processing logs
├── exports/            # Export packages
└── scripts/           # Processing scripts
```

## Common Tasks

### Process Single Document
```bash
# Quick process without AI
python -c "
from scripts.quick_process import *
text = extract_text_simple(Path('document.pdf'))
metadata = create_basic_metadata(Path('document.pdf'), text)
print(json.dumps(metadata, indent=2))
"
```

### Check Processing Status
```bash
# Count processed files
find ./output/metadata -name "*.json" | wc -l

# View recent processing log
cat ./output/logs/quick_process_*.json | jq '.'
```

### Validate Before Transfer
```bash
# Check for required files
ls -la ./output/metadata/*.json | head -5
ls -la ./output/chunks/*.json | head -5

# Verify JSON validity
python -m json.tool ./output/metadata/*_metadata.json > /dev/null && echo "✓ Valid JSON"
```

## Production Import

On your production server:

```bash
# 1. Extract package
tar -xzf legal_docs_export_*.tar.gz
cd legal_docs_export_*

# 2. View import instructions
cat IMPORT_INSTRUCTIONS.md

# 3. Run import (requires Qdrant running)
python import_metadata.py --import-dir . --collection legal_knowledge

# 4. Verify import
curl http://localhost:6333/collections/legal_knowledge
```

## Troubleshooting

### PDF Text Extraction Failed
- Check if PDF is scanned (image-based)
- Try OCR: `ocrmypdf input.pdf output.pdf`
- Verify poppler installation: `which pdftotext`

### No Metadata Generated
- Check input directory has PDFs: `ls -la ./input_pdfs/`
- Check output permissions: `ls -la ./output/`
- View error logs: `grep "failed" ./output/logs/*.json`

### Transfer Issues
- Verify SSH access: `ssh user@server echo "Connected"`
- Check available space: `ssh user@server df -h`
- Use rsync for large transfers: `rsync -avz --progress ./exports/ user@server:/imports/`

## Next Steps

1. **Add AI Processing**: Set up OpenAI API for fact extraction
2. **Human Review**: Use the review script to enrich metadata
3. **Automate Pipeline**: Create cron job for regular processing
4. **Monitor Quality**: Track processing metrics and errors

## Quick Commands Reference

```bash
# Process documents (no AI)
python scripts/quick_process.py ./pdfs ./output

# Package for production
./scripts/prepare_for_production.sh

# Transfer to server
scp exports/*.tar.gz user@server:/imports/

# On production: import data
python import_metadata.py --import-dir . --collection legal_knowledge
```

---

For full documentation, see [LOCAL_METADATA_PROCESSING.md](./LOCAL_METADATA_PROCESSING.md)