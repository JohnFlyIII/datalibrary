"""
Legal Knowledge System - Superlinked Configuration
Optimized for legal document ingestion and retrieval
"""
import os
from datetime import timedelta
from superlinked import framework as sl


# =============================================================================
# SCHEMA DEFINITIONS
# =============================================================================

@sl.schema
class LegalDocument:
    """Primary schema for legal documents"""
    id: sl.IdField
    title: sl.String
    content_text: sl.String
    practice_area: sl.String
    jurisdiction: sl.String
    authority_level: sl.String  # primary, secondary, tertiary
    document_type: sl.String   # case_law, statute, regulation, article
    publication_date: sl.Timestamp
    author: sl.String
    citations: sl.String  # JSON string list
    keywords: sl.String   # JSON string list
    summary: sl.String
    
    # Scoring fields
    authority_score: sl.Float      # 0.0-1.0
    relevance_score: sl.Float      # 0.0-1.0
    citation_count: sl.Integer
    
    # Metadata
    source_url: sl.String
    pdf_path: sl.String
    word_count: sl.Integer


@sl.schema
class PersonalInjuryDocument:
    """Schema for personal injury and medical malpractice cases"""
    id: sl.IdField
    title: sl.String
    content_text: sl.String
    practice_area: sl.String
    jurisdiction: sl.String
    authority_level: sl.String
    document_type: sl.String
    publication_date: sl.Timestamp
    author: sl.String
    citations: sl.String  # JSON string list
    keywords: sl.String   # JSON string list
    summary: sl.String
    authority_score: sl.Float
    citation_count: sl.Integer
    source_url: sl.String
    pdf_path: sl.String
    word_count: sl.Integer
    
    # Personal injury specific fields
    injury_type: sl.String                # "medical_malpractice", "auto_accident", etc.
    injury_severity: sl.String            # "minor", "moderate", "severe", "catastrophic"
    medical_specialty: sl.String          # "surgery", "neurology", etc.
    liability_theory: sl.String           # "negligence", "strict_liability"
    medical_treatment: sl.String          # "emergency_only", "ongoing", "long_term"
    trial_readiness: sl.String            # "settlement_track", "trial_ready"
    case_number: sl.String


# =============================================================================
# INITIALIZE SCHEMA INSTANCES
# =============================================================================

legal_document = LegalDocument()
personal_injury_document = PersonalInjuryDocument()


# =============================================================================
# EMBEDDING SPACES
# =============================================================================

# Text similarity for semantic search
content_space = sl.TextSimilaritySpace(
    text=legal_document.content_text,
    model="sentence-transformers/all-mpnet-base-v2",
)

title_space = sl.TextSimilaritySpace(
    text=legal_document.title,
    model="sentence-transformers/all-mpnet-base-v2",
)

summary_space = sl.TextSimilaritySpace(
    text=legal_document.summary,
    model="sentence-transformers/all-mpnet-base-v2",
)

keywords_space = sl.TextSimilaritySpace(
    text=legal_document.keywords,
    model="sentence-transformers/all-MiniLM-L6-v2"
)

# Practice area categorization
practice_area_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.practice_area,
    categories=[
        "immigration_law",
        "family_law", 
        "criminal_law",
        "business_law",
        "real_estate_law",
        "employment_law",
        "personal_injury",
        "estate_planning",
        "civil_law",
        "tort_law"
    ],
    negative_filter=-0.5,
    uncategorized_as_category=False
)

# Document type categorization
document_type_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.document_type,
    categories=[
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
    negative_filter=-0.3,
    uncategorized_as_category=False
)

# Authority level scoring
authority_space = sl.NumberSpace(
    number=legal_document.authority_score,
    min_value=0.0,
    max_value=1.0,
    mode=sl.Mode.MAXIMUM
)

# Citation count (popularity/importance)
citation_space = sl.NumberSpace(
    number=legal_document.citation_count,
    min_value=0,
    max_value=1000,
    mode=sl.Mode.MAXIMUM
)

# Recency weighting
recency_space = sl.RecencySpace(
    timestamp=legal_document.publication_date,
    period_time_list=[
        sl.PeriodTime(timedelta(days=30), 1.0),    # Very recent: full weight
        sl.PeriodTime(timedelta(days=365), 0.8),   # Recent: high weight  
        sl.PeriodTime(timedelta(days=1825), 0.5),  # 5 years: medium weight
        sl.PeriodTime(timedelta(days=3650), 0.2),  # 10 years: low weight
    ],
    negative_filter=-0.2
)

# Personal injury specific spaces
pi_content_space = sl.TextSimilaritySpace(
    text=personal_injury_document.content_text,
    model="sentence-transformers/all-mpnet-base-v2",
)

pi_injury_type_space = sl.CategoricalSimilaritySpace(
    category_input=personal_injury_document.injury_type,
    categories=[
        "medical_malpractice",
        "auto_accident",
        "slip_fall",
        "product_liability",
        "workplace_injury"
    ],
    negative_filter=-0.4,
    uncategorized_as_category=True
)

pi_medical_specialty_space = sl.CategoricalSimilaritySpace(
    category_input=personal_injury_document.medical_specialty,
    categories=[
        "surgery",
        "neurosurgery",
        "cardiology",
        "orthopedics",
        "emergency_medicine"
    ],
    negative_filter=-0.3,
    uncategorized_as_category=True
)


# =============================================================================
# INDEXES
# =============================================================================

# Primary legal research index
legal_research_index = sl.Index([
    content_space,
    title_space, 
    summary_space,
    practice_area_space,
    authority_space,
    recency_space,
    citation_space
])

# Personal injury specialized index
personal_injury_index = sl.Index([
    pi_content_space,
    pi_injury_type_space,
    pi_medical_specialty_space,
    authority_space,
    recency_space
])

# Quick lookup index
quick_lookup_index = sl.Index([
    title_space,
    practice_area_space,
    document_type_space
])


# =============================================================================
# QUERIES
# =============================================================================

# Comprehensive legal research query
legal_research_query = (
    sl.Query(
        legal_research_index,
        weights={
            content_space: sl.Param("content_weight", default=1.0),
            title_space: sl.Param("title_weight", default=0.6),
            summary_space: sl.Param("summary_weight", default=0.7),
            practice_area_space: sl.Param("practice_area_weight", default=0.8),
            authority_space: sl.Param("authority_weight", default=0.9),
            recency_space: sl.Param("recency_weight", default=0.4),
            citation_space: sl.Param("citation_weight", default=0.3),
        }
    )
    .find(legal_document)
    .similar(content_space.text, sl.Param("search_query"))
    .select_all()
    .limit(sl.Param("limit", default=20))
)

# Quick practice area search
practice_area_query = (
    sl.Query(
        quick_lookup_index,
        weights={
            title_space: sl.Param("title_weight", default=1.0),
            practice_area_space: sl.Param("practice_area_weight", default=1.2),
        }
    )
    .find(legal_document)
    .similar(title_space.text, sl.Param("search_query"))
    .select_all()
    .limit(sl.Param("limit", default=10))
)

# Authority-weighted content query
authority_query = (
    sl.Query(
        legal_research_index,
        weights={
            content_space: sl.Param("content_weight", default=0.8),
            authority_space: sl.Param("authority_weight", default=1.5),
            citation_space: sl.Param("citation_weight", default=1.2),
            recency_space: sl.Param("recency_weight", default=0.6),
        }
    )
    .find(legal_document)
    .similar(content_space.text, sl.Param("search_query"))
    .select_all()
    .limit(sl.Param("limit", default=15))
)

# Medical malpractice focused query
medical_malpractice_query = (
    sl.Query(
        personal_injury_index,
        weights={
            pi_content_space: sl.Param("content_weight", default=1.0),
            pi_injury_type_space: sl.Param("injury_type_weight", default=1.3),
            pi_medical_specialty_space: sl.Param("medical_specialty_weight", default=1.5),
            authority_space: sl.Param("authority_weight", default=1.0),
        }
    )
    .find(personal_injury_document)
    .similar(pi_content_space.text, sl.Param("search_query"))
    .select_all()
    .limit(sl.Param("limit", default=15))
)

# Recent developments query
recent_developments_query = (
    sl.Query(
        legal_research_index,
        weights={
            content_space: sl.Param("content_weight", default=0.8),
            recency_space: sl.Param("recency_weight", default=1.5),
            authority_space: sl.Param("authority_weight", default=0.7),
            citation_space: sl.Param("citation_weight", default=0.4),
        }
    )
    .find(legal_document)
    .similar(content_space.text, sl.Param("search_query"))
    .select_all()
    .limit(sl.Param("limit", default=15))
)


# =============================================================================
# DATA SOURCES
# =============================================================================

# REST sources for production API ingestion
legal_document_source = sl.RestSource(legal_document)
personal_injury_source = sl.RestSource(personal_injury_document)


# =============================================================================
# QUERIES 
# =============================================================================

# Wrap queries in RestQuery for API endpoints
legal_research_rest_query = sl.RestQuery(
    sl.RestDescriptor("legal_research"), 
    legal_research_query
)

practice_area_rest_query = sl.RestQuery(
    sl.RestDescriptor("practice_area"), 
    practice_area_query
)

authority_rest_query = sl.RestQuery(
    sl.RestDescriptor("authority"), 
    authority_query
)

medical_malpractice_rest_query = sl.RestQuery(
    sl.RestDescriptor("medical_malpractice"), 
    medical_malpractice_query
)

recent_developments_rest_query = sl.RestQuery(
    sl.RestDescriptor("recent_developments"), 
    recent_developments_query
)


# =============================================================================
# EXECUTORS
# =============================================================================

# Production REST executor with API endpoints
executor = sl.RestExecutor(
    sources=[legal_document_source, personal_injury_source],
    indices=[legal_research_index, personal_injury_index, quick_lookup_index],
    queries=[
        legal_research_rest_query,
        practice_area_rest_query, 
        authority_rest_query,
        medical_malpractice_rest_query,
        recent_developments_rest_query
    ],
    vector_database=sl.QdrantVectorDatabase(
        url=os.getenv("QDRANT_URL", "http://qdrant:6333"),
        api_key=None  # No authentication for local Qdrant
    )
)

# Register the executor
sl.SuperlinkedRegistry.register(executor)

# Configure CORS for the FastAPI app after registering
try:
    from fastapi.middleware.cors import CORSMiddleware
    import sys
    
    # Get the current app instance if it exists
    app_instance = getattr(sl.SuperlinkedRegistry, '_app', None)
    if app_instance and hasattr(app_instance, 'add_middleware'):
        app_instance.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        print("✅ CORS middleware added to Superlinked app")
    else:
        print("⚠️ Could not add CORS middleware - app instance not accessible")
except Exception as e:
    print(f"⚠️ CORS configuration failed: {e}")

print("🏛️ Legal Knowledge System Superlinked Configuration Loaded!")
print(f"Available Queries: legal_research_query, practice_area_query, authority_query, medical_malpractice_query, recent_developments_query")
print(f"Vector Database: {os.getenv('QDRANT_URL', 'In-Memory (Development)')}")