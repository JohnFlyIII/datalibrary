#!/bin/bash

echo "Testing Legal Document System with Document Types"
echo "================================================"

# Wait for health check
echo -e "\n1. Checking health..."
curl -s http://localhost:8080/health | jq '.'

echo -e "\n2. Ingesting documents with types..."
curl -X POST http://localhost:8080/api/v1/ingest/legal_document \
  -H "Content-Type: application/json" \
  -d '[
    {
      "id": "1",
      "title": "Texas Civil Practice and Remedies Code - Section 74",
      "content": "This section governs medical liability claims in Texas. It establishes requirements for expert reports in healthcare liability claims and sets standards for medical malpractice cases.",
      "document_type": "statute"
    },
    {
      "id": "2", 
      "title": "California Consumer Privacy Act",
      "content": "The CCPA provides California residents with rights regarding their personal information. Businesses must disclose data collection practices and allow consumers to opt out of data sales.",
      "document_type": "statute"
    },
    {
      "id": "3",
      "title": "Federal Rules of Civil Procedure - Rule 26",
      "content": "Parties must disclose witnesses and documents relevant to disputed facts. This rule governs discovery procedures and requires parties to provide initial disclosures without awaiting a discovery request.",
      "document_type": "rule"
    },
    {
      "id": "4",
      "title": "Smith v. Jones Medical Center",
      "content": "In this medical malpractice case, the court held that the plaintiff failed to provide adequate expert testimony regarding the standard of care. The case was dismissed for failure to meet statutory requirements.",
      "document_type": "case"
    },
    {
      "id": "5",
      "title": "HIPAA Privacy Rule",
      "content": "The Privacy Rule protects all individually identifiable health information held or transmitted by covered entities. It gives patients rights over their health information and sets rules for its use and disclosure.",
      "document_type": "regulation"
    },
    {
      "id": "6",
      "title": "CMS Guidance on Telehealth Services",
      "content": "This guidance clarifies Medicare coverage for telehealth services during the public health emergency. It expands the types of services that can be provided remotely and the locations where patients can receive them.",
      "document_type": "guidance"
    },
    {
      "id": "7",
      "title": "EPA Clean Water Act Regulations",
      "content": "These regulations implement the Clean Water Act provisions regarding discharge of pollutants into waters of the United States. They establish the National Pollutant Discharge Elimination System permit program.",
      "document_type": "regulation"
    },
    {
      "id": "8",
      "title": "Doe v. State Department of Health",
      "content": "The appellate court reversed the lower court decision, finding that the health department violated procedural due process rights when revoking the medical license without proper notice and hearing.",
      "document_type": "case"
    }
  ]'

echo -e "\n\nData ingested. Waiting 5 seconds for indexing..."
sleep 5

echo -e "\n3. Testing searches..."

echo -e "\n--- Search for all statutes ---"
curl -s -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "",
    "title_query": "",
    "document_type": "statute",
    "limit": 10
  }' | jq '.'

echo -e "\n--- Search for medical malpractice cases ---"
curl -s -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "medical malpractice",
    "title_query": "",
    "document_type": "case",
    "limit": 5
  }' | jq '.'

echo -e "\n--- Search for regulations about privacy ---"
curl -s -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "privacy",
    "title_query": "",
    "document_type": "regulation",
    "limit": 5
  }' | jq '.'

echo -e "\n--- Search for any document about Texas ---"
curl -s -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "Texas",
    "title_query": "Texas",
    "document_type": "",
    "limit": 5
  }' | jq '.'

echo -e "\nTest complete!"