#!/bin/bash

# setup_dependencies.sh - Install all system and Python dependencies for legal document processing

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Legal Document Processing - Dependency Setup${NC}"
echo "=============================================="

# Check if running on Amazon Linux 2023
if grep -q "Amazon Linux" /etc/os-release 2>/dev/null; then
    echo -e "${GREEN}Detected Amazon Linux 2023${NC}"
    IS_AMAZON_LINUX=true
else
    echo -e "${YELLOW}Not running on Amazon Linux 2023${NC}"
    IS_AMAZON_LINUX=false
fi

# 1. Install System Dependencies
echo -e "\n${GREEN}1. Installing System Dependencies${NC}"

if [ "$IS_AMAZON_LINUX" = true ]; then
    # Amazon Linux 2023 packages
    sudo yum update -y
    sudo yum install -y \
        poppler-utils \
        ghostscript \
        ImageMagick \
        git \
        gcc \
        gcc-c++ \
        make \
        python3-devel \
        libffi-devel \
        openssl-devel
    
    # Try to install OCR tools
    sudo yum search tesseract 2>/dev/null | grep -i tesseract | head -5
    echo -e "${YELLOW}Note: Tesseract OCR may need manual installation${NC}"
else
    # Ubuntu/Debian
    sudo apt-get update
    sudo apt-get install -y \
        poppler-utils \
        ghostscript \
        imagemagick \
        tesseract-ocr \
        python3-dev \
        python3-pip \
        python3-venv \
        build-essential \
        libffi-dev \
        libssl-dev
fi

# 2. Setup Python Environment
echo -e "\n${GREEN}2. Setting up Python Environment${NC}"

# Check if we should use /projects directory
if [ -d "/projects" ] && [ -w "/projects" ]; then
    VENV_BASE="/projects/legal-platform/datalibrary/Production"
    echo -e "Using /projects directory for virtual environment"
else
    VENV_BASE="$(pwd)"
    echo -e "Using current directory for virtual environment"
fi

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv "$VENV_BASE/venv"

# Activate virtual environment
source "$VENV_BASE/venv/bin/activate"

# 3. Upgrade pip and install wheel
echo -e "\n${GREEN}3. Upgrading pip and installing build tools${NC}"
pip install --upgrade pip wheel setuptools

# 4. Clean install of dependencies with proper versions
echo -e "\n${GREEN}4. Installing Python dependencies${NC}"

# First, uninstall problematic packages if they exist
pip uninstall -y numpy pandas scikit-learn sentence-transformers huggingface-hub nltk 2>/dev/null || true

# Install numpy first (specific version to avoid compatibility issues)
pip install numpy==1.24.3

# Install other core dependencies
pip install \
    pandas==2.0.3 \
    scikit-learn==1.3.0 \
    nltk==3.8.1

# Install huggingface-hub and sentence-transformers with compatible versions
pip install \
    huggingface-hub==0.19.4 \
    transformers==4.36.0 \
    sentence-transformers==2.2.2

# Install remaining dependencies from requirements file
pip install \
    anthropic==0.18.1 \
    pdfplumber==0.9.0 \
    pypdf2==3.0.1 \
    python-dotenv==1.0.0 \
    jsonlines==4.0.0 \
    tqdm==4.66.1 \
    click==8.1.7 \
    requests==2.31.0 \
    tenacity==8.2.3 \
    pytesseract==0.3.10 \
    tiktoken==0.5.1 \
    rich==13.5.2 \
    pytest==7.4.0 \
    black==23.7.0 \
    flake8==6.1.0

# 5. Download NLTK data
echo -e "\n${GREEN}5. Downloading NLTK data${NC}"
python3 -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet')"

# 6. Verify installations
echo -e "\n${GREEN}6. Verifying installations${NC}"

# Check system tools
echo -e "${YELLOW}System tools:${NC}"
command -v pdftotext >/dev/null 2>&1 && echo "✓ pdftotext installed" || echo "✗ pdftotext NOT installed"
command -v gs >/dev/null 2>&1 && echo "✓ ghostscript installed" || echo "✗ ghostscript NOT installed"
command -v convert >/dev/null 2>&1 && echo "✓ ImageMagick installed" || echo "✗ ImageMagick NOT installed"
command -v tesseract >/dev/null 2>&1 && echo "✓ tesseract installed" || echo "✗ tesseract NOT installed"

# Check Python packages
echo -e "\n${YELLOW}Python packages:${NC}"
python3 -c "import anthropic; print('✓ anthropic installed')" 2>/dev/null || echo "✗ anthropic NOT installed"
python3 -c "import sentence_transformers; print('✓ sentence-transformers installed')" 2>/dev/null || echo "✗ sentence-transformers NOT installed"
python3 -c "import pdfplumber; print('✓ pdfplumber installed')" 2>/dev/null || echo "✗ pdfplumber NOT installed"
python3 -c "import click; print('✓ click installed')" 2>/dev/null || echo "✗ click NOT installed"
python3 -c "import pandas; print('✓ pandas installed')" 2>/dev/null || echo "✗ pandas NOT installed"
python3 -c "import numpy; print('✓ numpy installed')" 2>/dev/null || echo "✗ numpy NOT installed"

# 7. Create activation script
echo -e "\n${GREEN}7. Creating activation script${NC}"
cat > "$VENV_BASE/activate_env.sh" << 'EOF'
#!/bin/bash
# Activate the virtual environment for legal document processing

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/venv/bin/activate"
echo "Virtual environment activated. Python: $(which python3)"
EOF
chmod +x "$VENV_BASE/activate_env.sh"

echo -e "\n${GREEN}Setup complete!${NC}"
echo -e "${YELLOW}To activate the environment, run:${NC}"
echo -e "  source $VENV_BASE/activate_env.sh"
echo -e "\n${YELLOW}Then run the processing script:${NC}"
echo -e "  ./scripts/start_processing.sh"