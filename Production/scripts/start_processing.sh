#!/bin/bash
# Start the document processing pipeline

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}Legal Document Processing Pipeline${NC}"
echo "===================================="

# Check environment
if [ ! -f ".env.local" ]; then
    echo -e "${YELLOW}Warning: .env.local not found${NC}"
    echo "Creating from template..."
    cp .env.local.example .env.local
    echo -e "${RED}Please edit .env.local and add your ANTHROPIC_API_KEY${NC}"
    exit 1
fi

# Source environment
set -a
source .env.local
set +a

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${RED}Error: ANTHROPIC_API_KEY not set in .env.local${NC}"
    exit 1
fi

# Check for PDFs
PDF_COUNT=$(find raw_data -name "*.pdf" -type f 2>/dev/null | wc -l)
if [ $PDF_COUNT -eq 0 ]; then
    echo -e "${RED}Error: No PDFs found in raw_data/${NC}"
    echo "Please download PDFs first using:"
    echo "  python scripts/download_s3_pdfs.py"
    exit 1
fi

echo -e "${GREEN}Found $PDF_COUNT PDFs to process${NC}"

# Create output directories
mkdir -p output/{metadata,chunks,embeddings,logs}
mkdir -p exports

# Menu
echo -e "\n${YELLOW}Processing Options:${NC}"
echo "1. Quick scan - Inventory PDFs (1 min)"
echo "2. Basic processing - No AI (30-60 min)"
echo "3. Test Claude - Single document (2 min)"
echo "4. Full AI processing - All documents (2-4 hours)"
echo "5. Human review interface"
echo "6. Generate embeddings (1 hour)"
echo "7. Package for production"
echo "8. Run complete pipeline (4-6 hours)"

read -p "Select option (1-8): " choice

case $choice in
    1)
        echo -e "\n${BLUE}Creating PDF inventory...${NC}"
        python3 -c "
import json
from pathlib import Path

pdfs = []
for p in Path('raw_data').rglob('*.pdf'):
    pdfs.append({
        'name': p.name,
        'path': str(p),
        'size_mb': round(p.stat().st_size / 1024 / 1024, 2)
    })

print(f'Total PDFs: {len(pdfs)}')
print(f'Total size: {sum(p[\"size_mb\"] for p in pdfs):.1f} MB')
print('\nFirst 10 PDFs:')
for p in sorted(pdfs, key=lambda x: x['name'])[:10]:
    print(f'  {p[\"name\"]} ({p[\"size_mb\"]} MB)')

with open('output/inventory.json', 'w') as f:
    json.dump(pdfs, f, indent=2)
"
        ;;
        
    2)
        echo -e "\n${BLUE}Running basic processing (no AI)...${NC}"
        python3 scripts/quick_process.py raw_data output
        echo -e "${GREEN}Basic processing complete!${NC}"
        echo "Check output/metadata/ for results"
        ;;
        
    3)
        echo -e "\n${BLUE}Testing Claude integration...${NC}"
        python3 scripts/test_claude_extraction.py
        ;;
        
    4)
        echo -e "\n${BLUE}Starting full AI processing...${NC}"
        echo -e "${YELLOW}This will process all PDFs with Claude${NC}"
        echo -e "${YELLOW}Estimated cost: \$10-20${NC}"
        read -p "Continue? (y/n): " confirm
        
        if [ "$confirm" = "y" ]; then
            python3 scripts/process_documents_claude.py \
                --input-dir raw_data \
                --output-dir output \
                --batch-size 10
        fi
        ;;
        
    5)
        echo -e "\n${BLUE}Starting review interface...${NC}"
        python3 scripts/review_metadata.py --metadata-dir output/metadata
        ;;
        
    6)
        echo -e "\n${BLUE}Generating embeddings...${NC}"
        # First check if we have reviewed metadata
        REVIEWED_COUNT=$(find output/metadata/reviewed -name "*.json" 2>/dev/null | wc -l)
        if [ $REVIEWED_COUNT -gt 0 ]; then
            echo "Processing $REVIEWED_COUNT reviewed documents..."
            # TODO: Create generate_embeddings.py script
            echo -e "${YELLOW}Note: generate_embeddings.py needs to be implemented${NC}"
        else
            echo -e "${YELLOW}No reviewed metadata found. Process documents first.${NC}"
        fi
        ;;
        
    7)
        echo -e "\n${BLUE}Creating production package...${NC}"
        ./scripts/prepare_for_production.sh
        ;;
        
    8)
        echo -e "\n${BLUE}Running complete pipeline...${NC}"
        echo -e "${YELLOW}This will:${NC}"
        echo "  1. Process all PDFs without AI"
        echo "  2. Enhance with Claude AI"
        echo "  3. Generate embeddings"
        echo "  4. Create production package"
        echo -e "${YELLOW}Estimated time: 4-6 hours${NC}"
        echo -e "${YELLOW}Estimated cost: \$10-20${NC}"
        read -p "Continue? (y/n): " confirm
        
        if [ "$confirm" = "y" ]; then
            # Basic processing
            python3 scripts/quick_process.py raw_data output
            
            # AI enhancement
            python3 scripts/process_documents_claude.py \
                --input-dir raw_data \
                --output-dir output \
                --batch-size 10
            
            # Note about manual review
            echo -e "${YELLOW}Automated processing complete!${NC}"
            echo -e "${YELLOW}Please run option 5 for human review before final packaging${NC}"
        fi
        ;;
        
    *)
        echo -e "${RED}Invalid option${NC}"
        exit 1
        ;;
esac

echo -e "\n${GREEN}Done!${NC}"
