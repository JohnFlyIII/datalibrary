#!/usr/bin/env python3
"""
Download PDFs from S3 bucket with various authentication options
"""

import os
import sys
from pathlib import Path
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import click
from tqdm import tqdm

def create_s3_client(profile=None, access_key=None, secret_key=None, region='us-east-1'):
    """Create S3 client with various auth methods"""
    
    if access_key and secret_key:
        # Use provided credentials
        return boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
    elif profile:
        # Use AWS profile
        session = boto3.Session(profile_name=profile)
        return session.client('s3', region_name=region)
    else:
        # Use default credentials
        return boto3.client('s3', region_name=region)

def download_file(s3_client, bucket, key, local_path):
    """Download a single file from S3"""
    try:
        s3_client.download_file(bucket, key, str(local_path))
        return True
    except Exception as e:
        print(f"Error downloading {key}: {e}")
        return False

@click.command()
@click.option('--bucket', default='medical-sexual-legal-pdfs', help='S3 bucket name')
@click.option('--prefix', default='', help='S3 prefix to filter files')
@click.option('--local-dir', default='./raw_data', help='Local directory to save files')
@click.option('--profile', help='AWS profile to use')
@click.option('--access-key', envvar='AWS_ACCESS_KEY_ID', help='AWS access key')
@click.option('--secret-key', envvar='AWS_SECRET_ACCESS_KEY', help='AWS secret key')
@click.option('--region', default='us-east-1', help='AWS region')
@click.option('--dry-run', is_flag=True, help='List files without downloading')
def download_pdfs(bucket, prefix, local_dir, profile, access_key, secret_key, region, dry_run):
    """Download PDFs from S3 bucket"""
    
    print(f"S3 PDF Downloader")
    print("=" * 50)
    print(f"Bucket: s3://{bucket}/{prefix}")
    print(f"Local directory: {local_dir}")
    
    # Create S3 client
    try:
        s3 = create_s3_client(profile, access_key, secret_key, region)
        
        # Test access
        s3.head_bucket(Bucket=bucket)
        print("✓ Successfully connected to S3")
        
    except NoCredentialsError:
        print("❌ No AWS credentials found!")
        print("\nPlease provide credentials using one of these methods:")
        print("1. Set environment variables:")
        print("   export AWS_ACCESS_KEY_ID=your_key")
        print("   export AWS_SECRET_ACCESS_KEY=your_secret")
        print("2. Use --profile option with configured AWS profile")
        print("3. Use --access-key and --secret-key options")
        sys.exit(1)
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"❌ Bucket '{bucket}' not found!")
        elif error_code == '403':
            print(f"❌ Access denied to bucket '{bucket}'!")
            print("   Check your permissions and bucket policy.")
        else:
            print(f"❌ Error accessing bucket: {e}")
        sys.exit(1)
    
    # Create local directory
    local_path = Path(local_dir)
    local_path.mkdir(parents=True, exist_ok=True)
    
    # List and download PDFs
    try:
        paginator = s3.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(
            Bucket=bucket,
            Prefix=prefix
        )
        
        pdf_files = []
        
        # Collect all PDF files
        for page in page_iterator:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    if key.lower().endswith('.pdf'):
                        pdf_files.append({
                            'key': key,
                            'size': obj['Size'],
                            'modified': obj['LastModified']
                        })
        
        if not pdf_files:
            print(f"No PDF files found in s3://{bucket}/{prefix}")
            return
        
        print(f"\nFound {len(pdf_files)} PDF files")
        total_size = sum(f['size'] for f in pdf_files)
        print(f"Total size: {total_size / 1024 / 1024:.2f} MB")
        
        if dry_run:
            print("\nDry run - files that would be downloaded:")
            for f in pdf_files[:10]:
                print(f"  {f['key']} ({f['size'] / 1024:.1f} KB)")
            if len(pdf_files) > 10:
                print(f"  ... and {len(pdf_files) - 10} more files")
            return
        
        # Download files
        print(f"\nDownloading to {local_path}/")
        
        downloaded = 0
        failed = 0
        
        with tqdm(total=len(pdf_files), desc="Downloading") as pbar:
            for file_info in pdf_files:
                key = file_info['key']
                
                # Create local file path
                local_file = local_path / key
                local_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Skip if already exists and same size
                if local_file.exists() and local_file.stat().st_size == file_info['size']:
                    pbar.update(1)
                    continue
                
                # Download file
                if download_file(s3, bucket, key, local_file):
                    downloaded += 1
                else:
                    failed += 1
                
                pbar.update(1)
        
        # Summary
        print(f"\n✓ Download complete!")
        print(f"  Downloaded: {downloaded} files")
        print(f"  Skipped (already exist): {len(pdf_files) - downloaded - failed} files")
        if failed > 0:
            print(f"  Failed: {failed} files")
        
        # Show local directory info
        print(f"\nLocal directory contents:")
        local_pdfs = list(local_path.rglob("*.pdf"))
        print(f"  Total PDFs: {len(local_pdfs)}")
        
        if local_pdfs:
            total_local_size = sum(p.stat().st_size for p in local_pdfs)
            print(f"  Total size: {total_local_size / 1024 / 1024:.2f} MB")
        
    except Exception as e:
        print(f"❌ Error listing bucket contents: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download_pdfs()