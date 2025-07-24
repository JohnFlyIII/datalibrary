# Legal Document Preprocessing Pipeline

## Overview

The preprocessing pipeline enriches legal documents with AI-extracted facts and summaries before ingestion into Superlinked. This two-step process dramatically improves search quality and enables fact-based queries.

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Input Document                           │
│                  (PDF, TXT, HTML, DOCX)                     │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Step 1: Text Extraction                   │
│                  - PDF → Text conversion                     │
│                  - Metadata extraction                       │
│                  - Structure preservation                    │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 Step 2: Fact Extraction                      │
│                  - Legal facts with citations               │
│                  - Key findings identification              │
│                  - Location mapping (APA 7th)               │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 Step 3: Summary Generation                   │
│                  - Executive summary (1 page)               │
│                  - Bullet points                            │
│                  - Conclusions                              │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│               Step 4: Enriched Document                      │
│            Ready for Superlinked Ingestion                  │
└─────────────────────────────────────────────────────────────┘
```

## Implementation

### Core Preprocessing Class

```python
"""
legal_preprocessor.py
Main preprocessing pipeline for legal documents
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import openai
import anthropic
from pypdf import PdfReader
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ExtractedFact:
    """Represents a single extracted fact with citation"""
    fact: str
    location: str
    page_number: Optional[int]
    section: Optional[str]
    citation_apa: str
    confidence: float
    category: str  # requirement, penalty, deadline, exception, definition


@dataclass
class DocumentSummary:
    """Contains all summary components"""
    executive_summary: str
    bullet_points: List[str]
    conclusion: str
    key_takeaways: List[str]
    

class LegalDocumentPreprocessor:
    """
    Preprocesses legal documents for Superlinked ingestion
    
    Features:
    - Fact extraction with APA 7th citations
    - Multi-format summary generation
    - Hierarchical categorization
    - Confidence scoring
    """
    
    def __init__(
        self,
        openai_api_key: str,
        anthropic_api_key: str,
        use_gpt4: bool = True,
        use_claude: bool = True
    ):
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        self.anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
        self.use_gpt4 = use_gpt4
        self.use_claude = use_claude
        
        # Model selection
        self.fact_model = "gpt-4-turbo-preview" if use_gpt4 else "gpt-3.5-turbo"
        self.summary_model = "claude-3-sonnet-20240229" if use_claude else self.fact_model
        
    def preprocess_document(
        self,
        file_path: str,
        metadata: Dict[str, any]
    ) -> Dict[str, any]:
        """
        Main preprocessing pipeline
        
        Args:
            file_path: Path to document
            metadata: Existing metadata (jurisdiction, practice area, etc.)
            
        Returns:
            Enriched metadata ready for Superlinked
        """
        logger.info(f"Starting preprocessing for: {file_path}")
        
        # Step 1: Extract text
        text_content, structure = self.extract_text(file_path)
        
        # Step 2: Extract facts
        facts = self.extract_facts(text_content, structure, metadata)
        
        # Step 3: Generate summaries
        summaries = self.generate_summaries(text_content, facts, metadata)
        
        # Step 4: Enrich metadata
        enriched_metadata = self.enrich_metadata(
            metadata, facts, summaries, text_content
        )
        
        logger.info(f"Preprocessing complete: {len(facts)} facts extracted")
        return enriched_metadata
    
    def extract_text(self, file_path: str) -> Tuple[str, Dict]:
        """Extract text and structure from document"""
        structure = {
            "pages": [],
            "sections": [],
            "total_pages": 0
        }
        
        if file_path.endswith('.pdf'):
            reader = PdfReader(file_path)
            text_parts = []
            
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                text_parts.append(page_text)
                
                # Track page structure
                structure["pages"].append({
                    "number": i + 1,
                    "text": page_text,
                    "char_start": sum(len(p) for p in text_parts[:-1]),
                    "char_end": sum(len(p) for p in text_parts)
                })
            
            structure["total_pages"] = len(reader.pages)
            full_text = "\n".join(text_parts)
            
        else:
            # Handle other formats (TXT, HTML, DOCX)
            with open(file_path, 'r', encoding='utf-8') as f:
                full_text = f.read()
                structure["pages"].append({
                    "number": 1,
                    "text": full_text,
                    "char_start": 0,
                    "char_end": len(full_text)
                })
        
        # Extract sections
        structure["sections"] = self.extract_sections(full_text)
        
        return full_text, structure
    
    def extract_sections(self, text: str) -> List[Dict]:
        """Extract document sections based on common legal formatting"""
        sections = []
        
        # Common section patterns
        patterns = [
            r"(?:SECTION|Section|Sec\.|§)\s*(\d+(?:\.\d+)*)\s*[.-]?\s*([^\n]+)",
            r"(?:ARTICLE|Article|Art\.)\s*(\w+)\s*[.-]?\s*([^\n]+)",
            r"^(\d+)\.\s+([A-Z][^\n]+)$",
            r"^([A-Z]+)\.\s+([^\n]+)$"
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.MULTILINE)
            for match in matches:
                sections.append({
                    "number": match.group(1),
                    "title": match.group(2).strip(),
                    "start": match.start(),
                    "end": match.end()
                })
        
        return sorted(sections, key=lambda x: x["start"])
    
    def extract_facts(
        self,
        text: str,
        structure: Dict,
        metadata: Dict
    ) -> List[ExtractedFact]:
        """Extract legal facts with citations"""
        
        # Prepare prompts based on document type
        doc_type = metadata.get("content_type", "general")
        
        fact_extraction_prompt = f"""
        You are a legal research assistant specializing in {doc_type} analysis.
        Extract key legal facts from the following document.
        
        For each fact:
        1. State the fact clearly and concisely
        2. Identify the exact location (page number and/or section)
        3. Categorize as: requirement, penalty, deadline, exception, or definition
        4. Rate confidence (0.0-1.0) based on clarity and directness
        
        Focus on:
        - Legal requirements and obligations
        - Penalties and consequences  
        - Deadlines and timeframes
        - Exceptions and exemptions
        - Key definitions
        - Jurisdictional elements
        - Affected parties
        
        Document metadata:
        - Type: {doc_type}
        - Jurisdiction: {metadata.get('jurisdiction', 'unknown')}
        - Practice Area: {metadata.get('practice_areas', 'unknown')}
        
        Document text:
        {text[:8000]}  # Limit for API
        
        Return as JSON array with this structure:
        [
            {{
                "fact": "Clear statement of the legal fact",
                "location": "p. 15, Section 3.2" or "Section 21.128(a)",
                "page_number": 15,
                "section": "3.2",
                "category": "requirement",
                "confidence": 0.95,
                "direct_quote": "Optional: exact quote from document"
            }}
        ]
        """
        
        try:
            if self.use_gpt4:
                response = self.openai_client.chat.completions.create(
                    model=self.fact_model,
                    messages=[
                        {"role": "system", "content": "You are a legal fact extraction specialist."},
                        {"role": "user", "content": fact_extraction_prompt}
                    ],
                    temperature=0.1,  # Low temperature for accuracy
                    response_format={"type": "json_object"}
                )
                
                facts_data = json.loads(response.choices[0].message.content)
            
            else:
                # Fallback or alternative extraction method
                facts_data = self.extract_facts_regex(text, structure)
            
            # Convert to ExtractedFact objects
            facts = []
            for fact_dict in facts_data.get("facts", []):
                # Generate APA citation
                citation = self.generate_apa_citation(
                    fact_dict,
                    metadata,
                    structure.get("total_pages", 0)
                )
                
                facts.append(ExtractedFact(
                    fact=fact_dict["fact"],
                    location=fact_dict["location"],
                    page_number=fact_dict.get("page_number"),
                    section=fact_dict.get("section"),
                    citation_apa=citation,
                    confidence=fact_dict.get("confidence", 0.8),
                    category=fact_dict.get("category", "general")
                ))
            
            return facts
            
        except Exception as e:
            logger.error(f"Fact extraction failed: {e}")
            return []
    
    def generate_apa_citation(
        self,
        fact_dict: Dict,
        metadata: Dict,
        total_pages: int
    ) -> str:
        """Generate APA 7th edition citation for a fact"""
        
        # Base citation components
        title = metadata.get("title", "Untitled Document")
        year = metadata.get("published_date", datetime.now().year)
        
        if isinstance(year, str):
            year = year[:4]  # Extract year from date string
        
        # Handle different document types
        doc_type = metadata.get("content_type", "document")
        
        if doc_type == "statute":
            # Statute citation format
            jurisdiction = metadata.get("jurisdiction", "").title()
            citation = f"{jurisdiction} {title}"
            if fact_dict.get("section"):
                citation += f" § {fact_dict['section']}"
            citation += f" ({year})"
            
        elif doc_type == "case_law":
            # Case citation format
            citation = f"{title}, {metadata.get('citation_format', '')} ({year})"
            
        elif doc_type == "regulation":
            # Regulation citation format
            citation = f"{title}, {metadata.get('citation_format', '')} ({year})"
            
        else:
            # Generic document citation
            citation = f"{title} ({year})"
        
        # Add page reference if available
        if fact_dict.get("page_number"):
            citation += f", p. {fact_dict['page_number']}"
        elif fact_dict.get("location"):
            citation += f", {fact_dict['location']}"
        
        return citation
    
    def extract_facts_regex(self, text: str, structure: Dict) -> Dict:
        """Fallback regex-based fact extraction"""
        facts = []
        
        # Patterns for common legal language
        requirement_patterns = [
            r"shall\s+([^.]+\.)",
            r"must\s+([^.]+\.)",
            r"required to\s+([^.]+\.)",
            r"obligation to\s+([^.]+\.)"
        ]
        
        penalty_patterns = [
            r"penalty of\s+([^.]+\.)",
            r"fine of\s+([^.]+\.)",
            r"imprisonment\s+([^.]+\.)",
            r"liable for\s+([^.]+\.)"
        ]
        
        for pattern_list, category in [
            (requirement_patterns, "requirement"),
            (penalty_patterns, "penalty")
        ]:
            for pattern in pattern_list:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    # Find page number
                    page_num = None
                    for page in structure["pages"]:
                        if page["char_start"] <= match.start() <= page["char_end"]:
                            page_num = page["number"]
                            break
                    
                    facts.append({
                        "fact": match.group(0).strip(),
                        "location": f"p. {page_num}" if page_num else "document",
                        "page_number": page_num,
                        "category": category,
                        "confidence": 0.7
                    })
        
        return {"facts": facts}
    
    def generate_summaries(
        self,
        text: str,
        facts: List[ExtractedFact],
        metadata: Dict
    ) -> DocumentSummary:
        """Generate multiple summary formats"""
        
        # Prepare fact summary for context
        fact_summary = "\n".join([
            f"- {fact.fact} ({fact.category})"
            for fact in facts[:20]  # Top 20 facts
        ])
        
        summary_prompt = f"""
        Create three types of summaries for this legal document.
        
        Document Type: {metadata.get('content_type', 'legal document')}
        Jurisdiction: {metadata.get('jurisdiction', 'unknown')}
        Practice Area: {metadata.get('practice_areas', 'unknown')}
        
        Key Facts Found:
        {fact_summary}
        
        Document Text (excerpt):
        {text[:6000]}
        
        Please provide:
        
        1. EXECUTIVE SUMMARY (300-500 words):
           - Purpose and scope of the document
           - Key legal provisions and requirements
           - Main compliance obligations
           - Critical deadlines or timeframes
           - Who is affected and how
        
        2. BULLET POINTS (5-10 bullets):
           - Most important takeaways
           - Action items for compliance
           - Key dates and deadlines
           - Notable penalties or consequences
           - Exceptions or special considerations
        
        3. CONCLUSION (100-150 words):
           - Main impact on affected parties
           - Next steps or recommendations
           - Overall significance
        
        Write for an audience of legal professionals and business executives.
        Be precise, clear, and actionable.
        """
        
        try:
            if self.use_claude:
                response = self.anthropic_client.messages.create(
                    model=self.summary_model,
                    max_tokens=2000,
                    temperature=0.3,
                    messages=[{
                        "role": "user",
                        "content": summary_prompt
                    }]
                )
                
                summary_text = response.content[0].text
                
            else:
                response = self.openai_client.chat.completions.create(
                    model=self.summary_model,
                    messages=[
                        {"role": "system", "content": "You are a legal document summarization expert."},
                        {"role": "user", "content": summary_prompt}
                    ],
                    temperature=0.3
                )
                
                summary_text = response.choices[0].message.content
            
            # Parse the response
            summary = self.parse_summary_response(summary_text)
            
            # Extract key takeaways from facts
            summary.key_takeaways = self.extract_key_takeaways(facts, text)
            
            return summary
            
        except Exception as e:
            logger.error(f"Summary generation failed: {e}")
            return DocumentSummary(
                executive_summary="Summary generation failed.",
                bullet_points=["Error in summary generation"],
                conclusion="Unable to generate conclusion.",
                key_takeaways=[]
            )
    
    def parse_summary_response(self, response_text: str) -> DocumentSummary:
        """Parse AI response into structured summary"""
        
        # Extract sections using markers
        exec_match = re.search(
            r"EXECUTIVE SUMMARY.*?:(.*?)(?=BULLET POINTS|$)",
            response_text,
            re.DOTALL | re.IGNORECASE
        )
        
        bullet_match = re.search(
            r"BULLET POINTS.*?:(.*?)(?=CONCLUSION|$)",
            response_text,
            re.DOTALL | re.IGNORECASE
        )
        
        conclusion_match = re.search(
            r"CONCLUSION.*?:(.*?)$",
            response_text,
            re.DOTALL | re.IGNORECASE
        )
        
        # Extract content
        executive_summary = exec_match.group(1).strip() if exec_match else ""
        
        # Parse bullet points
        bullet_text = bullet_match.group(1).strip() if bullet_match else ""
        bullets = []
        for line in bullet_text.split('\n'):
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                bullets.append(line.lstrip('-•* '))
        
        conclusion = conclusion_match.group(1).strip() if conclusion_match else ""
        
        return DocumentSummary(
            executive_summary=executive_summary,
            bullet_points=bullets,
            conclusion=conclusion,
            key_takeaways=[]
        )
    
    def extract_key_takeaways(
        self,
        facts: List[ExtractedFact],
        text: str
    ) -> List[str]:
        """Extract key takeaways from facts"""
        takeaways = []
        
        # Group facts by category
        by_category = {}
        for fact in facts:
            if fact.category not in by_category:
                by_category[fact.category] = []
            by_category[fact.category].append(fact)
        
        # Generate takeaways for each category
        if "requirement" in by_category:
            reqs = by_category["requirement"][:3]
            if reqs:
                takeaways.append(
                    f"Key Requirements: {len(by_category['requirement'])} legal obligations identified"
                )
        
        if "penalty" in by_category:
            penalties = by_category["penalty"]
            max_penalty = self.extract_max_penalty(penalties)
            if max_penalty:
                takeaways.append(f"Maximum Penalty: {max_penalty}")
        
        if "deadline" in by_category:
            deadlines = by_category["deadline"][:2]
            for deadline in deadlines:
                takeaways.append(f"Important Deadline: {deadline.fact}")
        
        return takeaways
    
    def extract_max_penalty(self, penalty_facts: List[ExtractedFact]) -> Optional[str]:
        """Extract maximum penalty amount from penalty facts"""
        amounts = []
        
        for fact in penalty_facts:
            # Extract dollar amounts
            matches = re.findall(r"\$[\d,]+(?:\.\d{2})?", fact.fact)
            for match in matches:
                amount = int(match.replace('$', '').replace(',', '').split('.')[0])
                amounts.append((amount, match))
        
        if amounts:
            max_amount = max(amounts, key=lambda x: x[0])
            return max_amount[1]
        
        return None
    
    def enrich_metadata(
        self,
        original_metadata: Dict,
        facts: List[ExtractedFact],
        summaries: DocumentSummary,
        full_text: str
    ) -> Dict[str, any]:
        """Combine all preprocessing results into enriched metadata"""
        
        # Convert facts to JSON format
        facts_json = []
        for fact in facts:
            facts_json.append({
                "fact": fact.fact,
                "location": fact.location,
                "citation_apa": fact.citation_apa,
                "confidence": fact.confidence,
                "category": fact.category
            })
        
        # Prepare enriched metadata
        enriched = original_metadata.copy()
        
        # Add preprocessing fields
        enriched.update({
            # Fact extraction fields
            "extracted_facts": json.dumps(facts_json),
            "fact_locations": " | ".join([f.location for f in facts]),
            "fact_count": len(facts),
            "key_findings": " ".join([f.fact for f in facts if f.confidence > 0.9][:5]),
            
            # Summary fields
            "executive_summary": summaries.executive_summary,
            "summary_bullet_points": "\n".join(summaries.bullet_points),
            "summary_conclusion": summaries.conclusion,
            "key_takeaways": "\n".join(summaries.key_takeaways),
            
            # Original text (kept for deep dive)
            "content_text": full_text,
            
            # Preprocessing metadata
            "preprocessing_version": "1.0",
            "preprocessing_date": datetime.now().isoformat(),
            "fact_extraction_model": self.fact_model,
            "summary_model": self.summary_model
        })
        
        # Add hierarchical categorization if not present
        if "jurisdiction_country" not in enriched:
            enriched.update(self.infer_hierarchical_metadata(full_text, facts))
        
        return enriched
    
    def infer_hierarchical_metadata(
        self,
        text: str,
        facts: List[ExtractedFact]
    ) -> Dict[str, str]:
        """Infer hierarchical jurisdiction and practice area from content"""
        
        metadata = {}
        
        # Jurisdiction inference
        if "federal" in text.lower() or "united states" in text.lower():
            metadata["jurisdiction_country"] = "united_states"
            
        # State detection
        state_mentions = {
            "texas": text.lower().count("texas"),
            "california": text.lower().count("california"),
            "new_york": text.lower().count("new york"),
            # Add more states as needed
        }
        
        if state_mentions:
            top_state = max(state_mentions, key=state_mentions.get)
            if state_mentions[top_state] > 3:  # Threshold
                metadata["jurisdiction_state"] = top_state
                metadata["jurisdiction_country"] = "united_states"
        
        # Practice area inference from facts
        practice_indicators = {
            "employment": ["employee", "employer", "workplace", "discrimination"],
            "personal_injury": ["injury", "accident", "negligence", "damages"],
            "corporate": ["corporation", "shareholder", "merger", "acquisition"],
            # Add more indicators
        }
        
        practice_scores = {}
        fact_text = " ".join([f.fact for f in facts])
        
        for practice, indicators in practice_indicators.items():
            score = sum(1 for ind in indicators if ind in fact_text.lower())
            if score > 0:
                practice_scores[practice] = score
        
        if practice_scores:
            top_practice = max(practice_scores, key=practice_scores.get)
            metadata["practice_area_primary"] = self.map_to_primary_practice(top_practice)
            metadata["practice_area_secondary"] = top_practice
        
        return metadata
    
    def map_to_primary_practice(self, secondary: str) -> str:
        """Map secondary practice area to primary category"""
        mapping = {
            "employment": "labor_employment",
            "discrimination": "labor_employment",
            "personal_injury": "litigation",
            "medical_malpractice": "litigation",
            "contracts": "corporate",
            "mergers": "corporate",
            # Add more mappings
        }
        return mapping.get(secondary, "general")


# Batch Processing Class
class BatchPreprocessor:
    """Handles batch preprocessing of multiple documents"""
    
    def __init__(self, preprocessor: LegalDocumentPreprocessor):
        self.preprocessor = preprocessor
        self.processed_count = 0
        self.failed_count = 0
        
    def process_directory(
        self,
        directory_path: str,
        output_path: str,
        file_pattern: str = "*.pdf",
        batch_size: int = 10,
        delay_seconds: float = 1.0
    ):
        """Process all documents in a directory"""
        import glob
        import time
        from pathlib import Path
        
        # Find all matching files
        files = glob.glob(f"{directory_path}/{file_pattern}")
        logger.info(f"Found {len(files)} files to process")
        
        # Process in batches
        for i in range(0, len(files), batch_size):
            batch = files[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}/{(len(files) + batch_size - 1)//batch_size}")
            
            for file_path in batch:
                try:
                    # Extract base metadata from filename/path
                    base_metadata = self.extract_base_metadata(file_path)
                    
                    # Preprocess
                    enriched = self.preprocessor.preprocess_document(
                        file_path,
                        base_metadata
                    )
                    
                    # Save enriched metadata
                    output_file = Path(output_path) / f"{Path(file_path).stem}_enriched.json"
                    with open(output_file, 'w') as f:
                        json.dump(enriched, f, indent=2)
                    
                    self.processed_count += 1
                    logger.info(f"Processed: {file_path}")
                    
                except Exception as e:
                    self.failed_count += 1
                    logger.error(f"Failed to process {file_path}: {e}")
                
                # Rate limiting
                time.sleep(delay_seconds)
            
            logger.info(f"Batch complete. Total processed: {self.processed_count}, Failed: {self.failed_count}")
    
    def extract_base_metadata(self, file_path: str) -> Dict:
        """Extract metadata from file path and name"""
        from pathlib import Path
        
        path_parts = Path(file_path).parts
        filename = Path(file_path).stem
        
        metadata = {
            "title": filename.replace('_', ' ').replace('-', ' ').title(),
            "source_file": file_path,
            "pdf_path": file_path
        }
        
        # Try to infer jurisdiction from path
        for part in path_parts:
            if part.lower() in ["texas", "california", "federal", "us"]:
                metadata["jurisdiction"] = part.lower()
                break
        
        # Try to infer document type
        if "statute" in filename.lower():
            metadata["content_type"] = "statute"
        elif "case" in filename.lower():
            metadata["content_type"] = "case_law"
        elif "reg" in filename.lower():
            metadata["content_type"] = "regulation"
        
        return metadata
```

## Usage Examples

### Single Document Processing

```python
# Initialize preprocessor
preprocessor = LegalDocumentPreprocessor(
    openai_api_key="your-key",
    anthropic_api_key="your-key",
    use_gpt4=True,
    use_claude=True
)

# Process a single document
metadata = {
    "title": "Texas Labor Code Chapter 21",
    "jurisdiction": "texas",
    "practice_areas": "employment,discrimination",
    "content_type": "statute",
    "published_date": "2023-01-01"
}

enriched = preprocessor.preprocess_document(
    "texas_labor_code_ch21.pdf",
    metadata
)

# Enriched metadata now contains:
# - extracted_facts: JSON array of facts with citations
# - executive_summary: One-page summary
# - summary_bullet_points: Key points
# - fact_count: Number of facts found
# etc.
```

### Batch Processing

```python
# Initialize batch processor
batch_processor = BatchPreprocessor(preprocessor)

# Process entire directory
batch_processor.process_directory(
    directory_path="/data/legal_documents/texas",
    output_path="/data/preprocessed",
    file_pattern="*.pdf",
    batch_size=10,
    delay_seconds=1.0  # Rate limiting
)
```

### Integration with Superlinked Ingestion

```python
import requests
import json

def ingest_preprocessed_document(enriched_metadata: Dict):
    """Ingest preprocessed document into Superlinked"""
    
    # Prepare for Superlinked API
    document = {
        "id": enriched_metadata.get("id", str(uuid.uuid4())),
        "title": enriched_metadata["title"],
        "content_text": enriched_metadata["content_text"],
        
        # Preprocessing fields
        "extracted_facts": enriched_metadata["extracted_facts"],
        "fact_locations": enriched_metadata["fact_locations"],
        "fact_count": enriched_metadata["fact_count"],
        "key_findings": enriched_metadata["key_findings"],
        "executive_summary": enriched_metadata["executive_summary"],
        "summary_bullet_points": enriched_metadata["summary_bullet_points"],
        "summary_conclusion": enriched_metadata["summary_conclusion"],
        
        # Hierarchical fields
        "jurisdiction_country": enriched_metadata.get("jurisdiction_country", ""),
        "jurisdiction_state": enriched_metadata.get("jurisdiction_state", ""),
        "jurisdiction_city": enriched_metadata.get("jurisdiction_city", ""),
        
        # Other metadata
        "published_date": enriched_metadata.get("published_date", ""),
        "content_type": enriched_metadata.get("content_type", ""),
        "practice_areas": enriched_metadata.get("practice_areas", ""),
        
        # Set as full document (not chunk)
        "is_chunk": "false"
    }
    
    # Send to Superlinked
    response = requests.post(
        "http://localhost:8080/api/v1/ingest",
        json={"documents": [document]},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        logger.info(f"Successfully ingested: {document['title']}")
    else:
        logger.error(f"Ingestion failed: {response.text}")
```

## Fact Extraction Patterns

### Legal Requirements
```python
requirement_patterns = {
    "mandatory": [
        r"shall\s+([^.]+)",
        r"must\s+([^.]+)",
        r"is required to\s+([^.]+)",
        r"has a duty to\s+([^.]+)"
    ],
    "prohibitive": [
        r"shall not\s+([^.]+)",
        r"must not\s+([^.]+)",
        r"is prohibited from\s+([^.]+)",
        r"may not\s+([^.]+)"
    ],
    "permissive": [
        r"may\s+([^.]+)",
        r"is authorized to\s+([^.]+)",
        r"has the right to\s+([^.]+)"
    ]
}
```

### Penalty Extraction
```python
penalty_patterns = {
    "monetary": [
        r"fine(?:s)? of\s+\$?([\d,]+)",
        r"penalty of\s+\$?([\d,]+)",
        r"not (?:to )?exceed\s+\$?([\d,]+)",
        r"damages of\s+\$?([\d,]+)"
    ],
    "imprisonment": [
        r"imprisonment for\s+(\d+\s+\w+)",
        r"incarceration of\s+(\d+\s+\w+)",
        r"jail term of\s+(\d+\s+\w+)"
    ],
    "license": [
        r"revocation of\s+(\w+\s+license)",
        r"suspension of\s+(\w+\s+license)",
        r"loss of\s+(\w+\s+license)"
    ]
}
```

### Deadline Detection
```python
deadline_patterns = {
    "specific_date": [
        r"by\s+(\w+\s+\d{1,2},?\s+\d{4})",
        r"no later than\s+(\w+\s+\d{1,2},?\s+\d{4})",
        r"on or before\s+(\w+\s+\d{1,2},?\s+\d{4})"
    ],
    "relative_time": [
        r"within\s+(\d+\s+days)",
        r"not more than\s+(\d+\s+days)",
        r"at least\s+(\d+\s+days)\s+before"
    ],
    "recurring": [
        r"annually",
        r"monthly",
        r"quarterly",
        r"every\s+(\d+\s+\w+)"
    ]
}
```

## Quality Assurance

### Fact Validation
```python
def validate_extracted_facts(facts: List[ExtractedFact]) -> Dict[str, any]:
    """Validate quality of extracted facts"""
    
    validation_results = {
        "total_facts": len(facts),
        "high_confidence": sum(1 for f in facts if f.confidence > 0.8),
        "low_confidence": sum(1 for f in facts if f.confidence < 0.5),
        "categories": {},
        "issues": []
    }
    
    # Check category distribution
    for fact in facts:
        if fact.category not in validation_results["categories"]:
            validation_results["categories"][fact.category] = 0
        validation_results["categories"][fact.category] += 1
    
    # Check for common issues
    if len(facts) < 5:
        validation_results["issues"].append("Very few facts extracted")
    
    if validation_results["low_confidence"] > len(facts) * 0.3:
        validation_results["issues"].append("Many low-confidence facts")
    
    # Check citation completeness
    missing_citations = sum(1 for f in facts if not f.citation_apa)
    if missing_citations > 0:
        validation_results["issues"].append(f"{missing_citations} facts missing citations")
    
    return validation_results
```

### Summary Quality Check
```python
def assess_summary_quality(summary: DocumentSummary) -> Dict[str, any]:
    """Assess quality of generated summaries"""
    
    quality_metrics = {
        "executive_length": len(summary.executive_summary.split()),
        "bullet_count": len(summary.bullet_points),
        "conclusion_length": len(summary.conclusion.split()),
        "key_takeaway_count": len(summary.key_takeaways),
        "issues": []
    }
    
    # Check lengths
    if quality_metrics["executive_length"] < 200:
        quality_metrics["issues"].append("Executive summary too short")
    elif quality_metrics["executive_length"] > 600:
        quality_metrics["issues"].append("Executive summary too long")
    
    if quality_metrics["bullet_count"] < 5:
        quality_metrics["issues"].append("Too few bullet points")
    elif quality_metrics["bullet_count"] > 10:
        quality_metrics["issues"].append("Too many bullet points")
    
    # Check content quality
    if not any(word in summary.executive_summary.lower() 
              for word in ["require", "must", "shall", "obligation"]):
        quality_metrics["issues"].append("Summary may lack legal requirements")
    
    return quality_metrics
```

## Performance Optimization

### Concurrent Processing
```python
import concurrent.futures
import asyncio

class ConcurrentPreprocessor:
    """Process multiple documents concurrently"""
    
    def __init__(self, num_workers: int = 4):
        self.num_workers = num_workers
        
    async def process_documents_async(
        self,
        documents: List[Tuple[str, Dict]],
        preprocessor: LegalDocumentPreprocessor
    ):
        """Process documents concurrently"""
        
        loop = asyncio.get_event_loop()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            tasks = []
            
            for file_path, metadata in documents:
                task = loop.run_in_executor(
                    executor,
                    preprocessor.preprocess_document,
                    file_path,
                    metadata
                )
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
        return results
```

### Caching for Efficiency
```python
from functools import lru_cache
import hashlib

class CachedPreprocessor(LegalDocumentPreprocessor):
    """Preprocessor with caching for repeated documents"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = {}
    
    def get_document_hash(self, file_path: str) -> str:
        """Generate hash of document content"""
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    
    def preprocess_document(self, file_path: str, metadata: Dict) -> Dict:
        """Check cache before processing"""
        
        doc_hash = self.get_document_hash(file_path)
        cache_key = f"{doc_hash}_{json.dumps(metadata, sort_keys=True)}"
        
        if cache_key in self.cache:
            logger.info(f"Using cached result for: {file_path}")
            return self.cache[cache_key]
        
        # Process normally
        result = super().preprocess_document(file_path, metadata)
        
        # Cache result
        self.cache[cache_key] = result
        
        return result
```

## Monitoring and Logging

### Preprocessing Metrics
```python
class PreprocessingMetrics:
    """Track preprocessing performance and quality"""
    
    def __init__(self):
        self.metrics = {
            "documents_processed": 0,
            "total_facts_extracted": 0,
            "average_facts_per_doc": 0,
            "processing_times": [],
            "error_count": 0,
            "api_costs": {
                "openai": 0,
                "anthropic": 0
            }
        }
    
    def log_processing(
        self,
        doc_id: str,
        facts_count: int,
        processing_time: float,
        tokens_used: Dict[str, int]
    ):
        """Log metrics for a processed document"""
        
        self.metrics["documents_processed"] += 1
        self.metrics["total_facts_extracted"] += facts_count
        self.metrics["processing_times"].append(processing_time)
        
        # Update averages
        self.metrics["average_facts_per_doc"] = (
            self.metrics["total_facts_extracted"] / 
            self.metrics["documents_processed"]
        )
        
        # Estimate API costs
        self.metrics["api_costs"]["openai"] += tokens_used.get("gpt4", 0) * 0.00003
        self.metrics["api_costs"]["anthropic"] += tokens_used.get("claude", 0) * 0.00001
        
        logger.info(f"Processed {doc_id}: {facts_count} facts in {processing_time:.2f}s")
    
    def generate_report(self) -> str:
        """Generate metrics report"""
        
        avg_time = sum(self.metrics["processing_times"]) / len(self.metrics["processing_times"])
        
        report = f"""
        Preprocessing Metrics Report
        ===========================
        Documents Processed: {self.metrics['documents_processed']}
        Total Facts Extracted: {self.metrics['total_facts_extracted']}
        Average Facts per Document: {self.metrics['average_facts_per_doc']:.1f}
        Average Processing Time: {avg_time:.2f} seconds
        Error Count: {self.metrics['error_count']}
        
        Estimated API Costs:
        - OpenAI: ${self.metrics['api_costs']['openai']:.2f}
        - Anthropic: ${self.metrics['api_costs']['anthropic']:.2f}
        - Total: ${sum(self.metrics['api_costs'].values()):.2f}
        """
        
        return report
```

## Error Handling

### Robust Error Recovery
```python
class RobustPreprocessor(LegalDocumentPreprocessor):
    """Preprocessor with comprehensive error handling"""
    
    def preprocess_document_safe(
        self,
        file_path: str,
        metadata: Dict,
        max_retries: int = 3
    ) -> Dict:
        """Process with retries and fallbacks"""
        
        for attempt in range(max_retries):
            try:
                return self.preprocess_document(file_path, metadata)
                
            except openai.RateLimitError:
                logger.warning(f"Rate limit hit, waiting {2**attempt} seconds")
                time.sleep(2**attempt)
                
            except anthropic.APIError as e:
                logger.error(f"Anthropic API error: {e}")
                # Fallback to OpenAI only
                self.use_claude = False
                
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                
                if attempt == max_retries - 1:
                    # Final fallback - return minimal metadata
                    return self.create_fallback_metadata(file_path, metadata, str(e))
        
        return self.create_fallback_metadata(file_path, metadata, "Max retries exceeded")
    
    def create_fallback_metadata(
        self,
        file_path: str,
        metadata: Dict,
        error_msg: str
    ) -> Dict:
        """Create minimal metadata when preprocessing fails"""
        
        fallback = metadata.copy()
        fallback.update({
            "preprocessing_error": error_msg,
            "preprocessing_status": "failed",
            "extracted_facts": "[]",
            "fact_count": 0,
            "executive_summary": "Preprocessing failed - manual review required",
            "summary_bullet_points": "• Document requires manual processing",
            "content_text": self.extract_text_basic(file_path)
        })
        
        return fallback
```

## Best Practices

### 1. Document Preparation
- Ensure PDFs have searchable text (OCR if needed)
- Remove password protection
- Split very large documents (>100 pages) into sections
- Maintain consistent file naming conventions

### 2. API Management
- Use environment variables for API keys
- Implement rate limiting and backoff strategies
- Monitor API usage and costs
- Consider using local models for high-volume processing

### 3. Quality Control
- Manually review a sample of preprocessed documents
- Track confidence scores and flag low-confidence extractions
- Maintain a feedback loop for improving prompts
- Version control preprocessing configurations

### 4. Performance Tuning
- Process documents in parallel when possible
- Cache results for frequently accessed documents
- Use streaming for large documents
- Optimize prompt lengths to reduce token usage

---

*Last Updated: 2024*
*Version: 1.0*