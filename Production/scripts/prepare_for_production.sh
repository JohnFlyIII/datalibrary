#!/bin/bash
# prepare_for_production.sh - Prepare processed data for production deployment

set -e  # Exit on error

# Configuration
OUTPUT_DIR="${OUTPUT_DIR:-./output}"
EXPORT_DIR="${EXPORT_DIR:-./exports}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
EXPORT_NAME="legal_docs_export_${TIMESTAMP}"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Legal Document Export Preparation${NC}"
echo "=================================="

# Check if output directory exists
if [ ! -d "$OUTPUT_DIR" ]; then
    echo -e "${RED}Error: Output directory $OUTPUT_DIR does not exist${NC}"
    echo "Please run processing scripts first."
    exit 1
fi

# Create export directory
mkdir -p "$EXPORT_DIR"

# Count files
METADATA_COUNT=$(find "$OUTPUT_DIR/metadata" -name "*.json" 2>/dev/null | wc -l)
CHUNKS_COUNT=$(find "$OUTPUT_DIR/chunks" -name "*.json" 2>/dev/null | wc -l)

echo -e "Found ${GREEN}$METADATA_COUNT${NC} metadata files"
echo -e "Found ${GREEN}$CHUNKS_COUNT${NC} chunk files"

if [ $METADATA_COUNT -eq 0 ]; then
    echo -e "${RED}No metadata files found. Nothing to export.${NC}"
    exit 1
fi

# Create staging directory
STAGING_DIR="$EXPORT_DIR/${EXPORT_NAME}_staging"
mkdir -p "$STAGING_DIR"

# Copy files to staging
echo -e "\n${YELLOW}Preparing export package...${NC}"

# Copy metadata (prefer reviewed if available)
if [ -d "$OUTPUT_DIR/metadata/reviewed" ] && [ "$(ls -A $OUTPUT_DIR/metadata/reviewed)" ]; then
    echo "  - Copying reviewed metadata..."
    cp -r "$OUTPUT_DIR/metadata/reviewed" "$STAGING_DIR/metadata"
else
    echo "  - Copying unreviewed metadata..."
    mkdir -p "$STAGING_DIR/metadata"
    cp "$OUTPUT_DIR/metadata"/*.json "$STAGING_DIR/metadata/" 2>/dev/null || true
fi

# Copy chunks
if [ -d "$OUTPUT_DIR/chunks" ]; then
    echo "  - Copying chunks..."
    cp -r "$OUTPUT_DIR/chunks" "$STAGING_DIR/"
fi

# Copy embeddings if they exist
if [ -d "$OUTPUT_DIR/embeddings" ] && [ "$(ls -A $OUTPUT_DIR/embeddings)" ]; then
    echo "  - Copying embeddings..."
    cp -r "$OUTPUT_DIR/embeddings" "$STAGING_DIR/"
fi

# Create manifest
echo "  - Creating manifest..."
cat > "$STAGING_DIR/manifest.json" << EOF
{
  "export_timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "export_name": "$EXPORT_NAME",
  "version": "1.0",
  "contents": {
    "metadata_files": $METADATA_COUNT,
    "chunks_files": $CHUNKS_COUNT,
    "has_embeddings": $([ -d "$OUTPUT_DIR/embeddings" ] && echo "true" || echo "false"),
    "processing_complete": $([ -d "$OUTPUT_DIR/metadata/reviewed" ] && echo "true" || echo "false")
  },
  "system_info": {
    "platform": "$(uname -s)",
    "hostname": "$(hostname)",
    "user": "$USER"
  }
}
EOF

# Create import instructions
cat > "$STAGING_DIR/IMPORT_INSTRUCTIONS.md" << 'EOF'
# Import Instructions

## Quick Import

1. Transfer this archive to your production server
2. Extract the archive:
   ```bash
   tar -xzf legal_docs_export_*.tar.gz
   cd legal_docs_export_*
   ```

3. Run the import script:
   ```bash
   python /path/to/import_metadata.py --import-dir . --collection legal_knowledge
   ```

## Manual Import

If automated import fails, you can manually import:

1. Check Qdrant is running:
   ```bash
   curl http://localhost:6333/collections
   ```

2. Import metadata files one by one:
   ```bash
   for file in metadata/*.json; do
     python import_single.py "$file"
   done
   ```

## Verification

After import, verify with:
```bash
curl http://localhost:6333/collections/legal_knowledge
```

Expected response should show point_count > 0
EOF

# Create archive
echo -e "\n${YELLOW}Creating archive...${NC}"
cd "$EXPORT_DIR"
tar -czf "${EXPORT_NAME}.tar.gz" "${EXPORT_NAME}_staging"

# Cleanup staging
rm -rf "${EXPORT_NAME}_staging"

# Calculate size
SIZE=$(du -h "${EXPORT_NAME}.tar.gz" | cut -f1)

# Create transfer script
cat > "$EXPORT_DIR/transfer_${EXPORT_NAME}.sh" << EOF
#!/bin/bash
# Transfer script for ${EXPORT_NAME}

REMOTE_USER=\${1:-user}
REMOTE_HOST=\${2:-production-server}
REMOTE_PATH=\${3:-/home/\$REMOTE_USER/imports}

echo "Transferring ${EXPORT_NAME}.tar.gz to \$REMOTE_USER@\$REMOTE_HOST:\$REMOTE_PATH"
scp "${EXPORT_NAME}.tar.gz" "\$REMOTE_USER@\$REMOTE_HOST:\$REMOTE_PATH/"

echo "Transfer complete. To import on remote server:"
echo "ssh \$REMOTE_USER@\$REMOTE_HOST"
echo "cd \$REMOTE_PATH"
echo "tar -xzf ${EXPORT_NAME}.tar.gz"
echo "cd ${EXPORT_NAME}_staging"
echo "cat IMPORT_INSTRUCTIONS.md"
EOF

chmod +x "$EXPORT_DIR/transfer_${EXPORT_NAME}.sh"

# Summary
echo -e "\n${GREEN}Export preparation complete!${NC}"
echo "=================================="
echo -e "Export package: ${GREEN}$EXPORT_DIR/${EXPORT_NAME}.tar.gz${NC}"
echo -e "Package size: ${GREEN}$SIZE${NC}"
echo -e "\nTo transfer to production:"
echo -e "  ${YELLOW}$EXPORT_DIR/transfer_${EXPORT_NAME}.sh [user] [host] [path]${NC}"
echo -e "\nOr manually:"
echo -e "  ${YELLOW}scp $EXPORT_DIR/${EXPORT_NAME}.tar.gz user@server:/path/${NC}"