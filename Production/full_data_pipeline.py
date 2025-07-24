#!/usr/bin/env python3
"""
Complete Data Pipeline: Raw PDFs → AI Processing → Superlinked Loading
====================================================================

Runs the full pipeline from raw PDF files to loaded vector database:
1. Process PDFs with Claude AI (facts, summaries, metadata)
2. Generate document chunks with precise positioning
3. Load both documents and chunks into Superlinked
4. Verify search functionality

Usage:
    python3 full_data_pipeline.py --all                    # Process all PDFs
    python3 full_data_pipeline.py --limit 5                # Process 5 PDFs
    python3 full_data_pipeline.py --process-only           # Only AI processing
    python3 full_data_pipeline.py --load-only              # Only load existing data
"""

import os
import sys
import json
import time
import subprocess
import requests
from pathlib import Path
from typing import Dict, List, Optional
import click
from tqdm import tqdm
from dotenv import load_dotenv

class FullDataPipeline:
    """Complete pipeline from raw PDFs to searchable vector database"""
    
    def __init__(self, superlinked_url: str = "http://localhost:8080"):
        # Load environment variables from .env.local if it exists
        if Path(".env.local").exists():
            load_dotenv(".env.local")
            print("✅ Loaded .env.local file")
        
        self.base_url = superlinked_url
        self.raw_data_dir = Path("raw_data")
        self.output_dir = Path("output")
        self.scripts_dir = Path("scripts")
        
        # Ensure directories exist
        self.output_dir.mkdir(exist_ok=True)
        for subdir in ["metadata", "chunks", "embeddings", "logs"]:
            (self.output_dir / subdir).mkdir(exist_ok=True)
    
    def check_environment(self) -> bool:
        """Check that all required components are available"""
        print("🔧 Checking environment...")
        
        # Check for Anthropic API key
        if not os.getenv("ANTHROPIC_API_KEY"):
            print("❌ ANTHROPIC_API_KEY not found in environment")
            print("   Set it in .env.local or environment variables")
            return False
        
        # Check for PDFs
        pdf_files = list(self.raw_data_dir.rglob("*.pdf"))
        if not pdf_files:
            print(f"❌ No PDF files found in {self.raw_data_dir}")
            return False
        
        print(f"✅ Found {len(pdf_files)} PDF files")
        
        # Check Superlinked server
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Superlinked server is running")
            else:
                print("❌ Superlinked server not healthy")
                return False
        except:
            print("❌ Cannot connect to Superlinked server")
            print("   Run: docker compose up -d")
            return False
        
        # Check required scripts
        required_scripts = ["process_documents_claude.py"]
        for script in required_scripts:
            if not (self.scripts_dir / script).exists():
                print(f"❌ Required script not found: {script}")
                return False
        
        print("✅ Environment check passed")
        return True
    
    def run_ai_processing(self, limit: Optional[int] = None) -> bool:
        """Run AI processing with Claude"""
        print("\n🤖 Starting AI processing with Claude...")
        
        cmd = [
            "python3", str(self.scripts_dir / "process_documents_claude.py"),
            "--input-dir", str(self.raw_data_dir),
            "--output-dir", str(self.output_dir),
            "--batch-size", "5"  # Conservative batch size
        ]
        
        if limit:
            cmd.extend(["--limit", str(limit)])
        
        print(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("✅ AI processing completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ AI processing failed: {e}")
            if e.stdout:
                print("STDOUT:", e.stdout)
            if e.stderr:
                print("STDERR:", e.stderr)
            return False
    
    def load_documents(self) -> Dict:
        """Load processed documents into Superlinked"""
        print("\n📄 Loading documents into Superlinked...")
        
        try:
            # Use existing load_real_data.py script
            result = subprocess.run([
                "python3", "load_real_data.py", "--all"
            ], check=True, capture_output=True, text=True)
            
            print("✅ Documents loaded successfully")
            
            # Parse output for statistics
            output_lines = result.stdout.split('\n')
            stats = {}
            for line in output_lines:
                if "Successfully loaded:" in line:
                    stats['documents'] = line.split(":")[1].strip()
                elif "By Document Type:" in line:
                    stats['by_type'] = True
            
            return {'success': True, 'stats': stats}
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Document loading failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def load_chunks(self) -> Dict:
        """Load document chunks into Superlinked"""
        print("\n🧩 Loading document chunks into Superlinked...")
        
        try:
            # Use existing load_chunks.py script
            result = subprocess.run([
                "python3", "load_chunks.py", "--all"
            ], check=True, capture_output=True, text=True)
            
            print("✅ Chunks loaded successfully")
            
            # Parse output for statistics
            output_lines = result.stdout.split('\n')
            stats = {}
            for line in output_lines:
                if "Total chunks loaded:" in line:
                    stats['chunks'] = line.split(":")[1].strip()
                elif "Successfully loaded:" in line and "files" in line:
                    stats['files'] = line.split(":")[1].split("files")[0].strip()
            
            return {'success': True, 'stats': stats}
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Chunk loading failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def verify_search(self) -> bool:
        """Test search functionality across all layers"""
        print("\n🔍 Verifying search functionality...")
        
        test_queries = [
            ("medical malpractice", "discovery_search"),
            ("healthcare provider", "exploration_search"),
            ("informed consent", "deep_dive_precise")
        ]
        
        for query, endpoint in test_queries:
            try:
                response = requests.post(
                    f"{self.base_url}/api/v1/search/{endpoint}",
                    json={"search_query": query, "limit": 3},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    entries = data.get('entries', [])
                    if entries:
                        best_score = entries[0].get('metadata', {}).get('score', 0)
                        print(f"✅ {endpoint}: {len(entries)} results (best score: {best_score:.3f})")
                    else:
                        print(f"⚠️  {endpoint}: No results found")
                else:
                    print(f"❌ {endpoint}: HTTP {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"❌ {endpoint} test failed: {e}")
                return False
        
        print("✅ Search verification completed")
        return True
    
    def run_full_pipeline(self, limit: Optional[int] = None, process_only: bool = False, load_only: bool = False):
        """Run the complete pipeline"""
        start_time = time.time()
        
        print("🚀 Starting Full Data Pipeline")
        print("=" * 50)
        
        if not self.check_environment():
            print("❌ Environment check failed. Exiting.")
            return False
        
        results = {}
        
        # Step 1: AI Processing (if not load-only)
        if not load_only:
            if not self.run_ai_processing(limit):
                print("❌ Pipeline failed at AI processing step")
                return False
            results['ai_processing'] = True
        
        if process_only:
            print("✅ Processing complete (process-only mode)")
            return True
        
        # Step 2: Load Documents
        doc_results = self.load_documents()
        if not doc_results['success']:
            print("❌ Pipeline failed at document loading step")
            return False
        results['documents'] = doc_results
        
        # Step 3: Load Chunks
        chunk_results = self.load_chunks()
        if not chunk_results['success']:
            print("❌ Pipeline failed at chunk loading step")
            return False
        results['chunks'] = chunk_results
        
        # Step 4: Verify Search
        if not self.verify_search():
            print("⚠️  Search verification had issues, but pipeline completed")
        
        # Summary
        elapsed = time.time() - start_time
        print(f"\n🎉 Pipeline Complete! ({elapsed/60:.1f} minutes)")
        print("=" * 50)
        
        if 'documents' in results:
            print(f"📄 Documents: {results['documents']['stats'].get('documents', 'loaded')}")
        if 'chunks' in results:
            print(f"🧩 Chunks: {results['chunks']['stats'].get('chunks', 'loaded')}")
        
        print("\n🔍 Ready for search:")
        print("  Discovery: /api/v1/search/discovery_search")
        print("  Exploration: /api/v1/search/exploration_search") 
        print("  Deep Dive: /api/v1/search/deep_dive_precise")
        
        return True

@click.command()
@click.option('--all', 'process_all', is_flag=True, help='Process all PDF files')
@click.option('--limit', '-l', type=int, help='Limit number of PDFs to process')
@click.option('--process-only', is_flag=True, help='Only run AI processing, skip loading')
@click.option('--load-only', is_flag=True, help='Only load existing data, skip AI processing')
@click.option('--url', '-u', default='http://localhost:8080', help='Superlinked server URL')
def main(process_all, limit, process_only, load_only, url):
    """Run the complete data pipeline from raw PDFs to searchable vector database"""
    
    if not process_all and not limit and not load_only:
        print("❌ Please specify --all, --limit N, or --load-only")
        print("   Use --help for more options")
        return
    
    if process_all and limit:
        print("❌ Cannot use both --all and --limit")
        return
    
    if process_only and load_only:
        print("❌ Cannot use both --process-only and --load-only")
        return
    
    pipeline = FullDataPipeline(url)
    
    # Determine limit
    actual_limit = None if process_all else limit
    
    success = pipeline.run_full_pipeline(
        limit=actual_limit,
        process_only=process_only,
        load_only=load_only
    )
    
    if success:
        print("\n✅ Pipeline completed successfully!")
        print("Your legal search system is ready to use.")
    else:
        print("\n❌ Pipeline failed. Check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()