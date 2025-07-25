#!/usr/bin/env python3
"""
Enhanced Preprocessing - Advanced Field Extraction
==================================================

Addresses gaps identified in metadata analysis by adding:
1. Temporal extraction (dates, deadlines, effective periods)
2. Legal hierarchy and citation mapping
3. Enhanced search optimization fields
4. Legal complexity and quality metrics
5. Document relationship tracking
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedFieldExtractor:
    """Enhanced field extraction for legal documents"""
    
    def __init__(self):
        # Legal date patterns
        self.date_patterns = {
            'effective_date': [
                r'effective\s+(?:on\s+)?([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})',
                r'shall\s+take\s+effect\s+(?:on\s+)?([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})',
                r'effective\s+([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})',
                r'beginning\s+([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})'
            ],
            'amendment_date': [
                r'amended\s+(?:on\s+)?([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})',
                r'revised\s+(?:on\s+)?([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})',
                r'modified\s+(?:on\s+)?([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})'
            ],
            'expiration_date': [
                r'expires?\s+(?:on\s+)?([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})',
                r'sunset\s+(?:on\s+)?([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})',
                r'shall\s+expire\s+(?:on\s+)?([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})'
            ]
        }
        
        # Deadline patterns
        self.deadline_patterns = [
            r'within\s+(\d+)\s+(days?|weeks?|months?|years?)',
            r'not\s+later\s+than\s+(\d+)\s+(days?|weeks?|months?|years?)',
            r'(\d+)[-\s](day|week|month|year)\s+(?:deadline|period|notice)',
            r'shall\s+be\s+filed\s+within\s+(\d+)\s+(days?|weeks?|months?|years?)'
        ]
        
        # Legal citation patterns
        self.citation_patterns = {
            'statute_citations': [
                r'(?:Section|Sec\.?|§)\s*(\d+(?:\.\d+)*)',
                r'(\d+)\s+U\.?S\.?C\.?\s*§?\s*(\d+)',
                r'(\d+)\s+Tex\.?\s*(?:Code|Stat\.?)\s*(?:§|Section)?\s*(\d+(?:\.\d+)*)'
            ],
            'case_citations': [
                r'([A-Z][a-z]+(?:\s+v\.?\s+[A-Z][a-z]+)?),?\s*(\d+)\s+([A-Z][a-z\.]+)\s+(\d+)',
                r'(\d+)\s+(F\.?(?:2d|3d)?|S\.?Ct\.?|U\.?S\.?)\s+(\d+)'
            ],
            'regulation_citations': [
                r'(\d+)\s+C\.?F\.?R\.?\s*§?\s*(\d+(?:\.\d+)*)',
                r'(\d+)\s+Fed\.?\s*Reg\.?\s+(\d+)'
            ]
        }
        
        # Legal authority levels
        self.authority_indicators = {
            'federal': ['USC', 'U.S.C', 'CFR', 'C.F.R', 'Fed. Reg', 'Federal'],
            'state': ['Tex.', 'Texas', 'Cal.', 'California', 'N.Y.', 'New York'],
            'local': ['municipal', 'county', 'city', 'local']
        }
        
        # Penalty indicators
        self.penalty_patterns = {
            'monetary': [
                r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
                r'fine\s+(?:of\s+)?(?:up\s+to\s+)?\$?(\d{1,3}(?:,\d{3})*)',
                r'penalty\s+(?:of\s+)?(?:up\s+to\s+)?\$?(\d{1,3}(?:,\d{3})*)'
            ],
            'criminal': [
                r'(Class\s+[ABC]\s+(?:misdemeanor|felony))',
                r'(first|second|third)\s+degree\s+(felony|misdemeanor)',
                r'(misdemeanor|felony)\s+of\s+the\s+(first|second|third)\s+degree'
            ]
        }
        
        # Medical specialties (for medical legal documents)
        self.medical_specialties = [
            'cardiology', 'oncology', 'neurology', 'orthopedic', 'pediatric',
            'obstetric', 'gynecology', 'psychiatry', 'radiology', 'anesthesiology',
            'emergency medicine', 'family medicine', 'internal medicine', 'surgery'
        ]
        
        # Legal terms dictionary
        self.legal_terms = {
            'malpractice': ['negligence', 'professional misconduct', 'standard of care'],
            'liability': ['responsibility', 'accountability', 'legal obligation'],
            'damages': ['compensation', 'monetary award', 'financial remedy'],
            'expert witness': ['professional testimony', 'specialized knowledge', 'expert opinion']
        }
    
    def extract_temporal_fields(self, text: str, metadata: Dict) -> Dict:
        """Extract temporal information from document text"""
        
        temporal_fields = {}
        
        # Extract dates
        for date_type, patterns in self.date_patterns.items():
            dates = []
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                dates.extend(matches)
            
            if dates:
                temporal_fields[date_type] = dates[0]  # Take first match
        
        # Extract deadlines
        deadlines = []
        for pattern in self.deadline_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple) and len(match) == 2:
                    deadlines.append(f"{match[0]} {match[1]}")
        
        if deadlines:
            temporal_fields['deadlines_specific'] = ', '.join(deadlines[:5])  # Top 5
        
        # Calculate temporal score
        temporal_fields['temporal_richness_score'] = len(temporal_fields)
        
        return temporal_fields
    
    def extract_legal_hierarchy(self, text: str, title: str) -> Dict:
        """Extract legal hierarchy and authority information"""
        
        hierarchy_fields = {}
        
        # Determine authority level
        text_lower = text.lower()
        title_lower = title.lower()
        
        authority_level = 'unknown'
        for level, indicators in self.authority_indicators.items():
            if any(indicator.lower() in text_lower or indicator.lower() in title_lower 
                   for indicator in indicators):
                authority_level = level
                break
        
        hierarchy_fields['authority_level'] = authority_level
        
        # Extract citations
        all_citations = []
        for citation_type, patterns in self.citation_patterns.items():
            citations = []
            for pattern in patterns:
                matches = re.findall(pattern, text)
                citations.extend(matches)
            
            if citations:
                hierarchy_fields[citation_type] = citations[:10]  # Limit to 10
                all_citations.extend(citations)
        
        # Calculate citation density
        if all_citations and len(text) > 0:
            hierarchy_fields['citation_density'] = len(all_citations) / (len(text) / 1000)  # Per 1000 chars
        else:
            hierarchy_fields['citation_density'] = 0
        
        return hierarchy_fields
    
    def extract_penalties_and_requirements(self, text: str) -> Dict:
        """Extract penalty information and requirements"""
        
        penalty_fields = {}
        
        # Extract monetary penalties
        monetary_penalties = []
        for pattern in self.penalty_patterns['monetary']:
            matches = re.findall(pattern, text, re.IGNORECASE)
            monetary_penalties.extend(matches)
        
        if monetary_penalties:
            penalty_fields['penalties_monetary'] = ', '.join(monetary_penalties[:5])
        
        # Extract criminal penalties
        criminal_penalties = []
        for pattern in self.penalty_patterns['criminal']:
            matches = re.findall(pattern, text, re.IGNORECASE)
            criminal_penalties.extend([match if isinstance(match, str) else ' '.join(match) 
                                     for match in matches])
        
        if criminal_penalties:
            penalty_fields['penalties_criminal'] = ', '.join(criminal_penalties[:5])
        
        # Extract mandatory vs optional requirements
        mandatory_patterns = [
            r'shall\s+([^.]+)',
            r'must\s+([^.]+)',
            r'required\s+to\s+([^.]+)',
            r'mandatory\s+([^.]+)'
        ]
        
        optional_patterns = [
            r'may\s+([^.]+)',
            r'optional\s+([^.]+)',
            r'at\s+(?:the\s+)?discretion\s+([^.]+)'
        ]
        
        mandatory_reqs = []
        for pattern in mandatory_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            mandatory_reqs.extend(matches[:3])  # Limit
        
        if mandatory_reqs:
            penalty_fields['requirements_mandatory'] = '. '.join(mandatory_reqs)
        
        return penalty_fields
    
    def extract_medical_specialties(self, text: str, title: str) -> List[str]:
        """Extract medical specialties mentioned in the document"""
        
        text_lower = (text + ' ' + title).lower()
        found_specialties = []
        
        for specialty in self.medical_specialties:
            if specialty in text_lower:
                found_specialties.append(specialty)
        
        return found_specialties
    
    def extract_legal_terms_and_synonyms(self, text: str) -> Dict:
        """Extract legal terms and identify synonyms"""
        
        terms_fields = {}
        
        # Find legal terms
        found_terms = []
        term_synonyms = []
        
        text_lower = text.lower()
        
        for main_term, synonyms in self.legal_terms.items():
            if main_term in text_lower:
                found_terms.append(main_term)
                
                # Check for synonyms
                found_synonyms = [syn for syn in synonyms if syn in text_lower]
                if found_synonyms:
                    term_synonyms.extend(found_synonyms)
        
        if found_terms:
            terms_fields['common_terms'] = ', '.join(found_terms)
        
        if term_synonyms:
            terms_fields['synonyms'] = ', '.join(term_synonyms)
        
        # Extract abbreviations
        abbreviation_pattern = r'\b([A-Z]{2,})\b'
        abbreviations = list(set(re.findall(abbreviation_pattern, text)))
        
        if abbreviations:
            terms_fields['abbreviations'] = ', '.join(abbreviations[:10])
        
        return terms_fields
    
    def calculate_quality_metrics(self, text: str, metadata: Dict) -> Dict:
        """Calculate document quality and complexity metrics"""
        
        quality_fields = {}
        
        # Basic readability (simplified Flesch-like)
        if len(text) > 100:
            sentences = len(re.findall(r'[.!?]+', text))
            words = len(text.split())
            avg_sentence_length = words / max(sentences, 1)
            
            # Simplified readability score (lower = more readable)
            readability = min(100, max(0, 100 - (avg_sentence_length - 15) * 2))
            quality_fields['readability_score'] = round(readability, 1)
        else:
            quality_fields['readability_score'] = 50  # Default
        
        # Legal complexity (based on citations, legal terms, sentence length)
        complexity_indicators = [
            len(re.findall(r'(?:Section|Sec\.|§)', text, re.IGNORECASE)),  # Citations
            len(re.findall(r'\b(?:shall|must|required|mandatory)\b', text, re.IGNORECASE)),  # Legal language
            len(re.findall(r'\b(?:notwithstanding|pursuant|thereof|whereas)\b', text, re.IGNORECASE)),  # Complex terms
        ]
        
        complexity_score = min(100, sum(complexity_indicators) / max(len(text) / 1000, 1) * 10)
        quality_fields['complexity_score'] = round(complexity_score, 1)
        
        # Document completeness
        fact_count = metadata.get('fact_count', 0)
        has_summary = bool(metadata.get('executive_summary'))
        has_findings = bool(metadata.get('key_findings'))
        
        completeness_score = (
            (fact_count > 0) * 25 +
            has_summary * 25 +
            has_findings * 25 +
            (len(text) > 1000) * 25
        )
        quality_fields['completeness_score'] = completeness_score
        
        return quality_fields
    
    def extract_document_relationships(self, text: str, title: str) -> Dict:
        """Extract document relationships and supersession information"""
        
        relationship_fields = {}
        
        # Look for supersession language
        supersedes_patterns = [
            r'supersede[sd]?\s+([^.]+)',
            r'replace[sd]?\s+([^.]+)',
            r'amend[sd]?\s+([^.]+)',
            r'repeal[sd]?\s+([^.]+)'
        ]
        
        supersedes = []
        for pattern in supersedes_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            supersedes.extend(matches[:3])
        
        if supersedes:
            relationship_fields['supersedes'] = '. '.join(supersedes)
        
        # Look for references to other documents
        reference_patterns = [
            r'[Ss]ee\s+(?:also\s+)?([^.]+)',
            r'[Cc]f\.\s+([^.]+)',
            r'[Pp]ursuant\s+to\s+([^.]+)'
        ]
        
        references = []
        for pattern in reference_patterns:
            matches = re.findall(pattern, text)
            references.extend(matches[:5])
        
        if references:
            relationship_fields['related_documents'] = '. '.join(references)
        
        return relationship_fields
    
    def enhance_existing_metadata(self, metadata_file: Path) -> Dict:
        """Enhance existing metadata with additional extracted fields"""
        
        try:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            # Get text content for extraction
            text = metadata.get('executive_summary', '') + ' ' + \
                   '. '.join(metadata.get('key_findings', [])) + ' ' + \
                   '. '.join(metadata.get('key_takeaways', []))
            
            title = metadata.get('title', '')
            
            if not text or len(text) < 50:
                logger.warning(f"Insufficient text content for enhancement: {metadata_file.name}")
                return metadata
            
            logger.info(f"Enhancing metadata for: {title[:50]}...")
            
            # Extract enhanced fields
            enhanced_fields = {}
            
            # Temporal fields
            enhanced_fields.update(self.extract_temporal_fields(text, metadata))
            
            # Legal hierarchy
            enhanced_fields.update(self.extract_legal_hierarchy(text, title))
            
            # Penalties and requirements
            enhanced_fields.update(self.extract_penalties_and_requirements(text))
            
            # Medical specialties (if applicable)
            if 'medical' in title.lower() or 'medical' in text.lower():
                specialties = self.extract_medical_specialties(text, title)
                if specialties:
                    enhanced_fields['specialties_medical'] = ', '.join(specialties)
            
            # Legal terms and synonyms
            enhanced_fields.update(self.extract_legal_terms_and_synonyms(text))
            
            # Quality metrics
            enhanced_fields.update(self.calculate_quality_metrics(text, metadata))
            
            # Document relationships
            enhanced_fields.update(self.extract_document_relationships(text, title))
            
            # Add enhancement metadata
            enhanced_fields['enhancement_timestamp'] = datetime.now().isoformat()
            enhanced_fields['enhancement_version'] = '1.0'
            enhanced_fields['enhanced_field_count'] = len([v for v in enhanced_fields.values() if v])
            
            # Merge with existing metadata
            enhanced_metadata = metadata.copy()
            enhanced_metadata.update(enhanced_fields)
            
            logger.info(f"Added {enhanced_fields['enhanced_field_count']} enhanced fields")
            return enhanced_metadata
            
        except Exception as e:
            logger.error(f"Error enhancing metadata for {metadata_file}: {e}")
            return metadata

def enhance_metadata_batch(limit: Optional[int] = None):
    """Enhance a batch of metadata files with additional fields"""
    
    print("🚀 Enhanced Metadata Extraction")
    print("=" * 50)
    
    metadata_dir = Path("output/metadata")
    if not metadata_dir.exists():
        print("❌ No metadata directory found")
        return
    
    metadata_files = list(metadata_dir.glob("*_metadata.json"))
    
    if limit:
        metadata_files = metadata_files[:limit]
    
    print(f"📄 Processing {len(metadata_files)} metadata files...")
    
    extractor = EnhancedFieldExtractor()
    enhanced_count = 0
    
    for metadata_file in metadata_files:
        try:
            # Enhance metadata
            enhanced_metadata = extractor.enhance_existing_metadata(metadata_file)
            
            # Save enhanced version
            enhanced_filename = metadata_file.name.replace('_metadata.json', '_enhanced_metadata.json')
            enhanced_path = metadata_dir / enhanced_filename
            
            with open(enhanced_path, 'w') as f:
                json.dump(enhanced_metadata, f, indent=2)
            
            enhanced_count += 1
            
            # Show sample of enhancements
            if enhanced_count <= 3:
                print(f"\n📋 Enhanced: {metadata_file.name}")
                enhanced_fields = [k for k, v in enhanced_metadata.items() 
                                 if k.startswith(('temporal', 'authority', 'penalties', 'requirements', 
                                                'specialties', 'readability', 'complexity')) and v]
                print(f"   New fields: {enhanced_fields}")
                
        except Exception as e:
            logger.error(f"Failed to enhance {metadata_file}: {e}")
    
    print(f"\n✅ Enhanced {enhanced_count}/{len(metadata_files)} metadata files")
    print(f"📁 Enhanced files saved with '_enhanced_metadata.json' suffix")

def main():
    """Run enhanced metadata extraction"""
    
    import argparse
    parser = argparse.ArgumentParser(description='Enhanced metadata field extraction')
    parser.add_argument('--limit', type=int, help='Limit number of files to process')
    args = parser.parse_args()
    
    enhance_metadata_batch(args.limit)

if __name__ == "__main__":
    main()