#!/usr/bin/env python3
"""
Debug Enhanced Metadata Loading
===============================
Test what happens when we load enhanced metadata files
"""

from load_real_data import SuperlinkedDataLoader
from pathlib import Path
import json

def debug_loading():
    print("🔍 DEBUG: Enhanced Metadata Loading")
    print("=" * 50)
    
    loader = SuperlinkedDataLoader()
    
    # Find enhanced metadata files
    enhanced_files = list(Path('output/metadata').glob('*_enhanced_metadata.json'))
    print(f"Enhanced files found: {len(enhanced_files)}")
    
    if not enhanced_files:
        print("❌ No enhanced files found!")
        return
    
    # Test with first enhanced file
    test_file = enhanced_files[0]
    print(f"\n📋 Testing: {test_file.name}")
    
    # Load the raw metadata to see what's in it
    with open(test_file, 'r') as f:
        raw_metadata = json.load(f)
    
    enhanced_field_names = [k for k in raw_metadata.keys() 
                           if k.startswith(('temporal', 'authority', 'penalties', 'requirements', 
                                         'specialties', 'readability', 'complexity', 'enhancement'))]
    
    print(f"📊 Enhanced fields in raw file: {len(enhanced_field_names)}")
    for field in enhanced_field_names:
        print(f"   {field}: {raw_metadata[field]}")
    
    # Now test the loading script
    print(f"\n🔄 Testing load_real_data.py processing...")
    document, original_metadata = loader.load_document(test_file)
    
    print(f"Document keys created: {len(document.keys())}")
    populated_fields = {k: v for k, v in document.items() 
                       if v and str(v) not in ['0', 'false', '', '[]', '{}']}
    print(f"Populated fields: {len(populated_fields)}")
    
    # Check if enhanced fields made it through
    print(f"\n✅ Enhanced Field Mapping Check:")
    for field in enhanced_field_names:
        if field in document:
            print(f"   ✅ {field}: {document[field]}")
        else:
            print(f"   ❌ {field}: MISSING from document")
    
    # Check if these fields are in the schema mapping
    print(f"\n📋 Sample of populated fields:")
    for k, v in list(populated_fields.items())[:10]:
        print(f"   {k}: {str(v)[:50]}...")

if __name__ == "__main__":
    debug_loading()