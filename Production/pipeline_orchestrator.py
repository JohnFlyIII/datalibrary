#!/usr/bin/env python3
"""
Complete Data Ingestion Pipeline Orchestrator
============================================

Comprehensive testing and execution system for the entire legal document 
processing pipeline from raw PDFs to searchable vector database.

Pipeline Architecture:
1. Document Preprocessing (PDFs → Basic Metadata + Chunks)
2. AI Enhancement (Claude Processing → Rich Content)  
3. Field Enhancement (Legal Field Extraction → 82+ Fields)
4. Vector Loading (Metadata → Superlinked Database)
5. Validation & Testing (Search Quality → Performance Metrics)
"""

import json
import time
import subprocess
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PipelineOrchestrator:
    """Complete data ingestion pipeline orchestrator and tester"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.raw_data_dir = Path("raw_data")
        self.output_dir = Path("output")
        self.metadata_dir = self.output_dir / "metadata"
        self.chunks_dir = self.output_dir / "chunks"
        
        # Pipeline state tracking
        self.pipeline_state = {
            "step_1_preprocessing": {"status": "pending", "files_processed": 0, "duration": 0},
            "step_2_ai_enhancement": {"status": "pending", "files_processed": 0, "duration": 0},
            "step_3_field_enhancement": {"status": "pending", "files_processed": 0, "duration": 0},
            "step_4_vector_loading": {"status": "pending", "files_loaded": 0, "duration": 0},
            "step_5_validation": {"status": "pending", "tests_passed": 0, "duration": 0}
        }
        
    def analyze_current_state(self) -> Dict:
        """Analyze current state of data processing pipeline"""
        
        print("🔍 **PIPELINE STATE ANALYSIS**")
        print("=" * 60)
        
        analysis = {
            "raw_documents": self._count_raw_documents(),
            "basic_metadata": self._count_basic_metadata(),
            "ai_processed": self._count_ai_processed(),
            "enhanced_metadata": self._count_enhanced_metadata(),
            "vector_loaded": self._check_vector_database(),
            "recommendations": []
        }
        
        # Display current state
        print(f"\n📊 **Current Pipeline State:**")
        print(f"  Raw Documents: {analysis['raw_documents']} PDFs")
        print(f"  Basic Metadata: {analysis['basic_metadata']} files")
        print(f"  AI Processed: {analysis['ai_processed']} files")
        print(f"  Enhanced Fields: {analysis['enhanced_metadata']} files")
        print(f"  Vector Database: {analysis['vector_loaded']} entries")
        
        # Generate recommendations
        if analysis['raw_documents'] > analysis['basic_metadata']:
            analysis['recommendations'].append("Run document preprocessing on remaining PDFs")
        
        if analysis['basic_metadata'] > analysis['ai_processed']:
            analysis['recommendations'].append("Complete AI processing for basic metadata files")
            
        if analysis['ai_processed'] > analysis['enhanced_metadata']:
            analysis['recommendations'].append("Run field enhancement on AI-processed files")
            
        if analysis['enhanced_metadata'] > analysis['vector_loaded']:
            analysis['recommendations'].append("Load enhanced metadata into vector database")
        
        if analysis['recommendations']:
            print(f"\n💡 **Recommendations:**")
            for i, rec in enumerate(analysis['recommendations'], 1):
                print(f"  {i}. {rec}")
        else:
            print(f"\n✅ **Pipeline is complete and up-to-date**")
            
        return analysis
    
    def _count_raw_documents(self) -> int:
        """Count raw PDF documents"""
        if not self.raw_data_dir.exists():
            return 0
        return len(list(self.raw_data_dir.glob("*.pdf")))
    
    def _count_basic_metadata(self) -> int:
        """Count basic metadata files"""
        if not self.metadata_dir.exists():
            return 0
        return len(list(self.metadata_dir.glob("*_metadata.json")))
    
    def _count_ai_processed(self) -> int:
        """Count AI-processed metadata files"""
        if not self.metadata_dir.exists():
            return 0
        
        ai_processed = 0
        for metadata_file in self.metadata_dir.glob("*_metadata.json"):
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                # Check if AI processing is complete
                if (metadata.get('ai_model') and 
                    metadata.get('executive_summary') and 
                    'Pending AI processing' not in str(metadata.get('executive_summary', ''))):
                    ai_processed += 1
            except Exception:
                continue
        
        return ai_processed
    
    def _count_enhanced_metadata(self) -> int:
        """Count enhanced metadata files"""
        if not self.metadata_dir.exists():
            return 0
        return len(list(self.metadata_dir.glob("*_enhanced_metadata.json")))
    
    def _check_vector_database(self) -> int:
        """Check vector database status"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code != 200:
                return 0
                
            # Test search to see how many documents are loaded
            search_response = requests.post(
                f"{self.base_url}/api/v1/search/discovery_search",
                json={"search_query": "legal", "limit": 50},
                timeout=10
            )
            
            if search_response.status_code == 200:
                results = search_response.json()
                return len(results.get('entries', []))
            
        except Exception:
            pass
        
        return 0
    
    def run_step_1_preprocessing(self, limit: Optional[int] = None) -> bool:
        """Step 1: Document Preprocessing (PDFs → Basic Metadata + Chunks)"""
        
        print(f"\n🔄 **STEP 1: DOCUMENT PREPROCESSING**")
        print("=" * 50)
        
        start_time = time.time()
        self.pipeline_state["step_1_preprocessing"]["status"] = "running"
        
        try:
            # Build command
            cmd = ["python3", "scripts/process_documents_claude.py", 
                   "--input-dir", "raw_data", "--output-dir", "output"]
            
            if limit:
                cmd.extend(["--limit", str(limit)])
            
            print(f"📋 Running: {' '.join(cmd)}")
            
            # Run preprocessing
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            duration = time.time() - start_time
            
            if result.returncode == 0:
                files_processed = self._count_basic_metadata()
                self.pipeline_state["step_1_preprocessing"].update({
                    "status": "completed",
                    "files_processed": files_processed,
                    "duration": duration
                })
                
                print(f"✅ Step 1 completed in {duration:.1f}s")
                print(f"📄 Files processed: {files_processed}")
                return True
            else:
                print(f"❌ Step 1 failed: {result.stderr}")
                self.pipeline_state["step_1_preprocessing"]["status"] = "failed"
                return False
                
        except Exception as e:
            print(f"❌ Step 1 error: {e}")
            self.pipeline_state["step_1_preprocessing"]["status"] = "failed"
            return False
    
    def run_step_2_ai_enhancement(self, limit: Optional[int] = None) -> bool:
        """Step 2: AI Enhancement (Claude Processing → Rich Content)"""
        
        print(f"\n🧠 **STEP 2: AI CONTENT ENHANCEMENT**")
        print("=" * 50)
        
        # Note: This step is integrated into step 1 with current architecture
        # But we can verify AI processing completion
        
        start_time = time.time()
        self.pipeline_state["step_2_ai_enhancement"]["status"] = "running"
        
        try:
            ai_processed = self._count_ai_processed()
            duration = time.time() - start_time
            
            self.pipeline_state["step_2_ai_enhancement"].update({
                "status": "completed",
                "files_processed": ai_processed,
                "duration": duration
            })
            
            print(f"✅ Step 2 verified in {duration:.1f}s")
            print(f"🧠 AI-processed files: {ai_processed}")
            
            if ai_processed == 0:
                print("⚠️  No AI-processed files found. Check Step 1 completion.")
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Step 2 error: {e}")
            self.pipeline_state["step_2_ai_enhancement"]["status"] = "failed"
            return False
    
    def run_step_3_field_enhancement(self, limit: Optional[int] = None) -> bool:
        """Step 3: Field Enhancement (Legal Field Extraction → 82+ Fields)"""
        
        print(f"\n⚡ **STEP 3: FIELD ENHANCEMENT**")
        print("=" * 50)
        
        start_time = time.time()
        self.pipeline_state["step_3_field_enhancement"]["status"] = "running"
        
        try:
            # Build command
            cmd = ["python3", "enhanced_preprocessing.py"]
            
            if limit:
                cmd.extend(["--limit", str(limit)])
            
            print(f"📋 Running: {' '.join(cmd)}")
            
            # Run field enhancement
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            duration = time.time() - start_time
            
            if result.returncode == 0:
                enhanced_files = self._count_enhanced_metadata()
                self.pipeline_state["step_3_field_enhancement"].update({
                    "status": "completed",
                    "files_processed": enhanced_files,
                    "duration": duration
                })
                
                print(f"✅ Step 3 completed in {duration:.1f}s")
                print(f"⚡ Enhanced files: {enhanced_files}")
                print(f"📋 Enhancement output: {result.stdout[-500:]}")  # Last 500 chars
                return True
            else:
                print(f"❌ Step 3 failed: {result.stderr}")
                self.pipeline_state["step_3_field_enhancement"]["status"] = "failed"
                return False
                
        except Exception as e:
            print(f"❌ Step 3 error: {e}")
            self.pipeline_state["step_3_field_enhancement"]["status"] = "failed"
            return False
    
    def run_step_4_vector_loading(self, limit: Optional[int] = None) -> bool:
        """Step 4: Vector Loading (Metadata → Superlinked Database)"""
        
        print(f"\n🚀 **STEP 4: VECTOR DATABASE LOADING**")
        print("=" * 50)
        
        start_time = time.time()
        self.pipeline_state["step_4_vector_loading"]["status"] = "running"
        
        try:
            # Check if Superlinked is running
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code != 200:
                print(f"❌ Superlinked server not accessible at {self.base_url}")
                return False
            
            # Build command
            cmd = ["python3", "load_real_data.py", "--url", self.base_url]
            
            if limit:
                cmd.extend(["--limit", str(limit)])
            
            print(f"📋 Running: {' '.join(cmd)}")
            
            # Run vector loading
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            duration = time.time() - start_time
            
            if result.returncode == 0:
                loaded_count = self._check_vector_database()
                self.pipeline_state["step_4_vector_loading"].update({
                    "status": "completed",
                    "files_loaded": loaded_count,
                    "duration": duration
                })
                
                print(f"✅ Step 4 completed in {duration:.1f}s")
                print(f"🚀 Documents loaded: {loaded_count}")
                print(f"📋 Loading output: {result.stdout[-500:]}")  # Last 500 chars
                return True
            else:
                print(f"❌ Step 4 failed: {result.stderr}")
                self.pipeline_state["step_4_vector_loading"]["status"] = "failed"
                return False
                
        except Exception as e:
            print(f"❌ Step 4 error: {e}")
            self.pipeline_state["step_4_vector_loading"]["status"] = "failed"
            return False
    
    def run_step_5_validation(self) -> bool:
        """Step 5: Validation & Testing (Search Quality → Performance Metrics)"""
        
        print(f"\n✅ **STEP 5: VALIDATION & TESTING**")
        print("=" * 50)
        
        start_time = time.time()
        self.pipeline_state["step_5_validation"]["status"] = "running"
        
        tests_passed = 0
        
        try:
            # Test 1: Basic connectivity
            print(f"🔹 Test 1: System Connectivity")
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                tests_passed += 1
                print(f"  ✅ Superlinked server accessible")
            else:
                print(f"  ❌ Server not accessible")
            
            # Test 2: Search functionality
            print(f"🔹 Test 2: Basic Search")
            search_response = requests.post(
                f"{self.base_url}/api/v1/search/discovery_search",
                json={"search_query": "medical", "limit": 3},
                timeout=10
            )
            
            if search_response.status_code == 200:
                results = search_response.json()
                if results.get('entries'):
                    tests_passed += 1
                    print(f"  ✅ Search returns {len(results['entries'])} results")
                else:
                    print(f"  ❌ Search returns no results")
            else:
                print(f"  ❌ Search request failed")
            
            # Test 3: Field population
            print(f"🔹 Test 3: Field Population")
            if search_response.status_code == 200:
                results = search_response.json()
                if results.get('entries'):
                    entry = results['entries'][0]
                    fields = entry.get('fields', {})
                    populated_fields = [k for k, v in fields.items() if v]
                    
                    if len(populated_fields) >= 10:
                        tests_passed += 1
                        print(f"  ✅ {len(populated_fields)} fields populated")
                    else:
                        print(f"  ❌ Only {len(populated_fields)} fields populated")
                        
            # Test 4: Enhanced field detection
            print(f"🔹 Test 4: Enhanced Field Detection")
            enhanced_count = self._count_enhanced_metadata()
            if enhanced_count > 0:
                tests_passed += 1
                print(f"  ✅ {enhanced_count} enhanced metadata files found")
            else:
                print(f"  ❌ No enhanced metadata files found")
            
            # Test 5: Performance test
            print(f"🔹 Test 5: Performance Test")
            performance_start = time.time()
            
            performance_queries = [
                "medical malpractice",
                "expert witness requirements", 
                "texas statute"
            ]
            
            performance_passed = True
            for query in performance_queries:
                query_start = time.time()
                response = requests.post(
                    f"{self.base_url}/api/v1/search/discovery_search",
                    json={"search_query": query, "limit": 1},
                    timeout=5
                )
                query_time = time.time() - query_start
                
                if response.status_code == 200 and query_time < 2.0:
                    print(f"    ✅ '{query}': {query_time:.3f}s")
                else:
                    print(f"    ❌ '{query}': {query_time:.3f}s (too slow or failed)")
                    performance_passed = False
            
            if performance_passed:
                tests_passed += 1
                print(f"  ✅ All performance tests passed")
            
            duration = time.time() - start_time
            
            self.pipeline_state["step_5_validation"].update({
                "status": "completed",
                "tests_passed": tests_passed,
                "duration": duration
            })
            
            print(f"\n✅ Validation completed in {duration:.1f}s")
            print(f"🎯 Tests passed: {tests_passed}/5")
            
            return tests_passed >= 4  # Must pass at least 4/5 tests
            
        except Exception as e:
            print(f"❌ Validation error: {e}")
            self.pipeline_state["step_5_validation"]["status"] = "failed"
            return False
    
    def run_complete_pipeline(self, limit: Optional[int] = None) -> bool:
        """Run the complete data ingestion pipeline"""
        
        print("🚀 **COMPLETE DATA INGESTION PIPELINE**")
        print("=" * 80)
        
        pipeline_start = time.time()
        
        # Analyze current state
        current_state = self.analyze_current_state()
        
        # Run pipeline steps
        steps = [
            ("Step 1: Document Preprocessing", self.run_step_1_preprocessing),
            ("Step 2: AI Enhancement Verification", self.run_step_2_ai_enhancement),
            ("Step 3: Field Enhancement", self.run_step_3_field_enhancement),
            ("Step 4: Vector Loading", self.run_step_4_vector_loading),
            ("Step 5: Validation & Testing", self.run_step_5_validation)
        ]
        
        pipeline_success = True
        
        for step_name, step_func in steps:
            print(f"\n{'='*20} {step_name} {'='*20}")
            
            if step_name == "Step 5: Validation & Testing":
                success = step_func()
            else:
                success = step_func(limit)
            
            if not success:
                print(f"❌ {step_name} failed - stopping pipeline")
                pipeline_success = False
                break
        
        # Final summary
        total_duration = time.time() - pipeline_start
        
        print(f"\n🎯 **PIPELINE SUMMARY**")
        print("=" * 80)
        print(f"Total Duration: {total_duration:.1f} seconds")
        print(f"Pipeline Status: {'✅ SUCCESS' if pipeline_success else '❌ FAILED'}")
        
        # Print step details
        for step_name, step_data in self.pipeline_state.items():
            status_icon = "✅" if step_data["status"] == "completed" else "❌"
            print(f"{status_icon} {step_name}: {step_data['status']} ({step_data['duration']:.1f}s)")
        
        return pipeline_success
    
    def run_incremental_pipeline(self) -> bool:
        """Run pipeline incrementally - process existing files through enhancement steps"""
        
        print("🔄 **INCREMENTAL PIPELINE PROCESSING**")
        print("=" * 80)
        print("Processing existing documents through enhancement pipeline one at a time")
        
        pipeline_start = time.time()
        total_processed = 0
        
        # Analyze starting state
        print(f"\n📊 **Starting State Analysis**")
        current_state = self.analyze_current_state()
        
        # Get list of AI-processed files that need enhancement
        import json
        from pathlib import Path
        
        metadata_dir = Path("output/metadata")
        ai_processed_files = []
        
        for file_path in metadata_dir.glob("*_metadata.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                if (data.get('ai_model') == 'claude-opus-4-20250514' and 
                    'Pending AI processing' not in str(data.get('executive_summary', ''))):
                    ai_processed_files.append(file_path)
            except:
                continue
        
        print(f"\n📋 **Found {len(ai_processed_files)} AI-processed files ready for enhancement**")
        
        if not ai_processed_files:
            print("⚠️  No AI-processed files found. Run preprocessing first.")
            return False
        
        # Process each AI-processed file through enhancement pipeline
        for i, metadata_file in enumerate(ai_processed_files):
            print(f"\n{'='*60}")
            print(f"🔍 **PROCESSING DOCUMENT #{i + 1}/{len(ai_processed_files)}**")
            print(f"📄 File: {metadata_file.name}")
            print(f"{'='*60}")
            
            # Load metadata to show document info
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                print(f"📋 Title: {metadata.get('title', 'Unknown')[:60]}...")
                print(f"📊 Facts: {metadata.get('fact_count', 0)} | Pages: {metadata.get('total_pages', 0)}")
            except:
                print(f"📋 Processing: {metadata_file.name}")
            
            # Step 3: Field enhancement for this specific document
            print(f"\n⚡ Step 3: Field Enhancement")
            from enhanced_preprocessing import EnhancedFieldExtractor
            
            try:
                extractor = EnhancedFieldExtractor()
                enhanced_metadata = extractor.enhance_existing_metadata(metadata_file)
                
                # Save enhanced version
                enhanced_filename = metadata_file.name.replace('_metadata.json', '_enhanced_metadata.json')
                enhanced_path = metadata_dir / enhanced_filename
                
                with open(enhanced_path, 'w') as f:
                    json.dump(enhanced_metadata, f, indent=2)
                
                # Show what was added
                new_fields = [k for k, v in enhanced_metadata.items() 
                             if k.startswith(('temporal', 'authority', 'penalties', 'requirements', 
                                           'specialties', 'readability', 'complexity', 'enhancement')) and v]
                
                print(f"   ✅ Enhanced with {len(new_fields)} additional fields")
                if new_fields:
                    print(f"   📊 New fields: {new_fields[:3]}{'...' if len(new_fields) > 3 else ''}")
                
                step3_success = True
                
            except Exception as e:
                print(f"   ❌ Enhancement failed: {e}")
                step3_success = False
                continue
            
            # Step 4: Load this document to vector database
            print(f"\n🚀 Step 4: Vector Loading")
            try:
                from load_real_data import SuperlinkedDataLoader
                loader = SuperlinkedDataLoader(self.base_url)
                
                # Load the enhanced metadata if it exists, otherwise original
                if enhanced_path.exists():
                    document, original_metadata = loader.load_document(enhanced_path)
                else:
                    document, original_metadata = loader.load_document(metadata_file)
                
                # Ingest document
                if loader.ingest_document(document):
                    print(f"   ✅ Successfully loaded to vector database")
                    step4_success = True
                else:
                    print(f"   ❌ Failed to load to vector database")
                    step4_success = False
                    continue
                    
            except Exception as e:
                print(f"   ❌ Vector loading failed: {e}")
                step4_success = False
                continue
            
            # Step 5: Quick validation
            print(f"\n✅ Step 5: Validation")
            try:
                response = requests.get(f"{self.base_url}/health", timeout=5)
                if response.status_code == 200:
                    print(f"   ✅ System healthy")
                    step5_success = True
                else:
                    print(f"   ⚠️  System health check failed")
                    step5_success = False
            except Exception as e:
                print(f"   ❌ Validation failed: {e}")
                step5_success = False
            
            total_processed += 1
            
            print(f"\n🎯 **DOCUMENT #{total_processed} COMPLETE**")
            print(f"   ⚡ Field Enhancement: {'SUCCESS' if step3_success else 'FAILED'}")
            print(f"   🚀 Vector Loading: {'SUCCESS' if step4_success else 'FAILED'}")
            print(f"   ✅ Validation: {'SUCCESS' if step5_success else 'FAILED'}")
            
            # Show current state
            vector_count = self._check_vector_database()
            enhanced_count = self._count_enhanced_metadata()
            
            print(f"\n📊 **Current Pipeline State:**")
            print(f"   📄 Documents Processed: {total_processed}/{len(ai_processed_files)}")
            print(f"   🧠 Enhanced Metadata: {enhanced_count}")
            print(f"   🚀 Vector Database: {vector_count} entries")
            
            # Ask user if they want to continue (for interactive mode)
            if i < len(ai_processed_files) - 1:  # Not the last document
                print(f"\n⏳ **Ready for Next Document** (Document #{total_processed + 1})")
                print(f"   Press Ctrl+C to stop, or wait 3 seconds to continue...")
                
                try:
                    time.sleep(3)
                except KeyboardInterrupt:
                    print(f"\n⚠️  **USER STOPPED PROCESSING**")
                    break
        
        # Final summary
        total_duration = time.time() - pipeline_start
        
        print(f"\n🎯 **INCREMENTAL PIPELINE SUMMARY**")
        print("=" * 80)
        print(f"Total Documents Processed: {total_processed}/{len(ai_processed_files)}")
        print(f"Total Duration: {total_duration:.1f} seconds")
        print(f"Average Time per Document: {total_duration/max(total_processed,1):.1f} seconds")
        
        # Final state and validation
        print(f"\n🔍 **Final Validation**")
        final_validation = self.run_step_5_validation()
        
        return total_processed > 0
    
    def quick_test(self) -> bool:
        """Quick pipeline test for development"""
        
        print("⚡ **QUICK PIPELINE TEST**")
        print("=" * 40)
        
        return self.run_complete_pipeline(limit=2)

def main():
    """Main pipeline orchestrator interface"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Data Ingestion Pipeline Orchestrator')
    parser.add_argument('--mode', choices=['analyze', 'quick', 'full', 'step', 'incremental'], 
                       default='analyze', help='Pipeline mode')
    parser.add_argument('--step', type=int, choices=[1,2,3,4,5], 
                       help='Specific step to run (1-5)')
    parser.add_argument('--limit', type=int, help='Limit files processed')
    parser.add_argument('--url', default='http://localhost:8080', 
                       help='Superlinked server URL')
    
    args = parser.parse_args()
    
    orchestrator = PipelineOrchestrator(args.url)
    
    if args.mode == 'analyze':
        orchestrator.analyze_current_state()
        
    elif args.mode == 'quick':
        success = orchestrator.quick_test()
        exit(0 if success else 1)
        
    elif args.mode == 'full':
        success = orchestrator.run_complete_pipeline(args.limit)
        exit(0 if success else 1)
        
    elif args.mode == 'incremental':
        success = orchestrator.run_incremental_pipeline()
        exit(0 if success else 1)
        
    elif args.mode == 'step' and args.step:
        step_functions = {
            1: orchestrator.run_step_1_preprocessing,
            2: orchestrator.run_step_2_ai_enhancement,
            3: orchestrator.run_step_3_field_enhancement,
            4: orchestrator.run_step_4_vector_loading,
            5: orchestrator.run_step_5_validation
        }
        
        if args.step == 5:
            success = step_functions[args.step]()
        else:
            success = step_functions[args.step](args.limit)
        exit(0 if success else 1)

if __name__ == "__main__":
    main()