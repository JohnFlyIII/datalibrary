# Space Architecture Reference Guide

## Overview

The Legal Knowledge Platform uses a modular space architecture that separates different aspects of legal documents into specialized embedding spaces. This design enables precise, multi-faceted search capabilities while maintaining performance and flexibility.

## Architecture Principles

### 1. Separation of Concerns
Each space handles a specific aspect of legal information:
- **Content Spaces**: Text similarity and semantic search
- **Categorical Spaces**: Classification and filtering
- **Hierarchical Spaces**: Multi-level navigation
- **Temporal Spaces**: Time-based relevance
- **Scoring Spaces**: Numerical rankings and metrics

### 2. Progressive Disclosure
Spaces are organized in three layers:
- **Discovery**: Broad exploration and understanding
- **Exploration**: Focused analysis and filtering
- **Deep Dive**: Detailed research and full context

### 3. Composability
Spaces can be combined with different weights to create specialized search patterns tailored to specific use cases.

## Space Categories

### Content Spaces (`spaces/content/`)

#### Discovery Spaces
**Purpose**: Enable broad, initial exploration of legal topics

```python
# discovery_spaces.py
discovery_summary_space        # High-level document summaries
discovery_topics_space         # Broad topic categorization
client_takeaways_space        # Simplified key points
```

**When to Use**:
- Initial research on unfamiliar topics
- Building understanding of available content
- Client-facing searches requiring simple language

**Example Usage**:
```python
# Broad exploration of employment law
weights = {
    discovery_summary_space: 3.0,
    discovery_topics_space: 2.5,
    client_takeaways_space: 2.0
}
```

#### Exploration Spaces
**Purpose**: Enable focused analysis of specific legal aspects

```python
# exploration_spaces.py
exploration_provisions_space   # Key legal requirements
exploration_concepts_space     # Legal concepts and principles
exploration_implications_space # Practical impacts
compliance_requirements_space  # Specific compliance needs
penalties_space               # Penalties and consequences
exceptions_space              # Exceptions and exclusions
```

**When to Use**:
- Analyzing specific legal requirements
- Understanding compliance obligations
- Identifying penalties and exceptions

**Example Usage**:
```python
# Compliance-focused search
weights = {
    compliance_requirements_space: 3.0,
    penalties_space: 2.5,
    exceptions_space: 2.0,
    exploration_provisions_space: 2.0
}
```

#### Deep Dive Spaces
**Purpose**: Enable detailed research with full context

```python
# deep_dive_spaces.py
deep_dive_content_space       # Full document text
deep_dive_precedents_space    # Case law references
deep_dive_citations_space     # Citation networks
legislative_history_space     # Historical context
related_documents_space       # Cross-references
chunk_context_space          # Precise citation context
```

**When to Use**:
- Detailed legal research
- Building legal arguments
- Citation verification
- Historical analysis

**Example Usage**:
```python
# Precedent research
weights = {
    deep_dive_precedents_space: 3.0,
    deep_dive_citations_space: 2.5,
    legislative_history_space: 2.0,
    deep_dive_content_space: 2.0
}
```

### Hierarchical Spaces (`spaces/hierarchical/`)

#### Jurisdiction Hierarchy
**Purpose**: Navigate geographic legal hierarchies

```python
# jurisdiction_hierarchy.py
country_jurisdiction_space    # National level (US, Canada)
state_jurisdiction_space      # State/Province level
city_jurisdiction_space       # Local/Municipal level
jurisdiction_path_space       # Full hierarchical paths
legacy_jurisdiction_space     # Backward compatibility
```

**Hierarchy Structure**:
```
United States
├── Federal (special case)
├── Texas
│   ├── Houston
│   ├── Dallas
│   └── Austin
├── California
│   ├── Los Angeles
│   └── San Francisco
└── New York
    └── New York City
```

**When to Use**:
- Jurisdiction-specific searches
- Multi-level geographic filtering
- Federal vs. state law comparisons

#### Practice Area Hierarchy
**Purpose**: Navigate legal practice specializations

```python
# practice_area_hierarchy.py
primary_practice_space        # Top-level categories
secondary_practice_space      # Specializations
specific_practice_space       # Ultra-specific areas
practice_path_space          # Full hierarchical paths
legacy_practice_space        # Backward compatibility
```

**Hierarchy Structure**:
```
Litigation
├── Personal Injury
│   ├── Auto Accidents
│   ├── Medical Malpractice
│   │   ├── Surgical Errors
│   │   └── Misdiagnosis
│   └── Product Liability
└── Commercial Litigation

Corporate
├── Mergers & Acquisitions
│   ├── Hostile Takeovers
│   └── Private Equity
└── Securities
    ├── Insider Trading
    └── IPO Compliance
```

### Preprocessing Spaces (`spaces/preprocessing/`)

#### Fact Extraction Spaces
**Purpose**: Search within AI-extracted facts and findings

```python
# fact_extraction_spaces.py
extracted_facts_space         # All extracted facts
key_findings_space           # Most important facts
fact_locations_space         # Fact source locations
fact_count_space            # Fact density metric
citations_apa_space         # APA formatted citations
internal_citations_space    # Within-document citations
external_citations_space    # Cross-document citations
```

**When to Use**:
- Evidence-based searches
- Fact verification
- Citation tracking
- High-density information retrieval

#### Summary Spaces
**Purpose**: Search within AI-generated summaries

```python
# summary_spaces.py
executive_summary_space      # One-page summaries
summary_bullets_space        # Bullet point summaries
summary_conclusion_space     # Main conclusions
detailed_summary_space       # Comprehensive summaries
key_takeaways_space         # Action items
```

**When to Use**:
- Quick overview searches
- Executive briefings
- Key point extraction

### Temporal Spaces (`spaces/temporal/`)

**Purpose**: Time-based relevance and recency

```python
# recency_spaces.py
published_recency_space      # Publication date recency
effective_date_space         # When laws take effect
last_updated_space          # Recent amendments
```

**Recency Calculation**:
```python
RecencySpace(
    timestamp=legal_document.published_date,
    decay_rate=0.5,  # How quickly relevance decays
    time_period=sl.TimePeriod.MONTHS
)
```

**When to Use**:
- Finding recent changes
- Time-sensitive compliance
- Historical progression analysis

### Scoring Spaces (`spaces/scoring/`)

**Purpose**: Numerical relevance and quality metrics

```python
# relevance_spaces.py
relevance_score_space       # Client relevance (0-10)
confidence_score_space      # AI confidence (0-100)
readability_score_space     # Reading difficulty (0-100)
search_weight_space        # Search boost factor (0-10)
```

**Number Space Modes**:
- `MAXIMUM`: Find highest scores
- `MINIMUM`: Find lowest scores
- `SIMILAR`: Find similar score ranges

**When to Use**:
- Quality filtering
- Relevance ranking
- Confidence thresholds

### Categorical Spaces (`spaces/categorical/`)

#### Legal Taxonomy Spaces
**Purpose**: Legal classification and filtering

```python
# legal_taxonomy_spaces.py
content_type_space          # Document types
authority_level_space       # Legal authority levels
target_audience_space       # Intended readers
complexity_level_space      # Difficulty levels
```

**Categories Example**:
```python
content_type_categories = [
    "statute",          # Legislative law
    "case_law",         # Court decisions
    "regulation",       # Administrative rules
    "commentary",       # Analysis
    "contract",         # Legal agreements
]

authority_level_categories = [
    "primary",          # Binding law
    "secondary",        # Persuasive sources
    "binding",          # Must follow
    "persuasive",       # May consider
]
```

## Space Combinations

### Query Pattern Examples

#### 1. Discovery Pattern
```python
DISCOVERY_PATTERN = {
    # Content understanding
    discovery_summary_space: 3.0,
    discovery_topics_space: 2.5,
    
    # Metadata context
    content_density_space: 1.5,
    coverage_scope_space: 1.5,
    
    # Basic categorization
    primary_practice_space: 1.0,
    country_jurisdiction_space: 1.0
}
```

#### 2. Compliance Pattern
```python
COMPLIANCE_PATTERN = {
    # Requirements focus
    compliance_requirements_space: 3.0,
    penalties_space: 3.0,
    exceptions_space: 2.5,
    
    # Time sensitivity
    effective_date_space: 2.5,
    update_priority_space: 2.0,
    
    # Authority
    authority_level_space: 2.0
}
```

#### 3. Research Pattern
```python
RESEARCH_PATTERN = {
    # Full content
    deep_dive_content_space: 3.0,
    
    # Citations and precedents
    deep_dive_precedents_space: 2.5,
    deep_dive_citations_space: 2.5,
    
    # Supporting information
    legislative_history_space: 2.0,
    related_documents_space: 1.5,
    
    # Search enhancement
    keywords_space: 1.5,
    synonyms_space: 1.0
}
```

#### 4. Executive Briefing Pattern
```python
EXECUTIVE_PATTERN = {
    # Summaries
    executive_summary_space: 3.0,
    summary_bullets_space: 3.0,
    summary_conclusion_space: 2.5,
    
    # Key information
    key_findings_space: 2.5,
    key_takeaways_space: 2.5,
    
    # Relevance
    client_relevance_score: 2.0,
    published_recency_space: 2.0
}
```

## Space Configuration

### Text Similarity Spaces

**Model Selection**:
```python
# Standard model for most content
model="sentence-transformers/all-mpnet-base-v2"

# Alternative models for specific use cases
legal_model="law-ai/bert-legal"  # Legal-specific
multilingual_model="sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
```

**Chunking Configuration**:
```python
# Discovery - larger chunks for context
chunking=sl.Chunking(chunk_size=500, chunk_overlap=100)

# Exploration - medium chunks for precision
chunking=sl.Chunking(chunk_size=300, chunk_overlap=50)

# Deep dive - standard chunks
chunking=sl.Chunking(chunk_size=500, chunk_overlap=100)
```

### Categorical Spaces

**Category Management**:
```python
# Static categories - predefined list
categories=["texas", "california", "florida", ...]

# Dynamic categories - loaded from database
categories=load_categories_from_db()

# Hierarchical categories
categories=build_hierarchy_categories()
```

### Number Spaces

**Range Configuration**:
```python
# Percentage scores
NumberSpace(
    number=field,
    min_value=0,
    max_value=100,
    mode=sl.Mode.MAXIMUM
)

# Rating scales
NumberSpace(
    number=field,
    min_value=0,
    max_value=10,
    mode=sl.Mode.SIMILAR
)
```

## Space Selection Guidelines

### By Use Case

| Use Case | Primary Spaces | Secondary Spaces | Weights |
|----------|---------------|------------------|---------|
| Initial Research | Discovery spaces | Jurisdiction, Practice | 3.0, 1.0 |
| Compliance Check | Compliance, Penalties | Temporal, Authority | 3.0, 2.0 |
| Case Law Research | Precedents, Citations | Deep dive content | 3.0, 2.0 |
| Client Brief | Executive summary | Key takeaways | 3.0, 2.5 |
| Fact Finding | Extracted facts | Citations | 3.0, 2.0 |

### By User Type

| User Type | Recommended Spaces | Avoid |
|-----------|-------------------|--------|
| Attorney | Deep dive, Precedents | Client takeaways |
| Paralegal | Provisions, Compliance | Executive summary |
| Client | Takeaways, Summary | Deep dive, Citations |
| Researcher | All spaces | None |

### By Document Type

| Document Type | Best Spaces | Weight Focus |
|--------------|-------------|--------------|
| Statutes | Provisions, Compliance | Requirements |
| Cases | Precedents, Citations | Facts, Holdings |
| Regulations | Compliance, Penalties | Effective dates |
| Contracts | Provisions, Exceptions | Key terms |

## Performance Optimization

### Space Pruning

```python
def optimize_query_spaces(query: sl.Query, max_spaces: int = 5):
    """
    Limit number of active spaces for performance
    """
    # Sort spaces by weight
    sorted_spaces = sorted(
        query.weights.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    # Keep only top N spaces
    optimized_weights = {}
    for space, weight in sorted_spaces[:max_spaces]:
        optimized_weights[space] = weight
    
    return sl.Query(query.index, weights=optimized_weights)
```

### Space Caching

```python
# Cache frequently used space combinations
CACHED_PATTERNS = {
    "discovery": pre_compute_discovery_pattern(),
    "compliance": pre_compute_compliance_pattern(),
    "research": pre_compute_research_pattern()
}

def get_cached_pattern(pattern_name: str) -> Dict:
    return CACHED_PATTERNS.get(pattern_name, {})
```

### Batch Space Processing

```python
def batch_space_search(
    documents: List[Dict],
    space_groups: Dict[str, List[Space]]
):
    """
    Process multiple space groups efficiently
    """
    results = {}
    
    for group_name, spaces in space_groups.items():
        # Combine spaces in group
        group_query = sl.Query(
            index,
            weights={space: 1.0 for space in spaces}
        )
        
        # Single search for group
        results[group_name] = group_query.execute()
    
    return results
```

## Monitoring Space Usage

### Space Analytics

```python
class SpaceUsageAnalytics:
    """Track which spaces are most effective"""
    
    def __init__(self):
        self.space_usage = {}
        self.space_performance = {}
    
    def log_query(
        self,
        spaces_used: Dict[Space, float],
        result_quality: float,
        user_satisfaction: bool
    ):
        """Log space usage and effectiveness"""
        
        for space, weight in spaces_used.items():
            space_name = space.__class__.__name__
            
            # Track usage frequency
            self.space_usage[space_name] = \
                self.space_usage.get(space_name, 0) + 1
            
            # Track performance
            if space_name not in self.space_performance:
                self.space_performance[space_name] = {
                    "total_quality": 0,
                    "satisfied_queries": 0,
                    "total_queries": 0
                }
            
            stats = self.space_performance[space_name]
            stats["total_quality"] += result_quality * weight
            stats["satisfied_queries"] += int(user_satisfaction)
            stats["total_queries"] += 1
    
    def get_space_effectiveness(self) -> Dict:
        """Calculate effectiveness metrics for each space"""
        
        effectiveness = {}
        
        for space_name, stats in self.space_performance.items():
            effectiveness[space_name] = {
                "usage_count": self.space_usage.get(space_name, 0),
                "avg_quality": stats["total_quality"] / stats["total_queries"],
                "satisfaction_rate": stats["satisfied_queries"] / stats["total_queries"],
                "effectiveness_score": (
                    stats["satisfied_queries"] / stats["total_queries"] *
                    stats["total_quality"] / stats["total_queries"]
                )
            }
        
        return effectiveness
```

### Space Coverage Analysis

```python
def analyze_space_coverage():
    """Analyze which spaces have good document coverage"""
    
    coverage_report = {}
    
    for space_name, space in ALL_SPACES.items():
        # Sample documents
        sample_query = sl.Query(index, weights={space: 1.0})
        results = sample_query.limit(1000).execute()
        
        # Analyze coverage
        non_empty = sum(1 for r in results if has_content(r, space))
        
        coverage_report[space_name] = {
            "total_documents": len(results),
            "populated_documents": non_empty,
            "coverage_percentage": (non_empty / len(results)) * 100,
            "recommendation": get_coverage_recommendation(non_empty / len(results))
        }
    
    return coverage_report
```

## Best Practices

### 1. Space Weight Guidelines

```python
# Weight ranges and their meanings
WEIGHT_GUIDELINES = {
    3.0: "Primary focus - dominant factor in search",
    2.0-2.9: "Important - significant influence",
    1.0-1.9: "Contextual - moderate influence", 
    0.1-0.9: "Minor - slight influence",
    0.0: "Excluded - no influence",
    -1.0: "Inverse - penalize matches"
}
```

### 2. Space Combination Rules

```python
# Complementary spaces that work well together
COMPLEMENTARY_SPACES = [
    (exploration_provisions_space, compliance_requirements_space),
    (deep_dive_precedents_space, deep_dive_citations_space),
    (executive_summary_space, key_takeaways_space),
    (fact_extraction_space, citations_apa_space)
]

# Conflicting spaces to avoid combining
CONFLICTING_SPACES = [
    (discovery_summary_space, deep_dive_content_space),  # Different depths
    (client_takeaways_space, legal_concepts_space),      # Different audiences
]
```

### 3. Space Testing Framework

```python
def test_space_configuration(
    space_config: Dict[Space, float],
    test_queries: List[str],
    expected_results: List[str]
):
    """Test if space configuration meets expectations"""
    
    results = []
    
    for test_query in test_queries:
        query = sl.Query(index, weights=space_config)
        query_results = query.similar(
            primary_space.text, test_query
        ).limit(10).execute()
        
        # Check if expected results appear
        found_expected = sum(
            1 for r in query_results 
            if r.id in expected_results
        )
        
        results.append({
            "query": test_query,
            "found": found_expected,
            "total_expected": len(expected_results),
            "precision": found_expected / 10,
            "recall": found_expected / len(expected_results)
        })
    
    return results
```

## Troubleshooting Common Issues

### Issue: Poor Search Results

**Diagnosis**:
```python
# Check space population
for space in query.weights.keys():
    check_space_data_quality(space)

# Verify weight distribution
total_weight = sum(query.weights.values())
for space, weight in query.weights.items():
    print(f"{space}: {weight/total_weight*100:.1f}%")
```

**Solutions**:
1. Adjust space weights
2. Add complementary spaces
3. Check data population in spaces
4. Verify preprocessing quality

### Issue: Slow Query Performance

**Diagnosis**:
```python
# Count active spaces
active_spaces = len([w for w in query.weights.values() if w > 0])
print(f"Active spaces: {active_spaces}")

# Check chunk sizes
for space in text_spaces:
    print(f"{space}: chunk_size={space.chunk_size}")
```

**Solutions**:
1. Reduce number of active spaces
2. Use space pruning
3. Optimize chunk sizes
4. Enable caching

### Issue: Inconsistent Results

**Diagnosis**:
```python
# Check for conflicting spaces
for space1, space2 in CONFLICTING_SPACES:
    if space1 in query.weights and space2 in query.weights:
        print(f"Warning: Conflicting spaces {space1} and {space2}")
```

**Solutions**:
1. Remove conflicting spaces
2. Adjust relative weights
3. Use space groups instead of individual spaces

## Space Extension Guide

### Adding New Spaces

```python
# Template for new space category
class NewCategorySpaces:
    """
    Purpose: [Describe the purpose]
    Usage: [When to use these spaces]
    """
    
    def __init__(self, schema):
        self.schema = schema
        
        # Define spaces
        self.primary_space = sl.TextSimilaritySpace(
            text=schema.new_field,
            model="sentence-transformers/all-mpnet-base-v2"
        )
        
        self.category_space = sl.CategoricalSimilaritySpace(
            category_list=schema.new_category,
            categories=["option1", "option2", "option3"]
        )
        
    def get_default_weights(self):
        """Default weight configuration"""
        return {
            self.primary_space: 3.0,
            self.category_space: 1.5
        }
```

### Space Migration

```python
def migrate_to_new_space(
    old_space: Space,
    new_space: Space,
    migration_func: callable
):
    """Migrate from old to new space configuration"""
    
    # Get all documents using old space
    old_results = query_with_space(old_space)
    
    # Transform data for new space
    for doc in old_results:
        new_value = migration_func(doc.old_field)
        update_document(doc.id, new_field=new_value)
    
    # Update queries to use new space
    update_query_patterns(old_space, new_space)
```

## Summary

The space architecture provides:

1. **Modularity**: Each space handles one aspect
2. **Flexibility**: Combine spaces for any use case
3. **Performance**: Optimized for specific searches
4. **Extensibility**: Easy to add new spaces
5. **Clarity**: Clear purpose for each space

Remember: The key to effective search is choosing the right combination of spaces with appropriate weights for your specific use case.

---

*Last Updated: 2024*
*Version: 1.0*