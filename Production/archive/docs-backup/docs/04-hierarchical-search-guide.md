# Hierarchical Search Best Practices Guide

## Overview

Hierarchical search enables precise navigation through legal content organized in tree structures. This guide covers best practices for leveraging jurisdiction (Country → State → City) and practice area hierarchies for optimal search results.

## Understanding Hierarchical Structure

### Jurisdiction Hierarchy

```
United States (Country)
├── Federal (Special case - applies nationwide)
├── Texas (State)
│   ├── Houston (City)
│   ├── Dallas (City)
│   ├── Austin (City)
│   └── San Antonio (City)
├── California (State)
│   ├── Los Angeles (City)
│   ├── San Francisco (City)
│   └── San Diego (City)
└── New York (State)
    ├── New York City (City)
    └── Buffalo (City)
```

### Practice Area Hierarchy

```
Litigation (Primary)
├── Personal Injury (Secondary)
│   ├── Auto Accidents (Specific)
│   ├── Medical Malpractice (Specific)
│   │   ├── Surgical Errors (Ultra-specific)
│   │   └── Misdiagnosis (Ultra-specific)
│   └── Product Liability (Specific)
├── Commercial Litigation (Secondary)
└── Civil Rights (Secondary)

Corporate (Primary)
├── Mergers & Acquisitions (Secondary)
│   ├── Hostile Takeovers (Specific)
│   └── Private Equity (Specific)
└── Securities (Secondary)
    ├── Insider Trading (Specific)
    └── IPO Compliance (Specific)
```

## Core Concepts

### 1. Hierarchy Levels and Weights

Each level in the hierarchy should be weighted based on search intent:

```python
# Searching for city-specific ordinances
city_focused_weights = {
    country_jurisdiction_space: 0.5,  # Minimal federal context
    state_jurisdiction_space: 1.0,    # Some state context
    city_jurisdiction_space: 3.0      # Primary focus
}

# Searching for state law with federal context
state_with_federal_weights = {
    country_jurisdiction_space: 2.0,  # Important federal overlap
    state_jurisdiction_space: 3.0,    # Primary focus
    city_jurisdiction_space: 0.0     # Exclude local variations
}
```

### 2. Path-Based Navigation

Use full hierarchical paths for precise matching:

```python
# Exact path matching
exact_path = "united_states/texas/houston"
practice_path = "litigation/personal_injury/medical_malpractice"

# Path pattern matching (prefix search)
path_prefix = "united_states/texas/*"  # All Texas cities
practice_prefix = "litigation/personal_injury/*"  # All PI subcategories
```

### 3. Inheritance and Context

Higher levels provide context for lower levels:

- Federal law influences state law
- State law influences city ordinances
- Primary practice areas inform secondary specializations

## Search Strategies

### 1. Bottom-Up Search (Specific to General)

Start with the most specific level and expand upward as needed.

```python
def bottom_up_search(city: str, state: str, country: str, query_text: str):
    """
    Search starting from city level, expanding up if needed
    """
    
    # Stage 1: City-specific search
    city_results = sl.Query(
        legal_knowledge_index,
        weights={
            city_jurisdiction_space: 3.0,
            deep_dive_content_space: 2.0
        }
    ).filter(
        legal_document.jurisdiction_city == city
    ).similar(
        deep_dive_content_space.text, query_text
    ).limit(20).execute()
    
    if len(city_results) >= 10:
        return city_results  # Sufficient city-level results
    
    # Stage 2: Expand to state level
    state_results = sl.Query(
        legal_knowledge_index,
        weights={
            state_jurisdiction_space: 3.0,
            city_jurisdiction_space: 1.0,  # Still prefer local
            deep_dive_content_space: 2.0
        }
    ).filter(
        legal_document.jurisdiction_state == state
    ).similar(
        deep_dive_content_space.text, query_text
    ).limit(20).execute()
    
    # Combine results, prioritizing city-level
    combined = city_results + [r for r in state_results if r not in city_results]
    
    if len(combined) >= 15:
        return combined[:20]
    
    # Stage 3: Include federal if still needed
    federal_results = sl.Query(
        legal_knowledge_index,
        weights={
            country_jurisdiction_space: 3.0,
            deep_dive_content_space: 2.0
        }
    ).filter(
        legal_document.jurisdiction_country == country
    ).similar(
        deep_dive_content_space.text, query_text
    ).limit(10).execute()
    
    return combined + federal_results
```

### 2. Top-Down Search (General to Specific)

Start broad and drill down based on relevance.

```python
def top_down_search(
    primary_practice: str,
    secondary_practice: str = None,
    specific_practice: str = None,
    query_text: str = None
):
    """
    Search starting from primary practice area, drilling down
    """
    
    # Stage 1: Broad primary category search
    primary_results = sl.Query(
        legal_knowledge_index,
        weights={
            primary_practice_space: 3.0,
            discovery_summary_space: 2.0,
            discovery_topics_space: 2.0
        }
    ).filter(
        legal_document.practice_area_primary == primary_practice
    ).limit(100).execute()  # Cast wide net
    
    # Analyze distribution of secondary areas
    secondary_distribution = {}
    for result in primary_results:
        sec = result.practice_area_secondary
        secondary_distribution[sec] = secondary_distribution.get(sec, 0) + 1
    
    # Stage 2: Focus on most relevant secondary area
    if secondary_practice:
        target_secondary = secondary_practice
    else:
        # Auto-select most common secondary area
        target_secondary = max(secondary_distribution, key=secondary_distribution.get)
    
    secondary_results = sl.Query(
        legal_knowledge_index,
        weights={
            secondary_practice_space: 3.0,
            primary_practice_space: 1.0,
            exploration_provisions_space: 2.5
        }
    ).filter(
        legal_document.practice_area_secondary == target_secondary
    ).similar(
        exploration_provisions_space.text, query_text
    ).limit(30).execute()
    
    # Stage 3: Drill to specific if provided
    if specific_practice:
        specific_results = sl.Query(
            legal_knowledge_index,
            weights={
                specific_practice_space: 3.0,
                secondary_practice_space: 1.5,
                deep_dive_content_space: 2.5
            }
        ).filter(
            legal_document.practice_area_specific == specific_practice
        ).limit(20).execute()
        
        return specific_results
    
    return secondary_results
```

### 3. Cross-Hierarchy Search

Combine jurisdiction and practice area hierarchies.

```python
def cross_hierarchy_search(
    jurisdiction_path: str,
    practice_path: str,
    query_text: str,
    temporal_filter: str = None
):
    """
    Search across both hierarchies simultaneously
    
    Example:
    - jurisdiction_path: "united_states/texas/houston"
    - practice_path: "litigation/personal_injury/auto_accidents"
    """
    
    # Parse paths
    j_parts = jurisdiction_path.split('/')
    p_parts = practice_path.split('/')
    
    # Build dynamic weights based on path depth
    weights = {
        deep_dive_content_space: 2.5,
        exploration_provisions_space: 2.0
    }
    
    # Jurisdiction weights (deeper = higher weight)
    if len(j_parts) >= 1:
        weights[country_jurisdiction_space] = 1.0
    if len(j_parts) >= 2:
        weights[state_jurisdiction_space] = 2.0
    if len(j_parts) >= 3:
        weights[city_jurisdiction_space] = 3.0
    
    # Practice area weights (deeper = higher weight)
    if len(p_parts) >= 1:
        weights[primary_practice_space] = 1.0
    if len(p_parts) >= 2:
        weights[secondary_practice_space] = 2.0
    if len(p_parts) >= 3:
        weights[specific_practice_space] = 3.0
    
    # Add temporal weight if specified
    if temporal_filter == "recent":
        weights[published_recency_space] = 2.5
    elif temporal_filter == "historical":
        weights[published_recency_space] = -1.0  # Negative for older docs
    
    # Build query
    query = sl.Query(legal_knowledge_index, weights=weights)
    
    # Apply filters
    query = query.filter(
        legal_document.jurisdiction_full_path == jurisdiction_path
    ).filter(
        legal_document.practice_area_full_path == practice_path
    )
    
    # Add text similarity if provided
    if query_text:
        query = query.similar(deep_dive_content_space.text, query_text)
    
    return query.limit(25).execute()
```

### 4. Sibling Search

Find related content at the same hierarchy level.

```python
def sibling_jurisdiction_search(
    current_state: str,
    query_text: str,
    exclude_current: bool = True
):
    """
    Search similar laws in sibling jurisdictions
    
    Example: If searching Texas employment law, also search
    California, New York, Florida employment laws
    """
    
    # Define sibling states (similar size/economy)
    state_siblings = {
        "texas": ["california", "florida", "new_york", "illinois"],
        "california": ["texas", "new_york", "florida", "illinois"],
        "new_york": ["california", "texas", "new_jersey", "pennsylvania"],
        # Add more mappings
    }
    
    siblings = state_siblings.get(current_state, [])
    
    if exclude_current and current_state in siblings:
        siblings.remove(current_state)
    
    # Search across sibling jurisdictions
    results = {}
    
    for sibling_state in siblings:
        sibling_results = sl.Query(
            legal_knowledge_index,
            weights={
                state_jurisdiction_space: 3.0,
                exploration_provisions_space: 2.5,
                deep_dive_content_space: 2.0
            }
        ).filter(
            legal_document.jurisdiction_state == sibling_state
        ).similar(
            exploration_provisions_space.text, query_text
        ).limit(10).execute()
        
        results[sibling_state] = sibling_results
    
    return results
```

## Advanced Hierarchical Patterns

### 1. Dynamic Hierarchy Exploration

```python
class HierarchicalExplorer:
    """
    Dynamically explore hierarchies based on result distribution
    """
    
    def __init__(self, index):
        self.index = index
        self.exploration_history = []
    
    def explore_jurisdiction(self, starting_point: str, topic: str):
        """
        Explore jurisdiction hierarchy adaptively
        """
        
        # Start with broad search
        initial_results = sl.Query(
            self.index,
            weights={
                discovery_summary_space: 3.0,
                discovery_topics_space: 2.5
            }
        ).similar(
            discovery_summary_space.text, topic
        ).limit(200).execute()
        
        # Analyze jurisdiction distribution
        jurisdiction_stats = self.analyze_jurisdiction_distribution(initial_results)
        
        # Identify promising branches
        promising_paths = self.identify_promising_paths(jurisdiction_stats)
        
        # Explore each promising path
        exploration_results = {}
        
        for path in promising_paths:
            depth_results = self.explore_path_depth(path, topic)
            exploration_results[path] = depth_results
            
        return exploration_results
    
    def analyze_jurisdiction_distribution(self, results):
        """Analyze how results are distributed across jurisdictions"""
        
        stats = {
            "country": {},
            "state": {},
            "city": {}
        }
        
        for result in results:
            # Country level
            country = result.jurisdiction_country
            if country:
                stats["country"][country] = stats["country"].get(country, 0) + 1
            
            # State level
            state = result.jurisdiction_state
            if state:
                stats["state"][state] = stats["state"].get(state, 0) + 1
            
            # City level
            city = result.jurisdiction_city
            if city:
                stats["city"][city] = stats["city"].get(city, 0) + 1
        
        return stats
    
    def identify_promising_paths(self, stats, threshold=0.1):
        """Identify jurisdiction paths worth exploring"""
        
        total_docs = sum(stats["country"].values())
        promising = []
        
        # Find jurisdictions with significant content
        for country, count in stats["country"].items():
            if count / total_docs > threshold:
                # Check state distribution within country
                country_states = self.get_states_for_country(country, stats)
                
                for state, state_count in country_states.items():
                    if state_count / count > threshold:
                        # Check city distribution within state
                        state_cities = self.get_cities_for_state(state, stats)
                        
                        if state_cities:
                            # Deep hierarchy available
                            for city, city_count in state_cities.items():
                                if city_count / state_count > threshold:
                                    promising.append(f"{country}/{state}/{city}")
                        else:
                            # State level only
                            promising.append(f"{country}/{state}")
        
        return promising
    
    def explore_path_depth(self, path: str, topic: str):
        """Explore a specific hierarchical path in depth"""
        
        parts = path.split('/')
        depth_results = {}
        
        # Explore each level
        for i in range(1, len(parts) + 1):
            current_path = '/'.join(parts[:i])
            level_name = ['country', 'state', 'city'][i-1]
            
            # Search at this level
            level_results = self.search_at_level(current_path, level_name, topic)
            
            depth_results[level_name] = {
                "path": current_path,
                "result_count": len(level_results),
                "top_results": level_results[:5]
            }
        
        return depth_results
```

### 2. Hierarchical Faceting

```python
def hierarchical_faceted_search(
    base_query: str,
    facet_hierarchy: Dict[str, List[str]],
    min_docs_per_facet: int = 5
):
    """
    Perform faceted search with hierarchical drill-down
    
    facet_hierarchy = {
        "jurisdiction": ["country", "state", "city"],
        "practice": ["primary", "secondary", "specific"],
        "time": ["year", "quarter", "month"]
    }
    """
    
    # Initial broad search
    base_results = sl.Query(
        legal_knowledge_index,
        weights={
            discovery_summary_space: 3.0,
            deep_dive_content_space: 2.0
        }
    ).similar(
        discovery_summary_space.text, base_query
    ).limit(500).execute()
    
    # Build facet tree
    facet_tree = {}
    
    for facet_name, levels in facet_hierarchy.items():
        facet_tree[facet_name] = build_facet_tree(
            base_results, 
            facet_name, 
            levels,
            min_docs_per_facet
        )
    
    return facet_tree


def build_facet_tree(results, facet_name, levels, min_docs):
    """Build hierarchical facet tree from results"""
    
    tree = {"name": facet_name, "children": {}}
    
    # Group by first level
    if facet_name == "jurisdiction":
        level_groups = group_by_jurisdiction_level(results, levels[0])
    elif facet_name == "practice":
        level_groups = group_by_practice_level(results, levels[0])
    else:
        level_groups = {}
    
    # Build tree recursively
    for group_value, group_results in level_groups.items():
        if len(group_results) >= min_docs:
            # Add this node
            node = {
                "value": group_value,
                "count": len(group_results),
                "children": {}
            }
            
            # Recurse to next level if available
            if len(levels) > 1:
                child_tree = build_facet_tree(
                    group_results,
                    facet_name,
                    levels[1:],
                    min_docs
                )
                node["children"] = child_tree["children"]
            
            tree["children"][group_value] = node
    
    return tree
```

### 3. Hierarchy-Aware Result Ranking

```python
class HierarchicalRanker:
    """
    Rank results considering hierarchical relationships
    """
    
    def __init__(self, hierarchy_weights: Dict[str, float]):
        """
        hierarchy_weights = {
            "exact_match": 1.0,      # Exact hierarchy match
            "parent_match": 0.7,     # Parent level match
            "child_match": 0.8,      # Child level match
            "sibling_match": 0.5,    # Sibling match
            "cousin_match": 0.3      # Cousin match (same parent)
        }
        """
        self.weights = hierarchy_weights
    
    def rank_results(
        self,
        results: List,
        target_jurisdiction: str,
        target_practice: str
    ) -> List:
        """
        Rank results based on hierarchical distance
        """
        
        scored_results = []
        
        for result in results:
            # Calculate jurisdiction score
            j_score = self.calculate_hierarchy_score(
                target_jurisdiction,
                result.jurisdiction_full_path,
                "jurisdiction"
            )
            
            # Calculate practice area score
            p_score = self.calculate_hierarchy_score(
                target_practice,
                result.practice_area_full_path,
                "practice"
            )
            
            # Combined score (customize weights as needed)
            combined_score = (j_score * 0.6) + (p_score * 0.4)
            
            scored_results.append((result, combined_score))
        
        # Sort by score descending
        scored_results.sort(key=lambda x: x[1], reverse=True)
        
        return [result for result, score in scored_results]
    
    def calculate_hierarchy_score(
        self,
        target_path: str,
        result_path: str,
        hierarchy_type: str
    ) -> float:
        """
        Calculate hierarchical distance score
        """
        
        if not target_path or not result_path:
            return 0.0
        
        target_parts = target_path.split('/')
        result_parts = result_path.split('/')
        
        # Exact match
        if target_path == result_path:
            return self.weights["exact_match"]
        
        # Parent match (result is parent of target)
        if len(result_parts) < len(target_parts):
            if target_path.startswith(result_path + '/'):
                return self.weights["parent_match"]
        
        # Child match (result is child of target)
        if len(result_parts) > len(target_parts):
            if result_path.startswith(target_path + '/'):
                return self.weights["child_match"]
        
        # Sibling match (same parent)
        if len(result_parts) == len(target_parts) and len(result_parts) > 1:
            if '/'.join(target_parts[:-1]) == '/'.join(result_parts[:-1]):
                return self.weights["sibling_match"]
        
        # Cousin match (same grandparent)
        if len(result_parts) >= 2 and len(target_parts) >= 2:
            if target_parts[0] == result_parts[0]:
                return self.weights["cousin_match"]
        
        return 0.0
```

## Implementation Best Practices

### 1. Metadata Enrichment During Ingestion

```python
def enrich_hierarchical_metadata(document: Dict) -> Dict:
    """
    Ensure all hierarchical fields are properly populated
    """
    
    # Build full paths if not present
    if not document.get("jurisdiction_full_path"):
        path_parts = []
        if document.get("jurisdiction_country"):
            path_parts.append(document["jurisdiction_country"])
        if document.get("jurisdiction_state"):
            path_parts.append(document["jurisdiction_state"])
        if document.get("jurisdiction_city"):
            path_parts.append(document["jurisdiction_city"])
        
        document["jurisdiction_full_path"] = "/".join(path_parts)
    
    # Infer missing levels from paths
    if document.get("jurisdiction_full_path") and not document.get("jurisdiction_state"):
        parts = document["jurisdiction_full_path"].split('/')
        if len(parts) >= 2:
            document["jurisdiction_country"] = parts[0]
            document["jurisdiction_state"] = parts[1]
        if len(parts) >= 3:
            document["jurisdiction_city"] = parts[2]
    
    # Similar for practice areas
    if not document.get("practice_area_full_path"):
        path_parts = []
        if document.get("practice_area_primary"):
            path_parts.append(document["practice_area_primary"])
        if document.get("practice_area_secondary"):
            path_parts.append(document["practice_area_secondary"])
        if document.get("practice_area_specific"):
            path_parts.append(document["practice_area_specific"])
        
        document["practice_area_full_path"] = "/".join(path_parts)
    
    return document
```

### 2. Query Optimization for Hierarchies

```python
class HierarchicalQueryOptimizer:
    """
    Optimize queries for hierarchical searches
    """
    
    def optimize_query(self, query: sl.Query, search_context: Dict) -> sl.Query:
        """
        Optimize query based on hierarchical context
        """
        
        # Determine search depth
        depth = search_context.get("hierarchy_depth", "auto")
        
        if depth == "shallow":
            # Emphasize higher levels
            return self.adjust_weights_for_shallow(query)
        elif depth == "deep":
            # Emphasize lower levels
            return self.adjust_weights_for_deep(query)
        else:
            # Auto-detect optimal depth
            return self.auto_optimize_depth(query, search_context)
    
    def adjust_weights_for_shallow(self, query: sl.Query) -> sl.Query:
        """Adjust weights for broad, shallow searches"""
        
        new_weights = {}
        for space, weight in query.weights.items():
            if space in [country_jurisdiction_space, primary_practice_space]:
                new_weights[space] = weight * 1.5
            elif space in [city_jurisdiction_space, specific_practice_space]:
                new_weights[space] = weight * 0.5
            else:
                new_weights[space] = weight
        
        return sl.Query(query.index, weights=new_weights)
    
    def adjust_weights_for_deep(self, query: sl.Query) -> sl.Query:
        """Adjust weights for narrow, deep searches"""
        
        new_weights = {}
        for space, weight in query.weights.items():
            if space in [city_jurisdiction_space, specific_practice_space]:
                new_weights[space] = weight * 1.5
            elif space in [country_jurisdiction_space, primary_practice_space]:
                new_weights[space] = weight * 0.5
            else:
                new_weights[space] = weight
        
        return sl.Query(query.index, weights=new_weights)
```

### 3. Hierarchy Navigation UI Patterns

```python
class HierarchicalNavigator:
    """
    Support UI navigation through hierarchies
    """
    
    def get_breadcrumb_data(self, current_path: str) -> List[Dict]:
        """
        Generate breadcrumb navigation data
        
        Example: "united_states/texas/houston" ->
        [
            {"label": "United States", "path": "united_states", "level": "country"},
            {"label": "Texas", "path": "united_states/texas", "level": "state"},
            {"label": "Houston", "path": "united_states/texas/houston", "level": "city"}
        ]
        """
        
        parts = current_path.split('/')
        breadcrumbs = []
        
        for i, part in enumerate(parts):
            level = ["country", "state", "city"][i] if i < 3 else f"level_{i}"
            
            breadcrumbs.append({
                "label": part.replace('_', ' ').title(),
                "path": '/'.join(parts[:i+1]),
                "level": level
            })
        
        return breadcrumbs
    
    def get_sibling_options(self, current_path: str) -> List[Dict]:
        """
        Get sibling options at current level
        """
        
        if not current_path:
            return []
        
        parts = current_path.split('/')
        current_level = len(parts)
        current_value = parts[-1]
        
        # Query for siblings
        if current_level == 1:  # Country level
            siblings = ["united_states", "canada", "mexico"]
        elif current_level == 2:  # State level
            parent_country = parts[0]
            siblings = self.get_states_for_country(parent_country)
        elif current_level == 3:  # City level
            parent_state = parts[1]
            siblings = self.get_cities_for_state(parent_state)
        
        # Format for UI
        sibling_options = []
        for sibling in siblings:
            if sibling != current_value:
                new_path = '/'.join(parts[:-1] + [sibling])
                sibling_options.append({
                    "label": sibling.replace('_', ' ').title(),
                    "value": sibling,
                    "path": new_path,
                    "is_current": False
                })
        
        return sibling_options
    
    def get_child_options(self, current_path: str) -> List[Dict]:
        """
        Get child options for drilling down
        """
        
        parts = current_path.split('/') if current_path else []
        current_level = len(parts)
        
        # Get children based on level
        if current_level == 0:  # No selection yet
            children = ["united_states", "canada", "mexico"]
            child_level = "country"
        elif current_level == 1:  # Country selected
            children = self.get_states_for_country(parts[0])
            child_level = "state"
        elif current_level == 2:  # State selected
            children = self.get_cities_for_state(parts[1])
            child_level = "city"
        else:
            return []  # No more levels
        
        # Format for UI
        child_options = []
        for child in children:
            child_path = current_path + '/' + child if current_path else child
            child_options.append({
                "label": child.replace('_', ' ').title(),
                "value": child,
                "path": child_path,
                "level": child_level,
                "has_children": current_level < 2  # Cities don't have children
            })
        
        return child_options
```

## Common Pitfalls and Solutions

### 1. Over-Specificity

**Problem**: Searching too deep in hierarchy returns no results

**Solution**: Implement fallback to parent levels

```python
def search_with_fallback(target_path: str, min_results: int = 5):
    parts = target_path.split('/')
    
    for i in range(len(parts), 0, -1):
        current_path = '/'.join(parts[:i])
        results = search_at_path(current_path)
        
        if len(results) >= min_results:
            return results, current_path
    
    return [], None
```

### 2. Missing Hierarchy Data

**Problem**: Documents lack complete hierarchical metadata

**Solution**: Infer from available data

```python
def infer_hierarchy(document: Dict) -> Dict:
    # Infer from title
    if "Houston" in document.get("title", ""):
        document["jurisdiction_city"] = "houston"
        document["jurisdiction_state"] = "texas"
        document["jurisdiction_country"] = "united_states"
    
    # Infer from content
    content = document.get("content_text", "")
    if "Texas Labor Code" in content:
        document["jurisdiction_state"] = "texas"
        document["practice_area_primary"] = "labor_employment"
    
    return document
```

### 3. Hierarchy Mismatch

**Problem**: User expects different hierarchy than data provides

**Solution**: Provide hierarchy mapping and translation

```python
HIERARCHY_ALIASES = {
    "jurisdiction": {
        "usa": "united_states",
        "us": "united_states",
        "tx": "texas",
        "ca": "california",
        "ny": "new_york",
        "nyc": "new_york_city"
    },
    "practice": {
        "pi": "personal_injury",
        "ip": "intellectual_property",
        "ma": "mergers_acquisitions"
    }
}

def normalize_hierarchy_value(value: str, hierarchy_type: str) -> str:
    """Normalize user input to canonical hierarchy values"""
    
    value_lower = value.lower().replace(' ', '_')
    
    if hierarchy_type in HIERARCHY_ALIASES:
        aliases = HIERARCHY_ALIASES[hierarchy_type]
        return aliases.get(value_lower, value_lower)
    
    return value_lower
```

## Performance Considerations

### 1. Index Optimization

```python
# Create composite indices for common hierarchy queries
composite_indices = [
    ["jurisdiction_country", "jurisdiction_state", "jurisdiction_city"],
    ["practice_area_primary", "practice_area_secondary"],
    ["jurisdiction_full_path"],
    ["practice_area_full_path"]
]
```

### 2. Caching Strategy

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_hierarchy_stats(path: str) -> Dict:
    """Cache hierarchy statistics for common paths"""
    
    results = query_path(path)
    return {
        "document_count": len(results),
        "child_distribution": analyze_children(results),
        "common_topics": extract_topics(results)
    }
```

### 3. Batch Processing

```python
def batch_hierarchy_search(paths: List[str]) -> Dict[str, List]:
    """Process multiple hierarchy paths efficiently"""
    
    # Group by common prefixes
    prefix_groups = {}
    for path in paths:
        prefix = path.split('/')[0]
        if prefix not in prefix_groups:
            prefix_groups[prefix] = []
        prefix_groups[prefix].append(path)
    
    # Search each group
    results = {}
    for prefix, group_paths in prefix_groups.items():
        # Single query for the group
        group_results = search_prefix_group(prefix, group_paths)
        
        # Distribute to individual paths
        for path in group_paths:
            results[path] = filter_results_for_path(group_results, path)
    
    return results
```

## Monitoring and Analytics

### 1. Hierarchy Usage Tracking

```python
class HierarchyAnalytics:
    """Track how users navigate hierarchies"""
    
    def __init__(self):
        self.path_visits = {}
        self.navigation_patterns = []
        
    def log_search(self, path: str, result_count: int, user_id: str):
        """Log hierarchy search"""
        
        self.path_visits[path] = self.path_visits.get(path, 0) + 1
        
        self.navigation_patterns.append({
            "timestamp": datetime.now(),
            "user_id": user_id,
            "path": path,
            "level": len(path.split('/')),
            "result_count": result_count
        })
    
    def get_popular_paths(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """Get most searched paths"""
        
        return sorted(
            self.path_visits.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]
    
    def analyze_navigation_depth(self) -> Dict:
        """Analyze how deep users typically navigate"""
        
        depth_stats = {}
        for pattern in self.navigation_patterns:
            depth = pattern["level"]
            depth_stats[depth] = depth_stats.get(depth, 0) + 1
        
        return depth_stats
```

### 2. Hierarchy Coverage Analysis

```python
def analyze_hierarchy_coverage() -> Dict:
    """Analyze document distribution across hierarchy"""
    
    coverage = {
        "jurisdiction": {
            "total_countries": 0,
            "total_states": 0,
            "total_cities": 0,
            "coverage_gaps": []
        },
        "practice": {
            "total_primary": 0,
            "total_secondary": 0,
            "total_specific": 0,
            "coverage_gaps": []
        }
    }
    
    # Query all unique values
    all_docs = query_all_documents()
    
    # Analyze jurisdiction coverage
    countries = set()
    states = set()
    cities = set()
    
    for doc in all_docs:
        if doc.jurisdiction_country:
            countries.add(doc.jurisdiction_country)
        if doc.jurisdiction_state:
            states.add(doc.jurisdiction_state)
        if doc.jurisdiction_city:
            cities.add(doc.jurisdiction_city)
    
    coverage["jurisdiction"]["total_countries"] = len(countries)
    coverage["jurisdiction"]["total_states"] = len(states)
    coverage["jurisdiction"]["total_cities"] = len(cities)
    
    # Identify gaps (expected but missing)
    expected_states = ["texas", "california", "new_york", "florida"]
    missing_states = [s for s in expected_states if s not in states]
    coverage["jurisdiction"]["coverage_gaps"] = missing_states
    
    return coverage
```

## Best Practices Summary

### Do's

1. **Always populate full hierarchy paths** during ingestion
2. **Use appropriate weights** for each hierarchy level
3. **Implement fallback strategies** for sparse data
4. **Cache hierarchy statistics** for performance
5. **Provide navigation aids** (breadcrumbs, siblings, children)
6. **Monitor usage patterns** to optimize common paths
7. **Test with real hierarchical queries** before deployment

### Don'ts

1. **Don't assume complete hierarchy data** - always handle missing levels
2. **Don't over-weight specific levels** without testing
3. **Don't ignore sibling relationships** - they provide valuable context
4. **Don't hardcode hierarchy structures** - keep them configurable
5. **Don't forget to index** hierarchical paths for performance

### Quick Reference

```python
# Jurisdiction hierarchy search template
def search_jurisdiction(country=None, state=None, city=None, topic=None):
    weights = {}
    filters = []
    
    if city:
        weights[city_jurisdiction_space] = 3.0
        filters.append(f"jurisdiction_city == '{city}'")
    if state:
        weights[state_jurisdiction_space] = 2.0 if not city else 1.0
        filters.append(f"jurisdiction_state == '{state}'")
    if country:
        weights[country_jurisdiction_space] = 1.0
        filters.append(f"jurisdiction_country == '{country}'")
    
    return build_query(weights, filters, topic)

# Practice area hierarchy search template  
def search_practice(primary=None, secondary=None, specific=None, topic=None):
    weights = {}
    filters = []
    
    if specific:
        weights[specific_practice_space] = 3.0
        filters.append(f"practice_area_specific == '{specific}'")
    if secondary:
        weights[secondary_practice_space] = 2.0 if not specific else 1.0
        filters.append(f"practice_area_secondary == '{secondary}'")
    if primary:
        weights[primary_practice_space] = 1.0
        filters.append(f"practice_area_primary == '{primary}'")
    
    return build_query(weights, filters, topic)
```

---

*Last Updated: 2024*
*Version: 1.0*