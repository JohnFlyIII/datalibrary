#!/usr/bin/env python3
"""
Complete Data Pipeline v2: Enhanced Logging & Timeout Handling
============================================================

Improved version with:
- Real-time progress logging
- Configurable timeouts
- Better error handling
- Live output streaming
"""

import os
import sys
import json
import time
import subprocess
import requests
import threading
import signal
from pathlib import Path
from typing import Dict, List, Optional
import click
from dotenv import load_dotenv

class FullDataPipelineV2:
    """Enhanced pipeline with better logging and timeout handling"""
    
    def __init__(self, superlinked_url: str = "http://localhost:8080"):
        # Load environment variables
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
    
    def stream_subprocess_output(self, process, timeout_hours=4):
        """Stream subprocess output in real-time with timeout"""
        timeout_seconds = timeout_hours * 3600
        start_time = time.time()
        
        print(f"⏱️  Timeout set to {timeout_hours} hours")
        print("📊 Streaming live output (Ctrl+C to cancel):")
        print("-" * 60)
        
        try:
            while True:
                # Check timeout
                if time.time() - start_time > timeout_seconds:
                    print(f"\n⏰ Timeout reached ({timeout_hours} hours). Terminating process...")
                    process.terminate()
                    time.sleep(5)
                    if process.poll() is None:
                        print("🔪 Force killing process...")
                        process.kill()
                    return False, "Timeout"
                
                # Read output
                output = process.stdout.readline()
                if output:
                    print(output.rstrip())
                elif process.poll() is not None:
                    # Process finished
                    break
                
                time.sleep(0.1)
            
            # Get final return code
            return_code = process.poll()
            if return_code == 0:
                print("-" * 60)
                print("✅ Process completed successfully")
                return True, "Success"
            else:
                print("-" * 60)
                print(f"❌ Process failed with return code {return_code}")
                return False, f"Exit code {return_code}"
                
        except KeyboardInterrupt:
            print("\n🛑 User cancelled. Terminating process...")
            process.terminate()
            time.sleep(5)
            if process.poll() is None:
                print("🔪 Force killing process...")
                process.kill()
            return False, "User cancelled"
    
    def monitor_progress(self):
        """Monitor processing progress by counting output files"""
        def progress_thread():
            last_metadata_count = 0
            last_chunk_count = 0
            
            while True:
                try:
                    metadata_count = len(list(self.output_dir.glob("metadata/*.json")))
                    chunk_count = len(list(self.output_dir.glob("chunks/*.json")))
                    
                    if metadata_count > last_metadata_count:
                        print(f"📄 Documents processed: {metadata_count}")
                        last_metadata_count = metadata_count
                    
                    if chunk_count > last_chunk_count:
                        print(f"🧩 Chunk files created: {chunk_count}")
                        last_chunk_count = chunk_count
                    
                    time.sleep(10)  # Check every 10 seconds
                except:
                    break
        
        thread = threading.Thread(target=progress_thread, daemon=True)
        thread.start()
        return thread
    
    def run_ai_processing(self, limit: Optional[int] = None, timeout_hours: float = 4) -> bool:
        """Run AI processing with real-time logging and timeout"""
        print(f"\n🤖 Starting AI processing with Claude...")
        estimated_hours = "1-2" if limit and limit <= 5 else "2-4"
        print(f"⏱️  Estimated time: {estimated_hours} hours")
        print(f"💰 Estimated cost: ${(limit or 20) * 1:.0f}-{(limit or 20) * 3:.0f}")
        
        cmd = [
            "python3", str(self.scripts_dir / "process_documents_claude.py"),
            "--input-dir", str(self.raw_data_dir),
            "--output-dir", str(self.output_dir),
            "--batch-size", "3"  # Smaller batches for better progress visibility
        ]
        
        if limit:
            cmd.extend(["--limit", str(limit)])
        
        print(f"🔧 Running: {' '.join(cmd)}")
        
        # Start progress monitoring
        progress_monitor = self.monitor_progress()
        
        try:
            # Start subprocess with real-time output
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Stream output with timeout
            success, message = self.stream_subprocess_output(process, timeout_hours)
            
            if success:
                print("✅ AI processing completed successfully")
                return True
            else:
                print(f"❌ AI processing failed: {message}")
                return False
                
        except Exception as e:
            print(f"❌ AI processing failed with exception: {e}")
            return False
    
    def load_documents(self, timeout_minutes: int = 30) -> Dict:
        """Load processed documents into Superlinked with timeout"""
        print(f"\n📄 Loading documents into Superlinked (timeout: {timeout_minutes}min)...")
        
        try:
            # Check what we have to load
            metadata_files = list(self.output_dir.glob("metadata/*.json"))
            if not metadata_files:
                print("⚠️  No metadata files found. Skipping document loading.")
                return {'success': True, 'stats': {'documents': '0 (none to load)'}}
            
            print(f"📊 Found {len(metadata_files)} metadata files to load")
            
            # Use existing load_real_data.py script with timeout
            process = subprocess.Popen([
                "python3", "load_real_data.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            
            print("📊 Document loading progress:")
            start_time = time.time()
            timeout_seconds = timeout_minutes * 60
            
            while True:
                # Check timeout
                if time.time() - start_time > timeout_seconds:
                    print(f"\n⏰ Document loading timeout ({timeout_minutes}min). Terminating...")
                    process.terminate()
                    time.sleep(5)
                    if process.poll() is None:
                        process.kill()
                    return {'success': False, 'error': 'Timeout'}
                
                # Read output
                output = process.stdout.readline()
                if output:
                    print(f"  {output.rstrip()}")
                elif process.poll() is not None:
                    break
                
                time.sleep(0.1)
            
            if process.returncode == 0:
                print("✅ Documents loaded successfully")
                return {'success': True, 'stats': {'documents': f'{len(metadata_files)} processed'}}
            else:
                print("❌ Document loading failed")
                return {'success': False, 'error': f'Exit code {process.returncode}'}
            
        except Exception as e:
            print(f"❌ Document loading failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def load_chunks(self, timeout_minutes: int = 45) -> Dict:
        """Load document chunks into Superlinked with timeout"""
        print(f"\n🧩 Loading document chunks into Superlinked (timeout: {timeout_minutes}min)...")
        
        try:
            # Check what we have to load
            chunk_files = list(self.output_dir.glob("chunks/*.json"))
            if not chunk_files:
                print("⚠️  No chunk files found. Skipping chunk loading.")
                return {'success': True, 'stats': {'chunks': '0 (none to load)'}}
            
            print(f"📊 Found {len(chunk_files)} chunk files to load")
            
            # Use existing load_chunks.py script with timeout
            process = subprocess.Popen([
                "python3", "load_chunks.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            
            print("📊 Chunk loading progress:")
            start_time = time.time()
            timeout_seconds = timeout_minutes * 60
            
            while True:
                # Check timeout
                if time.time() - start_time > timeout_seconds:
                    print(f"\n⏰ Chunk loading timeout ({timeout_minutes}min). Terminating...")
                    process.terminate()
                    time.sleep(5)
                    if process.poll() is None:
                        process.kill()
                    return {'success': False, 'error': 'Timeout'}
                
                # Read output
                output = process.stdout.readline()
                if output:
                    print(f"  {output.rstrip()}")
                elif process.poll() is not None:
                    break
                
                time.sleep(0.1)
            
            if process.returncode == 0:
                print("✅ Chunks loaded successfully")
                return {'success': True, 'stats': {'chunks': f'from {len(chunk_files)} files'}}
            else:
                print("❌ Chunk loading failed")
                return {'success': False, 'error': f'Exit code {process.returncode}'}
            
        except Exception as e:
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
        
        for i, (query, endpoint) in enumerate(test_queries, 1):
            print(f"  {i}/3 Testing {endpoint}...")
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
                        print(f"      ✅ {len(entries)} results (best score: {best_score:.3f})")
                    else:
                        print(f"      ⚠️  No results found")
                else:
                    print(f"      ❌ HTTP {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"      ❌ Test failed: {e}")
                return False
        
        print("✅ Search verification completed")
        return True
    
    def run_full_pipeline(self, limit: Optional[int] = None, process_only: bool = False, 
                         load_only: bool = False, timeout_hours: float = 4):
        """Run the complete pipeline with enhanced logging"""
        start_time = time.time()
        
        print("🚀 Enhanced Full Data Pipeline v2")
        print("=" * 60)
        
        if not self.check_environment():
            print("❌ Environment check failed. Exiting.")
            return False
        
        results = {}
        
        # Step 1: AI Processing (if not load-only)
        if not load_only:
            if not self.run_ai_processing(limit, timeout_hours):
                print("❌ Pipeline failed at AI processing step")
                return False
            results['ai_processing'] = True
        
        if process_only:
            elapsed = time.time() - start_time
            print(f"\n✅ Processing complete ({elapsed/60:.1f} minutes)")
            return True
        
        # Step 2: Load Documents (30min timeout)
        doc_results = self.load_documents(timeout_minutes=30)
        if not doc_results['success']:
            print("❌ Pipeline failed at document loading step")
            return False
        results['documents'] = doc_results
        
        # Step 3: Load Chunks (45min timeout - chunks take longer)
        chunk_results = self.load_chunks(timeout_minutes=45)
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
        print("=" * 60)
        
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
@click.option('--timeout', '-t', type=float, default=4.0, help='Timeout in hours (default: 4)')
@click.option('--url', '-u', default='http://localhost:8080', help='Superlinked server URL')
def main(process_all, limit, process_only, load_only, timeout, url):
    """Enhanced pipeline with real-time logging and timeout handling"""
    
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
    
    pipeline = FullDataPipelineV2(url)
    
    # Determine limit
    actual_limit = None if process_all else limit
    
    success = pipeline.run_full_pipeline(
        limit=actual_limit,
        process_only=process_only,
        load_only=load_only,
        timeout_hours=timeout
    )
    
    if success:
        print("\n✅ Enhanced pipeline completed successfully!")
        print("Your legal search system is ready to use.")
    else:
        print("\n❌ Pipeline failed. Check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()