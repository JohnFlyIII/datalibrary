-- Legal Knowledge System Database Initialization

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create legal_documents table for metadata
CREATE TABLE IF NOT EXISTS legal_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id VARCHAR(255) UNIQUE NOT NULL,
    title TEXT NOT NULL,
    practice_area VARCHAR(100) NOT NULL,
    jurisdiction VARCHAR(100),
    authority_level VARCHAR(50),
    document_type VARCHAR(100),
    publication_date TIMESTAMP,
    author VARCHAR(255),
    citations TEXT[],
    keywords TEXT[],
    summary TEXT,
    authority_score DECIMAL(3,2),
    relevance_score DECIMAL(3,2),
    citation_count INTEGER DEFAULT 0,
    source_url TEXT,
    pdf_path TEXT,
    word_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_status VARCHAR(50) DEFAULT 'pending'
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_legal_documents_practice_area ON legal_documents(practice_area);
CREATE INDEX IF NOT EXISTS idx_legal_documents_jurisdiction ON legal_documents(jurisdiction);
CREATE INDEX IF NOT EXISTS idx_legal_documents_authority_level ON legal_documents(authority_level);
CREATE INDEX IF NOT EXISTS idx_legal_documents_document_type ON legal_documents(document_type);
CREATE INDEX IF NOT EXISTS idx_legal_documents_publication_date ON legal_documents(publication_date);
CREATE INDEX IF NOT EXISTS idx_legal_documents_authority_score ON legal_documents(authority_score);
CREATE INDEX IF NOT EXISTS idx_legal_documents_title_trgm ON legal_documents USING gin (title gin_trgm_ops);

-- Create personal injury cases table
CREATE TABLE IF NOT EXISTS personal_injury_cases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id VARCHAR(255) REFERENCES legal_documents(document_id),
    injury_type VARCHAR(100),
    injury_severity VARCHAR(50),
    body_parts_affected TEXT[],
    liability_theory VARCHAR(100),
    causation_complexity VARCHAR(50),
    comparative_fault VARCHAR(100),
    insurance_coverage TEXT[],
    policy_limits VARCHAR(50),
    medical_treatment VARCHAR(100),
    future_medical_needs VARCHAR(100),
    medical_records_complexity VARCHAR(50),
    lost_wages VARCHAR(50),
    earning_capacity VARCHAR(50),
    special_damages TEXT[],
    statute_of_limitations VARCHAR(100),
    expert_witnesses_needed TEXT[],
    trial_readiness VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create user interactions table for analytics
CREATE TABLE IF NOT EXISTS user_interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(255),
    session_id VARCHAR(255),
    user_role VARCHAR(100),
    query_text TEXT,
    query_type VARCHAR(100),
    resources_accessed TEXT[],
    time_spent INTEGER,
    rating DECIMAL(2,1),
    feedback_text TEXT,
    successful_outcome VARCHAR(10),
    practice_area_focus VARCHAR(100),
    jurisdiction_focus VARCHAR(100),
    interaction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create content generation metadata table
CREATE TABLE IF NOT EXISTS content_generation_metadata (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    resource_id VARCHAR(255),
    target_audience VARCHAR(100),
    content_intent VARCHAR(100),
    content_type VARCHAR(100),
    target_keywords TEXT[],
    competitor_coverage TEXT[],
    market_opportunity VARCHAR(50),
    content_gap_score DECIMAL(3,2),
    usage_frequency INTEGER DEFAULT 0,
    conversion_potential DECIMAL(3,2),
    engagement_score DECIMAL(3,2),
    expert_review_required VARCHAR(10),
    fact_check_status VARCHAR(50),
    legal_risk_level VARCHAR(50),
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP,
    success_rate DECIMAL(3,2)
);

-- Insert sample practice areas
INSERT INTO legal_documents (document_id, title, practice_area, jurisdiction, authority_level, document_type, summary, authority_score, relevance_score, word_count) VALUES
('sample_immigration_001', 'Sample K-1 Visa Guide', 'immigration_law', 'federal', 'secondary', 'guide', 'Sample immigration document for testing', 0.75, 0.80, 2500),
('sample_personal_injury_001', 'Sample Medical Malpractice Case', 'personal_injury', 'california', 'primary', 'case_law', 'Sample personal injury case for testing', 0.90, 0.85, 3200)
ON CONFLICT (document_id) DO NOTHING;

-- Insert sample personal injury case
INSERT INTO personal_injury_cases (document_id, injury_type, injury_severity, liability_theory, medical_treatment, trial_readiness) VALUES
('sample_personal_injury_001', 'medical_malpractice', 'severe', 'negligence', 'long_term', 'complex_litigation')
ON CONFLICT DO NOTHING;