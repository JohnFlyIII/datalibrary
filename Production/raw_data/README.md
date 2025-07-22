# Raw Data Directory

This directory contains raw PDF files downloaded from S3 for processing.

## Download Instructions

### Method 1: Using Shell Script

```bash
# Make sure you have AWS credentials configured
aws configure

# Run the download script
../scripts/download_s3_pdfs.sh
```

### Method 2: Using Python Script

```bash
# Install boto3 if not already installed
pip install boto3 tqdm click

# Download with default settings
python ../scripts/download_s3_pdfs.py

# Download with specific AWS profile
python ../scripts/download_s3_pdfs.py --profile your-profile

# Dry run to see what would be downloaded
python ../scripts/download_s3_pdfs.py --dry-run

# Download from specific prefix/folder
python ../scripts/download_s3_pdfs.py --prefix "texas/"
```

### Method 3: Direct AWS CLI

```bash
# Sync all PDFs
aws s3 sync s3://medical-sexual-legal-pdfs/ . --exclude "*" --include "*.pdf"

# Copy specific files
aws s3 cp s3://medical-sexual-legal-pdfs/document.pdf .

# List contents first
aws s3 ls s3://medical-sexual-legal-pdfs/
```

## AWS Authentication

You need AWS credentials with read access to the bucket. Options:

1. **AWS CLI Configuration**
   ```bash
   aws configure
   # Enter your Access Key ID
   # Enter your Secret Access Key
   # Enter default region (e.g., us-east-1)
   ```

2. **Environment Variables**
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_DEFAULT_REGION=us-east-1
   ```

3. **AWS Profile**
   ```bash
   # In ~/.aws/credentials
   [medical-legal]
   aws_access_key_id = your_access_key
   aws_secret_access_key = your_secret_key
   ```

## Expected Content

The S3 bucket should contain legal PDFs related to:
- Medical malpractice cases and statutes
- Sexual abuse litigation documents
- Texas state legal codes
- Federal regulations
- Practice guides and forms

## Processing Pipeline

After downloading:

1. **Quick Processing (No AI)**
   ```bash
   python ../scripts/quick_process.py . ../output
   ```

2. **Full Processing (With Claude)**
   ```bash
   python ../scripts/process_documents_claude.py --input-dir . --output-dir ../output
   ```

3. **Review Metadata**
   ```bash
   python ../scripts/review_metadata.py --metadata-dir ../output/metadata
   ```

## Directory Structure

```
raw_data/
├── README.md (this file)
├── texas/
│   ├── statutes/
│   ├── cases/
│   └── regulations/
├── federal/
│   ├── cfr/
│   └── cases/
└── practice_guides/
    ├── medical_malpractice/
    └── sexual_abuse/
```

## Important Notes

- **Do not commit** PDF files to git (they're in .gitignore)
- **Keep originals** - These are source documents
- **Check file integrity** after download
- **Respect licensing** - Ensure you have rights to use these documents

## Troubleshooting

### "Access Denied" Error
- Check your AWS credentials
- Verify bucket name is correct
- Ensure your IAM user/role has s3:GetObject permission

### "No such bucket" Error
- Verify bucket name: `medical-sexual-legal-pdfs`
- Check region settings
- Try: `aws s3 ls --region us-east-1`

### Slow Downloads
- Use parallel downloads: `aws s3 sync --cli-write-timeout 0`
- Check your internet connection
- Consider downloading in batches