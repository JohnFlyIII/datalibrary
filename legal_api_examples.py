"""
Legal Knowledge System API Integration Examples
Demonstrates how to interact with the Superlinked Legal Knowledge System
"""
import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


class LegalKnowledgeAPI:
    """Client for interacting with the Legal Knowledge System APIs"""
    
    def __init__(self, 
                 superlinked_url: str = "http://localhost:8080",
                 api_url: str = "http://localhost:8000"):
        self.superlinked_url = superlinked_url
        self.api_url = api_url
        
    async def ingest_legal_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest a legal document into the system"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.superlinked_url}/ingest/legal_document_source",
                json=document,
                headers={"Content-Type": "application/json"}
            ) as response:
                return await response.json()
    
    async def search_legal_documents(self, 
                                   query: str,
                                   query_type: str = "legal_research_query",
                                   **params) -> Dict[str, Any]:
        """Search legal documents using various query types"""
        query_params = {
            "search_query": query,
            "limit": params.get("limit", 20),
            **params
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.superlinked_url}/query/{query_type}",
                json=query_params,
                headers={"Content-Type": "application/json"}
            ) as response:
                return await response.json()
    
    async def authority_search(self, 
                             query: str,
                             min_authority_score: float = 0.8) -> Dict[str, Any]:
        """Search for authoritative legal sources"""
        return await self.search_legal_documents(
            query=query,
            query_type="authority_query",
            authority_weight=1.5,
            citation_weight=1.2,
            content_weight=0.8,
            limit=15
        )
    
    async def recent_developments(self, 
                                query: str,
                                days_back: int = 90) -> Dict[str, Any]:
        """Find recent legal developments"""
        return await self.search_legal_documents(
            query=query,
            query_type="recent_developments_query",
            recency_weight=1.5,
            content_weight=0.8,
            authority_weight=0.7,
            limit=15
        )
    
    async def content_gap_analysis(self, 
                                 practice_area: str,
                                 keywords: List[str]) -> Dict[str, Any]:
        """Analyze content gaps for blog post opportunities"""
        search_query = f"{practice_area} " + " ".join(keywords)
        return await self.search_legal_documents(
            query=search_query,
            query_type="content_gap_query",
            keywords_weight=1.0,
            content_weight=0.7,
            authority_weight=0.3,  # Lower for gaps
            recency_weight=0.2,   # Older content indicates gaps
            limit=25
        )
    
    async def practice_area_search(self, 
                                 query: str,
                                 practice_area: str) -> Dict[str, Any]:
        """Quick search within a specific practice area"""
        return await self.search_legal_documents(
            query=query,
            query_type="practice_area_query",
            practice_area_weight=1.2,
            title_weight=1.0,
            document_type_weight=0.5,
            limit=10
        )


# =============================================================================
# EXAMPLE USAGE SCENARIOS
# =============================================================================

async def demo_legal_research_workflow():
    """Demonstrate a complete legal research workflow"""
    api = LegalKnowledgeAPI()
    
    print("🏛️  Legal Knowledge System Demo\n")
    
    # 1. Ingest sample legal documents
    print("1️⃣ Ingesting sample legal documents...")
    
    sample_docs = [
        {
            "id": "immigration_001",
            "title": "K-1 Visa Requirements and Recent Policy Changes",
            "content_text": "Recent changes to K-1 visa requirements include new documentation standards and processing timelines. The USCIS has updated form I-129F requirements...",
            "practice_area": "immigration_law",
            "jurisdiction": "federal",
            "authority_level": "primary", 
            "document_type": "regulation",
            "publication_date": int((datetime.now() - timedelta(days=30)).timestamp()),
            "author": "U.S. Citizenship and Immigration Services",
            "citations": ["8 CFR 214.2(k)", "INA 101(a)(15)(K)"],
            "keywords": ["K-1 visa", "fiancé visa", "immigration", "USCIS"],
            "summary": "Updated K-1 visa requirements and processing procedures",
            "authority_score": 0.95,
            "relevance_score": 0.9,
            "citation_count": 45,
            "source_url": "https://uscis.gov/k1-visa-updates",
            "pdf_path": "/docs/k1_visa_updates.pdf",
            "word_count": 2500
        },
        {
            "id": "family_law_001", 
            "title": "Child Custody Modifications in California",
            "content_text": "California Family Code Section 3087 outlines the standards for modifying child custody arrangements. Courts consider the best interests of the child...",
            "practice_area": "family_law",
            "jurisdiction": "california",
            "authority_level": "primary",
            "document_type": "case_law", 
            "publication_date": int((datetime.now() - timedelta(days=60)).timestamp()),
            "author": "California Court of Appeals",
            "citations": ["Cal. Fam. Code § 3087", "In re Marriage of Brown"],
            "keywords": ["child custody", "modification", "best interests", "California"],
            "summary": "Standards for modifying child custody in California courts",
            "authority_score": 0.88,
            "relevance_score": 0.85,
            "citation_count": 23,
            "source_url": "https://courts.ca.gov/custody-modification",
            "pdf_path": "/docs/custody_modification_ca.pdf", 
            "word_count": 1800
        }
    ]
    
    for doc in sample_docs:
        result = await api.ingest_legal_document(doc)
        print(f"   ✅ Ingested: {doc['title']}")
    
    print("\n2️⃣ Searching for K-1 visa information...")
    
    # 2. General legal research
    research_results = await api.search_legal_documents(
        query="K-1 visa requirements documentation",
        content_weight=1.0,
        authority_weight=0.9,
        recency_weight=0.6
    )
    
    print(f"   📚 Found {len(research_results.get('results', []))} relevant documents")
    for result in research_results.get('results', [])[:3]:
        print(f"   📄 {result.get('title', 'Unknown Title')} (Score: {result.get('similarity_score', 0):.3f})")
    
    print("\n3️⃣ Finding authoritative sources...")
    
    # 3. Authority-weighted search
    authority_results = await api.authority_search(
        query="immigration visa requirements",
        min_authority_score=0.8
    )
    
    print(f"   ⚖️  Found {len(authority_results.get('results', []))} authoritative sources")
    for result in authority_results.get('results', [])[:3]:
        authority_score = result.get('authority_score', 0)
        print(f"   📋 {result.get('title', 'Unknown')} (Authority: {authority_score:.2f})")
    
    print("\n4️⃣ Analyzing content gaps for blog opportunities...")
    
    # 4. Content gap analysis
    gap_results = await api.content_gap_analysis(
        practice_area="immigration_law",
        keywords=["green card", "employment visa", "H1B"]
    )
    
    print(f"   🔍 Found {len(gap_results.get('results', []))} potential content opportunities")
    for result in gap_results.get('results', [])[:3]:
        print(f"   💡 Topic opportunity: {result.get('title', 'Unknown')}")
    
    print("\n5️⃣ Checking recent legal developments...")
    
    # 5. Recent developments
    recent_results = await api.recent_developments(
        query="immigration policy changes",
        days_back=90
    )
    
    print(f"   📅 Found {len(recent_results.get('results', []))} recent developments")
    for result in recent_results.get('results', [])[:3]:
        pub_date = result.get('publication_date', 0)
        if pub_date:
            date_str = datetime.fromtimestamp(pub_date).strftime('%Y-%m-%d')
            print(f"   🆕 {result.get('title', 'Unknown')} ({date_str})")
    
    print("\n✅ Legal research workflow completed!")


# =============================================================================
# CONTENT GENERATION HELPERS
# =============================================================================

async def generate_blog_post_research(topic: str, practice_area: str) -> Dict[str, Any]:
    """Research and gather sources for a legal blog post"""
    api = LegalKnowledgeAPI()
    
    # Gather multiple types of sources
    research_data = {
        "topic": topic,
        "practice_area": practice_area,
        "sources": {
            "authoritative": [],
            "recent_developments": [],
            "related_content": [],
            "content_gaps": []
        },
        "recommended_keywords": [],
        "seo_opportunities": []
    }
    
    # Get authoritative sources
    auth_results = await api.authority_search(topic)
    research_data["sources"]["authoritative"] = auth_results.get("results", [])[:5]
    
    # Get recent developments
    recent_results = await api.recent_developments(topic)
    research_data["sources"]["recent_developments"] = recent_results.get("results", [])[:5]
    
    # Get related content
    related_results = await api.practice_area_search(topic, practice_area)
    research_data["sources"]["related_content"] = related_results.get("results", [])[:5]
    
    # Analyze content gaps
    gap_results = await api.content_gap_analysis(practice_area, [topic])
    research_data["sources"]["content_gaps"] = gap_results.get("results", [])[:5]
    
    # Extract keywords from all sources
    all_sources = []
    for source_type in research_data["sources"].values():
        all_sources.extend(source_type)
    
    keywords = set()
    for source in all_sources:
        keywords.update(source.get("keywords", []))
    
    research_data["recommended_keywords"] = list(keywords)[:20]
    
    return research_data


async def legal_seo_analysis(practice_area: str, target_keywords: List[str]) -> Dict[str, Any]:
    """Analyze SEO opportunities in legal practice area"""
    api = LegalKnowledgeAPI()
    
    seo_analysis = {
        "practice_area": practice_area,
        "target_keywords": target_keywords,
        "content_opportunities": [],
        "authority_gaps": [],
        "trending_topics": [],
        "recommended_actions": []
    }
    
    for keyword in target_keywords:
        # Check content coverage
        coverage = await api.search_legal_documents(
            query=keyword,
            practice_area_weight=1.2,
            content_weight=1.0
        )
        
        # Check authority coverage
        authority_coverage = await api.authority_search(keyword)
        
        # Check recency
        recent_coverage = await api.recent_developments(keyword, days_back=180)
        
        seo_analysis["content_opportunities"].append({
            "keyword": keyword,
            "total_docs": len(coverage.get("results", [])),
            "authority_docs": len(authority_coverage.get("results", [])),
            "recent_docs": len(recent_coverage.get("results", [])),
            "opportunity_score": calculate_opportunity_score(
                len(coverage.get("results", [])),
                len(authority_coverage.get("results", [])),
                len(recent_coverage.get("results", []))
            )
        })
    
    return seo_analysis


def calculate_opportunity_score(total_docs: int, authority_docs: int, recent_docs: int) -> float:
    """Calculate SEO opportunity score based on content analysis"""
    # Higher score = better opportunity
    # Factors: low total content, low authority content, few recent updates
    
    base_score = 1.0
    
    # Penalize high content volume (saturated topics)
    if total_docs > 20:
        base_score *= 0.5
    elif total_docs > 10:
        base_score *= 0.7
    
    # Penalize high authority coverage
    if authority_docs > 10:
        base_score *= 0.4
    elif authority_docs > 5:
        base_score *= 0.6
    
    # Boost for stale content (opportunity for fresh content)
    if recent_docs < 3:
        base_score *= 1.5
    elif recent_docs < 5:
        base_score *= 1.2
    
    return min(base_score, 1.0)


# =============================================================================
# STARTUP AND DEPLOYMENT
# =============================================================================

async def startup_deployment_commands():
    """Commands to start the legal knowledge system"""
    commands = """
🚀 Legal Knowledge System Deployment Commands:

1. Start the complete system:
   docker-compose -f legal-docker-compose.yml up -d

2. Check service health:
   docker-compose -f legal-docker-compose.yml ps

3. View Superlinked API docs:
   http://localhost:8080/docs

4. Access legal research API:
   http://localhost:8000/docs

5. Monitor logs:
   docker-compose -f legal-docker-compose.yml logs -f legal-superlinked

6. Scale Superlinked service:
   docker-compose -f legal-docker-compose.yml up -d --scale legal-superlinked=2

7. Backup Qdrant data:
   docker-compose -f legal-docker-compose.yml exec qdrant qdrant-backup

8. Restart with fresh data:
   docker-compose -f legal-docker-compose.yml down -v
   docker-compose -f legal-docker-compose.yml up -d

📊 Performance Monitoring:
   - Qdrant UI: http://localhost:6333/dashboard
   - Redis CLI: docker-compose exec redis redis-cli
   - Postgres CLI: docker-compose exec postgres psql -U legal_user -d legal_research

🔧 Development Commands:
   - Hot reload API: docker-compose up legal-api --build
   - Debug Superlinked: docker-compose exec legal-superlinked python -c "import app"
   - Check model cache: docker-compose exec legal-superlinked ls -la /app/model_cache/
"""
    print(commands)


if __name__ == "__main__":
    print("🏛️  Legal Knowledge System API Examples")
    print("="*50)
    
    # Run the demo
    asyncio.run(demo_legal_research_workflow())
    
    print("\n" + "="*50)
    print("📚 Blog Post Research Example:")
    
    # Blog post research example
    async def blog_research_demo():
        research = await generate_blog_post_research(
            topic="H1B visa lottery system changes",
            practice_area="immigration_law"
        )
        print(f"✅ Gathered research for: {research['topic']}")
        print(f"📄 Authoritative sources: {len(research['sources']['authoritative'])}")
        print(f"🆕 Recent developments: {len(research['sources']['recent_developments'])}")
        print(f"🔗 Related content: {len(research['sources']['related_content'])}")
        print(f"💡 Content gaps: {len(research['sources']['content_gaps'])}")
        print(f"🏷️  Recommended keywords: {', '.join(research['recommended_keywords'][:10])}")
    
    asyncio.run(blog_research_demo())
    
    print("\n" + "="*50)
    await startup_deployment_commands()