#!/usr/bin/env python3
"""
Legal Knowledge System - Directory Ingestion CLI
Command-line tool for ingesting legal documents from directories
"""
import argparse
import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime
import aiohttp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LegalDirectoryIngester:
    """CLI tool for legal document directory ingestion"""
    
    def __init__(self, superlinked_url="http://localhost:8080", api_url="http://localhost:8000"):
        self.superlinked_url = superlinked_url
        self.api_url = api_url
    
    async def ingest_directory(self, directory_path: str, recursive: bool = True, 
                             practice_area: str = None, dry_run: bool = False):
        """Ingest all legal documents from a directory"""
        directory = Path(directory_path)
        if not directory.exists():
            logger.error(f"Directory does not exist: {directory_path}")
            return False
        
        logger.info(f"Starting ingestion of directory: {directory_path}")
        logger.info(f"Recursive: {recursive}, Practice Area: {practice_area}, Dry Run: {dry_run}")
        
        supported_extensions = {'.pdf', '.docx', '.txt'}
        files_found = []
        
        # Find files
        if recursive:
            for file_path in directory.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                    if not file_path.name.endswith('.metadata.json'):
                        files_found.append(file_path)
        else:
            for file_path in directory.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                    if not file_path.name.endswith('.metadata.json'):
                        files_found.append(file_path)
        
        logger.info(f"Found {len(files_found)} files to process")
        
        if dry_run:
            logger.info("DRY RUN MODE - Files that would be processed:")
            for file_path in files_found:
                logger.info(f"  - {file_path}")
            return True
        
        # Process files
        successful = 0
        failed = 0
        
        for file_path in files_found:
            try:
                success = await self.process_single_file(file_path, practice_area)
                if success:
                    successful += 1
                    logger.info(f"✅ Successfully processed: {file_path.name}")
                else:
                    failed += 1
                    logger.error(f"❌ Failed to process: {file_path.name}")
            except Exception as e:
                failed += 1
                logger.error(f"❌ Error processing {file_path.name}: {e}")
        
        logger.info(f"Ingestion complete - Successful: {successful}, Failed: {failed}")
        return failed == 0
    
    async def process_single_file(self, file_path: Path, default_practice_area: str = None):
        """Process a single file"""
        try:
            # Load metadata
            metadata = await self.load_metadata(file_path, default_practice_area)
            
            # Extract text (simplified for CLI - would use GROBID in full system)
            content_text = await self.extract_text_simple(file_path)
            if not content_text.strip():
                logger.warning(f"No text content extracted from {file_path}")
                return False
            
            # Prepare document for ingestion
            document = {
                **metadata,
                'content_text': content_text,
                'word_count': len(content_text.split()),
                'pdf_path': str(file_path)
            }
            
            # Ingest via API
            return await self.ingest_document_via_api(document)
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return False
    
    async def load_metadata(self, file_path: Path, default_practice_area: str = None):
        """Load and merge metadata for a file"""
        # Load directory metadata
        directory_meta = {}
        metadata_file = file_path.parent / "metadata.json"
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    directory_meta = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load directory metadata: {e}")
        
        # Load file-specific metadata
        file_meta = {}
        file_metadata_path = file_path.parent / f"{file_path.name}.metadata.json"
        if file_metadata_path.exists():
            try:
                with open(file_metadata_path, 'r') as f:
                    file_meta = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load file metadata: {e}")
        
        # Merge metadata
        merged = directory_meta.copy()
        merged.update(file_meta)
        
        # Set defaults
        if 'id' not in merged:
            import hashlib
            file_hash = hashlib.md5(str(file_path).encode()).hexdigest()[:12]
            merged['id'] = f"doc_{file_hash}"
        
        if 'title' not in merged:
            merged['title'] = file_path.stem
        
        merged.setdefault('practice_area', default_practice_area or 'general_law')
        merged.setdefault('jurisdiction', 'federal')
        merged.setdefault('authority_level', 'secondary')
        merged.setdefault('document_type', 'article')
        merged.setdefault('author', 'Unknown')
        merged.setdefault('citations', [])
        merged.setdefault('keywords', [])
        merged.setdefault('summary', '')
        merged.setdefault('authority_score', 0.5)
        merged.setdefault('relevance_score', 0.5)
        merged.setdefault('citation_count', 0)
        merged.setdefault('source_url', '')
        
        if 'publication_date' not in merged:
            merged['publication_date'] = int(datetime.now().timestamp())
        
        return merged
    
    async def extract_text_simple(self, file_path: Path):
        """Simple text extraction (fallback method)"""
        try:
            if file_path.suffix.lower() == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            elif file_path.suffix.lower() == '.pdf':
                # Simple PDF text extraction using PyPDF2
                try:
                    import PyPDF2
                    with open(file_path, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        text = ""
                        for page in reader.pages:
                            text += page.extract_text() + "\n"
                        return text.strip()
                except ImportError:
                    logger.warning("PyPDF2 not available for PDF processing")
                    return f"PDF file: {file_path.name} (text extraction requires PyPDF2)"
            elif file_path.suffix.lower() == '.docx':
                try:
                    from docx import Document
                    doc = Document(file_path)
                    text = []
                    for paragraph in doc.paragraphs:
                        text.append(paragraph.text)
                    return "\n".join(text)
                except ImportError:
                    logger.warning("python-docx not available for DOCX processing")
                    return f"DOCX file: {file_path.name} (text extraction requires python-docx)"
            else:
                return f"Unsupported file type: {file_path.suffix}"
        except Exception as e:
            logger.error(f"Text extraction error for {file_path}: {e}")
            return ""
    
    async def ingest_document_via_api(self, document):
        """Ingest document via Legal Knowledge System API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/api/v1/documents/ingest",
                    json=document,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(f"API ingestion failed: {error_text}")
                        return False
        except Exception as e:
            logger.error(f"API ingestion error: {e}")
            return False
    
    async def test_connection(self):
        """Test connection to Legal Knowledge System"""
        try:
            async with aiohttp.ClientSession() as session:
                # Test API
                async with session.get(f"{self.api_url}/api/v1/health", timeout=5) as response:
                    api_status = response.status == 200
                
                # Test Superlinked
                async with session.get(f"{self.superlinked_url}/docs", timeout=5) as response:
                    superlinked_status = response.status == 200
                
                logger.info(f"API Status: {'✅ Connected' if api_status else '❌ Failed'}")
                logger.info(f"Superlinked Status: {'✅ Connected' if superlinked_status else '❌ Failed'}")
                
                return api_status and superlinked_status
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    async def create_sample_metadata(self, directory_path: str, practice_area: str = "personal_injury"):
        """Create sample metadata files for a directory"""
        directory = Path(directory_path)
        directory.mkdir(parents=True, exist_ok=True)
        
        # Create directory metadata
        directory_metadata = {
            "practice_area": practice_area,
            "jurisdiction": "california",
            "authority_level": "primary",
            "document_type": "case_law",
            "source_type": "court_records",
            "collection_date": datetime.now().strftime("%Y-%m-%d"),
            "source_attribution": "Legal Document Collection",
            "authority_score": 0.8,
            "relevance_score": 0.75
        }
        
        if practice_area == "personal_injury":
            directory_metadata.update({
                "injury_type": "medical_malpractice",
                "liability_theory": "negligence",
                "medical_treatment": "ongoing",
                "trial_readiness": "settlement_track"
            })
        
        metadata_file = directory / "metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(directory_metadata, f, indent=2)
        
        # Create sample file metadata
        sample_file_metadata = {
            "id": "sample_case_001",
            "title": "Sample Medical Malpractice Case",
            "injury_severity": "severe",
            "body_parts_affected": ["spine"],
            "medical_records_complexity": "expert_needed",
            "expert_witnesses_needed": ["medical_expert"],
            "citations": ["Sample Citation"],
            "keywords": ["medical_malpractice", "negligence"],
            "summary": "Sample case summary for demonstration",
            "authority_score": 0.9
        }
        
        sample_metadata_file = directory / "sample_case.pdf.metadata.json"
        with open(sample_metadata_file, 'w') as f:
            json.dump(sample_file_metadata, f, indent=2)
        
        logger.info(f"Created sample metadata files in: {directory}")
        logger.info(f"  - {metadata_file}")
        logger.info(f"  - {sample_metadata_file}")


async def main():
    parser = argparse.ArgumentParser(description="Legal Knowledge System - Directory Ingestion CLI")
    parser.add_argument("command", choices=["ingest", "test", "create-samples"], 
                       help="Command to execute")
    parser.add_argument("--directory", "-d", required=False,
                       help="Directory path to process")
    parser.add_argument("--practice-area", "-p", 
                       choices=["immigration_law", "family_law", "criminal_law", "business_law", 
                               "real_estate_law", "employment_law", "personal_injury", "estate_planning"],
                       default="personal_injury",
                       help="Default practice area for documents")
    parser.add_argument("--recursive", "-r", action="store_true", 
                       help="Process directories recursively")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be processed without actually doing it")
    parser.add_argument("--api-url", default="http://localhost:8000",
                       help="Legal Knowledge System API URL")
    parser.add_argument("--superlinked-url", default="http://localhost:8080",
                       help="Superlinked server URL")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    ingester = LegalDirectoryIngester(args.superlinked_url, args.api_url)
    
    if args.command == "test":
        logger.info("Testing connection to Legal Knowledge System...")
        success = await ingester.test_connection()
        if success:
            logger.info("✅ All connections successful")
            sys.exit(0)
        else:
            logger.error("❌ Connection test failed")
            sys.exit(1)
    
    elif args.command == "create-samples":
        if not args.directory:
            logger.error("--directory is required for create-samples command")
            sys.exit(1)
        await ingester.create_sample_metadata(args.directory, args.practice_area)
        
    elif args.command == "ingest":
        if not args.directory:
            logger.error("--directory is required for ingest command")
            sys.exit(1)
        
        # Test connection first
        logger.info("Testing system connection...")
        if not await ingester.test_connection():
            logger.error("Cannot connect to Legal Knowledge System. Please ensure services are running.")
            sys.exit(1)
        
        # Perform ingestion
        success = await ingester.ingest_directory(
            args.directory, 
            recursive=args.recursive,
            practice_area=args.practice_area,
            dry_run=args.dry_run
        )
        
        if success:
            logger.info("✅ Ingestion completed successfully")
            sys.exit(0)
        else:
            logger.error("❌ Ingestion completed with errors")
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())