# Local Metadata Processing Guide

This guide explains how to process legal documents locally to create metadata, and then transfer the processed data to your production server.

## Table of Contents
1. [Overview](#overview)
2. [Local Setup](#local-setup)
3. [Processing Pipeline](#processing-pipeline)
4. [Data Export](#data-export)
5. [Transfer to Production](#transfer-to-production)
6. [Verification](#verification)

## Overview

Processing documents locally allows you to:
- Use local GPU resources for faster processing
- Review and validate metadata before production deployment
- Process sensitive documents without uploading raw files
- Batch process documents during off-hours

### Architecture

```
Local Machine                      Production Server
┌─────────────────┐               ┌─────────────────┐
│ PDF Documents   │               │                 │
│       ↓         │               │   Qdrant DB     │
│ AI Processing   │               │       ↑         │
│       ↓         │               │   Import Tool   │
│ Metadata JSON   │ ──────────>   │       ↑         │
│       ↓         │   Transfer    │  Metadata JSON  │
│ Embeddings      │               │                 │
└─────────────────┘               └─────────────────┘
```

## Local Setup

### 1. Install Requirements

Create a local processing environment:

```bash
# Create virtual environment
python -m venv legal_processing_env
source legal_processing_env/bin/activate  # On Windows: legal_processing_env\Scripts\activate

# Install requirements
pip install -r requirements-local.txt
```

Create `requirements-local.txt`:
```txt
# Core processing
pdfplumber==0.9.0
pypdf2==3.0.1
pytesseract==0.3.10

# AI/ML
openai==1.3.0
sentence-transformers==2.2.2
torch==2.1.0

# Data handling
pandas==2.1.0
numpy==1.24.3
jsonlines==4.0.0

# Utilities
tqdm==4.66.1
python-dotenv==1.0.0
click==8.1.7
```

### 2. Configure Environment

Create `.env.local`:
```bash
# API Keys
OPENAI_API_KEY=your_api_key_here

# Processing Settings
CHUNK_SIZE=2000
CHUNK_OVERLAP=200
BATCH_SIZE=10

# Model Settings
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
EXTRACTION_MODEL=gpt-4-turbo
SUMMARY_MODEL=gpt-4-turbo

# Output Settings
OUTPUT_DIR=./processed_data
TEMP_DIR=./temp
```

### 3. Directory Structure

Create the following structure:
```
local_processing/
├── input/              # Place PDFs here
├── output/             # Processed metadata
│   ├── metadata/       # JSON metadata files
│   ├── embeddings/     # Vector embeddings
│   └── logs/          # Processing logs
├── scripts/           # Processing scripts
├── config/            # Configuration files
└── temp/              # Temporary files
```

## Processing Pipeline

### 1. Main Processing Script

Create `scripts/process_documents.py`:

```python
#!/usr/bin/env python3
"""
Local Document Processing Pipeline

Processes legal documents to extract metadata, facts, and generate embeddings.
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import click
import pdfplumber
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

# Initialize models
embedding_model = SentenceTransformer(os.getenv('EMBEDDING_MODEL'))
openai.api_key = os.getenv('OPENAI_API_KEY')

class DocumentProcessor:
    """Process legal documents locally"""
    
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.metadata_dir = self.output_dir / "metadata"
        self.embeddings_dir = self.output_dir / "embeddings"
        self.logs_dir = self.output_dir / "logs"
        
        for dir in [self.metadata_dir, self.embeddings_dir, self.logs_dir]:
            dir.mkdir(exist_ok=True)
            
        # Initialize processing log
        self.log_file = self.logs_dir / f"processing_{datetime.now():%Y%m%d_%H%M%S}.log"
        
    def process_pdf(self, pdf_path: Path) -> Dict:
        """Process a single PDF file"""
        print(f"\nProcessing: {pdf_path.name}")
        
        # Generate document ID
        doc_id = self._generate_doc_id(pdf_path)
        
        # Extract text
        text = self._extract_text(pdf_path)
        
        # Create chunks
        chunks = self._create_chunks(text)
        
        # Extract metadata
        metadata = self._extract_metadata(pdf_path, text, doc_id)
        
        # AI processing
        facts = self._extract_facts(text)
        summary = self._generate_summary(text)
        
        # Update metadata
        metadata.update({
            'extracted_facts': facts['facts'],
            'fact_count': facts['count'],
            'executive_summary': summary['executive_summary'],
            'summary_bullet_points': summary['bullet_points'],
            'summary_conclusion': summary['conclusion'],
            'preprocessing_timestamp': datetime.now().isoformat(),
            'preprocessing_version': '1.0'
        })
        
        # Generate embeddings
        embeddings = self._generate_embeddings(chunks, metadata)
        
        # Save results
        self._save_metadata(doc_id, metadata)
        self._save_embeddings(doc_id, embeddings)
        
        # Log processing
        self._log_processing(doc_id, pdf_path, len(chunks))
        
        return {
            'doc_id': doc_id,
            'metadata': metadata,
            'chunks': len(chunks),
            'status': 'success'
        }
    
    def _generate_doc_id(self, pdf_path: Path) -> str:
        """Generate unique document ID"""
        content = f"{pdf_path.name}_{pdf_path.stat().st_size}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _extract_text(self, pdf_path: Path) -> str:
        """Extract text from PDF"""
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    
    def _create_chunks(self, text: str) -> List[Dict]:
        """Create text chunks with overlap"""
        chunk_size = int(os.getenv('CHUNK_SIZE', 2000))
        overlap = int(os.getenv('CHUNK_OVERLAP', 200))
        
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            
            chunks.append({
                'chunk_index': chunk_index,
                'text': chunk_text,
                'start_char': start,
                'end_char': min(end, len(text))
            })
            
            start = end - overlap
            chunk_index += 1
            
        return chunks
    
    def _extract_metadata(self, pdf_path: Path, text: str, doc_id: str) -> Dict:
        """Extract basic metadata"""
        # Detect jurisdiction and practice area from filename/content
        filename = pdf_path.stem.lower()
        
        # Basic detection (enhance this based on your needs)
        jurisdiction_state = None
        if 'texas' in filename or 'tx' in filename:
            jurisdiction_state = 'texas'
        elif 'california' in filename or 'ca' in filename:
            jurisdiction_state = 'california'
            
        return {
            'id': doc_id,
            'title': pdf_path.stem.replace('_', ' ').title(),
            'source_filename': pdf_path.name,
            'file_size_bytes': pdf_path.stat().st_size,
            'jurisdiction_country': 'united_states',
            'jurisdiction_state': jurisdiction_state,
            'content_type': 'statute' if 'code' in filename else 'unknown',
            'processed_date': datetime.now().isoformat(),
            'total_pages': text.count('\n\n'),  # Rough estimate
            'total_chars': len(text)
        }
    
    def _extract_facts(self, text: str) -> Dict:
        """Extract facts using AI"""
        # Limit text for API
        sample_text = text[:8000]
        
        prompt = f"""
        Extract key legal facts from this document. For each fact:
        1. State the fact clearly and concisely
        2. Provide the location (page or section reference)
        3. Add relevant context keywords
        
        Format as JSON array with objects containing: fact, location, context, confidence
        
        Text: {sample_text}
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=os.getenv('EXTRACTION_MODEL'),
                messages=[
                    {"role": "system", "content": "You are a legal fact extraction expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            facts_data = json.loads(response.choices[0].message.content)
            return {
                'facts': facts_data,
                'count': len(facts_data)
            }
        except Exception as e:
            print(f"Error extracting facts: {e}")
            return {'facts': [], 'count': 0}
    
    def _generate_summary(self, text: str) -> Dict:
        """Generate executive summary"""
        # Limit text for API
        sample_text = text[:10000]
        
        prompt = f"""
        Create an executive summary for this legal document:
        
        1. Executive summary (1 paragraph, max 200 words)
        2. Key bullet points (5-8 bullets)
        3. Brief conclusion (1-2 sentences)
        
        Format as JSON with keys: executive_summary, bullet_points, conclusion
        
        Text: {sample_text}
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=os.getenv('SUMMARY_MODEL'),
                messages=[
                    {"role": "system", "content": "You are a legal document summarization expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error generating summary: {e}")
            return {
                'executive_summary': '',
                'bullet_points': [],
                'conclusion': ''
            }
    
    def _generate_embeddings(self, chunks: List[Dict], metadata: Dict) -> List[Dict]:
        """Generate embeddings for chunks"""
        embeddings = []
        
        for chunk in tqdm(chunks, desc="Generating embeddings"):
            # Combine chunk text with metadata for richer embeddings
            enriched_text = f"""
            Title: {metadata.get('title', '')}
            Type: {metadata.get('content_type', '')}
            Jurisdiction: {metadata.get('jurisdiction_state', '')}
            
            Content: {chunk['text'][:1000]}
            """
            
            # Generate embedding
            embedding = embedding_model.encode(enriched_text).tolist()
            
            embeddings.append({
                'chunk_index': chunk['chunk_index'],
                'embedding': embedding,
                'metadata': {
                    'doc_id': metadata['id'],
                    'chunk_size': len(chunk['text'])
                }
            })
            
        return embeddings
    
    def _save_metadata(self, doc_id: str, metadata: Dict):
        """Save metadata to JSON"""
        output_path = self.metadata_dir / f"{doc_id}_metadata.json"
        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _save_embeddings(self, doc_id: str, embeddings: List[Dict]):
        """Save embeddings to JSON"""
        output_path = self.embeddings_dir / f"{doc_id}_embeddings.json"
        with open(output_path, 'w') as f:
            json.dump(embeddings, f, indent=2)
    
    def _log_processing(self, doc_id: str, pdf_path: Path, num_chunks: int):
        """Log processing details"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'doc_id': doc_id,
            'filename': pdf_path.name,
            'chunks': num_chunks,
            'status': 'completed'
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

@click.command()
@click.option('--input-dir', default='./input', help='Directory containing PDFs')
@click.option('--output-dir', default='./output', help='Output directory')
@click.option('--batch-size', default=10, help='Batch size for processing')
def main(input_dir: str, output_dir: str, batch_size: int):
    """Process legal documents locally"""
    processor = DocumentProcessor(output_dir)
    
    # Find all PDFs
    input_path = Path(input_dir)
    pdf_files = list(input_path.glob('*.pdf'))
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    # Process in batches
    results = []
    for i in range(0, len(pdf_files), batch_size):
        batch = pdf_files[i:i+batch_size]
        print(f"\nProcessing batch {i//batch_size + 1}/{(len(pdf_files) + batch_size - 1)//batch_size}")
        
        for pdf_path in batch:
            try:
                result = processor.process_pdf(pdf_path)
                results.append(result)
            except Exception as e:
                print(f"Error processing {pdf_path.name}: {e}")
                results.append({
                    'doc_id': None,
                    'filename': pdf_path.name,
                    'status': 'failed',
                    'error': str(e)
                })
    
    # Summary
    print("\n" + "="*60)
    print("Processing Complete!")
    print(f"Successfully processed: {sum(1 for r in results if r['status'] == 'success')}")
    print(f"Failed: {sum(1 for r in results if r['status'] == 'failed')}")
    print(f"Output directory: {output_dir}")

if __name__ == "__main__":
    main()
```

### 2. Human Review Script

Create `scripts/review_metadata.py`:

```python
#!/usr/bin/env python3
"""
Human Review Interface for Metadata

Allows human experts to review and enrich automatically generated metadata.
"""

import json
from pathlib import Path
from datetime import datetime
import click

class MetadataReviewer:
    """Interactive metadata review tool"""
    
    def __init__(self, metadata_dir: str):
        self.metadata_dir = Path(metadata_dir)
        self.reviewed_dir = self.metadata_dir / "reviewed"
        self.reviewed_dir.mkdir(exist_ok=True)
        
    def review_file(self, metadata_file: Path):
        """Review a single metadata file"""
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
            
        print("\n" + "="*60)
        print(f"Document: {metadata.get('title', 'Unknown')}")
        print(f"ID: {metadata.get('id', 'Unknown')}")
        print(f"Type: {metadata.get('content_type', 'Unknown')}")
        print(f"Jurisdiction: {metadata.get('jurisdiction_state', 'Unknown')}")
        print("="*60)
        
        # Display current metadata
        print("\nCurrent Metadata:")
        print(f"  Facts extracted: {metadata.get('fact_count', 0)}")
        print(f"  Summary: {metadata.get('executive_summary', '')[:200]}...")
        
        # Review options
        while True:
            print("\nReview Options:")
            print("1. Add practice areas")
            print("2. Correct jurisdiction")
            print("3. Add compliance requirements")
            print("4. Add key deadlines")
            print("5. Add related documents")
            print("6. Mark as reviewed")
            print("7. Skip to next")
            
            choice = input("\nSelect option (1-7): ")
            
            if choice == '1':
                self._add_practice_areas(metadata)
            elif choice == '2':
                self._correct_jurisdiction(metadata)
            elif choice == '3':
                self._add_compliance_requirements(metadata)
            elif choice == '4':
                self._add_deadlines(metadata)
            elif choice == '5':
                self._add_related_documents(metadata)
            elif choice == '6':
                self._mark_reviewed(metadata, metadata_file)
                break
            elif choice == '7':
                break
    
    def _add_practice_areas(self, metadata: Dict):
        """Add practice area information"""
        print("\nCurrent practice areas:", metadata.get('practice_areas', []))
        
        primary = input("Primary practice area: ")
        secondary = input("Secondary practice area: ")
        specific = input("Specific topics (comma-separated): ")
        
        metadata['practice_area_primary'] = primary
        metadata['practice_area_secondary'] = secondary
        metadata['practice_area_specific'] = [s.strip() for s in specific.split(',')]
        
    def _correct_jurisdiction(self, metadata: Dict):
        """Correct jurisdiction information"""
        country = input("Country (e.g., united_states): ")
        state = input("State (e.g., texas): ")
        city = input("City (optional): ")
        
        metadata['jurisdiction_country'] = country
        metadata['jurisdiction_state'] = state
        if city:
            metadata['jurisdiction_city'] = city
            
    def _add_compliance_requirements(self, metadata: Dict):
        """Add compliance requirements"""
        requirements = []
        print("\nEnter compliance requirements (empty line to finish):")
        
        while True:
            req = input("Requirement: ")
            if not req:
                break
            requirements.append(req)
            
        metadata['compliance_requirements'] = requirements
        
    def _add_deadlines(self, metadata: Dict):
        """Add important deadlines"""
        deadlines = []
        print("\nEnter deadlines/timeframes (empty line to finish):")
        
        while True:
            deadline = input("Deadline (e.g., '60 days - file notice'): ")
            if not deadline:
                break
            deadlines.append(deadline)
            
        metadata['deadlines_timeframes'] = deadlines
        
    def _add_related_documents(self, metadata: Dict):
        """Add related document references"""
        related = input("\nRelated documents (comma-separated): ")
        metadata['related_documents'] = [r.strip() for r in related.split(',')]
        
    def _mark_reviewed(self, metadata: Dict, original_file: Path):
        """Mark as reviewed and save"""
        metadata['human_reviewed'] = True
        metadata['review_date'] = datetime.now().isoformat()
        metadata['reviewer'] = input("Your name: ")
        
        # Save reviewed version
        output_file = self.reviewed_dir / original_file.name
        with open(output_file, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        print(f"\nSaved reviewed metadata to: {output_file}")

@click.command()
@click.option('--metadata-dir', default='./output/metadata', help='Metadata directory')
def main(metadata_dir: str):
    """Review and enrich metadata"""
    reviewer = MetadataReviewer(metadata_dir)
    
    # Find unreviewed files
    metadata_files = list(Path(metadata_dir).glob('*_metadata.json'))
    reviewed_files = {f.name for f in (Path(metadata_dir) / 'reviewed').glob('*.json')}
    
    unreviewed = [f for f in metadata_files if f.name not in reviewed_files]
    
    print(f"Found {len(unreviewed)} unreviewed files")
    
    for file in unreviewed:
        reviewer.review_file(file)
        
        if input("\nContinue to next file? (y/n): ").lower() != 'y':
            break
    
    print("\nReview session complete!")

if __name__ == "__main__":
    main()
```

## Data Export

### 1. Export Script

Create `scripts/export_for_production.py`:

```python
#!/usr/bin/env python3
"""
Export processed data for production deployment
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
import tarfile
import click

@click.command()
@click.option('--output-dir', default='./output', help='Output directory')
@click.option('--export-name', default='export', help='Export package name')
def export_data(output_dir: str, export_name: str):
    """Create export package for production"""
    output_path = Path(output_dir)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    export_filename = f"{export_name}_{timestamp}.tar.gz"
    
    # Create manifest
    manifest = {
        'export_timestamp': datetime.now().isoformat(),
        'version': '1.0',
        'contents': {
            'metadata_files': 0,
            'embedding_files': 0,
            'total_documents': 0
        }
    }
    
    # Count files
    metadata_files = list((output_path / 'metadata' / 'reviewed').glob('*.json'))
    embedding_files = list((output_path / 'embeddings').glob('*.json'))
    
    manifest['contents']['metadata_files'] = len(metadata_files)
    manifest['contents']['embedding_files'] = len(embedding_files)
    manifest['contents']['total_documents'] = len(metadata_files)
    
    # Write manifest
    with open(output_path / 'manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)
    
    # Create archive
    with tarfile.open(export_filename, 'w:gz') as tar:
        tar.add(output_path / 'metadata' / 'reviewed', arcname='metadata')
        tar.add(output_path / 'embeddings', arcname='embeddings')
        tar.add(output_path / 'manifest.json', arcname='manifest.json')
    
    print(f"Export created: {export_filename}")
    print(f"Total documents: {manifest['contents']['total_documents']}")
    print(f"File size: {Path(export_filename).stat().st_size / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    export_data()
```

## Transfer to Production

### 1. Secure Transfer Options

#### Option A: SCP (Recommended)
```bash
# Transfer to production server
scp export_20240117_143022.tar.gz user@production-server:/home/user/imports/

# On production server
cd /home/user/imports
tar -xzf export_20240117_143022.tar.gz
```

#### Option B: AWS S3
```bash
# Upload to S3
aws s3 cp export_20240117_143022.tar.gz s3://your-bucket/imports/

# On production server
aws s3 cp s3://your-bucket/imports/export_20240117_143022.tar.gz .
tar -xzf export_20240117_143022.tar.gz
```

#### Option C: rsync
```bash
# Sync entire output directory
rsync -avz --progress ./output/ user@production-server:/home/user/imports/current/
```

### 2. Production Import Script

Create this script on your production server as `import_metadata.py`:

```python
#!/usr/bin/env python3
"""
Import processed metadata into production Qdrant
"""

import json
from pathlib import Path
from datetime import datetime
import click
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

@click.command()
@click.option('--import-dir', required=True, help='Import directory')
@click.option('--qdrant-host', default='localhost', help='Qdrant host')
@click.option('--qdrant-port', default=6333, help='Qdrant port')
@click.option('--collection', default='legal_knowledge', help='Collection name')
def import_data(import_dir: str, qdrant_host: str, qdrant_port: int, collection: str):
    """Import metadata and embeddings into Qdrant"""
    import_path = Path(import_dir)
    
    # Initialize Qdrant client
    client = QdrantClient(host=qdrant_host, port=qdrant_port)
    
    # Load manifest
    with open(import_path / 'manifest.json', 'r') as f:
        manifest = json.load(f)
    
    print(f"Importing {manifest['contents']['total_documents']} documents")
    
    # Process each document
    metadata_dir = import_path / 'metadata'
    embeddings_dir = import_path / 'embeddings'
    
    points = []
    
    for metadata_file in metadata_dir.glob('*.json'):
        doc_id = metadata_file.stem.replace('_metadata', '')
        
        # Load metadata
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        # Load embeddings
        embedding_file = embeddings_dir / f"{doc_id}_embeddings.json"
        if embedding_file.exists():
            with open(embedding_file, 'r') as f:
                embeddings = json.load(f)
            
            # Create points for each chunk
            for emb_data in embeddings:
                point_id = f"{doc_id}_{emb_data['chunk_index']}"
                
                # Combine metadata with chunk info
                payload = {
                    **metadata,
                    'chunk_index': emb_data['chunk_index'],
                    'is_chunk': True,
                    'parent_document_id': doc_id
                }
                
                points.append(PointStruct(
                    id=point_id,
                    vector=emb_data['embedding'],
                    payload=payload
                ))
        
        # Also create a point for the full document
        if metadata.get('executive_summary'):
            # Use summary embedding for document-level search
            summary_text = metadata['executive_summary']
            # Note: You'd need to generate this embedding
            # For now, using first chunk embedding as placeholder
            if embeddings:
                points.append(PointStruct(
                    id=doc_id,
                    vector=embeddings[0]['embedding'],
                    payload={**metadata, 'is_chunk': False}
                ))
    
    # Upload to Qdrant in batches
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i:i+batch_size]
        client.upsert(collection_name=collection, points=batch)
        print(f"Uploaded batch {i//batch_size + 1}/{(len(points) + batch_size - 1)//batch_size}")
    
    print(f"\nImport complete! Uploaded {len(points)} points to collection '{collection}'")

if __name__ == "__main__":
    import_data()
```

## Verification

### 1. Local Verification Script

Create `scripts/verify_export.py`:

```python
#!/usr/bin/env python3
"""
Verify export package before transfer
"""

import json
import tarfile
from pathlib import Path
import click

@click.command()
@click.argument('export_file')
def verify_export(export_file: str):
    """Verify export package integrity"""
    print(f"Verifying: {export_file}")
    
    try:
        with tarfile.open(export_file, 'r:gz') as tar:
            # Check manifest
            manifest_file = tar.extractfile('manifest.json')
            manifest = json.load(manifest_file)
            
            print(f"Export timestamp: {manifest['export_timestamp']}")
            print(f"Total documents: {manifest['contents']['total_documents']}")
            
            # Verify file counts
            metadata_files = [m for m in tar.getmembers() if m.name.startswith('metadata/')]
            embedding_files = [m for m in tar.getmembers() if m.name.startswith('embeddings/')]
            
            print(f"Metadata files: {len(metadata_files)}")
            print(f"Embedding files: {len(embedding_files)}")
            
            # Check for matching pairs
            metadata_ids = {Path(m.name).stem.replace('_metadata', '') for m in metadata_files}
            embedding_ids = {Path(m.name).stem.replace('_embeddings', '') for m in embedding_files}
            
            missing_embeddings = metadata_ids - embedding_ids
            if missing_embeddings:
                print(f"Warning: Missing embeddings for: {missing_embeddings}")
            
            print("\n✅ Export package is valid!")
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")

if __name__ == "__main__":
    verify_export()
```

### 2. Production Verification

After import, verify on production:

```python
# Quick verification script
from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)

# Check collection info
info = client.get_collection("legal_knowledge")
print(f"Total points: {info.points_count}")
print(f"Vectors dimension: {info.config.params.vectors.size}")

# Test search
results = client.search(
    collection_name="legal_knowledge",
    query_vector=[0.1] * 768,  # Dummy vector
    limit=5
)

print(f"\nTest search returned {len(results)} results")
```

## Complete Workflow

1. **Local Processing**
   ```bash
   # Process documents
   python scripts/process_documents.py --input-dir ./input --output-dir ./output
   
   # Review metadata
   python scripts/review_metadata.py --metadata-dir ./output/metadata
   
   # Create export
   python scripts/export_for_production.py --output-dir ./output
   
   # Verify export
   python scripts/verify_export.py export_20240117_143022.tar.gz
   ```

2. **Transfer to Production**
   ```bash
   # Transfer file
   scp export_*.tar.gz user@production:/imports/
   
   # SSH to production
   ssh user@production
   
   # Extract and import
   cd /imports
   tar -xzf export_*.tar.gz
   python import_metadata.py --import-dir . --collection legal_knowledge
   ```

3. **Verify on Production**
   ```bash
   # Run verification
   python verify_import.py
   ```

## Best Practices

1. **Always verify exports** before transfer
2. **Keep processing logs** for audit trail
3. **Test with small batches** first
4. **Backup production data** before large imports
5. **Use version control** for metadata schemas
6. **Document any manual corrections** made during review

## Troubleshooting

### Common Issues

1. **Out of Memory during embedding generation**
   - Process in smaller batches
   - Use CPU instead of GPU for large batches
   - Consider using smaller embedding model

2. **API rate limits**
   - Add retry logic with exponential backoff
   - Process during off-peak hours
   - Use batch API endpoints when available

3. **Import failures**
   - Verify Qdrant collection exists
   - Check embedding dimensions match
   - Ensure proper network connectivity

4. **Data inconsistencies**
   - Always match metadata with embeddings
   - Verify document IDs are unique
   - Check for missing required fields