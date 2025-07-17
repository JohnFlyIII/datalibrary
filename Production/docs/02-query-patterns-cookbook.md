# Legal Knowledge Platform - Query Patterns Cookbook

## Table of Contents
1. [Basic Query Patterns](#basic-query-patterns)
2. [Hierarchical Searches](#hierarchical-searches)
3. [Fact-Based Research](#fact-based-research)
4. [Progressive Disclosure Patterns](#progressive-disclosure-patterns)
5. [Combined Query Strategies](#combined-query-strategies)
6. [Advanced Techniques](#advanced-techniques)

## Basic Query Patterns

### 1. Simple Text Search

**Use Case**: Find documents containing specific terms or phrases

```python
# Search for employment discrimination cases
query = sl.Query(legal_knowledge_index)
    .find(legal_document)
    .similar(deep_dive_content_space.text, "employment discrimination wrongful termination")
    .limit(20)
    .select_all()

# Weight multiple text spaces
query = sl.Query(
    legal_knowledge_index,
    weights={
        deep_dive_content_space: 3.0,      # Full text
        keywords_space: 2.0,               # Keywords
        synonyms_space: 1.5                # Alternative terms
    }
)
```

### 2. Filtered Search by Jurisdiction

**Use Case**: Find Texas state employment laws only

```python
query = (
    sl.Query(legal_knowledge_index)
    .find(legal_document)
    .filter(legal_document.jurisdiction_state == "texas")
    .similar(exploration_provisions_space.text, "overtime pay requirements")
    .limit(10)
    .select_all()
)
```

### 3. Practice Area Focused Search

**Use Case**: Medical malpractice cases involving surgical errors

```python
query = sl.Query(
    legal_knowledge_index,
    weights={
        specific_practice_space: 3.0,      # "surgical_errors"
        secondary_practice_space: 2.0,     # "medical_malpractice"
        deep_dive_content_space: 2.5
    }
).filter(
    legal_document.practice_area_specific.contains("surgical_errors")
)
```

## Hierarchical Searches

### 1. Geographic Drill-Down

**Use Case**: Search federal → state → city employment laws

```python
# Federal employment law
federal_query = sl.Query(
    legal_knowledge_index,
    weights={
        country_jurisdiction_space: 3.0,
        state_jurisdiction_space: 0.0,
        city_jurisdiction_space: 0.0,
        exploration_provisions_space: 2.5
    }
).filter(legal_document.jurisdiction_country == "united_states")

# Texas state employment law
texas_query = sl.Query(
    legal_knowledge_index,
    weights={
        country_jurisdiction_space: 1.0,    # Include federal context
        state_jurisdiction_space: 3.0,      # Focus on Texas
        city_jurisdiction_space: 0.0,
        exploration_provisions_space: 2.5
    }
).filter(legal_document.jurisdiction_state == "texas")

# Houston city ordinances
houston_query = sl.Query(
    legal_knowledge_index,
    weights={
        country_jurisdiction_space: 0.5,
        state_jurisdiction_space: 1.0,
        city_jurisdiction_space: 3.0,       # Focus on Houston
        exploration_provisions_space: 2.5
    }
).filter(legal_document.jurisdiction_city == "houston")
```

### 2. Practice Area Hierarchy Navigation

**Use Case**: Litigation → Personal Injury → Auto Accidents

```python
# Broad litigation search
litigation_query = sl.Query(
    legal_knowledge_index,
    weights={
        primary_practice_space: 3.0,        # "litigation"
        secondary_practice_space: 1.0,
        specific_practice_space: 0.5
    }
).filter(legal_document.practice_area_primary == "litigation")

# Personal injury focus
personal_injury_query = sl.Query(
    legal_knowledge_index,
    weights={
        primary_practice_space: 1.0,
        secondary_practice_space: 3.0,      # "personal_injury"
        specific_practice_space: 1.5
    }
).filter(legal_document.practice_area_secondary == "personal_injury")

# Auto accident specialization
auto_accident_query = sl.Query(
    legal_knowledge_index,
    weights={
        primary_practice_space: 0.5,
        secondary_practice_space: 1.5,
        specific_practice_space: 3.0        # "auto_accidents"
    }
).filter(legal_document.practice_area_specific == "auto_accidents")
```

### 3. Path-Based Hierarchical Search

**Use Case**: Exact hierarchical path matching

```python
# Search specific path: US → Texas → Houston
geographic_path_query = sl.Query(
    legal_knowledge_index,
    weights={
        jurisdiction_path_space: 3.0,
        deep_dive_content_space: 2.0
    }
).filter(
    legal_document.jurisdiction_full_path == "united_states/texas/houston"
)

# Practice area path: litigation/personal_injury/medical_malpractice
practice_path_query = sl.Query(
    legal_knowledge_index,
    weights={
        practice_path_space: 3.0,
        exploration_provisions_space: 2.0
    }
).filter(
    legal_document.practice_area_full_path == "litigation/personal_injury/medical_malpractice"
)
```

## Fact-Based Research

### 1. Search Within Extracted Facts

**Use Case**: Find specific legal requirements with citations

```python
# Find facts about disability accommodations
facts_query = sl.Query(
    legal_knowledge_index,
    weights={
        extracted_facts_space: 3.0,
        key_findings_space: 2.5,
        citations_apa_space: 2.0
    }
).similar(
    extracted_facts_space.text, 
    "reasonable accommodation disability ADA compliance"
)
```

### 2. High Fact-Density Documents

**Use Case**: Find documents with many relevant facts

```python
# Documents with 50+ extracted facts about employment law
dense_facts_query = sl.Query(
    legal_knowledge_index,
    weights={
        fact_count_space: 3.0,
        extracted_facts_space: 2.0,
        practice_areas_space: 1.5
    }
).filter(
    legal_document.fact_count > 50
).filter(
    legal_document.practice_areas.contains("employment")
)
```

### 3. Citation Verification

**Use Case**: Find documents citing specific statutes

```python
# Find documents citing Texas Labor Code § 21.128
citation_query = sl.Query(
    legal_knowledge_index,
    weights={
        citations_apa_space: 3.0,
        internal_citations_space: 2.0,
        fact_locations_space: 2.0
    }
).similar(
    citations_apa_space.text,
    "Texas Labor Code § 21.128"
)
```

## Progressive Disclosure Patterns

### 1. Discovery Phase - Broad Exploration

**Use Case**: Initial research on unfamiliar topic

```python
# What exists about data privacy in healthcare?
discovery_query = sl.Query(
    legal_knowledge_index,
    weights={
        discovery_summary_space: 3.0,
        discovery_topics_space: 2.5,
        client_takeaways_space: 2.0,
        content_density_space: 1.5,
        coverage_scope_space: 1.5
    }
).similar(
    discovery_summary_space.text,
    "healthcare data privacy HIPAA patient information"
).limit(50)  # Cast wide net
```

### 2. Exploration Phase - Focused Analysis

**Use Case**: Dive deeper into specific aspects

```python
# Focus on HIPAA compliance requirements
exploration_query = sl.Query(
    legal_knowledge_index,
    weights={
        exploration_provisions_space: 3.0,
        compliance_requirements_space: 3.0,
        penalties_space: 2.5,
        exceptions_space: 2.0,
        relevance_score_space: 2.0
    }
).similar(
    compliance_requirements_space.text,
    "HIPAA compliance requirements healthcare providers"
).filter(
    legal_document.client_relevance_score >= 7
).limit(20)
```

### 3. Deep Dive Phase - Detailed Research

**Use Case**: Full analysis with citations and context

```python
# Detailed HIPAA violation penalties and case law
deep_dive_query = sl.Query(
    legal_knowledge_index,
    weights={
        deep_dive_content_space: 3.0,
        deep_dive_precedents_space: 2.5,
        deep_dive_citations_space: 2.5,
        legislative_history_space: 2.0,
        chunk_context_space: 2.0
    }
).similar(
    deep_dive_content_space.text,
    "HIPAA violation penalties enforcement actions OCR"
).filter(
    legal_document.authority_level.in_(["primary", "binding"])
).limit(100)
```

## Combined Query Strategies

### 1. Texas Employment Discrimination Research

**Use Case**: Comprehensive research combining jurisdiction, practice area, and content

```python
texas_employment_discrimination = sl.Query(
    legal_knowledge_index,
    weights={
        # Jurisdiction hierarchy
        state_jurisdiction_space: 3.0,      # Texas focus
        country_jurisdiction_space: 1.0,    # Federal context
        
        # Practice area hierarchy
        primary_practice_space: 1.0,        # Labor/employment
        secondary_practice_space: 3.0,      # Discrimination
        specific_practice_space: 2.0,       # Specific types
        
        # Content layers
        exploration_provisions_space: 2.5,
        compliance_requirements_space: 2.5,
        penalties_space: 2.0,
        
        # Facts and findings
        extracted_facts_space: 2.0,
        key_findings_space: 2.0
    }
).filter(
    legal_document.jurisdiction_state == "texas"
).filter(
    legal_document.practice_area_secondary.contains("discrimination")
).similar(
    exploration_provisions_space.text,
    "employment discrimination protected classes remedies"
)
```

### 2. Executive Briefing on Recent Healthcare Regulations

**Use Case**: Quick overview for C-suite presentation

```python
executive_healthcare_brief = sl.Query(
    legal_knowledge_index,
    weights={
        # Summary spaces
        executive_summary_space: 3.0,
        summary_bullets_space: 3.0,
        summary_conclusion_space: 2.5,
        
        # Recency
        published_recency_space: 3.0,
        effective_date_space: 2.5,
        
        # Relevance
        client_relevance_score: 2.0,
        
        # Practice area
        primary_practice_space: 2.0         # Healthcare
    }
).filter(
    legal_document.practice_area_primary == "healthcare"
).filter(
    legal_document.published_date >= "2023-01-01"
).filter(
    legal_document.target_audience.contains("business_owners")
).limit(10)
```

### 3. Compliance Audit Preparation

**Use Case**: Gather all compliance requirements for specific industry

```python
compliance_audit_query = sl.Query(
    legal_knowledge_index,
    weights={
        # Compliance focus
        compliance_requirements_space: 3.0,
        penalties_space: 3.0,
        exceptions_space: 2.5,
        
        # Time sensitivity
        effective_date_space: 2.5,
        update_priority_space: 2.0,
        
        # Facts
        extracted_facts_space: 2.0,
        fact_count_space: 1.5,
        
        # Authority
        authority_level_space: 2.0
    }
).filter(
    legal_document.content_type.in_(["regulation", "statute"])
).filter(
    legal_document.authority_level.in_(["primary", "binding"])
).filter(
    legal_document.update_priority.in_(["high", "urgent"])
)
```

## Advanced Techniques

### 1. Multi-Stage Query Pipeline

**Use Case**: Progressive refinement of search results

```python
# Stage 1: Broad discovery
stage1_results = discovery_query.limit(100).execute()

# Extract document IDs from top results
top_doc_ids = [r.id for r in stage1_results[:20]]

# Stage 2: Detailed exploration of top documents
stage2_query = sl.Query(
    legal_knowledge_index,
    weights={
        exploration_provisions_space: 3.0,
        extracted_facts_space: 2.5,
        compliance_requirements_space: 2.5
    }
).filter(
    legal_document.id.in_(top_doc_ids)
)

# Stage 3: Deep dive into most relevant
stage3_results = deep_dive_query.filter(
    legal_document.id.in_(most_relevant_ids)
).execute()
```

### 2. Cross-Reference Search

**Use Case**: Find related documents through citation networks

```python
# Find a seed document
seed_doc = sl.Query(legal_knowledge_index)
    .filter(legal_document.id == "texas-labor-code-21-128")
    .select_all()
    .execute()[0]

# Find documents citing this one
citing_docs = sl.Query(
    legal_knowledge_index,
    weights={
        external_citations_space: 3.0,
        deep_dive_citations_space: 2.5,
        related_documents_space: 2.0
    }
).similar(
    external_citations_space.text,
    seed_doc.citation_format
)

# Find documents this one cites
cited_docs = sl.Query(
    legal_knowledge_index,
    weights={
        related_documents_space: 3.0,
        citation_context_space: 2.5
    }
).filter(
    legal_document.id.in_(seed_doc.cites_documents.split(","))
)
```

### 3. Temporal Analysis

**Use Case**: Track legal evolution over time

```python
# Find how employment law has evolved
temporal_evolution = sl.Query(
    legal_knowledge_index,
    weights={
        legislative_history_space: 3.0,
        published_recency_space: -1.0,      # Negative weight for historical
        deep_dive_content_space: 2.0,
        primary_practice_space: 2.0
    }
).filter(
    legal_document.practice_area_primary == "labor_employment"
).filter(
    legal_document.content_type.in_(["statute", "regulation"])
).sort_by(
    legal_document.published_date, 
    ascending=True
).limit(50)
```

### 4. Confidence-Based Filtering

**Use Case**: Only high-confidence, verified content

```python
high_confidence_query = sl.Query(
    legal_knowledge_index,
    weights={
        confidence_score_space: 3.0,
        authority_level_space: 2.5,
        deep_dive_content_space: 2.0
    }
).filter(
    legal_document.confidence_score >= 90
).filter(
    legal_document.human_reviewed == "true"
).filter(
    legal_document.authority_level.in_(["primary", "binding"])
)
```

### 5. Natural Language Query Patterns

**Use Case**: Convert natural language to structured queries

```python
def natural_language_to_query(user_input: str):
    """
    Example: "Find recent Texas cases about workplace discrimination 
              against pregnant employees with high penalties"
    """
    
    # Parse intent (simplified example)
    if "recent" in user_input.lower():
        recency_weight = 3.0
    else:
        recency_weight = 0.0
    
    if "texas" in user_input.lower():
        jurisdiction_filter = "texas"
        state_weight = 3.0
    else:
        jurisdiction_filter = None
        state_weight = 0.0
    
    if "high penalties" in user_input.lower():
        penalty_weight = 3.0
    else:
        penalty_weight = 1.0
    
    # Build dynamic query
    return sl.Query(
        legal_knowledge_index,
        weights={
            state_jurisdiction_space: state_weight,
            published_recency_space: recency_weight,
            penalties_space: penalty_weight,
            deep_dive_content_space: 2.5,
            extracted_facts_space: 2.0
        }
    ).filter(
        legal_document.jurisdiction_state == jurisdiction_filter
        if jurisdiction_filter else True
    )
```

## Best Practices

### 1. Query Weight Guidelines

- **3.0**: Primary focus of the search
- **2.0-2.5**: Important supporting aspects
- **1.0-1.5**: Contextual relevance
- **0.5**: Minor influence
- **0.0**: Exclude from search

### 2. Filter vs. Weight

Use **filters** when you need hard constraints:
- Specific jurisdiction
- Document type
- Date ranges
- Authority level

Use **weights** when you want flexible matching:
- Content relevance
- Conceptual similarity
- Importance ranking

### 3. Result Set Sizing

- **Discovery**: 50-100 results (cast wide net)
- **Exploration**: 20-30 results (focused set)
- **Deep Dive**: 10-20 results (detailed analysis)
- **Executive Summary**: 5-10 results (key highlights)

### 4. Performance Optimization

```python
# Good: Specific filters reduce search space
optimized_query = query.filter(
    legal_document.jurisdiction_state == "texas"
).filter(
    legal_document.published_date >= "2020-01-01"
)

# Better: Combine related spaces
combined_text_query = sl.Query(
    legal_knowledge_index,
    weights={
        sl.combine_spaces([
            deep_dive_content_space,
            keywords_space,
            synonyms_space
        ]): 3.0
    }
)

# Best: Use appropriate chunk sizes
chunked_query = sl.Query(
    legal_knowledge_index,
    weights={
        deep_dive_content_space: 3.0  # Already chunked at ingestion
    }
)
```

## Query Templates

### Employment Law Research Template

```python
def employment_law_query(
    topic: str,
    jurisdiction_state: str = None,
    include_federal: bool = True,
    recency_days: int = None
):
    weights = {
        primary_practice_space: 2.0,        # Employment
        exploration_provisions_space: 3.0,
        compliance_requirements_space: 2.5,
        extracted_facts_space: 2.0
    }
    
    if jurisdiction_state:
        weights[state_jurisdiction_space] = 3.0
    if include_federal:
        weights[country_jurisdiction_space] = 1.5
    if recency_days:
        weights[published_recency_space] = 2.5
        
    query = sl.Query(legal_knowledge_index, weights=weights)
    
    if jurisdiction_state:
        query = query.filter(
            legal_document.jurisdiction_state == jurisdiction_state
        )
    
    return query.similar(
        exploration_provisions_space.text, 
        topic
    )
```

### Compliance Audit Template

```python
def compliance_audit_query(
    industry: str,
    jurisdictions: List[str],
    include_penalties: bool = True,
    confidence_threshold: int = 80
):
    weights = {
        compliance_requirements_space: 3.0,
        authority_level_space: 2.5,
        effective_date_space: 2.0,
        confidence_score_space: 2.0
    }
    
    if include_penalties:
        weights[penalties_space] = 2.5
        weights[exceptions_space] = 2.0
        
    query = sl.Query(legal_knowledge_index, weights=weights)
    
    query = query.filter(
        legal_document.jurisdiction_state.in_(jurisdictions)
    ).filter(
        legal_document.confidence_score >= confidence_threshold
    ).filter(
        legal_document.target_audience.contains(industry)
    )
    
    return query
```

## Debugging Queries

### 1. Explain Query Weights

```python
def explain_query(query: sl.Query):
    """Show how different spaces contribute to results"""
    print("Query Weight Distribution:")
    total_weight = sum(query.weights.values())
    
    for space, weight in sorted(
        query.weights.items(), 
        key=lambda x: x[1], 
        reverse=True
    ):
        percentage = (weight / total_weight) * 100
        print(f"  {space.__class__.__name__}: {weight} ({percentage:.1f}%)")
```

### 2. Test Individual Spaces

```python
def test_space_contribution(base_query: sl.Query, test_text: str):
    """Test how each space affects results"""
    results = {}
    
    for space in base_query.weights.keys():
        # Create query with only this space
        single_space_query = sl.Query(
            legal_knowledge_index,
            weights={space: 1.0}
        ).similar(space.text, test_text).limit(5)
        
        results[space.__class__.__name__] = single_space_query.execute()
    
    return results
```

---

*Last Updated: 2024*
*Version: 1.0*