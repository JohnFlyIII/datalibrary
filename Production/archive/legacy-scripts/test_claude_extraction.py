#!/usr/bin/env python3
"""
Test Claude Extraction

A simple script to test Claude's fact extraction and summarization
capabilities on a sample legal text.
"""

import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment
load_dotenv('.env.local')

# Sample legal text for testing
SAMPLE_TEXT = """
[Page 1]
TEXAS CIVIL PRACTICE AND REMEDIES CODE
TITLE 2. TRIAL, JUDGMENT, AND APPEAL
SUBTITLE B. TRIAL MATTERS
CHAPTER 16. LIMITATIONS

Sec. 16.003. TWO-YEAR LIMITATIONS PERIOD. 
(a) Except as provided by Sections 16.010, 16.0031, and 16.0045, a person must bring suit for trespass for injury to the person or for injury to the personal property of another not later than two years after the day the cause of action accrues.
(b) A person must bring suit not later than two years after the day the cause of action accrues for:
(1) taking or detaining the personal property of another; or
(2) personal injury.

Sec. 16.004. FOUR-YEAR LIMITATIONS PERIOD.
(a) A person must bring suit on the following actions not later than four years after the day the cause of action accrues:
(1) specific performance of a contract for the conveyance of real property;
(2) penalty or damages on the penal clause of a bond to execute the process of a court;
(3) debt;
(4) fraud; or
(5) breach of fiduciary duty.

[Page 2]
CHAPTER 41. DAMAGES

Sec. 41.001. DEFINITIONS. In this chapter:
(1) "Claimant" means a party seeking recovery of damages or on whose behalf damages are sought.
(2) "Defendant" means a party from whom a claimant seeks recovery of damages.

Sec. 41.008. LIMITATION ON AMOUNT OF RECOVERY.
(a) In an action in which a claimant seeks recovery of damages, the trier of fact shall determine the amount of economic damages separately from the amount of other compensatory damages.
(b) Exemplary damages awarded against a defendant may not exceed an amount equal to the greater of:
(1)(A) two times the amount of economic damages; plus
(B) an amount equal to any noneconomic damages found by the jury, not to exceed $750,000; or
(2) $200,000.
"""

def test_fact_extraction():
    """Test Claude's fact extraction capability"""
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    model = os.getenv('CLAUDE_MODEL', 'claude-3-sonnet-20240229')
    
    print(f"Testing fact extraction with {model}...")
    print("="*60)
    
    prompt = f"""You are a legal analysis expert. Extract key legal facts from this Texas statute excerpt.

For each fact:
1. State the fact clearly
2. Provide the exact location (page/section)
3. Include an APA citation
4. Add context keywords
5. Assign confidence (0.0-1.0)

Return as JSON with structure:
{{
  "facts": [
    {{
      "fact": "...",
      "location": "...",
      "citation": "...",
      "context": [...],
      "confidence": 0.95
    }}
  ],
  "key_findings": ["..."]
}}

Document:
{SAMPLE_TEXT}"""
    
    try:
        response = client.messages.create(
            model=model,
            max_tokens=2000,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = response.content[0].text
        print("Raw Response:")
        print(response_text)
        print("\n" + "="*60 + "\n")
        
        # Try to parse JSON
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            facts_data = json.loads(json_match.group())
            print("Parsed Facts:")
            print(json.dumps(facts_data, indent=2))
        else:
            print("Could not parse JSON from response")
            
    except Exception as e:
        print(f"Error: {e}")

def test_summary_generation():
    """Test Claude's summary generation capability"""
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    model = os.getenv('CLAUDE_MODEL', 'claude-3-sonnet-20240229')
    
    print(f"\n\nTesting summary generation with {model}...")
    print("="*60)
    
    prompt = f"""Create a legal document summary with:
1. Executive summary (max 150 words)
2. Key bullet points (4-6)
3. Brief conclusion
4. Plain language takeaways (2-3)

Format as JSON.

Document:
{SAMPLE_TEXT}"""
    
    try:
        response = client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = response.content[0].text
        print("Summary Response:")
        print(response_text)
        
    except Exception as e:
        print(f"Error: {e}")

def test_model_comparison():
    """Compare different Claude models"""
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    models = [
        'claude-3-haiku-20240307',
        'claude-3-sonnet-20240229',
        'claude-3-opus-20240229'
    ]
    
    print("\n\nModel Comparison Test")
    print("="*60)
    
    simple_prompt = "What is the statute of limitations for personal injury in this text?\n\n" + SAMPLE_TEXT
    
    for model in models:
        try:
            print(f"\n{model}:")
            response = client.messages.create(
                model=model,
                max_tokens=100,
                temperature=0,
                messages=[{"role": "user", "content": simple_prompt}]
            )
            print(response.content[0].text)
        except Exception as e:
            print(f"Error with {model}: {e}")

def main():
    """Run all tests"""
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("Error: ANTHROPIC_API_KEY not set")
        print("Please create .env.local with your API key")
        return
        
    print("Claude Legal Processing Test Suite")
    print("="*60)
    
    # Run tests
    test_fact_extraction()
    test_summary_generation()
    
    # Optional: compare models
    if input("\nCompare different Claude models? (y/n): ").lower() == 'y':
        test_model_comparison()

if __name__ == "__main__":
    main()