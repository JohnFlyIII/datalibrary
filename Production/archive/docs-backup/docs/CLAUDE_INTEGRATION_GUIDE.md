# Claude Integration Guide for Legal Document Processing

This guide explains how to use Claude (Anthropic) for AI-powered legal document preprocessing.

## Why Claude for Legal Documents?

Claude offers several advantages for legal document processing:

1. **Large Context Window**: Claude can handle up to 100k+ tokens, allowing analysis of lengthy legal documents
2. **Precise Fact Extraction**: Excellent at identifying specific legal provisions and citations
3. **Structured Output**: Reliably produces well-formatted JSON responses
4. **Legal Understanding**: Strong comprehension of legal terminology and concepts
5. **Citation Awareness**: Can format legal citations properly (APA, Bluebook, etc.)

## Setup

### 1. Get API Key

1. Sign up at [console.anthropic.com](https://console.anthropic.com)
2. Create an API key
3. Add to `.env.local`:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
   ```

### 2. Install Dependencies

```bash
pip install anthropic sentence-transformers pdfplumber
```

### 3. Choose Your Model

| Model | Best For | Speed | Cost | Context |
|-------|----------|-------|------|---------|
| **Claude 3 Opus** | Complex analysis, comprehensive extraction | Slower | Higher | 200k tokens |
| **Claude 3 Sonnet** | Balanced performance, most tasks | Medium | Medium | 200k tokens |
| **Claude 3 Haiku** | Quick summaries, simple extraction | Fast | Lower | 200k tokens |

**Recommendation**: Use Sonnet for most legal document processing tasks.

## Usage Examples

### Basic Processing

```bash
# Process documents with Claude
python scripts/process_documents_claude.py \
  --input-dir ./pdfs \
  --output-dir ./output \
  --model claude-3-sonnet-20240229
```

### Test Claude Integration

```bash
# Test fact extraction and summarization
python scripts/test_claude_extraction.py
```

### Custom Model Selection

```bash
# Use Opus for complex documents
python scripts/process_documents_claude.py \
  --input-dir ./complex_pdfs \
  --model claude-3-opus-20240229

# Use Haiku for quick processing
python scripts/process_documents_claude.py \
  --input-dir ./simple_pdfs \
  --model claude-3-haiku-20240307
```

## Configuration

### Environment Variables

```bash
# .env.local
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
CLAUDE_MODEL=claude-3-sonnet-20240229
AI_PROVIDER=anthropic

# Processing settings
CHUNK_SIZE=2000
CHUNK_OVERLAP=200
MAX_TOKENS_PER_REQUEST=4000
```

### Configuration File

```json
// config.json
{
  "processing": {
    "ai_provider": "anthropic",
    "fact_extraction_model": "claude-3-sonnet-20240229",
    "summary_model": "claude-3-sonnet-20240229",
    "claude_models": {
      "opus": "claude-3-opus-20240229",
      "sonnet": "claude-3-sonnet-20240229",
      "haiku": "claude-3-haiku-20240307"
    }
  }
}
```

## Claude-Specific Features

### 1. Fact Extraction with Citations

Claude excels at extracting facts with proper legal citations:

```python
# Example output from Claude
{
  "facts": [
    {
      "fact": "The statute of limitations for personal injury claims is two years",
      "location": "Page 12, Section 16.003",
      "citation": "Tex. Civ. Prac. & Rem. Code § 16.003 (2024)",
      "context": ["statute of limitations", "personal injury", "two years"],
      "confidence": 0.95
    }
  ]
}
```

### 2. Hierarchical Analysis

Claude can identify hierarchical structures in legal documents:
- Chapters → Sections → Subsections
- Primary provisions → Exceptions → Special cases

### 3. Cross-Reference Detection

Claude automatically identifies:
- Internal references ("as provided in Section 16.010")
- External references to other codes
- Case law citations

## Best Practices

### 1. Prompt Engineering

```python
# Good prompt structure for Claude
prompt = f"""You are a legal analysis expert. Extract key legal facts.

For each fact:
1. State the fact clearly and concisely
2. Provide exact location (page/section)
3. Include proper legal citation
4. Add searchable context keywords
5. Assign confidence score

Document text:
{document_text}

Return as JSON with structure: {{...}}"""
```

### 2. Token Management

```python
# Chunk large documents appropriately
if len(document_text) > 50000:  # ~12k tokens
    # Process in sections
    chunks = split_by_sections(document_text)
    for chunk in chunks:
        process_chunk(chunk)
```

### 3. Error Handling

```python
try:
    response = anthropic_client.messages.create(...)
except anthropic.RateLimitError:
    time.sleep(60)  # Wait and retry
except anthropic.APIError as e:
    log.error(f"API error: {e}")
```

## Cost Optimization

### Estimated Costs (as of 2024)

| Model | Input | Output | 1000-page document |
|-------|-------|--------|-------------------|
| Opus | $15/MTok | $75/MTok | ~$3-5 |
| Sonnet | $3/MTok | $15/MTok | ~$0.60-1 |
| Haiku | $0.25/MTok | $1.25/MTok | ~$0.05-0.10 |

### Tips to Reduce Costs

1. **Use Haiku for initial classification**
   ```python
   # Quick classification with Haiku
   doc_type = classify_with_haiku(first_page)
   
   # Detailed extraction with Sonnet
   if doc_type in ['statute', 'regulation']:
       extract_with_sonnet(full_document)
   ```

2. **Process in batches during off-peak**
3. **Cache results** to avoid reprocessing
4. **Use embeddings** for similarity search instead of re-analyzing

## Comparison: Claude vs GPT-4

| Feature | Claude | GPT-4 |
|---------|--------|-------|
| Context Window | 200k tokens | 128k tokens |
| Legal Citations | Excellent | Good |
| JSON Formatting | Very Reliable | Reliable |
| Processing Speed | Fast | Moderate |
| Cost | Lower | Higher |

## Troubleshooting

### Common Issues

1. **"Invalid API Key"**
   - Check `.env.local` exists and contains valid key
   - Ensure no extra spaces in API key

2. **"Rate limit exceeded"**
   - Implement exponential backoff
   - Reduce batch size
   - Upgrade API tier if needed

3. **"JSON parsing failed"**
   - Claude may add explanation text
   - Use regex to extract JSON: `re.search(r'\{.*\}', response, re.DOTALL)`

4. **"Context length exceeded"**
   - Split document into smaller chunks
   - Use section-aware splitting
   - Consider using Haiku for large documents

### Debug Mode

```bash
# Enable debug logging
export ANTHROPIC_LOG=debug
python scripts/process_documents_claude.py --input-dir ./test
```

## Migration from OpenAI

If migrating from OpenAI/GPT-4:

1. **Update API client**:
   ```python
   # Old
   import openai
   openai.ChatCompletion.create(...)
   
   # New
   from anthropic import Anthropic
   client = Anthropic()
   client.messages.create(...)
   ```

2. **Adjust prompts** - Claude prefers direct instructions
3. **Update token counting** - Claude uses different tokenizer
4. **Modify temperature** - Claude is often more deterministic

## Support

- Anthropic Documentation: [docs.anthropic.com](https://docs.anthropic.com)
- API Status: [status.anthropic.com](https://status.anthropic.com)
- Community: [github.com/anthropics/anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python)