# Superlinked Developer Documentation

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Core Concepts](#core-concepts)
4. [Quick Start](#quick-start)
5. [Building Blocks](#building-blocks)
6. [Spaces Reference](#spaces-reference)
7. [Query System](#query-system)
8. [Production Deployment](#production-deployment)
9. [Vector Database Integration](#vector-database-integration)
10. [Examples and Use Cases](#examples-and-use-cases)
11. [API Reference](#api-reference)
12. [Troubleshooting](#troubleshooting)

---

## Overview

Superlinked is a Python framework for AI Engineers building high-performance search & recommendation applications that combine structured and unstructured data.

### Key Benefits

- **Improved Vector Search Relevance**: Improve your vector search relevance by encoding metadata together with your unstructured data into vectors
- **Multi-Modal Embeddings**: Combine text, images and structured metadata into multi-modal vectors that fully describe your entities in their complex context
- **Query-Time Flexibility**: Smoothly navigate the trade-off between multiple competing objectives like relevance, freshness and popularity
- **Production Ready**: The Superlinked Server is a deployable component available as a Python package on PyPI, designed to enhance the operation of Superlinked by providing a RESTful API

### Why Superlinked?

Vector Search with text-only embeddings fails on complex queries, because complex queries are never just about text. Traditional approaches face several challenges:

1. **Stringify and Embed Problems**: OpenAI embeddings result in noisy, non-monotonic cosine similarity scores. For example, CosSim(25, 50) equals to 0.69 when CosSim(32, 50) equals 0.42 meaning 25 is more similar to 50 than 32 which doesn't make sense

2. **Multi-Attribute Search Limitations**: Our naive approach - storing and searching attribute vectors separately, then combining results - is limited in ability, subtlety, and efficiency when we need to retrieve objects with multiple simultaneous attributes

3. **Filter Resolution**: When you convert a fuzzy preference like "recent", "risky" or "popular" into a filter, you model a sigmoid with a binary step function = not enough resolution

---

## Installation

### Requirements

- Python version: `>= 3.10` and `<= 3.12`

### Installation Steps

**In a notebook:**
```bash
%pip install superlinked
```

**As a script:**
```bash
# Check Python version
python -V  # Should be 3.10.x to 3.12.x

# Upgrade pip and install
python -m pip install --upgrade pip
python -m pip install superlinked
```

First run will take slightly longer as it has to download the embedding model.

---

## Core Concepts

### The Superlinked Approach

Instead of embedding all the data you have about an entity as a single vector, you can use Superlinked Spaces to embed it as different modalities, one vector per modality, and concatenate those vectors into a multimodal vector

### Key Principles

1. **Spaces-First Design**: At Superlinked, we use Spaces to embed different pieces of data, structured or unstructured, about an entity and concatenate them into a single, representative multimodal vector

2. **Better Vectors Upfront**: By prioritizing the creation of smarter vectors up front - and only then creating the index - we can achieve better quality retrieval, without costly and time-consuming reranking and general post-processing work

3. **Modular Architecture**: This modular approach separates query description from execution, enabling you to run the same query across different environments without reimplementation

---

## Quick Start

Here's a complete example to get you started:

```python
import json
import os
from superlinked import framework as sl

# Define your data schema
class Product(sl.Schema):
    id: sl.IdField
    description: sl.String
    rating: sl.Integer

# Create schema instance
product = Product()

# Define embedding spaces
description_space = sl.TextSimilaritySpace(
    text=product.description, 
    model="Alibaba-NLP/gte-large-en-v1.5"
)

rating_space = sl.NumberSpace(
    number=product.rating, 
    min_value=1, 
    max_value=5, 
    mode=sl.Mode.MAXIMUM
)

# Create index
index = sl.Index([description_space, rating_space], fields=[product.rating])

# Define query with parameters
query = (
    sl.Query(
        index,
        weights={
            description_space: sl.Param("description_weight"),
            rating_space: sl.Param("rating_weight"),
        },
    )
    .find(product)
    .similar(
        description_space,
        sl.Param(
            "description_query",
            description="The text in the user's query that refers to product descriptions.",
        ),
    )
    .select_all()
    .limit(sl.Param("limit"))
    .with_natural_query(
        sl.Param("natural_language_query"),
        sl.OpenAIClientConfig(api_key=os.environ["OPEN_AI_API_KEY"], model="gpt-4o")
    )
)

# Set up execution environment
source = sl.InMemorySource(product)
executor = sl.InMemoryExecutor(sources=[source], indices=[index])
app = executor.run()

# Ingest data
source.put([
    {
        "id": 1,
        "description": "Budget toothbrush in black color. Just what you need.",
        "rating": 1,
    },
    {
        "id": 2,
        "description": "High-end toothbrush created with no compromises.",
        "rating": 5,
    },
    {
        "id": 3,
        "description": "A toothbrush created for the smart 21st century man.",
        "rating": 3,
    },
])

# Query the system
result = app.query(query, natural_query="best toothbrushes", limit=1)

# Examine results
print(json.dumps(result.metadata, indent=2))
sl.PandasConverter.to_pandas(result)
```

---

## Building Blocks

Superlinked's framework is built on key components: @schema, Source, Spaces, Index, Query, and Executor. These building blocks allow you to create a modular system tailored to your specific use cases.

### 1. Schema (@schema)

To do this, you use the Schema decorator to annotate your class as a schema representing your structured data. Schemas translate to searchable entities in the embedding space.

```python
from superlinked import framework as sl

@sl.schema
class News(sl.Schema):
    id: sl.IdField
    created_at: sl.Timestamp
    like_count: sl.Integer
    moderation_score: sl.Float
    content: sl.String

@sl.schema
class User(sl.Schema):
    id: sl.IdField
    interest: sl.String

@sl.event_schema
class Event(sl.EventSchema):
    id: sl.IdField
    news: sl.SchemaReference[News]
    user: sl.SchemaReference[User]
    event_type: sl.String
```

**Field Types:**
- `sl.IdField`: Unique identifier
- `sl.String`: Text data
- `sl.Integer`: Numeric integers
- `sl.Float`: Numeric floats
- `sl.Timestamp`: Time-based data
- `sl.SchemaReference[T]`: References to other schemas

### 2. Spaces

The Space module encapsulates the vector creation logic that will be used at ingestion time, and again at query time.

Spaces lets you tailor how you embed different attributes of your data and can be categorized along 2 key dimensions: what input types the Space permits - e.g., text, timestamp, numeric, categorical; whether the Space represents similarity (e.g, TextSimilaritySpace) or scale (e.g., numeric space)

#### Available Spaces:

**Text Similarity Space:**
```python
text_space = sl.TextSimilaritySpace(
    text=schema.text_field,
    model="sentence-transformers/all-mpnet-base-v2"
)
```

**Number Space:**
```python
number_space = sl.NumberSpace(
    number=schema.numeric_field,
    min_value=0,
    max_value=100,
    mode=sl.Mode.MAXIMUM  # or sl.Mode.MINIMUM
)
```

**Categorical Similarity Space:**
```python
categorical_space = sl.CategoricalSimilaritySpace(
    category_input=schema.category_field,
    categories=["category1", "category2", "category3"]
)
```

**Recency Space:**
```python
recency_space = sl.RecencySpace(
    timestamp=schema.timestamp_field
)
```

**Image Space:**
```python
image_space = sl.ImageSpace(
    image=schema.image_field,
    model="open-clip"
)
```

### 3. Index

Superlinked's Index module components enable you to group Spaces into indices that make your queries more efficient.

```python
# Single space index
index = sl.Index(space)

# Multi-space index
index = sl.Index([space1, space2, space3])

# Index with additional fields
index = sl.Index(spaces, fields=[schema.field1, schema.field2])
```

### 4. Query

Query: defines the index you want it to search, and you can add Params here

```python
query = (
    sl.Query(index)
    .find(schema)
    .similar(space, sl.Param("query_param"))
    .select_all()
    .limit(sl.Param("limit"))
)
```

**Query Methods:**
- `.find(schema)`: Specify what to search for
- `.similar(space, param)`: Define similarity matching
- `.select_all()`: Return all stored fields
- `.limit(param)`: Limit number of results
- `.with_vector(vector)`: Search with specific vector
- `.with_natural_query(param, config)`: Enable natural language queries

### 5. Source

Use Source to connect your data to the schema.

```python
# In-memory source
source = sl.InMemorySource(schema)

# Add data
source.put([
    {"id": 1, "field1": "value1", "field2": 123},
    {"id": 2, "field1": "value2", "field2": 456},
])
```

### 6. Executor

Now that you've connected data with schema, you use the Executor to prepare your code to run. The Executor connects the source data with the index

```python
# In-memory executor
executor = sl.InMemoryExecutor(sources=[source], indices=[index])
app = executor.run()

# REST API executor
executor = sl.RestExecutor(sources=[source], indices=[index])
app = executor.run()
```

---

## Spaces Reference

### TextSimilaritySpace

Embeds text data for semantic similarity search.

```python
text_space = sl.TextSimilaritySpace(
    text=schema.text_field,
    model="sentence-transformers/all-mpnet-base-v2"  # or other supported models
)
```

**Supported Models:**
- Sentence Transformers models
- Custom models from Hugging Face
- OpenAI embedding models

### NumberSpace

Embed numerical values within a specified range for effective similarity comparisons.

```python
number_space = sl.NumberSpace(
    number=schema.numeric_field,
    min_value=0,
    max_value=100,
    mode=sl.Mode.MAXIMUM  # Optimize for higher values
    # mode=sl.Mode.MINIMUM  # Optimize for lower values
)
```

### CategoricalSimilaritySpace

Efficiently represent and compare categorical data in vector space for similarity searches.

```python
categorical_space = sl.CategoricalSimilaritySpace(
    category_input=schema.category_field,
    categories=["electronics", "clothing", "books"]
)
```

### RecencySpace

Incorporate time-based relevance into vector representations for up-to-date search results.

```python
recency_space = sl.RecencySpace(
    timestamp=schema.created_at
)
```

### ImageSpace

Embed text or images into a multi-modal vector space.

```python
image_space = sl.ImageSpace(
    image=schema.image_field,
    model="open-clip"
)
```

### Custom Spaces

Create and manage custom vector spaces for specialized similarity searches.

```python
custom_space = sl.CustomSpace(
    # Custom embedding logic
)
```

---

## Query System

### Basic Querying

```python
# Simple similarity query
query = (
    sl.Query(index)
    .find(schema)
    .similar(text_space, sl.Param("search_text"))
    .select_all()
)

result = app.query(query, search_text="artificial intelligence")
```

### Dynamic Parameters

Adjust query parameters dynamically to fine-tune search results.

```python
# Query with dynamic weights
query = (
    sl.Query(
        index,
        weights={
            text_space: sl.Param("text_weight"),
            number_space: sl.Param("number_weight"),
        }
    )
    .find(schema)
    .similar(text_space, sl.Param("query_text"))
    .select_all()
)

# Execute with different weights
result1 = app.query(
    query, 
    query_text="search term",
    text_weight=0.8,
    number_weight=0.2
)

result2 = app.query(
    query,
    query_text="search term", 
    text_weight=0.3,
    number_weight=0.7
)
```

### Natural Language Queries

Perform similarity searches using natural language queries instead of vector representations.

```python
query = (
    sl.Query(index)
    .find(schema)
    .similar(text_space, sl.Param("structured_query"))
    .with_natural_query(
        sl.Param("natural_language_query"),
        sl.OpenAIClientConfig(
            api_key=os.environ["OPEN_AI_API_KEY"],
            model="gpt-4o"
        )
    )
    .select_all()
)

result = app.query(
    query,
    natural_language_query="recent news about crop yield"
)
```

### Query Filters

Apply strict criteria to narrow down search results before similarity ranking.

```python
# Add filters to queries
query = (
    sl.Query(index)
    .find(schema)
    .similar(text_space, sl.Param("query_text"))
    .filter(schema.category == sl.Param("category_filter"))
    .select_all()
)
```

### Result Processing

```python
# Convert results to pandas DataFrame
df = sl.PandasConverter.to_pandas(result)

# Access result metadata
print(result.metadata)

# Iterate through results
for item in result.entries:
    print(f"ID: {item.id}, Score: {item.score}")
```

---

## Production Deployment

### Superlinked Server

The Superlinked Server is a deployable component available as a Python package on PyPI, designed to enhance the operation of Superlinked by providing a RESTful API for communicating with your application

### REST API Setup

```python
from superlinked import framework as sl

# Configure REST executor
executor = sl.RestExecutor(
    sources=[source],
    indices=[index],
    queries=[query]
)

# Run as REST API server
app = executor.run()
```

### API Endpoints

**Query Endpoint:**
```bash
curl -X POST \
  'http://localhost:8000/api/v1/search/query' \
  --header 'Accept: */*' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "query_text": "search term",
    "text_weight": 0.7,
    "number_weight": 0.3,
    "limit": 10
  }'
```

**Natural Language Query:**
```bash
curl -X POST \
  'http://localhost:8000/api/v1/search/query' \
  --header 'Accept: */*' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "natural_language_query": "recent news about crop yield"
  }'
```

### Configuration

```python
# REST configuration
rest_config = sl.RestConfiguration(
    host="0.0.0.0",
    port=8000,
    cors_enabled=True
)

executor = sl.RestExecutor(
    sources=[source],
    indices=[index],
    configuration=rest_config
)
```

---

## Vector Database Integration

Superlinked supports integration with multiple vector databases for production deployments.

### Supported Databases

1. **Redis**
2. **MongoDB Atlas**
3. **Qdrant**
4. **In-Memory** (for development)

### Redis Integration

```python
from superlinked import framework as sl

vector_database = sl.RedisVectorDatabase(
    host="localhost",
    port=6379,
    db=0,
    password="your_password"  # if required
)

executor = sl.RestExecutor(
    sources=[source],
    indices=[index],
    vector_database=vector_database
)
```

### MongoDB Atlas Integration

To integrate MongoDB with Superlinked, ensure you are using a version that supports Atlas Vector Search capabilities

```python
vector_database = sl.MongoDBVectorDatabase(
    host="<USER>:<PASSWORD>@<HOST_URL>",
    db_name="<DATABASE_NAME>",
    cluster_name="<CLUSTER_NAME>",
    project_id="<PROJECT_ID>",
    admin_api_user="<API_USER>",
    admin_api_password="<API_PASSWORD>",
    default_query_limit=10
)
```

**MongoDB Setup Requirements:**
- MongoDB separates functionality by database instance sizes. If you use anything below M10, the database does not support creating, listing, and deleting the Atlas Search Index via a standard user
- An API key with the Project Data Access Admin role is required

### Qdrant Integration

To use Superlinked with Qdrant, start a managed instance provided by Qdrant (a free-tier is available)

```python
vector_database = sl.QdrantVectorDatabase(
    "<your_qdrant_url>",  # Qdrant URL with port
    "<your_api_key>",     # API key for authentication
    # Additional configuration parameters
)
```

---

## Examples and Use Cases

### 1. E-commerce Product Search

A query like "comfortable running shoes for marathon training under $150" involves text, numerical data (price), and categorical information (product type, use case)

```python
@sl.schema
class Product(sl.Schema):
    id: sl.IdField
    name: sl.String
    description: sl.String
    price: sl.Float
    category: sl.String
    rating: sl.Float

product = Product()

# Define spaces
description_space = sl.TextSimilaritySpace(
    text=product.description,
    model="all-MiniLM-L6-v2"
)

price_space = sl.NumberSpace(
    number=product.price,
    min_value=0,
    max_value=1000,
    mode=sl.Mode.MINIMUM  # Prefer lower prices
)

category_space = sl.CategoricalSimilaritySpace(
    category_input=product.category,
    categories=["shoes", "clothing", "accessories"]
)

rating_space = sl.NumberSpace(
    number=product.rating,
    min_value=1,
    max_value=5,
    mode=sl.Mode.MAXIMUM  # Prefer higher ratings
)

# Create index and query
index = sl.Index([description_space, price_space, category_space, rating_space])

query = (
    sl.Query(
        index,
        weights={
            description_space: sl.Param("desc_weight"),
            price_space: sl.Param("price_weight"),
            category_space: sl.Param("category_weight"),
            rating_space: sl.Param("rating_weight"),
        }
    )
    .find(product)
    .similar(description_space, sl.Param("search_query"))
    .select_all()
    .limit(10)
)
```

### 2. News Search with Recency

Imagine you are building a system that can deal with a query like "recent news about crop yield"

```python
@sl.schema
class News(sl.Schema):
    id: sl.IdField
    created_at: sl.Timestamp
    like_count: sl.Integer
    moderation_score: sl.Float
    content: sl.String

news = News()

# Define spaces for multi-modal search
recency_space = sl.RecencySpace(timestamp=news.created_at)
popularity_space = sl.NumberSpace(
    number=news.like_count, 
    mode=sl.Mode.MAXIMUM
)
trust_space = sl.NumberSpace(
    number=news.moderation_score, 
    mode=sl.Mode.MAXIMUM
)
semantic_space = sl.TextSimilaritySpace(
    text=news.content,
    model="sentence-transformers/all-mpnet-base-v2"
)

index = sl.Index([recency_space, popularity_space, trust_space, semantic_space])

query = (
    sl.Query(
        index,
        weights={
            semantic_space: sl.Param("semantic_weight"),
            recency_space: sl.Param("recency_weight"),
            popularity_space: sl.Param("popularity_weight"),
            trust_space: sl.Param("trust_weight"),
        }
    )
    .find(news)
    .similar(semantic_space, sl.Param("content_query"))
    .select_all()
    .limit(sl.Param("limit"))
)
```

### 3. Multi-Modal Image and Text Search

This use-case notebook shows semantic search in fashion images for e-commerce. Users predominantly use text to describe what they would like and that poses a problem e-commerce websites face: products generally lack extensive textual information

```python
@sl.schema
class Product(sl.Schema):
    id: sl.IdField
    name: sl.String
    description: sl.String
    image_url: sl.String
    category: sl.String
    price: sl.Float

product = Product()

# Multi-modal spaces
text_space = sl.TextSimilaritySpace(
    text=product.description,
    model="sentence-transformers/all-mpnet-base-v2"
)

image_space = sl.ImageSpace(
    image=product.image_url,
    model="open-clip"
)

category_space = sl.CategoricalSimilaritySpace(
    category_input=product.category,
    categories=["fashion", "accessories", "shoes"]
)

# Combined multi-modal index
index = sl.Index([text_space, image_space, category_space])

# Query can search across text and image simultaneously
query = (
    sl.Query(
        index,
        weights={
            text_space: sl.Param("text_weight"),
            image_space: sl.Param("image_weight"),
            category_space: sl.Param("category_weight"),
        }
    )
    .find(product)
    .similar(text_space.text, sl.Param("query_text"))
    .select_all()
)
```

### 4. Recommendation System

```python
@sl.schema
class User(sl.Schema):
    id: sl.IdField
    interests: sl.String
    location: sl.String

@sl.schema  
class Item(sl.Schema):
    id: sl.IdField
    description: sl.String
    category: sl.String
    popularity: sl.Integer

@sl.event_schema
class Interaction(sl.EventSchema):
    id: sl.IdField
    user: sl.SchemaReference[User]
    item: sl.SchemaReference[Item]
    interaction_type: sl.String
    timestamp: sl.Timestamp

# Recommendation spaces
user_interest_space = sl.TextSimilaritySpace(
    text=user.interests,
    model="sentence-transformers/all-mpnet-base-v2"
)

item_desc_space = sl.TextSimilaritySpace(
    text=item.description,
    model="sentence-transformers/all-mpnet-base-v2"
)

popularity_space = sl.NumberSpace(
    number=item.popularity,
    min_value=0,
    max_value=10000,
    mode=sl.Mode.MAXIMUM
)

# Cross-modal space for user-item interactions
interaction_space = sl.TextSimilaritySpace(
    text=[user.interests, item.description],
    model="sentence-transformers/all-mpnet-base-v2"
)
```

---

## API Reference

### Core Classes

#### Schema

```python
@sl.schema
class MySchema(sl.Schema):
    id: sl.IdField
    field1: sl.String
    field2: sl.Integer
    # ... other fields
```

**Field Types:**
- `sl.IdField`: Primary key field
- `sl.String`: Text field
- `sl.Integer`: Integer field  
- `sl.Float`: Float field
- `sl.Timestamp`: Timestamp field
- `sl.SchemaReference[T]`: Reference to another schema

#### Spaces

**TextSimilaritySpace:**
```python
sl.TextSimilaritySpace(
    text: Union[Field, List[Field]],
    model: str = "sentence-transformers/all-mpnet-base-v2"
)
```

**NumberSpace:**
```python
sl.NumberSpace(
    number: Field,
    min_value: float,
    max_value: float,
    mode: sl.Mode = sl.Mode.MAXIMUM
)
```

**CategoricalSimilaritySpace:**
```python
sl.CategoricalSimilaritySpace(
    category_input: Field,
    categories: List[str]
)
```

**RecencySpace:**
```python
sl.RecencySpace(
    timestamp: Field
)
```

**ImageSpace:**
```python
sl.ImageSpace(
    image: Field,
    model: str = "open-clip"
)
```

#### Index

```python
sl.Index(
    spaces: Union[Space, List[Space]],
    fields: Optional[List[Field]] = None
)
```

#### Query

```python
sl.Query(
    index: Index,
    weights: Optional[Dict[Space, Param]] = None
)
```

**Query Methods:**
- `.find(schema: Schema) -> Query`
- `.similar(space: Space, param: Param) -> Query`
- `.select_all() -> Query`
- `.limit(limit: Union[int, Param]) -> Query`
- `.with_vector(vector: List[float]) -> Query`
- `.with_natural_query(param: Param, config: OpenAIClientConfig) -> Query`
- `.filter(condition) -> Query`

#### Parameters

```python
sl.Param(
    name: str,
    description: Optional[str] = None
)
```

#### Sources

```python
sl.InMemorySource(schema: Schema)
```

#### Executors

```python
sl.InMemoryExecutor(
    sources: List[Source],
    indices: List[Index],
    queries: Optional[List[Query]] = None
)

sl.RestExecutor(
    sources: List[Source], 
    indices: List[Index],
    queries: Optional[List[Query]] = None,
    vector_database: Optional[VectorDatabase] = None,
    configuration: Optional[RestConfiguration] = None
)
```

#### Vector Databases

```python
sl.RedisVectorDatabase(
    host: str,
    port: int = 6379,
    db: int = 0,
    password: Optional[str] = None
)

sl.QdrantVectorDatabase(
    url: str,
    api_key: str,
    **kwargs
)

sl.MongoDBVectorDatabase(
    host: str,
    db_name: str,
    cluster_name: str,
    project_id: str,
    admin_api_user: str,
    admin_api_password: str,
    default_query_limit: int = 10
)
```

### Configuration Classes

#### OpenAIClientConfig

```python
sl.OpenAIClientConfig(
    api_key: str,
    model: str = "gpt-4o"
)
```

#### RestConfiguration

```python
sl.RestConfiguration(
    host: str = "localhost",
    port: int = 8000,
    cors_enabled: bool = False
)
```

### Utility Classes

#### PandasConverter

```python
sl.PandasConverter.to_pandas(result) -> pd.DataFrame
```

### Enums

#### Mode

```python
sl.Mode.MAXIMUM  # Optimize for higher values
sl.Mode.MINIMUM  # Optimize for lower values
```

---

## Troubleshooting

### Common Issues

#### Installation Problems

**Python Version Issues:**
- Ensure Python version is between 3.10 and 3.12
- Use `pyenv` to manage Python versions if needed

**Dependency Conflicts:**
- Use virtual environments to isolate dependencies
- Update pip before installation: `python -m pip install --upgrade pip`

#### Model Download Issues

- First run will take slightly longer as it has to download the embedding model
- Ensure stable internet connection
- Check disk space for model storage

#### Memory Issues

**Large Dataset Handling:**
- Use appropriate vector databases instead of in-memory storage
- Implement batching for large data ingestion
- Consider using REST executor for production workloads

#### Vector Database Connection Issues

**MongoDB Atlas:**
- If you use anything below M10, the database does not support creating, listing, and deleting the Atlas Search Index via a standard user
- Ensure API key has `Project Data Access Admin` role
- Verify cluster name and project ID are correct

**Qdrant:**
- Verify Qdrant instance is accessible
- Check API key permissions
- Ensure correct URL format with port

**Redis:**
- Verify Redis server is running
- Check connection parameters (host, port, password)
- Ensure Redis version supports vector operations

### Performance Optimization

#### Query Performance

1. **Index Optimization:**
   - Group related spaces in the same index
   - Use appropriate field selections
   - Consider index size vs. query complexity trade-offs

2. **Parameter Tuning:**
   - Experiment with different space weights
   - Optimize min/max values for number spaces
   - Use appropriate embedding models for your use case

3. **Batch Processing:**
   - Use batch ingestion for large datasets
   - Implement incremental updates when possible

#### Memory Optimization

1. **Model Selection:**
   - Choose smaller embedding models when appropriate
   - Consider model size vs. accuracy trade-offs

2. **Data Management:**
   - Implement data pagination for large result sets
   - Use vector databases for persistent storage

### Debugging

#### Enable Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Query Debugging

```python
# Examine query metadata
result = app.query(query, **params)
print("Query metadata:", result.metadata)

# Check parameter extraction for natural language queries
if hasattr(result, 'extracted_params'):
    print("Extracted parameters:", result.extracted_params)
```

#### Performance Monitoring

```python
import time

start_time = time.time()
result = app.query(query, **params)
query_time = time.time() - start_time

print(f"Query took {query_time:.2f} seconds")
print(f"Returned {len(result.entries)} results")
```

### Getting Help

- **Documentation**: Visit [docs.superlinked.com](https://docs.superlinked.com)
- **GitHub Issues**: Report bugs and feature requests
- **Community**: Join discussions and get support
- **Examples**: Check out the [recipe collection](https://docs.superlinked.com/recipes/overview) for real-world applications

---

## Advanced Topics

### Event Schema and Time-Based Effects

Model and apply the impact of events on vector representations over time.

```python
@sl.event_schema
class UserItemInteraction(sl.EventSchema):
    id: sl.IdField
    user: sl.SchemaReference[User]
    item: sl.SchemaReference[Item]
    interaction_type: sl.String
    timestamp: sl.Timestamp
    rating: sl.Float

# Use events to build dynamic user preferences
interaction_effect = sl.EventAggregationEffect(
    event_schema=UserItemInteraction,
    affected_schema=User,
    aggregation_field=UserItemInteraction.rating,
    time_decay=sl.TimeDecay(half_life_days=30)
)
```

### Custom Embedding Models

```python
# Using custom sentence transformers model
custom_text_space = sl.TextSimilaritySpace(
    text=schema.text_field,
    model="your-org/custom-model-name"
)

# Using OpenAI embeddings
openai_text_space = sl.TextSimilaritySpace(
    text=schema.text_field,
    model="text-embedding-ada-002",
    model_config=sl.OpenAIModelConfig(
        api_key=os.environ["OPENAI_API_KEY"]
    )
)
```

### Advanced Query Patterns

#### Multi-Step Queries

```python
# First query to find relevant categories
category_query = (
    sl.Query(category_index)
    .find(category_schema)
    .similar(category_space, sl.Param("user_query"))
    .limit(5)
)

category_results = app.query(category_query, user_query="electronics")

# Use results to refine main query
main_query = (
    sl.Query(
        product_index,
        weights={
            text_space: 0.6,
            category_space: 0.4
        }
    )
    .find(product_schema)
    .similar(text_space, sl.Param("search_text"))
    .filter(product_schema.category.in_([r.category for r in category_results]))
    .select_all()
)
```

#### Personalized Queries

```python
# Build user profile from interaction history
user_profile_space = sl.TextSimilaritySpace(
    text=[user.interests, interaction.item_description],
    model="sentence-transformers/all-mpnet-base-v2"
)

personalized_query = (
    sl.Query(
        recommendation_index,
        weights={
            content_space: sl.Param("content_weight"),
            user_profile_space: sl.Param("personalization_weight"),
            popularity_space: sl.Param("popularity_weight")
        }
    )
    .find(item_schema)
    .similar(content_space, sl.Param("search_query"))
    .similar(user_profile_space, user_vector)
    .select_all()
    .limit(20)
)
```

