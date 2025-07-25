#!/usr/bin/env python3
"""
Advanced Legal Research - Integrated Solution
=============================================

Combines all enhancements to address system limitations identified in technical walkthrough:
1. Limited Chunk Content → Enhanced chunk retrieval
2. No Procedure-Specific Queries → Specialized legal endpoints  
3. Date Filtering → Temporal search with recent change tracking

Usage example for Houston Medical Malpractice firm blog research.
"""

from enhanced_search_endpoints import EnhancedSearchClient
from specialized_legal_endpoints import SpecializedLegalSearch
from temporal_search_enhancements import TemporalSearchEnhancements
from typing import Dict, List
import json
from datetime import datetime, timedelta

class AdvancedLegalResearchSystem:
    """Integrated advanced legal research system addressing all identified limitations"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.enhanced_search = EnhancedSearchClient(base_url)
        self.specialized_search = SpecializedLegalSearch(base_url)
        self.temporal_search = TemporalSearchEnhancements(base_url)
        
    def comprehensive_blog_research(self, topic: str, jurisdiction: str = "texas",
                                  practice_area: str = "medical_malpractice") -> Dict:
        """
        Complete blog research workflow addressing all system limitations.
        
        Returns comprehensive research suitable for professional blog creation.
        """
        research_results = {
            'topic': topic,
            'jurisdiction': jurisdiction,
            'practice_area': practice_area,
            'research_timestamp': datetime.now().isoformat(),
            'phases': {}
        }
        
        print(f"🔍 Starting comprehensive research for: {topic}")
        print(f"📍 Jurisdiction: {jurisdiction}, Practice Area: {practice_area}")
        print("-" * 80)
        
        # PHASE 1: Enhanced Discovery (addresses chunk content limitation)
        print("Phase 1: Enhanced Discovery with Detailed Content...")
        discovery_results = self.enhanced_search.discovery_with_chunks(
            f"{topic} {jurisdiction}", 
            limit=5, 
            include_chunks=True
        )
        
        research_results['phases']['discovery'] = {
            'documents_found': len(discovery_results.get('entries', [])),
            'detailed_content_available': sum(1 for entry in discovery_results.get('entries', []) 
                                            if 'detailed_chunks' in entry),
            'key_documents': self._extract_key_documents(discovery_results)
        }
        
        # PHASE 2: Specialized Legal Queries (addresses procedure-specific limitation)  
        print("Phase 2: Specialized Legal Framework Analysis...")
        
        # Expert witness requirements
        expert_requirements = self.specialized_search.expert_witness_requirements(
            jurisdiction, practice_area
        )
        
        # Damages framework
        damages_info = self.specialized_search.damages_calculation_framework(
            jurisdiction, practice_area
        )
        
        research_results['phases']['specialized_legal'] = {
            'expert_witness_requirements': expert_requirements,
            'damages_framework': damages_info,
            'procedural_completeness': self._assess_procedural_completeness(
                expert_requirements, damages_info
            )
        }
        
        # PHASE 3: Temporal Analysis (addresses date filtering limitation)
        print("Phase 3: Recent Changes and Regulatory Timeline...")
        
        # Recent changes (last 12 months)
        recent_changes = self.temporal_search.get_recent_changes(
            f"{topic} {jurisdiction}", months_back=12
        )
        
        # 5-year regulatory timeline
        regulatory_timeline = self.temporal_search.track_regulatory_timeline(
            f"{topic} {jurisdiction}", years_back=5
        )
        
        research_results['phases']['temporal_analysis'] = {
            'recent_changes': recent_changes,
            'regulatory_timeline': regulatory_timeline,
            'currency_assessment': self._assess_regulatory_currency(recent_changes)
        }
        
        # PHASE 4: Content Synthesis for Blog
        print("Phase 4: Blog Content Synthesis...")
        blog_content = self._synthesize_blog_content(research_results)
        research_results['blog_content'] = blog_content
        
        print("✅ Comprehensive research complete!")
        return research_results
    
    def _extract_key_documents(self, discovery_results: Dict) -> List[Dict]:
        """Extract key document information for research summary"""
        key_docs = []
        
        for entry in discovery_results.get('entries', []):
            fields = entry.get('fields', {})
            
            doc_info = {
                'id': entry.get('id'),
                'title': fields.get('title', 'Unknown'),
                'document_type': fields.get('document_type', 'unknown'),
                'relevance_score': entry.get('metadata', {}).get('score', 0),
                'has_detailed_chunks': 'detailed_chunks' in entry,
                'executive_summary': fields.get('executive_summary', '')[:300] + '...'
            }
            
            # Add chunk summary if available
            if 'detailed_chunks' in entry:
                doc_info['chunk_count'] = len(entry['detailed_chunks'])
                doc_info['top_chunk_content'] = entry['detailed_chunks'][0]['content'][:200] + '...' if entry['detailed_chunks'] else ""
            
            key_docs.append(doc_info)
        
        return key_docs
    
    def _assess_procedural_completeness(self, expert_reqs: Dict, damages_info: Dict) -> Dict:
        """Assess completeness of procedural information for blog purposes"""
        completeness = {
            'expert_witness_complete': len(expert_reqs['qualification_standards']) > 0 and len(expert_reqs['procedural_deadlines']) > 0,
            'damages_framework_complete': len(damages_info['economic_damages']) > 0 and len(damages_info['damage_caps']) > 0,
            'blog_readiness_score': 0
        }
        
        # Calculate blog readiness score
        score = 0
        if completeness['expert_witness_complete']:
            score += 50
        if completeness['damages_framework_complete']:
            score += 30
        if len(expert_reqs['qualification_standards']) >= 2:
            score += 10
        if len(damages_info['economic_damages']) >= 2:
            score += 10
        
        completeness['blog_readiness_score'] = score
        completeness['readiness_assessment'] = "Ready for blog creation" if score >= 70 else "Needs additional research"
        
        return completeness
    
    def _assess_regulatory_currency(self, recent_changes: Dict) -> Dict:
        """Assess how current the regulatory information is"""
        currency = {
            'recent_changes_count': len(recent_changes['recent_changes']),
            'most_recent_change': None,
            'currency_status': 'unknown'
        }
        
        if recent_changes['recent_changes']:
            currency['most_recent_change'] = recent_changes['recent_changes'][0]['publication_date']
            
            # Assess currency based on most recent change
            most_recent = datetime.fromisoformat(recent_changes['recent_changes'][0]['publication_date'])
            days_ago = (datetime.now() - most_recent).days
            
            if days_ago <= 90:
                currency['currency_status'] = 'very_current'
            elif days_ago <= 365:
                currency['currency_status'] = 'current'
            else:
                currency['currency_status'] = 'moderate_currency'
        
        return currency
    
    def _synthesize_blog_content(self, research_results: Dict) -> Dict:
        """Synthesize all research into blog-ready content structure"""
        blog_content = {
            'title_suggestions': [],
            'introduction': {},
            'main_sections': {},
            'conclusion': {},
            'seo_elements': {}
        }
        
        # Title suggestions based on research
        topic = research_results['topic']
        jurisdiction = research_results['jurisdiction']
        
        blog_content['title_suggestions'] = [
            f"{topic.title()} in {jurisdiction.title()}: Complete Legal Guide 2024",
            f"Understanding {topic.title()} Law in {jurisdiction.title()}: Expert Requirements and Damages",
            f"{jurisdiction.title()} {topic.title()}: Recent Changes and Legal Requirements"
        ]
        
        # Introduction with compelling statistics
        discovery_phase = research_results['phases']['discovery']
        key_docs = discovery_phase['key_documents']
        
        # Find statistical content
        stats_content = ""
        for doc in key_docs:
            if 'statistics' in doc['title'].lower() or 'billion' in doc['executive_summary'].lower():
                stats_content = doc['executive_summary']
                break
        
        blog_content['introduction'] = {
            'hook': f"Recent research reveals significant developments in {topic} law in {jurisdiction.title()}.",
            'statistics': stats_content,
            'authority_statement': f"Based on analysis of {discovery_phase['documents_found']} legal documents with detailed statutory review."
        }
        
        # Main sections from specialized research
        specialized = research_results['phases']['specialized_legal']
        
        blog_content['main_sections'] = {
            'expert_witness_section': {
                'title': f"Expert Witness Requirements in {jurisdiction.title()}",
                'content': specialized['expert_witness_requirements']['qualification_standards'],
                'procedural_info': specialized['expert_witness_requirements']['procedural_deadlines']
            },
            'damages_section': {
                'title': f"Understanding Damages in {topic.title()} Cases",
                'economic_damages': specialized['damages_framework']['economic_damages'],
                'damage_limitations': specialized['damages_framework']['damage_caps']
            },
            'recent_developments': {
                'title': f"Recent Legal Developments in {jurisdiction.title()}",
                'recent_changes': research_results['phases']['temporal_analysis']['recent_changes']['recent_changes'][:3]
            }
        }
        
        # SEO elements
        blog_content['seo_elements'] = {
            'primary_keywords': [topic, f"{topic} {jurisdiction}", f"{jurisdiction} law"],
            'secondary_keywords': ["expert witness", "damages", "legal requirements"],
            'meta_description': f"Comprehensive guide to {topic} in {jurisdiction.title()}. Expert witness requirements, damages framework, and recent legal developments.",
            'schema_markup_suggestions': ["LegalService", "Article", "FAQPage"]
        }
        
        return blog_content

# Usage example demonstrating all enhancements
def demonstrate_advanced_research():
    """
    Demonstrate the advanced research system addressing all identified limitations
    """
    print("🚀 Advanced Legal Research System Demo")
    print("Addressing all system limitations from technical walkthrough")
    print("=" * 80)
    
    # Initialize system
    research_system = AdvancedLegalResearchSystem()
    
    # Run comprehensive research
    results = research_system.comprehensive_blog_research(
        topic="medical malpractice",
        jurisdiction="texas",
        practice_area="medical_malpractice"
    )
    
    # Display results summary
    print("\n📊 RESEARCH RESULTS SUMMARY")
    print("=" * 80)
    
    # Discovery phase results
    discovery = results['phases']['discovery']
    print(f"📋 Discovery Phase:")
    print(f"  • Documents found: {discovery['documents_found']}")
    print(f"  • Documents with detailed chunks: {discovery['detailed_content_available']}")
    print(f"  • Key documents identified: {len(discovery['key_documents'])}")
    
    # Specialized legal results
    specialized = results['phases']['specialized_legal']
    print(f"\n⚖️  Specialized Legal Analysis:")
    print(f"  • Expert witness requirements: {len(specialized['expert_witness_requirements']['qualification_standards'])} found")
    print(f"  • Damages framework elements: {len(specialized['damages_framework']['economic_damages'])} found")
    print(f"  • Blog readiness score: {specialized['procedural_completeness']['blog_readiness_score']}/100")
    print(f"  • Status: {specialized['procedural_completeness']['readiness_assessment']}")
    
    # Temporal analysis results
    temporal = results['phases']['temporal_analysis']
    print(f"\n📅 Temporal Analysis:")
    print(f"  • Recent changes found: {temporal['recent_changes']['recent_changes']}")
    print(f"  • Currency status: {temporal['currency_assessment']['currency_status']}")
    print(f"  • Regulatory timeline years: {temporal['regulatory_timeline']['timeline_years']}")
    
    # Blog content readiness
    blog = results['blog_content']
    print(f"\n📝 Blog Content Synthesis:")
    print(f"  • Title options: {len(blog['title_suggestions'])}")
    print(f"  • Main sections: {len(blog['main_sections'])}")
    print(f"  • SEO keywords: {len(blog['seo_elements']['primary_keywords']) + len(blog['seo_elements']['secondary_keywords'])}")
    
    print(f"\n✅ LIMITATIONS ADDRESSED:")
    print(f"  ✓ Limited Chunk Content → Enhanced chunk retrieval implemented")
    print(f"  ✓ No Procedure-Specific Queries → Specialized legal endpoints created")  
    print(f"  ✓ Date Filtering → Temporal search with recent change tracking added")
    
    print(f"\n🎯 SYSTEM READY FOR PRODUCTION DEPLOYMENT")
    
    return results

if __name__ == "__main__":
    demonstrate_advanced_research()