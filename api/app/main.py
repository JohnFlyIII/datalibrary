"""
Legal Knowledge System API
FastAPI application for legal research and document management
"""
import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import aiohttp
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional

# Initialize FastAPI app
app = FastAPI(
    title="Legal Knowledge System API",
    description="API for legal document research and content generation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
SUPERLINKED_URL = os.getenv("SUPERLINKED_URL", "http://localhost:8080")
GROBID_URL = os.getenv("GROBID_URL", "http://localhost:8070")


class LegalKnowledgeAPI:
    """Client for interacting with Superlinked Legal Knowledge System"""
    
    def __init__(self):
        self.superlinked_url = SUPERLINKED_URL
    
    async def ingest_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest a legal document into the system using default source"""
        return await self.ingest_document_to_source(document, "legal_document_source")
    
    async def ingest_document_to_source(self, document: Dict[str, Any], source_name: str) -> Dict[str, Any]:
        """Ingest a legal document into a specific source"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.superlinked_url}/ingest/{source_name}",
                json=document,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Superlinked ingestion failed: {await response.text()}"
                    )
    
    async def search_documents(self, 
                             query: str,
                             query_type: str = "legal_research_query",
                             **params) -> Dict[str, Any]:
        """Search legal documents"""
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
                if response.status == 200:
                    return await response.json()
                else:
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Superlinked search failed: {await response.text()}"
                    )


# Initialize legal API client
legal_api = LegalKnowledgeAPI()


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test Superlinked connection
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{SUPERLINKED_URL}/docs", timeout=5) as response:
                superlinked_status = response.status == 200
    except:
        superlinked_status = False
    
    try:
        # Test GROBID connection
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{GROBID_URL}/api/isalive", timeout=5) as response:
                grobid_status = response.status == 200
    except:
        grobid_status = False
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "superlinked": superlinked_status,
            "grobid": grobid_status
        }
    }


@app.post("/api/v1/documents/ingest")
async def ingest_legal_document(document: Dict[str, Any]):
    """
    Ingest a legal document into the knowledge system
    Automatically routes to appropriate schema based on practice area
    """
    try:
        # Validate required fields
        required_fields = ["id", "title", "content_text", "practice_area"]
        for field in required_fields:
            if field not in document:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required field: {field}"
                )
        
        # Set defaults for optional fields
        document.setdefault("jurisdiction", "federal")
        document.setdefault("authority_level", "secondary")
        document.setdefault("document_type", "article")
        document.setdefault("publication_date", int(datetime.now().timestamp()))
        document.setdefault("author", "Unknown")
        document.setdefault("citations", [])
        document.setdefault("keywords", [])
        document.setdefault("summary", "")
        document.setdefault("authority_score", 0.5)
        document.setdefault("relevance_score", 0.5)
        document.setdefault("citation_count", 0)
        document.setdefault("source_url", "")
        document.setdefault("pdf_path", "")
        document.setdefault("word_count", len(document["content_text"].split()))
        
        # Determine appropriate source based on practice area and document type
        practice_area = document["practice_area"]
        source_endpoint = "legal_document_source"  # default
        
        if practice_area == "personal_injury" or document.get("injury_type"):
            source_endpoint = "personal_injury_source"
            # Set personal injury specific defaults
            document.setdefault("injury_type", "general")
            document.setdefault("injury_severity", "moderate")
            document.setdefault("liability_theory", "negligence")
            document.setdefault("medical_treatment", "ongoing")
            document.setdefault("trial_readiness", "settlement_track")
            
        elif practice_area == "immigration_law" or document.get("visa_category"):
            source_endpoint = "immigration_source"
            # Set immigration specific defaults
            document.setdefault("benefit_type", "visa")
            document.setdefault("responsible_agency", "USCIS")
            document.setdefault("complexity_level", "moderate")
        
        # Ingest to appropriate source
        result = await legal_api.ingest_document_to_source(document, source_endpoint)
        
        return {
            "status": "success", 
            "document_id": document["id"], 
            "schema_used": source_endpoint,
            "result": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


@app.post("/api/v1/documents/ingest/personal-injury")
async def ingest_personal_injury_document(document: Dict[str, Any]):
    """
    Ingest a personal injury document with specialized schema
    """
    try:
        # Validate required fields
        required_fields = ["id", "title", "content_text"]
        for field in required_fields:
            if field not in document:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required field: {field}"
                )
        
        # Set personal injury specific defaults
        document.setdefault("practice_area", "personal_injury")
        document.setdefault("injury_type", "general")
        document.setdefault("injury_severity", "moderate")
        document.setdefault("liability_theory", "negligence")
        document.setdefault("medical_treatment", "ongoing")
        document.setdefault("trial_readiness", "settlement_track")
        document.setdefault("jurisdiction", "federal")
        document.setdefault("authority_level", "secondary")
        document.setdefault("document_type", "case_law")
        document.setdefault("publication_date", int(datetime.now().timestamp()))
        document.setdefault("author", "Unknown")
        document.setdefault("citations", [])
        document.setdefault("keywords", [])
        document.setdefault("summary", "")
        document.setdefault("authority_score", 0.5)
        document.setdefault("citation_count", 0)
        document.setdefault("source_url", "")
        document.setdefault("pdf_path", "")
        document.setdefault("word_count", len(document["content_text"].split()))
        
        result = await legal_api.ingest_document_to_source(document, "personal_injury_source")
        
        return {
            "status": "success", 
            "document_id": document["id"],
            "schema_used": "PersonalInjuryDocument", 
            "result": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Personal injury ingestion failed: {str(e)}")


@app.post("/api/v1/documents/ingest/immigration")
async def ingest_immigration_document(document: Dict[str, Any]):
    """
    Ingest an immigration document with specialized schema
    """
    try:
        # Validate required fields
        required_fields = ["id", "title", "content_text"]
        for field in required_fields:
            if field not in document:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required field: {field}"
                )
        
        # Set immigration specific defaults
        document.setdefault("practice_area", "immigration_law")
        document.setdefault("benefit_type", "visa")
        document.setdefault("responsible_agency", "USCIS")
        document.setdefault("complexity_level", "moderate")
        document.setdefault("jurisdiction", "federal")
        document.setdefault("authority_level", "secondary")
        document.setdefault("document_type", "regulation")
        document.setdefault("publication_date", int(datetime.now().timestamp()))
        document.setdefault("author", "Unknown")
        document.setdefault("citations", [])
        document.setdefault("keywords", [])
        document.setdefault("summary", "")
        document.setdefault("authority_score", 0.5)
        document.setdefault("citation_count", 0)
        document.setdefault("source_url", "")
        document.setdefault("pdf_path", "")
        document.setdefault("word_count", len(document["content_text"].split()))
        
        result = await legal_api.ingest_document_to_source(document, "immigration_source")
        
        return {
            "status": "success", 
            "document_id": document["id"],
            "schema_used": "ImmigrationDocument", 
            "result": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Immigration ingestion failed: {str(e)}")


@app.post("/api/v1/search/legal")
async def search_legal_documents(
    query: str,
    query_type: str = "legal_research_query",
    limit: int = 20,
    content_weight: float = 1.0,
    title_weight: float = 0.6,
    summary_weight: float = 0.7,
    practice_area_weight: float = 0.8,
    authority_weight: float = 0.9,
    recency_weight: float = 0.4,
    citation_weight: float = 0.3
):
    """
    Search legal documents with configurable weights
    
    Query types:
    - legal_research_query: Comprehensive legal research
    - practice_area_query: Quick practice area search
    - authority_query: Authority-weighted search
    - content_gap_query: Content opportunity analysis
    - recent_developments_query: Recent legal updates
    """
    try:
        params = {
            "limit": limit,
            "content_weight": content_weight,
            "title_weight": title_weight,
            "summary_weight": summary_weight,
            "practice_area_weight": practice_area_weight,
            "authority_weight": authority_weight,
            "recency_weight": recency_weight,
            "citation_weight": citation_weight
        }
        
        result = await legal_api.search_documents(query, query_type, **params)
        return {"status": "success", "query": query, "query_type": query_type, "results": result}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.post("/api/v1/search/authority")
async def search_authoritative_sources(
    query: str,
    min_authority_score: float = 0.8,
    limit: int = 15
):
    """Search for authoritative legal sources"""
    try:
        result = await legal_api.search_documents(
            query=query,
            query_type="authority_query",
            authority_weight=1.5,
            citation_weight=1.2,
            content_weight=0.8,
            limit=limit
        )
        
        # Filter by minimum authority score if results contain authority_score
        if "results" in result:
            filtered_results = [
                doc for doc in result["results"]
                if doc.get("authority_score", 0) >= min_authority_score
            ]
            result["results"] = filtered_results
        
        return {"status": "success", "query": query, "min_authority_score": min_authority_score, "results": result}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authority search failed: {str(e)}")


@app.post("/api/v1/search/recent")
async def search_recent_developments(
    query: str,
    days_back: int = 90,
    limit: int = 15
):
    """Find recent legal developments"""
    try:
        result = await legal_api.search_documents(
            query=query,
            query_type="recent_developments_query",
            recency_weight=1.5,
            content_weight=0.8,
            authority_weight=0.7,
            limit=limit
        )
        
        return {"status": "success", "query": query, "days_back": days_back, "results": result}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recent developments search failed: {str(e)}")


@app.post("/api/v1/content/gap-analysis")
async def content_gap_analysis(
    practice_area: str,
    keywords: List[str],
    limit: int = 25
):
    """Analyze content gaps for blog post opportunities"""
    try:
        search_query = f"{practice_area} " + " ".join(keywords)
        result = await legal_api.search_documents(
            query=search_query,
            query_type="content_gap_query",
            keywords_weight=1.0,
            content_weight=0.7,
            authority_weight=0.3,  # Lower for gaps
            recency_weight=0.2,   # Older content indicates gaps
            limit=limit
        )
        
        return {
            "status": "success",
            "practice_area": practice_area,
            "keywords": keywords,
            "content_opportunities": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content gap analysis failed: {str(e)}")


@app.post("/api/v1/search/personal-injury")
async def search_personal_injury_documents(
    query: str,
    query_type: str = "personal_injury_research_query",
    limit: int = 20,
    content_weight: float = 1.0,
    injury_type_weight: float = 1.2,
    medical_specialty_weight: float = 1.0,
    authority_weight: float = 0.9
):
    """
    Search personal injury documents with specialized weighting
    
    Query types:
    - personal_injury_research_query: Comprehensive PI research
    - medical_malpractice_query: Medical malpractice focused
    - case_similarity_query: Find similar cases
    """
    try:
        params = {
            "limit": limit,
            "content_weight": content_weight,
            "injury_type_weight": injury_type_weight,
            "medical_specialty_weight": medical_specialty_weight,
            "authority_weight": authority_weight
        }
        
        result = await legal_api.search_documents(query, query_type, **params)
        return {"status": "success", "query": query, "query_type": query_type, "results": result}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Personal injury search failed: {str(e)}")


@app.post("/api/v1/search/medical-malpractice")
async def search_medical_malpractice_cases(
    query: str,
    medical_specialty: Optional[str] = None,
    injury_severity: Optional[str] = None,
    limit: int = 15
):
    """
    Specialized search for medical malpractice cases
    """
    try:
        # Use medical malpractice specific query
        params = {
            "limit": limit,
            "content_weight": 1.0,
            "medical_specialty_weight": 1.5,
            "injury_type_weight": 1.3,
            "authority_weight": 1.0
        }
        
        # Enhance query with specialty filter if provided
        enhanced_query = query
        if medical_specialty:
            enhanced_query += f" {medical_specialty}"
        if injury_severity:
            enhanced_query += f" {injury_severity}"
        
        result = await legal_api.search_documents(
            enhanced_query, 
            "medical_malpractice_query", 
            **params
        )
        
        return {
            "status": "success", 
            "query": query,
            "medical_specialty": medical_specialty,
            "injury_severity": injury_severity,
            "results": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Medical malpractice search failed: {str(e)}")


@app.post("/api/v1/search/immigration")
async def search_immigration_documents(
    query: str,
    query_type: str = "immigration_research_query",
    visa_category: Optional[str] = None,
    limit: int = 20
):
    """
    Search immigration documents with specialized parameters
    
    Query types:
    - immigration_research_query: Comprehensive immigration research
    - visa_specific_query: Visa-focused search
    """
    try:
        params = {
            "limit": limit,
            "content_weight": 1.0,
            "authority_weight": 1.1,
            "recency_weight": 0.8 if query_type == "immigration_research_query" else 0.9
        }
        
        # Enhance query with visa category if provided
        enhanced_query = query
        if visa_category:
            enhanced_query += f" {visa_category}"
        
        result = await legal_api.search_documents(enhanced_query, query_type, **params)
        return {
            "status": "success", 
            "query": query,
            "visa_category": visa_category,
            "query_type": query_type,
            "results": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Immigration search failed: {str(e)}")


@app.post("/api/v1/search/precedent")
async def search_legal_precedent(
    query: str,
    min_authority_score: float = 0.8,
    min_citation_count: int = 5,
    limit: int = 10
):
    """
    Search for high-authority legal precedent
    Focuses on highly cited, authoritative sources
    """
    try:
        params = {
            "limit": limit,
            "content_weight": 0.9,
            "authority_weight": 1.8,  # Maximum authority focus
            "citation_weight": 1.5,   # Maximum citation focus
            "recency_weight": 0.2     # Less focus on recency for precedent
        }
        
        result = await legal_api.search_documents(query, "precedent_research_query", **params)
        
        # Filter results by minimum thresholds if results contain scores
        if "results" in result and "results" in result["results"]:
            filtered_results = []
            for doc in result["results"]["results"]:
                authority_score = doc.get("authority_score", 0)
                citation_count = doc.get("citation_count", 0)
                
                if authority_score >= min_authority_score and citation_count >= min_citation_count:
                    filtered_results.append(doc)
            
            result["results"]["results"] = filtered_results
        
        return {
            "status": "success",
            "query": query,
            "min_authority_score": min_authority_score,
            "min_citation_count": min_citation_count,
            "results": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Precedent search failed: {str(e)}")


@app.get("/api/v1/system/info")
async def system_info():
    """Get system information and available practice areas"""
    return {
        "system": "Legal Knowledge System API",
        "version": "2.0.0",
        "modular_architecture": True,
        "available_practice_areas": [
            "immigration_law",
            "family_law",
            "criminal_law",
            "business_law",
            "real_estate_law",
            "employment_law",
            "personal_injury",
            "estate_planning",
            "intellectual_property",
            "tax_law",
            "bankruptcy_law",
            "constitutional_law"
        ],
        "available_query_types": {
            "general_legal": [
                "legal_research_query",
                "practice_area_query", 
                "authority_query",
                "content_gap_query",
                "recent_developments_query"
            ],
            "personal_injury": [
                "personal_injury_research_query",
                "medical_malpractice_query",
                "case_similarity_query"
            ],
            "immigration": [
                "immigration_research_query",
                "visa_specific_query"
            ],
            "cross_practice": [
                "multi_practice_query",
                "precedent_research_query"
            ]
        },
        "available_schemas": [
            "LegalDocument",
            "PersonalInjuryDocument",
            "ImmigrationDocument", 
            "LegalTopic"
        ],
        "authority_levels": ["primary", "secondary", "tertiary"],
        "document_types": [
            "case_law",
            "statute",
            "regulation", 
            "article",
            "brief",
            "opinion",
            "commentary",
            "form",
            "guide"
        ],
        "injury_types": [
            "medical_malpractice",
            "auto_accident",
            "slip_fall",
            "product_liability",
            "workplace_injury"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)