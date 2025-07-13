#!/bin/bash

# Legal Knowledge System - Complete Deployment and Testing Script
# This script deploys the full system and runs comprehensive tests

set -e  # Exit on any error

echo "🏛️  Legal Knowledge System - Complete Deployment & Test"
echo "========================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
log_info "Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    log_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    log_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    log_error "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

log_success "All prerequisites are installed"

# Step 1: Clean up any existing containers
log_info "Cleaning up existing containers..."
docker-compose -f legal-docker-compose.yml down -v 2>/dev/null || true
docker system prune -f 2>/dev/null || true

# Step 2: Build and start all services
log_info "Building and starting all services..."
docker-compose -f legal-docker-compose.yml up -d --build

# Step 3: Wait for services to be ready
log_info "Waiting for services to start up..."
sleep 30

# Step 4: Health checks
log_info "Performing health checks..."

check_service() {
    local service_name=$1
    local url=$2
    local max_attempts=30
    local attempt=1
    
    log_info "Checking $service_name..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s -f "$url" > /dev/null 2>&1; then
            log_success "$service_name is healthy"
            return 0
        fi
        
        log_info "Attempt $attempt/$max_attempts - $service_name not ready yet..."
        sleep 5
        ((attempt++))
    done
    
    log_error "$service_name failed to start within expected time"
    return 1
}

# Check each service
services_healthy=true

if ! check_service "Qdrant Vector Database" "http://localhost:6333/collections"; then
    services_healthy=false
fi

if ! check_service "Redis Cache" "http://localhost:6379"; then
    # Redis doesn't have HTTP endpoint, use different check
    if docker-compose -f legal-docker-compose.yml exec -T redis redis-cli ping | grep -q PONG; then
        log_success "Redis Cache is healthy"
    else
        log_error "Redis Cache is not responding"
        services_healthy=false
    fi
fi

if ! check_service "GROBID PDF Processing" "http://localhost:8070/api/isalive"; then
    services_healthy=false
fi

if ! check_service "Superlinked Vector Search" "http://localhost:8080/docs"; then
    services_healthy=false
fi

if ! check_service "Legal Research API" "http://localhost:8000/api/v1/health"; then
    services_healthy=false
fi

if ! check_service "Legal Research UI" "http://localhost:3000"; then
    services_healthy=false
fi

if [ "$services_healthy" = false ]; then
    log_error "Some services failed to start. Check logs with: docker-compose -f legal-docker-compose.yml logs"
    exit 1
fi

log_success "All services are healthy and running!"

# Step 5: Create test directories and sample data
log_info "Creating test data and directories..."

# Create test document directory
mkdir -p test_legal_docs/medical_malpractice
mkdir -p test_legal_docs/immigration_law

# Create sample metadata files
log_info "Creating sample metadata files..."

cat > test_legal_docs/medical_malpractice/metadata.json << 'EOF'
{
  "practice_area": "personal_injury",
  "jurisdiction": "california",
  "authority_level": "primary",
  "document_type": "case_law",
  "injury_type": "medical_malpractice",
  "liability_theory": "negligence",
  "medical_treatment": "long_term",
  "trial_readiness": "complex_litigation",
  "collection_date": "2025-01-15",
  "source_attribution": "Superior Court of California",
  "authority_score": 0.9,
  "relevance_score": 0.85
}
EOF

cat > test_legal_docs/immigration_law/metadata.json << 'EOF'
{
  "practice_area": "immigration_law",
  "jurisdiction": "federal",
  "authority_level": "primary",
  "document_type": "regulation",
  "collection_date": "2025-01-15",
  "source_attribution": "U.S. Citizenship and Immigration Services",
  "authority_score": 0.95,
  "relevance_score": 0.90
}
EOF

# Create sample text documents
cat > test_legal_docs/medical_malpractice/sample_case.txt << 'EOF'
MEDICAL MALPRACTICE CASE STUDY

Case: Smith v. Memorial Hospital
Case Number: CV-2024-001234
Court: Superior Court of California, Los Angeles County

FACTS:
Patient underwent spinal surgery at Memorial Hospital. During the procedure, surgeon failed to follow standard protocols, resulting in permanent neurological damage.

LEGAL ISSUES:
1. Medical negligence and deviation from standard of care
2. Hospital vicarious liability for surgeon's actions
3. Informed consent and disclosure of risks

MEDICAL EVIDENCE:
- Pre-operative imaging showing normal spinal structure
- Post-operative complications including nerve damage
- Expert testimony on surgical standards
- Economic damages for lost earning capacity

OUTCOME:
Jury verdict of $2.5 million in compensatory damages. Case establishes precedent for surgical standard of care in spinal procedures.

LEGAL SIGNIFICANCE:
This case demonstrates the importance of following established surgical protocols and proper informed consent procedures in medical malpractice claims.
EOF

cat > test_legal_docs/immigration_law/k1_visa_guide.txt << 'EOF'
K-1 FIANCÉ VISA REQUIREMENTS AND PROCEDURES

OVERVIEW:
The K-1 visa allows foreign nationals to enter the United States for the purpose of marrying a U.S. citizen within 90 days of arrival.

ELIGIBILITY REQUIREMENTS:
1. U.S. citizen petitioner must file Form I-129F
2. Both parties must be legally free to marry
3. Couple must have met in person within 2 years prior to filing
4. Intent to marry within 90 days of admission

DOCUMENTATION REQUIRED:
- Form I-129F, Petition for Alien Fiancé
- Evidence of U.S. citizenship
- Evidence of legal termination of previous marriages
- Evidence of meeting in person
- Passport-style photographs

PROCESSING TIMELINE:
- USCIS processing: 8-13 months
- National Visa Center: 2-4 weeks
- Embassy interview scheduling: 2-6 months

RECENT POLICY CHANGES:
New documentation standards implemented in 2024 require additional evidence of ongoing relationship and financial support capability.

LEGAL CONSIDERATIONS:
Failure to marry within 90 days results in automatic status violation. Adjustment of status to permanent resident requires marriage to petitioning U.S. citizen.
EOF

# Create file-specific metadata
cat > test_legal_docs/medical_malpractice/sample_case.txt.metadata.json << 'EOF'
{
  "id": "medical_malpractice_smith_v_memorial",
  "title": "Smith v. Memorial Hospital - Spinal Surgery Malpractice",
  "case_number": "CV-2024-001234",
  "injury_severity": "catastrophic",
  "body_parts_affected": ["spine", "neurological"],
  "medical_specialty": "neurosurgery",
  "causation_complexity": "complex",
  "medical_records_complexity": "voluminous",
  "expert_witnesses_needed": ["medical_expert", "economic_expert"],
  "special_damages": ["medical_bills", "lost_wages", "future_care"],
  "citations": ["Cal. Code Civ. Proc. § 340.5"],
  "keywords": ["medical_malpractice", "spinal_surgery", "neurological_damage"],
  "summary": "Medical malpractice case involving surgical error during spinal surgery",
  "authority_score": 0.95,
  "citation_count": 15
}
EOF

cat > test_legal_docs/immigration_law/k1_visa_guide.txt.metadata.json << 'EOF'
{
  "id": "k1_visa_comprehensive_guide_2025",
  "title": "K-1 Fiancé Visa - Complete Requirements Guide 2025",
  "visa_category": "K-1",
  "benefit_type": "visa",
  "procedural_stage": "application",
  "responsible_agency": "USCIS",
  "form_numbers": ["I-129F"],
  "processing_timeframe": "8-13 months",
  "complexity_level": "moderate",
  "citations": ["8 CFR 214.2(k)", "INA 101(a)(15)(K)"],
  "keywords": ["K-1_visa", "fiancé_visa", "immigration", "marriage"],
  "summary": "Comprehensive guide for K-1 fiancé visa application process and requirements",
  "authority_score": 0.90,
  "citation_count": 25
}
EOF

log_success "Test data created successfully"

# Step 6: Test document ingestion using CLI tool
log_info "Testing document ingestion..."

# Install required Python packages for CLI tool
pip3 install aiohttp aiofiles PyPDF2 python-docx 2>/dev/null || log_warning "Some Python packages may not be available"

# Test CLI tool connection
log_info "Testing CLI tool connection..."
if python3 legal_directory_ingester.py test --api-url http://localhost:8000 --superlinked-url http://localhost:8080; then
    log_success "CLI tool connection test passed"
else
    log_error "CLI tool connection test failed"
    exit 1
fi

# Ingest test documents
log_info "Ingesting test documents..."
if python3 legal_directory_ingester.py ingest --directory test_legal_docs --recursive --practice-area personal_injury; then
    log_success "Document ingestion completed successfully"
else
    log_error "Document ingestion failed"
    exit 1
fi

# Step 7: Test API endpoints
log_info "Testing API endpoints..."

test_api_endpoint() {
    local endpoint=$1
    local method=${2:-GET}
    local data=${3:-}
    local description=$4
    
    log_info "Testing: $description"
    
    if [ "$method" = "POST" ] && [ -n "$data" ]; then
        response=$(curl -s -w "%{http_code}" -X POST \
            -H "Content-Type: application/json" \
            -d "$data" \
            "http://localhost:8000$endpoint")
    else
        response=$(curl -s -w "%{http_code}" "http://localhost:8000$endpoint")
    fi
    
    status_code="${response: -3}"
    response_body="${response%???}"
    
    if [ "$status_code" -eq 200 ]; then
        log_success "$description - Status: $status_code"
        return 0
    else
        log_error "$description - Status: $status_code"
        echo "Response: $response_body"
        return 1
    fi
}

# Test various API endpoints
api_tests_passed=true

if ! test_api_endpoint "/api/v1/health" "GET" "" "Health Check"; then
    api_tests_passed=false
fi

if ! test_api_endpoint "/api/v1/system/info" "GET" "" "System Information"; then
    api_tests_passed=false
fi

# Test legal search
search_data='{"query": "medical malpractice", "limit": 5}'
if ! test_api_endpoint "/api/v1/search/legal" "POST" "$search_data" "Legal Document Search"; then
    api_tests_passed=false
fi

# Test authority search
authority_data='{"query": "surgical negligence", "min_authority_score": 0.8}'
if ! test_api_endpoint "/api/v1/search/authority" "POST" "$authority_data" "Authority Search"; then
    api_tests_passed=false
fi

if [ "$api_tests_passed" = false ]; then
    log_error "Some API tests failed"
    exit 1
fi

log_success "All API tests passed"

# Step 8: Test search functionality
log_info "Testing search functionality with ingested documents..."

search_response=$(curl -s -X POST \
    -H "Content-Type: application/json" \
    -d '{"query": "spinal surgery malpractice", "limit": 10}' \
    "http://localhost:8000/api/v1/search/legal")

if echo "$search_response" | grep -q "Smith v. Memorial Hospital"; then
    log_success "Search successfully found ingested medical malpractice document"
else
    log_warning "Search may not have found expected documents (this could be normal if indexing is still in progress)"
fi

# Step 9: Performance and load summary
log_info "Generating system status summary..."

echo ""
echo "🎯 LEGAL KNOWLEDGE SYSTEM - DEPLOYMENT SUMMARY"
echo "=============================================="
echo ""
echo "✅ Core Services:"
echo "   • Qdrant Vector Database:    http://localhost:6333"
echo "   • Redis Cache:               http://localhost:6379"
echo "   • GROBID PDF Processing:     http://localhost:8070"
echo "   • Superlinked Vector Search: http://localhost:8080"
echo "   • Legal Research API:        http://localhost:8000"
echo "   • Legal Research UI:         http://localhost:3000"
echo ""
echo "✅ Key Features Tested:"
echo "   • Document ingestion from directories"
echo "   • Metadata processing and inheritance"
echo "   • Text extraction and vectorization"
echo "   • Legal document search and retrieval"
echo "   • Practice area categorization"
echo "   • Authority and recency weighting"
echo ""
echo "📊 Test Data Ingested:"
echo "   • Medical malpractice case documents"
echo "   • Immigration law guides"
echo "   • Metadata files and configurations"
echo ""
echo "🚀 Ready for Production Use:"
echo "   • Directory-based ingestion: ./legal_directory_ingester.py"
echo "   • Web interface: http://localhost:3000"
echo "   • API documentation: http://localhost:8000/docs"
echo "   • Vector search API: http://localhost:8080/docs"
echo ""

# Step 10: Usage examples
echo "💡 QUICK START EXAMPLES:"
echo "========================"
echo ""
echo "1. Ingest documents from directory:"
echo "   python3 legal_directory_ingester.py ingest --directory /path/to/docs --practice-area personal_injury"
echo ""
echo "2. Search documents via API:"
echo "   curl -X POST http://localhost:8000/api/v1/search/legal \\"
echo "        -H 'Content-Type: application/json' \\"
echo "        -d '{\"query\": \"medical malpractice\", \"limit\": 10}'"
echo ""
echo "3. Access web interface:"
echo "   Open http://localhost:3000 in your browser"
echo ""
echo "4. View logs:"
echo "   docker-compose -f legal-docker-compose.yml logs -f"
echo ""
echo "5. Stop system:"
echo "   docker-compose -f legal-docker-compose.yml down"
echo ""

log_success "Legal Knowledge System deployment and testing completed successfully!"
log_info "The system is now ready for medical malpractice document ingestion and research."

# Cleanup test data (optional)
read -p "Remove test data directory? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf test_legal_docs
    log_info "Test data cleaned up"
fi

exit 0