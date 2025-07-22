#!/bin/bash
# Script to download PDFs from S3 bucket

set -e

# Configuration
BUCKET_NAME="medical-sexual-legal-pdfs"
LOCAL_DIR="./raw_data"
REGION="${AWS_REGION:-us-east-1}"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}S3 PDF Download Script${NC}"
echo "======================="

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}Error: AWS CLI is not installed${NC}"
    echo "Install with: brew install awscli (Mac) or apt-get install awscli (Linux)"
    exit 1
fi

# Create local directory
mkdir -p "$LOCAL_DIR"
echo -e "${GREEN}Created directory: $LOCAL_DIR${NC}"

# Check AWS credentials
echo -e "\n${YELLOW}Checking AWS credentials...${NC}"
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}AWS credentials not configured.${NC}"
    echo -e "\nPlease configure AWS credentials using one of these methods:"
    echo "1. Run: aws configure"
    echo "2. Set environment variables:"
    echo "   export AWS_ACCESS_KEY_ID=your_access_key"
    echo "   export AWS_SECRET_ACCESS_KEY=your_secret_key"
    echo "3. Use AWS SSO: aws sso login"
    exit 1
fi

# Get AWS identity
IDENTITY=$(aws sts get-caller-identity --query 'Arn' --output text)
echo -e "${GREEN}AWS Identity: $IDENTITY${NC}"

# Download PDFs
echo -e "\n${YELLOW}Downloading PDFs from s3://$BUCKET_NAME/...${NC}"

# Try to sync the bucket
if aws s3 sync "s3://$BUCKET_NAME/" "$LOCAL_DIR/" \
    --exclude "*" \
    --include "*.pdf" \
    --include "*.PDF" \
    --region "$REGION" \
    --no-progress; then
    
    echo -e "${GREEN}Download complete!${NC}"
    
    # Count downloaded files
    PDF_COUNT=$(find "$LOCAL_DIR" -name "*.pdf" -o -name "*.PDF" | wc -l)
    echo -e "${GREEN}Downloaded $PDF_COUNT PDF files${NC}"
    
    # Show file sizes
    echo -e "\n${YELLOW}File summary:${NC}"
    du -sh "$LOCAL_DIR"
    
    # List first 10 files
    echo -e "\n${YELLOW}First 10 PDFs:${NC}"
    find "$LOCAL_DIR" -name "*.pdf" -o -name "*.PDF" | head -10
    
else
    echo -e "${RED}Download failed!${NC}"
    echo -e "\nPossible issues:"
    echo "1. Bucket name might be incorrect"
    echo "2. You might not have access to this bucket"
    echo "3. The bucket might be in a different region"
    echo -e "\nTry listing bucket contents first:"
    echo "  aws s3 ls s3://$BUCKET_NAME/ --region $REGION"
fi