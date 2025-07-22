#!/usr/bin/env python3
"""
Local Document Processing Pipeline with Claude (Anthropic)

Processes legal documents to extract metadata, facts, and generate embeddings.
Uses Claude for AI-powered fact extraction and summarization.
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
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

# Initialize models
embedding_model = SentenceTransformer(os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-mpnet-base-v2'))
anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Model configuration
CLAUDE_MODEL = os.getenv('CLAUDE_MODEL', 'claude-3-sonnet-20240229')  # or claude-3-opus-20240229 for best quality

class DocumentProcessor:
    """Process legal documents locally using Claude"""
    
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
        
        # AI processing with Claude
        facts = self._extract_facts_claude(text)
        summary = self._generate_summary_claude(text)
        
        # Update metadata
        metadata.update({
            'extracted_facts': facts['facts'],
            'fact_count': facts['count'],
            'key_findings': facts.get('key_findings', []),
            'executive_summary': summary['executive_summary'],
            'summary_bullet_points': summary['bullet_points'],
            'summary_conclusion': summary['conclusion'],
            'key_takeaways': summary.get('key_takeaways', []),
            'preprocessing_timestamp': datetime.now().isoformat(),
            'preprocessing_version': '1.0',
            'ai_model': CLAUDE_MODEL
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
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    # Add page markers for citation purposes
                    text += f"\n[Page {i+1}]\n{page_text}\n"
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
            
            # Find page context for this chunk
            page_marker_before = text.rfind('[Page', 0, start)
            if page_marker_before != -1:
                page_end = text.find(']', page_marker_before)
                if page_end != -1:
                    page_context = text[page_marker_before:page_end+1]
                else:
                    page_context = "Unknown page"
            else:
                page_context = "Page 1"
            
            chunks.append({
                'chunk_index': chunk_index,
                'text': chunk_text,
                'start_char': start,
                'end_char': min(end, len(text)),
                'chunk_context': page_context
            })
            
            start = end - overlap
            chunk_index += 1
            
        return chunks
    
    def _extract_metadata(self, pdf_path: Path, text: str, doc_id: str) -> Dict:
        """Extract basic metadata"""
        # Detect jurisdiction and practice area from filename/content
        filename = pdf_path.stem.lower()
        text_lower = text.lower()[:5000]  # First 5000 chars for detection
        
        # Jurisdiction detection
        jurisdiction_state = None
        state_patterns = {
            'texas': ['texas', 'tex.', ' tx ', 'state of texas'],
            'california': ['california', 'cal.', ' ca ', 'state of california'],
            'new_york': ['new york', 'n.y.', ' ny ', 'state of new york'],
            'florida': ['florida', 'fla.', ' fl ', 'state of florida'],
        }
        
        for state, patterns in state_patterns.items():
            if any(pattern in filename or pattern in text_lower for pattern in patterns):
                jurisdiction_state = state
                break
        
        # Content type detection
        content_type = 'unknown'
        if any(word in text_lower for word in ['statute', 'code', 'chapter', 'section']):
            content_type = 'statute'
        elif any(word in text_lower for word in ['opinion', 'court', 'plaintiff', 'defendant']):
            content_type = 'case_law'
        elif any(word in text_lower for word in ['regulation', 'rule', 'cfr', 'administrative']):
            content_type = 'regulation'
        elif any(word in text_lower for word in ['contract', 'agreement', 'parties']):
            content_type = 'contract'
            
        return {
            'id': doc_id,
            'title': pdf_path.stem.replace('_', ' ').replace('-', ' ').title(),
            'source_filename': pdf_path.name,
            'file_size_bytes': pdf_path.stat().st_size,
            'jurisdiction_country': 'united_states',
            'jurisdiction_state': jurisdiction_state,
            'content_type': content_type,
            'processed_date': datetime.now().isoformat(),
            'total_pages': text.count('[Page'),
            'total_chars': len(text)
        }
    
    def _extract_facts_claude(self, text: str) -> Dict:
        """Extract facts using Claude"""
        # Limit text for API (Claude has 100k+ context but we'll be conservative)
        sample_text = text[:15000]
        
        prompt = f"""You are a legal analysis expert. Extract key legal facts from this document.

For each fact you identify:
1. State the fact clearly and concisely
2. Provide the exact location (page number or section reference from the text)
3. Include an APA 7th edition style citation reference
4. Add relevant context keywords for searchability
5. Assign a confidence score (0.0-1.0)

Also identify 3-5 key findings that summarize the most important aspects of the document.

Return your response as a JSON object with this structure:
{{
  "facts": [
    {{
      "fact": "The statute of limitations for personal injury claims is two years",
      "location": "Page 12, Section 16.003",
      "citation": "Tex. Civ. Prac. & Rem. Code § 16.003 (2024)",
      "context": ["statute of limitations", "personal injury", "two years", "time limit"],
      "confidence": 0.95
    }}
  ],
  "key_findings": [
    "Primary finding about the document's main purpose or impact"
  ]
}}

Document text:
{sample_text}"""
        
        try:
            response = anthropic_client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=4000,
                temperature=0.1,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Parse Claude's response
            response_text = response.content[0].text
            
            # Extract JSON from response (Claude sometimes adds explanation)
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                facts_data = json.loads(json_match.group())
            else:
                facts_data = {"facts": [], "key_findings": []}
                
            return {
                'facts': facts_data.get('facts', []),
                'key_findings': facts_data.get('key_findings', []),
                'count': len(facts_data.get('facts', []))
            }
            
        except Exception as e:
            print(f"Error extracting facts with Claude: {e}")
            return {'facts': [], 'key_findings': [], 'count': 0}
    
    def _generate_summary_claude(self, text: str) -> Dict:
        """Generate executive summary using Claude"""
        # Limit text for API
        sample_text = text[:20000]
        
        prompt = f"""You are a legal document summarization expert. Create a comprehensive summary of this legal document.

Provide:
1. An executive summary (1 paragraph, maximum 250 words) that captures the document's essence and primary purpose
2. Key bullet points (6-10 bullets) highlighting the most important provisions, requirements, or findings
3. A brief conclusion (2-3 sentences) stating the document's significance and implications
4. Key takeaways (3-5 points) written in plain language for non-lawyers

Format your response as a JSON object:
{{
  "executive_summary": "Comprehensive paragraph summary...",
  "bullet_points": [
    "• First key point",
    "• Second key point"
  ],
  "conclusion": "Brief conclusion statement...",
  "key_takeaways": [
    "Plain language takeaway for clients",
    "Another accessible point"
  ]
}}

Document text:
{sample_text}"""
        
        try:
            response = anthropic_client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=2000,
                temperature=0.3,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Parse Claude's response
            response_text = response.content[0].text
            
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                summary_data = json.loads(json_match.group())
            else:
                summary_data = {
                    'executive_summary': 'Summary generation failed',
                    'bullet_points': [],
                    'conclusion': '',
                    'key_takeaways': []
                }
                
            return summary_data
            
        except Exception as e:
            print(f"Error generating summary with Claude: {e}")
            return {
                'executive_summary': '',
                'bullet_points': [],
                'conclusion': '',
                'key_takeaways': []
            }
    
    def _generate_embeddings(self, chunks: List[Dict], metadata: Dict) -> List[Dict]:
        """Generate embeddings for chunks"""
        embeddings = []
        
        for chunk in tqdm(chunks, desc="Generating embeddings"):
            # Combine chunk text with metadata for richer embeddings
            enriched_text = f"""
            Title: {metadata.get('title', '')}
            Document Type: {metadata.get('content_type', '')}
            Jurisdiction: {metadata.get('jurisdiction_state', '')}
            Page Context: {chunk.get('chunk_context', '')}
            
            Content: {chunk['text'][:1500]}
            """
            
            # Generate embedding
            embedding = embedding_model.encode(enriched_text).tolist()
            
            embeddings.append({
                'chunk_index': chunk['chunk_index'],
                'embedding': embedding,
                'metadata': {
                    'doc_id': metadata['id'],
                    'chunk_size': len(chunk['text']),
                    'chunk_context': chunk.get('chunk_context', '')
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
            'ai_model': CLAUDE_MODEL,
            'status': 'completed'
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

@click.command()
@click.option('--input-dir', default='./input', help='Directory containing PDFs')
@click.option('--output-dir', default='./output', help='Output directory')
@click.option('--batch-size', default=10, help='Batch size for processing')
@click.option('--model', default=None, help='Claude model to use (defaults to env var)')
def main(input_dir: str, output_dir: str, batch_size: int, model: Optional[str]):
    """Process legal documents locally using Claude"""
    
    # Check for API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("Error: ANTHROPIC_API_KEY not found in environment")
        print("Please set it in .env.local or export ANTHROPIC_API_KEY=your-key")
        return
    
    # Override model if specified
    if model:
        global CLAUDE_MODEL
        CLAUDE_MODEL = model
        
    processor = DocumentProcessor(output_dir)
    
    # Find all PDFs
    input_path = Path(input_dir)
    pdf_files = list(input_path.glob('*.pdf'))
    
    print(f"Found {len(pdf_files)} PDF files to process")
    print(f"Using Claude model: {CLAUDE_MODEL}")
    
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
    print(f"AI Model used: {CLAUDE_MODEL}")

if __name__ == "__main__":
    main()