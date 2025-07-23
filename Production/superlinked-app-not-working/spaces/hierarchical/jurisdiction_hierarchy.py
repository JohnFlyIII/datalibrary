"""
Hierarchical Jurisdiction Spaces

Purpose:
- Enable drill-down search by geographic hierarchy (Country -> State -> City)
- Support multi-level jurisdiction filtering
- Allow searches at any level of the hierarchy

Usage:
- Use country_space for broad federal/national searches
- Use state_space for state-level filtering
- Use city_space for local/municipal searches
- Combine spaces with different weights for flexible geographic search

Human Note: These spaces work together to create a geographic hierarchy
AI Agent Note: When querying, consider using multiple levels with decreasing weights
"""

from superlinked import framework as sl
from schema.base.legal_document import LegalDocument

# Initialize the legal document schema
legal_document = LegalDocument()

# Country Level - Highest geographic hierarchy
country_jurisdiction_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.jurisdiction_country,
    categories=[
        # North America
        "united_states",
        "canada",
        "mexico",
        
        # Future expansion
        "united_kingdom",
        "european_union",
        "australia",
        "international"
    ]
)

# State/Province Level - Middle hierarchy
state_jurisdiction_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.jurisdiction_state,
    categories=[
        # US States (all 50 + territories)
        "alabama", "alaska", "arizona", "arkansas", "california",
        "colorado", "connecticut", "delaware", "florida", "georgia",
        "hawaii", "idaho", "illinois", "indiana", "iowa",
        "kansas", "kentucky", "louisiana", "maine", "maryland",
        "massachusetts", "michigan", "minnesota", "mississippi", "missouri",
        "montana", "nebraska", "nevada", "new_hampshire", "new_jersey",
        "new_mexico", "new_york", "north_carolina", "north_dakota", "ohio",
        "oklahoma", "oregon", "pennsylvania", "rhode_island", "south_carolina",
        "south_dakota", "tennessee", "texas", "utah", "vermont",
        "virginia", "washington", "west_virginia", "wisconsin", "wyoming",
        
        # US Territories
        "puerto_rico", "us_virgin_islands", "guam", "american_samoa",
        
        # Canadian Provinces
        "ontario", "quebec", "british_columbia", "alberta", "manitoba",
        "saskatchewan", "nova_scotia", "new_brunswick", "newfoundland",
        "prince_edward_island", "northwest_territories", "yukon", "nunavut",
        
        # Special
        "federal", "multi_state", "interstate"
    ]
)

# City/Local Level - Lowest hierarchy
city_jurisdiction_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.jurisdiction_city,
    categories=[
        # Major US Cities (expandable based on your needs)
        # Texas
        "houston", "dallas", "austin", "san_antonio", "fort_worth",
        "el_paso", "arlington", "corpus_christi", "plano", "lubbock",
        
        # California
        "los_angeles", "san_diego", "san_francisco", "san_jose", "sacramento",
        "fresno", "oakland", "long_beach", "bakersfield", "anaheim",
        
        # Florida
        "miami", "tampa", "orlando", "jacksonville", "st_petersburg",
        "hialeah", "tallahassee", "fort_lauderdale", "cape_coral", "pembroke_pines",
        
        # New York
        "new_york_city", "buffalo", "rochester", "yonkers", "syracuse",
        "albany", "new_rochelle", "mount_vernon", "schenectady", "utica",
        
        # Illinois
        "chicago", "aurora", "rockford", "joliet", "naperville",
        "springfield", "peoria", "elgin", "waukegan", "cicero",
        
        # Add more cities as needed
        "philadelphia", "phoenix", "detroit", "seattle", "boston",
        "denver", "washington_dc", "las_vegas", "portland", "atlanta",
        
        # Generic
        "county_level", "municipal", "township", "unincorporated"
    ]
)

# Full Path Space - For exact hierarchical matching
jurisdiction_path_space = sl.TextSimilaritySpace(
    text=legal_document.jurisdiction_full_path,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Legacy Jurisdiction Space - For backward compatibility
legacy_jurisdiction_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.jurisdiction,
    categories=[
        "federal", "supreme_court", "circuit_court", "district_court",
        "texas", "california", "florida", "new_york", "illinois",
        "municipal", "county", "local_government", "international"
    ]
)

# Hierarchical Query Collections
JURISDICTION_HIERARCHY_SPACES = [
    country_jurisdiction_space,
    state_jurisdiction_space,
    city_jurisdiction_space,
    jurisdiction_path_space
]

# Export all spaces
__all__ = [
    'country_jurisdiction_space',
    'state_jurisdiction_space', 
    'city_jurisdiction_space',
    'jurisdiction_path_space',
    'legacy_jurisdiction_space',
    'JURISDICTION_HIERARCHY_SPACES'
]

# Usage Examples in Comments:
"""
Example Query Patterns:

1. Federal Law Search (Country-level only):
   weights = {
       country_jurisdiction_space: 3.0,
       state_jurisdiction_space: 0.0,
       city_jurisdiction_space: 0.0
   }

2. Texas State Law (State-specific):
   weights = {
       country_jurisdiction_space: 1.0,  # Include federal
       state_jurisdiction_space: 3.0,    # Focus on Texas
       city_jurisdiction_space: 0.0      # Exclude city-specific
   }

3. Houston Municipal Law (City-specific):
   weights = {
       country_jurisdiction_space: 0.5,  # Some federal context
       state_jurisdiction_space: 1.0,    # State law matters
       city_jurisdiction_space: 3.0      # Focus on Houston
   }

4. Hierarchical Drill-down (US -> Texas -> Houston):
   weights = {
       jurisdiction_path_space: 3.0      # Match exact path
   }
"""