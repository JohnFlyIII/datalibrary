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
    """Unified schema for all legal documents with multi-area support and passage-level chunking"""
    id: sl.IdField
    title: sl.String
    content_text: sl.String
    practice_areas: sl.StringList  # Multiple practice areas: ["civil_law", "personal_injury", "medical_malpractice"]
    legal_topics: sl.StringList    # Granular topics: ["civil_procedure", "tort_liability", "damages"]
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
    
    # Optional specialized fields (for personal injury, medical malpractice, etc.)
    injury_type: sl.String                # "medical_malpractice", "auto_accident", etc. (optional)
    injury_severity: sl.String            # "minor", "moderate", "severe", "catastrophic" (optional)
    medical_specialty: sl.String          # "surgery", "neurology", etc. (optional)
    liability_theory: sl.String           # "negligence", "strict_liability" (optional)
    medical_treatment: sl.String          # "emergency_only", "ongoing", "long_term" (optional)
    trial_readiness: sl.String            # "settlement_track", "trial_ready" (optional)
    case_number: sl.String                # Case reference number (optional)
    
    # Passage-level fields (for chunked documents)
    parent_document_id: sl.String         # ID of the parent document if this is a chunk
    chunk_index: sl.Integer               # Position of this chunk in the document (0-based)
    start_char: sl.Integer                # Character offset where this chunk starts in original document
    end_char: sl.Integer                  # Character offset where this chunk ends in original document
    chunk_context: sl.String             # Brief context around this chunk for citation purposes
    is_chunk: sl.String                  # "true" if this is a chunk, "false" if full document
    
    # Metadata
    source_url: sl.String
    pdf_path: sl.String
    word_count: sl.Integer


# =============================================================================
# INITIALIZE SCHEMA INSTANCES
# =============================================================================

legal_document = LegalDocument()


# =============================================================================
# EMBEDDING SPACES
# =============================================================================

# Text similarity for semantic search with chunking support
content_space = sl.TextSimilaritySpace(
    text=sl.chunk(
        legal_document.content_text,
        chunk_size=1000,      # ~1000 tokens per chunk for manageable sections
        chunk_overlap=200     # 200 token overlap to maintain context
    ),
    model="sentence-transformers/all-mpnet-base-v2"
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

# Practice areas categorization (multi-value support)
practice_areas_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.practice_areas,  # Now StringList
    categories=[
        "immigration_law",
        "family_law", 
        "criminal_law",
        "business_law",
        "real_estate_law",
        "employment_law",
        "personal_injury",
        "medical_malpractice",
        "estate_planning",
        "civil_law",
        "tort_law",
        "constitutional_law",
        "administrative_law"
    ],
    negative_filter=-0.5,
    uncategorized_as_category=False
)

# Legal topics categorization (granular multi-value support) 
legal_topics_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.legal_topics,  # StringList
    categories=[
        "civil_procedure",
        "tort_liability",
        "damages",
        "medical_negligence",
        "statute_of_limitations",
        "venue",
        "discovery",
        "judgments",
        "contracts",
        "evidence",
        "appeals",
        "injunctions"
    ],
    negative_filter=-0.4,
    uncategorized_as_category=True  # Allow unknown topics
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

# Specialized spaces for optional fields (personal injury, medical malpractice)
injury_type_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.injury_type,
    categories=[
        "medical_malpractice",
        "auto_accident",
        "slip_fall",
        "product_liability",
        "workplace_injury",
        "wrongful_death",
        "nursing_home_abuse"
    ],
    negative_filter=-0.4,
    uncategorized_as_category=True
)

medical_specialty_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.medical_specialty,
    categories=[
        "surgery",
        "neurosurgery",
        "cardiology",
        "orthopedics",
        "emergency_medicine",
        "anesthesiology",
        "radiology",
        "obstetrics",
        "pediatrics"
    ],
    negative_filter=-0.3,
    uncategorized_as_category=True
)


# =============================================================================
# INDEXES
# =============================================================================

# Comprehensive legal research index (unified)
legal_research_index = sl.Index([
    content_space,
    title_space, 
    summary_space,
    practice_areas_space,      # Updated to multi-value
    legal_topics_space,        # New granular topics
    authority_space,
    recency_space,
    citation_space,
    document_type_space
])

# Specialized medical malpractice index
medical_malpractice_index = sl.Index([
    content_space,
    title_space,
    summary_space,
    practice_areas_space,
    legal_topics_space,
    injury_type_space,
    medical_specialty_space,
    authority_space,
    recency_space
])

# Quick lookup index
quick_lookup_index = sl.Index([
    title_space,
    practice_areas_space,      # Updated to multi-value
    document_type_space,
    legal_topics_space
])


# =============================================================================
# QUERIES
# =============================================================================

# Comprehensive legal research query (enhanced with multi-area support and passage-level search)
legal_research_query = (
    sl.Query(
        legal_research_index,
        weights={
            content_space: sl.Param("content_weight", default=1.0),
            title_space: sl.Param("title_weight", default=0.6),
            summary_space: sl.Param("summary_weight", default=0.7),
            practice_areas_space: sl.Param("practice_area_weight", default=0.8),  # Backward compatible
            legal_topics_space: sl.Param("legal_topics_weight", default=0.6),     # New
            authority_space: sl.Param("authority_weight", default=0.9),
            recency_space: sl.Param("recency_weight", default=0.4),
            citation_space: sl.Param("citation_weight", default=0.3),
            document_type_space: sl.Param("document_type_weight", default=0.5),
        }
    )
    .find(legal_document)
    .similar(content_space.text, sl.Param("search_query"))
    .select_all()
    .limit(sl.Param("limit", default=20))
)

# Passage-level search query for finding specific sections within documents
passage_search_query = (
    sl.Query(
        legal_research_index,
        weights={
            content_space: sl.Param("content_weight", default=1.5),  # Higher weight on content for passage search
            practice_areas_space: sl.Param("practice_area_weight", default=0.6),
            legal_topics_space: sl.Param("legal_topics_weight", default=0.6),
            authority_space: sl.Param("authority_weight", default=0.7),
        }
    )
    .find(legal_document)
    .similar(content_space.text, sl.Param("search_query"))
    .filter(legal_document.is_chunk == "true")  # Only return chunks for passage-level results
    .select_all()
    .limit(sl.Param("limit", default=50))  # More results for passage-level search
)

# Quick practice area search (updated for multi-area)
practice_area_query = (
    sl.Query(
        quick_lookup_index,
        weights={
            title_space: sl.Param("title_weight", default=1.0),
            practice_areas_space: sl.Param("practice_area_weight", default=1.2),  # Backward compatible
            legal_topics_space: sl.Param("legal_topics_weight", default=0.8),     # New
            document_type_space: sl.Param("document_type_weight", default=0.5),
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

# Medical malpractice focused query (updated for unified schema)
medical_malpractice_query = (
    sl.Query(
        medical_malpractice_index,
        weights={
            content_space: sl.Param("content_weight", default=1.0),
            title_space: sl.Param("title_weight", default=0.7),
            summary_space: sl.Param("summary_weight", default=0.8),
            practice_areas_space: sl.Param("practice_area_weight", default=1.2),
            legal_topics_space: sl.Param("legal_topics_weight", default=1.1),
            injury_type_space: sl.Param("injury_type_weight", default=1.3),
            medical_specialty_space: sl.Param("medical_specialty_weight", default=1.5),
            authority_space: sl.Param("authority_weight", default=1.0),
            recency_space: sl.Param("recency_weight", default=0.6),
        }
    )
    .find(legal_document)
    .similar(content_space.text, sl.Param("search_query"))
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

# Unified REST source for all legal documents
legal_document_source = sl.RestSource(legal_document)


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

passage_search_rest_query = sl.RestQuery(
    sl.RestDescriptor("passage_search"), 
    passage_search_query
)


# =============================================================================
# EXECUTORS
# =============================================================================

# Production REST executor with unified schema
executor = sl.RestExecutor(
    sources=[legal_document_source],  # Single unified source
    indices=[legal_research_index, medical_malpractice_index, quick_lookup_index],  # Updated indices
    queries=[
        legal_research_rest_query,
        practice_area_rest_query, 
        authority_rest_query,
        medical_malpractice_rest_query,
        recent_developments_rest_query,
        passage_search_rest_query
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
print(f"Available Queries: legal_research_query, practice_area_query, authority_query, medical_malpractice_query, recent_developments_query, passage_search_query")
print(f"Vector Database: {os.getenv('QDRANT_URL', 'In-Memory (Development)')}")
print(f"🔍 Passage-level search enabled for finding specific sections and citations")