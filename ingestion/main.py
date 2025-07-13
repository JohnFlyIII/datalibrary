"""
Legal Knowledge System - Directory Ingestion Service
Monitors directories for new legal documents and processes them
"""
import asyncio
import json
import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import aiohttp
import aiofiles
import magic
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
SUPERLINKED_URL = os.getenv("SUPERLINKED_URL", "http://localhost:8080")
GROBID_URL = os.getenv("GROBID_URL", "http://localhost:8070")
LEGAL_DOCS_PATH = os.getenv("LEGAL_DOCS_PATH", "/app/legal_documents")
PROCESSED_DOCS_PATH = os.getenv("PROCESSED_DOCS_PATH", "/app/processed_docs")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")


class DocumentProcessor:
    """Processes legal documents and extracts content"""
    
    def __init__(self):
        self.grobid_url = GROBID_URL
        self.mime = magic.Magic(mime=True)
    
    async def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using GROBID"""
        try:
            async with aiohttp.ClientSession() as session:
                with open(pdf_path, 'rb') as pdf_file:
                    files = {'input': pdf_file}
                    async with session.post(
                        f"{self.grobid_url}/api/processFulltextDocument",
                        data=files
                    ) as response:
                        if response.status == 200:
                            xml_content = await response.text()
                            # Simple XML text extraction (could be enhanced)
                            # Remove XML tags for basic text extraction
                            import re
                            text = re.sub(r'<[^>]+>', '', xml_content)
                            return text.strip()
                        else:
                            logger.error(f"GROBID processing failed: {response.status}")
                            return ""
        except Exception as e:
            logger.error(f"PDF text extraction failed: {e}")
            # Fallback to PyPDF2
            try:
                import PyPDF2
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text.strip()
            except Exception as fallback_e:
                logger.error(f"Fallback PDF extraction failed: {fallback_e}")
                return ""
    
    async def extract_text_from_docx(self, docx_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            from docx import Document
            doc = Document(docx_path)
            text = []
            for paragraph in doc.paragraphs:
                text.append(paragraph.text)
            return "\n".join(text)
        except Exception as e:
            logger.error(f"DOCX text extraction failed: {e}")
            return ""
    
    async def extract_text_from_txt(self, txt_path: str) -> str:
        """Extract text from TXT file"""
        try:
            async with aiofiles.open(txt_path, 'r', encoding='utf-8') as file:
                return await file.read()
        except Exception as e:
            logger.error(f"TXT text extraction failed: {e}")
            return ""
    
    async def extract_text(self, file_path: str) -> str:
        """Extract text based on file type"""
        mime_type = self.mime.from_file(file_path)
        
        if 'pdf' in mime_type:
            return await self.extract_text_from_pdf(file_path)
        elif 'officedocument.wordprocessingml' in mime_type:
            return await self.extract_text_from_docx(file_path)
        elif 'text/plain' in mime_type:
            return await self.extract_text_from_txt(file_path)
        else:
            logger.warning(f"Unsupported file type: {mime_type}")
            return ""


class MetadataProcessor:
    """Processes metadata files and merges with document data"""
    
    def __init__(self):
        pass
    
    async def load_directory_metadata(self, directory: Path) -> Dict[str, Any]:
        """Load directory-level metadata.json"""
        metadata_file = directory / "metadata.json"
        if metadata_file.exists():
            try:
                async with aiofiles.open(metadata_file, 'r') as file:
                    content = await file.read()
                    return json.loads(content)
            except Exception as e:
                logger.error(f"Failed to load directory metadata {metadata_file}: {e}")
        return {}
    
    async def load_file_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Load file-specific metadata.json"""
        metadata_file = file_path.parent / f"{file_path.name}.metadata.json"
        if metadata_file.exists():
            try:
                async with aiofiles.open(metadata_file, 'r') as file:
                    content = await file.read()
                    return json.loads(content)
            except Exception as e:
                logger.error(f"Failed to load file metadata {metadata_file}: {e}")
        return {}
    
    def merge_metadata(self, directory_meta: Dict, file_meta: Dict, file_path: Path) -> Dict[str, Any]:
        """Merge directory and file metadata with defaults"""
        # Start with directory defaults
        merged = directory_meta.copy()
        
        # Override with file-specific metadata
        merged.update(file_meta)
        
        # Generate document ID if not provided
        if 'id' not in merged:
            file_hash = hashlib.md5(str(file_path).encode()).hexdigest()[:12]
            merged['id'] = f"doc_{file_hash}"
        
        # Set title if not provided
        if 'title' not in merged:
            merged['title'] = file_path.stem
        
        # Set defaults for required fields
        merged.setdefault('practice_area', 'general_law')
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
        merged.setdefault('pdf_path', str(file_path))
        
        # Set publication date if not provided
        if 'publication_date' not in merged:
            merged['publication_date'] = int(datetime.now().timestamp())
        
        return merged


class SuperlinkedClient:
    """Client for ingesting documents into Superlinked system"""
    
    def __init__(self):
        self.superlinked_url = SUPERLINKED_URL
    
    async def ingest_document(self, document: Dict[str, Any]) -> bool:
        """Ingest document into Superlinked system"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.superlinked_url}/ingest/legal_document_source",
                    json=document,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        logger.info(f"Successfully ingested document: {document['id']}")
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(f"Ingestion failed for {document['id']}: {error_text}")
                        return False
        except Exception as e:
            logger.error(f"Ingestion error for {document['id']}: {e}")
            return False


class DirectoryIngestionService:
    """Main service for monitoring and processing legal documents"""
    
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.metadata_processor = MetadataProcessor()
        self.superlinked_client = SuperlinkedClient()
        self.processed_files = set()
        self.processing_lock = asyncio.Lock()
    
    async def process_file(self, file_path: Path) -> bool:
        """Process a single file"""
        async with self.processing_lock:
            if str(file_path) in self.processed_files:
                return True
            
            logger.info(f"Processing file: {file_path}")
            
            try:
                # Extract text content
                content_text = await self.document_processor.extract_text(str(file_path))
                if not content_text.strip():
                    logger.warning(f"No text content extracted from {file_path}")
                    return False
                
                # Load and merge metadata
                directory_meta = await self.metadata_processor.load_directory_metadata(file_path.parent)
                file_meta = await self.metadata_processor.load_file_metadata(file_path)
                merged_meta = self.metadata_processor.merge_metadata(directory_meta, file_meta, file_path)
                
                # Add extracted content
                merged_meta['content_text'] = content_text
                merged_meta['word_count'] = len(content_text.split())
                
                # Handle personal injury specific metadata
                if merged_meta.get('practice_area') == 'personal_injury' or merged_meta.get('injury_type'):
                    merged_meta = self._add_personal_injury_metadata(merged_meta)
                
                # Ingest into Superlinked
                success = await self.superlinked_client.ingest_document(merged_meta)
                
                if success:
                    self.processed_files.add(str(file_path))
                    
                    # Save processing record
                    await self._save_processing_record(file_path, merged_meta, success)
                    
                    logger.info(f"Successfully processed: {file_path}")
                    return True
                else:
                    logger.error(f"Failed to ingest: {file_path}")
                    return False
                    
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                return False
    
    def _add_personal_injury_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Add personal injury specific metadata fields"""
        # Set defaults for personal injury cases
        metadata.setdefault('injury_type', 'general')
        metadata.setdefault('injury_severity', 'moderate')
        metadata.setdefault('body_parts_affected', [])
        metadata.setdefault('liability_theory', 'negligence')
        metadata.setdefault('causation_complexity', 'clear')
        metadata.setdefault('comparative_fault', 'none')
        metadata.setdefault('insurance_coverage', [])
        metadata.setdefault('policy_limits', 'adequate')
        metadata.setdefault('medical_treatment', 'ongoing')
        metadata.setdefault('future_medical_needs', 'likely')
        metadata.setdefault('medical_records_complexity', 'simple')
        metadata.setdefault('lost_wages', 'temporary')
        metadata.setdefault('earning_capacity', 'unaffected')
        metadata.setdefault('special_damages', [])
        metadata.setdefault('statute_of_limitations', 'standard')
        metadata.setdefault('expert_witnesses_needed', [])
        metadata.setdefault('trial_readiness', 'settlement_track')
        
        return metadata
    
    async def _save_processing_record(self, file_path: Path, metadata: Dict, success: bool):
        """Save processing record for tracking"""
        record = {
            'file_path': str(file_path),
            'document_id': metadata.get('id'),
            'processed_at': datetime.now().isoformat(),
            'success': success,
            'word_count': metadata.get('word_count', 0),
            'practice_area': metadata.get('practice_area')
        }
        
        record_file = Path(PROCESSED_DOCS_PATH) / f"processing_log_{datetime.now().strftime('%Y%m%d')}.jsonl"
        record_file.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(record_file, 'a') as file:
            await file.write(json.dumps(record) + '\n')
    
    async def process_directory(self, directory_path: str) -> Dict[str, Any]:
        """Process all files in a directory recursively"""
        directory = Path(directory_path)
        if not directory.exists():
            logger.error(f"Directory does not exist: {directory_path}")
            return {"error": "Directory does not exist"}
        
        supported_extensions = {'.pdf', '.docx', '.txt'}
        files_to_process = []
        
        # Find all supported files recursively
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                # Skip metadata files
                if not file_path.name.endswith('.metadata.json'):
                    files_to_process.append(file_path)
        
        logger.info(f"Found {len(files_to_process)} files to process in {directory_path}")
        
        # Process files
        successful = 0
        failed = 0
        
        for file_path in files_to_process:
            try:
                success = await self.process_file(file_path)
                if success:
                    successful += 1
                else:
                    failed += 1
            except Exception as e:
                logger.error(f"Processing error for {file_path}: {e}")
                failed += 1
        
        return {
            "directory": directory_path,
            "total_files": len(files_to_process),
            "successful": successful,
            "failed": failed,
            "processed_files": list(self.processed_files)
        }


class DirectoryWatcher(FileSystemEventHandler):
    """File system event handler for real-time monitoring"""
    
    def __init__(self, ingestion_service: DirectoryIngestionService):
        self.ingestion_service = ingestion_service
        self.supported_extensions = {'.pdf', '.docx', '.txt'}
    
    def on_created(self, event):
        if not event.is_directory:
            file_path = Path(event.src_path)
            if file_path.suffix.lower() in self.supported_extensions:
                logger.info(f"New file detected: {file_path}")
                # Process file asynchronously
                asyncio.create_task(self.ingestion_service.process_file(file_path))
    
    def on_modified(self, event):
        if not event.is_directory:
            file_path = Path(event.src_path)
            if file_path.suffix.lower() in self.supported_extensions:
                # Check if this is a metadata file update
                if str(file_path) not in self.ingestion_service.processed_files:
                    logger.info(f"Modified file detected: {file_path}")
                    asyncio.create_task(self.ingestion_service.process_file(file_path))


async def main():
    """Main service entry point"""
    logger.info("Starting Legal Directory Ingestion Service")
    
    # Initialize service
    ingestion_service = DirectoryIngestionService()
    
    # Create necessary directories
    Path(LEGAL_DOCS_PATH).mkdir(parents=True, exist_ok=True)
    Path(PROCESSED_DOCS_PATH).mkdir(parents=True, exist_ok=True)
    
    # Process existing files on startup
    logger.info(f"Processing existing files in: {LEGAL_DOCS_PATH}")
    initial_result = await ingestion_service.process_directory(LEGAL_DOCS_PATH)
    logger.info(f"Initial processing complete: {initial_result}")
    
    # Set up file system monitoring
    event_handler = DirectoryWatcher(ingestion_service)
    observer = Observer()
    observer.schedule(event_handler, LEGAL_DOCS_PATH, recursive=True)
    observer.start()
    
    logger.info(f"Monitoring directory: {LEGAL_DOCS_PATH}")
    
    try:
        # Keep service running
        while True:
            await asyncio.sleep(60)  # Check every minute
            
            # Periodic health check
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{SUPERLINKED_URL}/docs", timeout=5) as response:
                        if response.status != 200:
                            logger.warning("Superlinked service health check failed")
            except Exception as e:
                logger.warning(f"Health check failed: {e}")
    
    except KeyboardInterrupt:
        logger.info("Shutting down ingestion service")
        observer.stop()
    
    observer.join()


if __name__ == "__main__":
    asyncio.run(main())