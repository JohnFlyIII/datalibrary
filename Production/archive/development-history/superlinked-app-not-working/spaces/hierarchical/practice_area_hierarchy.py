"""
Hierarchical Practice Area Spaces

Purpose:
- Enable drill-down search by legal practice hierarchy
- Support broad to specific practice area navigation
- Allow combined searches across hierarchy levels

Usage:
- Primary level: Broad categories (litigation, corporate, etc.)
- Secondary level: Specific practice types
- Tertiary level: Highly specialized areas
- Path-based: Exact hierarchical matching

Human Note: Practice areas follow a logical hierarchy from general to specific
AI Agent Note: Use higher weights on more specific levels for targeted results
"""

from superlinked import framework as sl
from schema.base.legal_document import LegalDocument

# Initialize the legal document schema
legal_document = LegalDocument()

# Primary Practice Areas - Top Level Categories
primary_practice_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.practice_area_primary,
    categories=[
        # Major Practice Divisions
        "litigation",           # All dispute resolution
        "corporate",           # Business and transactions
        "regulatory",          # Government compliance
        "intellectual_property", # IP and technology
        "real_estate",         # Property and land use
        "tax",                 # Tax planning and disputes
        "labor_employment",    # Workplace law
        "family",              # Personal/family matters
        "criminal",            # Criminal defense/prosecution
        "estate_planning",     # Wills, trusts, probate
        "bankruptcy",          # Debt and insolvency
        "healthcare",          # Medical and healthcare law
        "environmental",       # Environmental regulation
        "immigration",         # Immigration and naturalization
        "international",       # Cross-border matters
    ]
)

# Secondary Practice Areas - Mid Level Specializations
secondary_practice_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.practice_area_secondary,
    categories=[
        # Litigation Subspecialties
        "personal_injury", "medical_malpractice", "product_liability",
        "class_action", "commercial_litigation", "civil_rights",
        "appeals", "arbitration", "mediation",
        
        # Corporate Subspecialties
        "mergers_acquisitions", "securities", "corporate_governance",
        "contracts", "joint_ventures", "private_equity",
        "startup_law", "corporate_finance", "restructuring",
        
        # Regulatory Subspecialties
        "compliance", "antitrust", "trade_regulation",
        "banking_regulation", "energy_regulation", "telecommunications",
        "pharmaceutical", "data_privacy", "cybersecurity",
        
        # IP Subspecialties
        "patents", "trademarks", "copyrights",
        "trade_secrets", "licensing", "technology_transactions",
        "media_entertainment", "software_law", "biotechnology",
        
        # Employment Subspecialties
        "discrimination", "wage_hour", "workers_compensation",
        "employee_benefits", "labor_relations", "workplace_safety",
        "executive_compensation", "non_compete", "whistleblower",
        
        # Real Estate Subspecialties
        "commercial_real_estate", "residential_real_estate", "land_use",
        "construction", "leasing", "zoning", "property_tax",
        
        # Family Law Subspecialties
        "divorce", "child_custody", "child_support", "adoption",
        "prenuptial", "domestic_violence", "guardianship",
        
        # Criminal Law Subspecialties
        "white_collar", "dui_dwi", "drug_crimes", "violent_crimes",
        "federal_crimes", "juvenile", "expungement",
        
        # Healthcare Subspecialties
        "healthcare_compliance", "medical_device", "hipaa",
        "medicare_medicaid", "healthcare_transactions", "telemedicine",
        
        # Add more as needed...
    ]
)

# Tertiary Practice Areas - Highly Specialized
specific_practice_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.practice_area_specific,
    categories=[
        # Ultra-specific specializations
        # Personal Injury Specific
        "auto_accidents", "slip_fall", "traumatic_brain_injury",
        "spinal_cord_injury", "wrongful_death", "nursing_home_abuse",
        
        # Medical Malpractice Specific
        "surgical_errors", "misdiagnosis", "birth_injuries",
        "medication_errors", "hospital_negligence", "dental_malpractice",
        
        # Employment Specific
        "sexual_harassment", "age_discrimination", "disability_discrimination",
        "retaliation", "fmla_violations", "overtime_disputes",
        
        # Corporate Specific
        "hostile_takeovers", "proxy_fights", "insider_trading",
        "sarbanes_oxley", "dodd_frank", "fcpa_compliance",
        
        # IP Specific
        "software_patents", "biotech_patents", "design_patents",
        "trademark_infringement", "copyright_dmca", "patent_litigation",
        
        # Real Estate Specific
        "foreclosure", "eminent_domain", "historic_preservation",
        "environmental_contamination", "affordable_housing", "opportunity_zones",
        
        # Tax Specific
        "tax_controversy", "international_tax", "estate_tax",
        "sales_tax", "tax_credits", "tax_fraud",
        
        # Healthcare Specific
        "stark_law", "anti_kickback", "clinical_trials",
        "pharmacy_law", "behavioral_health", "long_term_care",
        
        # Environmental Specific
        "clean_air", "clean_water", "hazardous_waste",
        "endangered_species", "climate_change", "environmental_justice",
        
        # Add more ultra-specific areas as needed...
    ]
)

# Full Practice Area Path - For hierarchical matching
practice_path_space = sl.TextSimilaritySpace(
    text=legal_document.practice_area_full_path,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Legacy Practice Areas - Backward compatibility
legacy_practice_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.practice_areas,
    categories=[
        "employment", "personal_injury", "medical_malpractice",
        "civil_law", "tort_law", "corporate", "contract_law",
        "intellectual_property", "family_law", "criminal_law",
        "real_estate", "tax_law", "immigration", "bankruptcy"
    ]
)

# Hierarchical Collections
PRACTICE_HIERARCHY_SPACES = [
    primary_practice_space,
    secondary_practice_space,
    specific_practice_space,
    practice_path_space
]

# Export all spaces
__all__ = [
    'primary_practice_space',
    'secondary_practice_space',
    'specific_practice_space',
    'practice_path_space',
    'legacy_practice_space',
    'PRACTICE_HIERARCHY_SPACES'
]

# Usage Examples:
"""
Query Patterns for Practice Area Hierarchy:

1. Broad Litigation Search:
   weights = {
       primary_practice_space: 3.0,      # Focus on "litigation"
       secondary_practice_space: 1.0,    # Include subspecialties
       specific_practice_space: 0.5      # Some specific context
   }

2. Medical Malpractice Focus:
   weights = {
       primary_practice_space: 1.0,      # "litigation" context
       secondary_practice_space: 3.0,    # "medical_malpractice" focus
       specific_practice_space: 2.0      # Include specific types
   }

3. Surgical Error Cases (Ultra-specific):
   weights = {
       primary_practice_space: 0.5,      # General litigation context
       secondary_practice_space: 1.5,    # Medical malpractice
       specific_practice_space: 3.0      # "surgical_errors" focus
   }

4. Path-based Search (litigation/personal_injury/auto_accidents):
   weights = {
       practice_path_space: 3.0          # Exact hierarchical match
   }

5. Cross-hierarchy Search (IP + Patents + Software):
   weights = {
       primary_practice_space: 2.0,      # "intellectual_property"
       secondary_practice_space: 2.5,    # "patents"
       specific_practice_space: 3.0      # "software_patents"
   }
"""