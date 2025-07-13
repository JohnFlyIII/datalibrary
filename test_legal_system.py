#!/usr/bin/env python3
"""
Legal Knowledge System Test Suite
Tests various queries and features
"""
import requests
import json
import time

def test_query(endpoint, query, description):
    """Test a query endpoint"""
    url = f"http://localhost:8080/api/v1/search/{endpoint}"
    data = {"search_query": query}
    
    print(f"\n🔍 Testing: {description}")
    print(f"Query: '{query}'")
    print(f"Endpoint: {endpoint}")
    
    try:
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            entries = result.get('entries', [])
            print(f"✅ Found {len(entries)} results")
            
            if entries:
                # Show first result snippet
                first = entries[0]['fields']
                title = first.get('title', 'No title')
                content = first.get('content_text', '')[:200] + "..."
                print(f"📄 Top result: {title}")
                print(f"📝 Snippet: {content}")
            
            return True
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🏛️ Legal Knowledge System Test Suite")
    print("=" * 50)
    
    test_cases = [
        # Medical malpractice queries
        ("medical_malpractice", "hospital negligence standard of care", "Medical Malpractice - Standard of Care"),
        ("medical_malpractice", "informed consent medical procedure", "Medical Malpractice - Informed Consent"),
        ("medical_malpractice", "expert witness medical testimony", "Medical Malpractice - Expert Witness"),
        
        # General legal queries
        ("legal_research", "damages personal injury", "Personal Injury Damages"),
        ("legal_research", "statute of limitations tort", "Statute of Limitations"),
        ("legal_research", "civil procedure discovery", "Civil Procedure Discovery"),
        
        # Practice area queries
        ("practice_area", "frivolous lawsuit sanctions", "Frivolous Lawsuits"),
        ("practice_area", "court fees exemption", "Court Fees and Exemptions"),
        
        # Authority-based queries
        ("authority", "Texas Supreme Court precedent", "Supreme Court Authority"),
        ("authority", "appellate procedure", "Appellate Authority"),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for endpoint, query, description in test_cases:
        if test_query(endpoint, query, description):
            passed += 1
        time.sleep(1)  # Brief pause between tests
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Legal Knowledge System is working perfectly.")
    elif passed > total * 0.8:
        print("✅ Most tests passed. System is functioning well.")
    else:
        print("⚠️ Some tests failed. Check system configuration.")

if __name__ == "__main__":
    main()