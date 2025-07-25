#!/usr/bin/env python3
"""
Metadata Analysis - Examine preprocessing vs loading gaps
========================================================

Analyzes what fields we're extracting in preprocessing vs what we're 
successfully loading into Superlinked to identify extraction gaps.
"""

import json
import requests
from pathlib import Path
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetadataAnalyzer:
    """Analyze metadata extraction and loading effectiveness"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.metadata_dir = Path("output/metadata")
        
    def analyze_preprocessing_extraction(self):
        """Analyze what fields are being extracted during preprocessing"""
        
        print("🔍 Analyzing Preprocessing Extraction")
        print("=" * 50)
        
        metadata_files = list(self.metadata_dir.glob("*_metadata.json"))
        
        if not metadata_files:
            print("❌ No metadata files found")
            return
        
        print(f"📄 Found {len(metadata_files)} metadata files")
        
        # Analyze field coverage across files
        field_coverage = defaultdict(int)
        field_types = defaultdict(set)
        total_files = len(metadata_files)
        
        # Sample analysis
        sample_data = []
        
        for metadata_file in metadata_files[:10]:  # Analyze first 10 files
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                sample_data.append({
                    'file': metadata_file.name,
                    'id': metadata.get('id'),
                    'title': metadata.get('title', '')[:50] + '...',
                    'content_type': metadata.get('content_type'),
                    'jurisdiction_state': metadata.get('jurisdiction_state'),
                    'fact_count': metadata.get('fact_count', 0),
                    'total_pages': metadata.get('total_pages', 0),
                    'ai_model': metadata.get('ai_model', ''),
                    'has_executive_summary': bool(metadata.get('executive_summary')),
                    'has_key_findings': bool(metadata.get('key_findings')),
                    'has_extracted_facts': bool(metadata.get('extracted_facts'))
                })
                
                # Track field coverage
                for field, value in metadata.items():
                    if value:  # Only count non-empty fields
                        field_coverage[field] += 1
                        field_types[field].add(type(value).__name__)
                
            except Exception as e:
                logger.error(f"Error processing {metadata_file}: {e}")
        
        # Display field coverage analysis
        print(f"\n📊 Field Coverage Analysis (across {total_files} files)")
        print("-" * 60)
        
        sorted_fields = sorted(field_coverage.items(), key=lambda x: x[1], reverse=True)
        
        for field, count in sorted_fields:
            coverage_pct = (count / total_files) * 100
            types = ', '.join(field_types[field])
            print(f"  {field:<25} {count:>3}/{total_files} ({coverage_pct:>5.1f}%) [{types}]")
        
        # Display sample data
        print(f"\n📋 Sample Extracted Data")
        print("-" * 60)
        
        for sample in sample_data[:5]:
            print(f"\nFile: {sample['file']}")
            print(f"  ID: {sample['id']}")
            print(f"  Title: {sample['title']}")
            print(f"  Type: {sample['content_type']}")
            print(f"  Jurisdiction: {sample['jurisdiction_state']}")
            print(f"  Facts: {sample['fact_count']}")
            print(f"  Pages: {sample['total_pages']}")
            print(f"  AI Model: {sample['ai_model']}")
            print(f"  Has Summary: {sample['has_executive_summary']}")
            print(f"  Has Findings: {sample['has_key_findings']}")
            print(f"  Has Facts: {sample['has_extracted_facts']}")
        
        return field_coverage, sample_data
    
    def analyze_loading_process(self):
        """Analyze what's happening during the loading process"""
        
        print(f"\n🔄 Analyzing Loading Process")
        print("=" * 50)
        
        # Check if Superlinked is running
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            print("✅ Superlinked server is accessible")
        except Exception as e:
            print(f"❌ Cannot connect to Superlinked: {e}")
            return
        
        # Test a basic search to see what fields are returned
        try:
            search_response = requests.post(
                f"{self.base_url}/api/v1/search/discovery_search",
                json={"search_query": "medical", "limit": 1},
                timeout=10
            )
            search_response.raise_for_status()
            search_data = search_response.json()
            
            print(f"📊 Search Response Analysis")
            print("-" * 30)
            
            if search_data.get('entries'):
                entry = search_data['entries'][0]
                print(f"Entry structure: {list(entry.keys())}")
                print(f"Fields structure: {list(entry.get('fields', {}).keys())}")
                print(f"Metadata structure: {list(entry.get('metadata', {}).keys())}")
                
                # Check if fields are populated
                fields = entry.get('fields', {})
                if fields:
                    print(f"✅ Fields are populated: {len(fields)} fields")
                    for field, value in list(fields.items())[:5]:
                        print(f"  {field}: {str(value)[:50]}...")
                else:
                    print(f"❌ Fields are empty - this is the issue!")
                
            else:
                print("❌ No search results returned")
                
        except Exception as e:
            print(f"❌ Search test failed: {e}")
    
    def analyze_loading_script_mapping(self):
        """Analyze the loading script to see if there are mapping issues"""
        
        print(f"\n🔧 Analyzing Loading Script Mapping")
        print("=" * 50)
        
        # Load a sample metadata file
        metadata_files = list(self.metadata_dir.glob("*_metadata.json"))
        if not metadata_files:
            print("❌ No metadata files to analyze")
            return
        
        try:
            with open(metadata_files[0], 'r') as f:
                sample_metadata = json.load(f)
            
            print(f"📄 Sample metadata file: {metadata_files[0].name}")
            print(f"Available fields: {list(sample_metadata.keys())}")
            
            # Simulate the loading process
            from load_real_data import SuperlinkedDataLoader
            
            loader = SuperlinkedDataLoader()
            document, original_metadata = loader.load_document(metadata_files[0])
            
            print(f"\n📊 Loading Script Output Analysis")
            print("-" * 40)
            print(f"Document keys created: {len(document.keys())}")
            print(f"Non-empty fields: {sum(1 for v in document.values() if v)}")
            print(f"Empty fields: {sum(1 for v in document.values() if not v)}")
            
            # Show sample mapped fields
            print(f"\n📋 Sample Mapped Fields")
            print("-" * 30)
            for field, value in list(document.items())[:10]:
                if value:
                    value_str = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                    print(f"  {field}: {value_str}")
                else:
                    print(f"  {field}: <EMPTY>")
            
            # Check critical fields
            critical_fields = [
                'title', 'content', 'executive_summary', 'key_findings', 
                'jurisdiction_state', 'practice_area_primary', 'extracted_facts'
            ]
            
            print(f"\n🔍 Critical Fields Analysis")
            print("-" * 30)
            for field in critical_fields:
                value = document.get(field, '<MISSING>')
                status = "✅" if value and value != '<MISSING>' else "❌"
                print(f"  {status} {field}: {'Present' if value and value != '<MISSING>' else 'Empty/Missing'}")
            
            return document, original_metadata
            
        except Exception as e:
            print(f"❌ Loading script analysis failed: {e}")
            return None, None
    
    def identify_extraction_gaps(self):
        """Identify gaps in our extraction process"""
        
        print(f"\n🎯 Identifying Extraction Gaps")
        print("=" * 50)
        
        # Fields we COULD extract but might not be
        potential_fields = {
            # Temporal fields
            'effective_date': 'Extract legal effective dates from document text',
            'last_amended_date': 'Find amendment dates in legal documents',
            'expiration_date': 'Identify expiration dates for regulations',
            
            # Legal hierarchy fields
            'authority_level': 'Classify authority level (federal, state, local)',
            'legal_hierarchy': 'Extract citation hierarchy and dependencies',
            'supersedes': 'Identify what this document supersedes',
            'superseded_by': 'Track if document has been superseded',
            
            # Enhanced content fields
            'penalties_monetary': 'Extract specific monetary penalties',
            'penalties_criminal': 'Extract criminal penalty classifications',
            'deadlines_specific': 'Extract specific deadlines (30 days, 120 days, etc.)',
            'requirements_mandatory': 'Extract mandatory vs optional requirements',
            
            # Practice area enhancements
            'specialties_medical': 'Extract medical specialties mentioned',
            'procedure_types': 'Extract types of legal procedures',
            'court_levels': 'Extract court levels and jurisdictions',
            
            # Document relationships
            'cites_statutes': 'Extract statute citations',
            'cites_cases': 'Extract case law citations',
            'cites_regulations': 'Extract regulation citations',
            
            # Search optimization
            'common_terms': 'Extract frequently used legal terms',
            'synonyms': 'Identify legal synonyms and alternative terms',
            'abbreviations': 'Extract legal abbreviations and acronyms',
            
            # Quality metrics
            'readability_score': 'Calculate document readability',
            'complexity_score': 'Assess legal complexity',
            'citation_density': 'Count citations per page',
        }
        
        print("🚀 Potential Enhancement Fields:")
        print("-" * 40)
        
        for field, description in potential_fields.items():
            print(f"  💡 {field}: {description}")
        
        # Check current vs potential
        field_coverage, _ = self.analyze_preprocessing_extraction()
        current_fields = set(field_coverage.keys())
        potential_field_names = set(potential_fields.keys())
        
        missing_fields = potential_field_names - current_fields
        
        print(f"\n📊 Extraction Coverage Summary:")
        print(f"  Current fields extracted: {len(current_fields)}")
        print(f"  Potential additional fields: {len(missing_fields)}")
        print(f"  Enhancement opportunity: {len(missing_fields)} new fields")
        
        return potential_fields, missing_fields
    
    def recommend_improvements(self):
        """Provide specific recommendations for improving extraction"""
        
        print(f"\n💡 Improvement Recommendations")
        print("=" * 50)
        
        recommendations = [
            {
                "priority": "HIGH",
                "category": "Search Field Population",
                "issue": "Search results return empty fields despite rich metadata",
                "recommendation": "Investigate Superlinked ingestion process - fields may not be properly indexed",
                "action": "Debug load_real_data.py ingestion and verify field mapping"
            },
            {
                "priority": "HIGH", 
                "category": "Temporal Enhancement",
                "issue": "Limited temporal field extraction",
                "recommendation": "Add regex extraction for legal dates (effective dates, amendment dates)",
                "action": "Enhance preprocessing to extract 'effective on', 'amended', 'expires' patterns"
            },
            {
                "priority": "MEDIUM",
                "category": "Legal Hierarchy",
                "issue": "Missing document authority and relationship data",
                "recommendation": "Extract citation networks and legal hierarchy information",
                "action": "Add citation parsing and authority level classification"
            },
            {
                "priority": "MEDIUM",
                "category": "Search Optimization",
                "issue": "Basic keyword extraction only",
                "recommendation": "Enhanced legal term extraction and synonym identification",
                "action": "Implement legal thesaurus and term normalization"
            },
            {
                "priority": "LOW",
                "category": "Quality Metrics",
                "issue": "No document quality or complexity metrics",
                "recommendation": "Add readability and complexity scoring",
                "action": "Implement legal complexity algorithms"
            }
        ]
        
        for rec in recommendations:
            print(f"\n🔹 {rec['priority']} PRIORITY: {rec['category']}")
            print(f"   Issue: {rec['issue']}")
            print(f"   Recommendation: {rec['recommendation']}")
            print(f"   Action: {rec['action']}")
        
        return recommendations

def main():
    """Run comprehensive metadata analysis"""
    
    print("🔍 Comprehensive Metadata Analysis")
    print("=" * 60)
    
    analyzer = MetadataAnalyzer()
    
    # Step 1: Analyze preprocessing extraction
    field_coverage, sample_data = analyzer.analyze_preprocessing_extraction()
    
    # Step 2: Analyze loading process
    analyzer.analyze_loading_process()
    
    # Step 3: Analyze loading script mapping
    document, metadata = analyzer.analyze_loading_script_mapping()
    
    # Step 4: Identify extraction gaps
    potential_fields, missing_fields = analyzer.identify_extraction_gaps()
    
    # Step 5: Provide recommendations
    recommendations = analyzer.recommend_improvements()
    
    print(f"\n🎯 Analysis Complete")
    print("=" * 60)
    print(f"✅ Preprocessing extracts {len(field_coverage)} fields with good coverage")
    print(f"❌ Search results show empty fields - ingestion issue identified")
    print(f"💡 {len(missing_fields)} potential enhancement fields identified")
    print(f"📋 {len(recommendations)} improvement recommendations provided")

if __name__ == "__main__":
    main()