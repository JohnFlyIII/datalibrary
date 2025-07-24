# Complete Data Loading Guide

## 🚀 Full Pipeline Script

Use `full_data_pipeline.py` to process all PDFs from `raw_data/` and load them into Superlinked.

### Quick Start Options

```bash
# Process ALL PDFs and load into Superlinked (recommended for production)
python3 full_data_pipeline.py --all

# Process only 5 PDFs (for testing)  
python3 full_data_pipeline.py --limit 5

# Only AI processing (no loading)
python3 full_data_pipeline.py --limit 3 --process-only

# Only load existing processed data
python3 full_data_pipeline.py --load-only
```

## 📋 What the Pipeline Does

### Step 1: AI Processing with Claude
- Extracts facts, summaries, and metadata from PDFs
- Creates chunks with precise character positioning
- Generates JSON files in `output/metadata/` and `output/chunks/`
- **Cost**: ~$0.50-$2.00 per document depending on size

### Step 2: Document Loading
- Loads document-level data for Discovery & Exploration layers
- Uses `load_real_data.py` script
- Creates searchable document summaries

### Step 3: Chunk Loading  
- Loads chunk-level data for Deep Dive layer
- Uses `load_chunks.py` script
- Enables precise text passage search

### Step 4: Search Verification
- Tests all three search layers
- Verifies functionality across endpoints
- Reports search quality scores

## ⚙️ Prerequisites

### Environment Setup
```bash
# 1. Set your Claude API key
export ANTHROPIC_API_KEY="your-key-here"
# OR create .env.local file with key

# 2. Ensure Superlinked is running
docker compose up -d

# 3. Verify server health
curl http://localhost:8080/health
```

### Data Requirements
- PDF files in `raw_data/` directory
- Sufficient disk space (processed data ~2x PDF size)
- Network connection for AI processing

## 📊 Expected Processing Times

### Small Dataset (5-10 PDFs)
- AI Processing: 5-15 minutes
- Data Loading: 1-2 minutes  
- **Total**: ~20 minutes

### Medium Dataset (50+ PDFs)
- AI Processing: 1-3 hours
- Data Loading: 5-10 minutes
- **Total**: ~3.5 hours

### Large Dataset (200+ PDFs)
- AI Processing: 6-12 hours  
- Data Loading: 15-30 minutes
- **Total**: ~12 hours

## 💰 Cost Estimates

### Claude API Costs (per document)
- **Small docs** (5-20 pages): $0.20-$0.50
- **Medium docs** (20-50 pages): $0.50-$1.50  
- **Large docs** (50+ pages): $1.50-$3.00

### Your Current Dataset
Based on files in `raw_data/`:
```bash
# Get cost estimate
python3 -c "
import os
from pathlib import Path
pdfs = list(Path('raw_data').rglob('*.pdf'))
total_mb = sum(p.stat().st_size for p in pdfs) / 1024 / 1024
estimated_cost = len(pdfs) * 1.0  # $1 average per document
print(f'PDFs: {len(pdfs)}')
print(f'Total size: {total_mb:.1f} MB') 
print(f'Estimated cost: ${estimated_cost:.2f}')
"
```

## 🔍 Monitoring Progress

### Watch Processing Logs
```bash
# In another terminal
tail -f output/logs/processing_*.log
```

### Check Output Files
```bash
# See what's been processed
ls -la output/metadata/
ls -la output/chunks/

# Count processed files
echo "Metadata files: $(ls output/metadata/*.json | wc -l)"
echo "Chunk files: $(ls output/chunks/*.json | wc -l)"
```

## 🛠️ Troubleshooting

### Common Issues

**"ANTHROPIC_API_KEY not found"**
```bash
# Set in environment
export ANTHROPIC_API_KEY="your-key-here"

# Or create .env.local file
echo "ANTHROPIC_API_KEY=your-key-here" > .env.local
```

**"Superlinked server not healthy"**
```bash
# Restart containers
docker compose down
docker compose up -d

# Check logs
docker logs production-legal-superlinked
```

**"Processing timeout/memory errors"**
```bash
# Reduce batch size
python3 full_data_pipeline.py --limit 1  # Process one at a time
```

**"Loading failed"**
```bash
# Check processed files exist
ls output/metadata/
ls output/chunks/

# Try loading manually
python3 load_real_data.py --limit 2
python3 load_chunks.py --limit 2
```

### Recovery from Partial Processing

**Resume from where you left off:**
```bash
# Check what's already processed
ls output/metadata/ | wc -l

# If you have 10 processed files, skip them:
# (Note: Current script doesn't have skip functionality yet)
# For now, move processed files to backup and re-run
```

## 📈 Performance Optimization

### For Large Datasets
```bash
# Process in smaller batches
python3 full_data_pipeline.py --limit 10 --process-only
python3 full_data_pipeline.py --limit 10 --process-only  # Next batch
# ... continue until all processed
python3 full_data_pipeline.py --load-only  # Load everything
```

### Parallel Processing (Advanced)
```bash
# Split PDFs into subdirectories and run multiple processes
# (Requires manual setup - not automated yet)
```

## ✅ Verification After Loading

### Test All Search Layers
```bash
# Run comprehensive test
./test_layered_search.sh

# Or test individual endpoints
curl -X POST http://localhost:8080/api/v1/search/discovery_search \
  -H "Content-Type: application/json" \
  -d '{"search_query": "your search term", "limit": 5}'
```

### Check Data Quality
```bash
# View sample loaded data
python3 -c "
import requests
r = requests.post('http://localhost:8080/api/v1/search/deep_dive_precise', 
                  json={'search_query': 'legal', 'limit': 3})
print('Chunks found:', len(r.json().get('entries', [])))
for entry in r.json().get('entries', [])[:2]:
    print('ID:', entry['id'])
    print('Score:', entry['metadata']['score'])
    print()
"
```

## 🎯 Next Steps After Loading

1. **Test search quality** with your specific legal terms
2. **Deploy to AWS** for production use  
3. **Scale testing** with larger datasets
4. **Add monitoring** and alerting
5. **Implement caching** for frequently accessed content

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review container logs: `docker logs production-legal-superlinked`
3. Verify environment variables and API keys
4. Test with smaller datasets first (`--limit 1`)