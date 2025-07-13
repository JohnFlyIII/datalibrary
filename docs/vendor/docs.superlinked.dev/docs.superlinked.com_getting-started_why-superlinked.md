---
url: "https://docs.superlinked.com/getting-started/why-superlinked"
title: "Why Superlinked? | Superlinked Docs"
---

![Page cover image](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-743a202f75fa561ee870a1b482d7bf3be6df0d53%252Fwhy-superlinked-cover.png%3Falt%3Dmedia&width=1248&dpr=4&quality=100&sign=631e78da&sv=2)

**Table of Contents**

- [Why Superlinked?](https://docs.superlinked.com/getting-started/why-superlinked#why-superlinked)



- [Your users expect better search](https://docs.superlinked.com/getting-started/why-superlinked#your-users-expect-better-search)

- [Enter Superlinked](https://docs.superlinked.com/getting-started/why-superlinked#enter-superlinked)

- [But can't I put all my data in json, stringify it and embed using LLM?](https://docs.superlinked.com/getting-started/why-superlinked#but-cant-i-put-all-my-data-in-json-stringify-it-and-embed-using-llm)

- [Okay, But can't I ...](https://docs.superlinked.com/getting-started/why-superlinked#okay-but-cant-i--)



- [1\. Use different already existing storages per attribute, fire multiple searches and then reconcile results?](https://docs.superlinked.com/getting-started/why-superlinked#1-use-different-already-existing-storages-per-attribute-fire-multiple-searches-and-then-reconcile-results)

- [2\. Use Metadata filters or Candidate re-ranking](https://docs.superlinked.com/getting-started/why-superlinked#2-use-metadata-filters-or-candidate-re-ranking)


- [Okay, seems like Superlinked proposes a nice approach, but](https://docs.superlinked.com/getting-started/why-superlinked#okay-seems-like-superlinked-proposes-a-nice-approach-but)

- [How does it fit in the big picture?](https://docs.superlinked.com/getting-started/why-superlinked#how-does-it-fit-in-the-big-picture)


### [Direct link to heading](https://docs.superlinked.com/getting-started/why-superlinked\#your-users-expect-better-search)    Your users expect better search

The landscape of search and information retrieval is rapidly evolving. With the rise of AI and large language models, user expectations for search capabilities have skyrocketed. Your users now expect that your search can handle complex, nuanced queries that go beyond simple keyword matching. Just hear what Algolia CTO has to say -

> "We saw 2x more keywords search 6 months after the ChatGPT launch." _Algolia CTO, 2023_

They have 17,000 customers accounting for 120B searches/month. This trend isn't isolated. Across industries, we're seeing a shift towards more sophisticated search queries that blend multiple concepts, contexts, and data types.

Vector Search with text-only embeddings (& also multi-modal) fails on complex queries, because complex queries are never just about text. They involve other data too!

Consider these examples:

1. **E-commerce**: A query like "comfortable running shoes for marathon training under $150" involves text, numerical data (price), and categorical information (product type, use case).

2. **Content platforms**: "Popular science fiction movies from the 80s with strong female leads" combines text analysis, temporal data, and popularity metrics.

3. **Job search**: "Entry-level data science positions in tech startups with good work-life balance" requires understanding of text, categorical data (industry, job level), and even subjective metrics.


![](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-f0d6f81bbf00059411a1dd1b1e8bf60ecf65cfdc%252Fwhy-superlinked-image1.png%3Falt%3Dmedia&width=768&dpr=4&quality=100&sign=b314b88e&sv=2)

Example of queries needing other data than text

### [Direct link to heading](https://docs.superlinked.com/getting-started/why-superlinked\#enter-superlinked)    Enter Superlinked

This is where Superlinked comes in, offering a powerful, flexible framework designed to handle the complexities of modern search and information retrieval challenges. Superlinked is a vector embedding solution for AI teams working with complicated data within their [RAG](https://docs.superlinked.com/tutorials/rag-hr), [Search](https://docs.superlinked.com/tutorials/semantic-search-news), [Recommendations](https://docs.superlinked.com/tutorials/recsys-ecomm) and [Analytics](https://docs.superlinked.com/tutorials/analytics-keyword-expansion) stack.

Let's quickly go through an example. Keep in mind that there are a ton of new concepts thrown at you, but this is just to illustrate how Superlinked 'looks'. We'll go over each concept in detail in the [following sections](https://docs.superlinked.com/getting-started/basic-building-blocks).

Imagine you are building a system that can deal with a query like `“recent news about crop yield”`. After collecting your data, you define your schema, ingest data and build index like this:

**Schema definition**

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap

class News(sl.Schema):
    id: sl.IdField
    created_at: sl.Timestamp
    like_count: sl.Integer
    moderation_score: sl.Float
    content: sl.String

class User(sl.Schema):
    id: sl.IdField
    interest: sl.String

class Event(sl.EventSchema):
    id: sl.IdField
    news: sl.SchemaReference[News]
    user: sl.SchemaReference[User]
    event_type: sl.String

```

**Encoder definition**

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap

recency_space = sl.RecencySpace(timestamp=news.created_at)
popularity_space = sl.NumberSpace(number=news.like_count, mode=sl.Mode.MAXIMUM)
trust_space = sl.NumberSpace(number=news.moderation_score, mode=sl.Mode.MAXIMUM)
semantic_space = sl.TextSimilarity(
    text=[news.content, user.interest], model="sentence-transformers/all-mpnet-base-v2"
)

```

**Define Indexes**

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
index = sl.Index(
    spaces=[recency_space, popularity_space, trust_space, semantic_space],
    effects=[sl.Effect(semantic_space, event.user, 0.8 * event.news)],
)

```

You define your queries and parameterize them like this:

**Query definition**

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap

query = (
    sl.Query(
        index,
        weights={
            recency_space: sl.Param("recency_weight"),
            popularity_space: sl.Param("popularity_weight"),
            trust_space: sl.Param("trust_weight"),
            semantic_space: sl.Param("semantic_weight"),
        },
    )
    .find(news)
    .similar(semantic_space.text, sl.Param("content_query"))
    .with_vector(user, sl.Param("user_id"))
    .select_all()
)

```

**Debug in notebook, run as server**

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap

sl.RestExecutor(
    sources=[sl.RestSource(news), sl.RestSource(user)],
    index=[index],
    query=[query],
    vector_database = sl.InMemoryVectorDatabase()
    # vector_database = sl.MongoDBVectorDatabase(...),
    # vector_database = sl.RedisVectorDatabase(...),
    # vector_database = sl.QdrantVectorDatabase(...),
)

# SparkExecutor()   <-- Coming soon in Superlinked Cloud

```

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap

curl -X POST \
    'http://localhost:8000/api/v1/search/query' \
    --header 'Accept: */*' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "content_query": "crop yields",
        "semantic_weight": 0.5,
        "recency_weight": 0.9,
        "popularity_weight": 0.5,
        "trust_weight": 0.2,
    }'

```

**Handle natural language queries**

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
#In a notebook like this:

query = (
    sl.Query(...)
    .with_natural_query(Param("recent news about crop yield"))
)

```

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
# As an API call like this:

curl -X POST \
    'http://localhost:8000/api/v1/search/query' \
    --header 'Accept: */*' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "natural_language_query": "recent news about crop yield"
    }'

```

Discover the powerful capabilities Superlinked offers [here](https://docs.superlinked.com/concepts/overview).

### [Direct link to heading](https://docs.superlinked.com/getting-started/why-superlinked\#but-cant-i-put-all-my-data-in-json-stringify-it-and-embed-using-llm)    But can't I put all my data in json, stringify it and embed using LLM?

Stringify and embed approach produces unpredictable results. For example (code below):

- Embed 0..100 with OpenAI API

- Calculate and plot the cosine similarity

- Observe the difference between expected and actual results


Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap

from openai import OpenAI
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

response = OpenAI().embeddings.create(
    input=[str(i) for i in range(0, 101)],
    model="text-embedding-3-small",
)
embeddings = np.array([r.embedding for r in response.data])
scores = cosine_similarity(embeddings, embeddings)

```

![](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-f85b20eaa8a1cb56f2cf8f5aba20b0d110b6180a%252Fwhy-superlinked-stringify.svg%3Falt%3Dmedia&width=768&dpr=4&quality=100&sign=e33ceb29&sv=2)

OpenAI embeddings result in noisy, non-monotonic cosine similarity scores. For example, CosSim(25, 50) equals to 0.69 when CosSim(32, 50) equals 0.42 meaning 25 is more similar to 50 than 32 which doesn't make sense. Superlinked number embeddings avoid such inconsistencies by design.

### [Direct link to heading](https://docs.superlinked.com/getting-started/why-superlinked\#okay-but-cant-i)    Okay, But can't I ...

#### [Direct link to heading](https://docs.superlinked.com/getting-started/why-superlinked\#id-1.-use-different-already-existing-storages-per-attribute-fire-multiple-searches-and-then-reconcile-r)    1\. Use different already existing storages per attribute, fire multiple searches and then reconcile results?

Our naive approach (above) - storing and searching attribute vectors separately, then combining results - is limited in ability, subtlety, and efficiency when we need to retrieve objects with multiple simultaneous attributes. Moreover, multiple kNN searches take [more time than a single search with concatenated vectors](https://redis.io/blog/benchmarking-results-for-vector-databases/).

It's better to store all your attribute vectors in the same vector store and perform a single search, weighting your attributes at query time.

Read more here: [Multi-attribute search with vector embeddings](https://superlinked.com/vectorhub/articles/multi-attribute-semantic-search)

#### [Direct link to heading](https://docs.superlinked.com/getting-started/why-superlinked\#id-2.-use-metadata-filters-or-candidate-re-ranking)    2\. Use Metadata filters or Candidate re-ranking

When you convert a fuzzy preference like “recent”, “risky” or “popular” into a filter, you model a sigmoid with a binary step function = not enough resolution.

Semantic ranking & ColBERT only use text, learn2rank models need ML Engineers. Broad queries eg “popular pants” can’t be handled by re-ranking at all, due to poor candidate recall.

![](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-11d81586a19c53676b981b55ae7b1f8ea8a977b1%252Fwhy-superlinked-filterreranking.png%3Falt%3Dmedia&width=768&dpr=4&quality=100&sign=1585e3d6&sv=2)

### [Direct link to heading](https://docs.superlinked.com/getting-started/why-superlinked\#okay-seems-like-superlinked-proposes-a-nice-approach-but)    Okay, seems like Superlinked proposes a nice approach, but

1. How can I build with it at scale? The [Superlinked Server](https://docs.superlinked.com/run-in-production/overview) is a deployable component available as a [Python package on PyPI](https://pypi.org/project/superlinked-server/), designed to enhance the operation of Superlinked by providing a RESTful API for communicating with your application. This package streamlines the integration of Superlinked's sophisticated search functionalities into existing applications by offering REST endpoints and Vector Database connectivity. It enables developers to focus on leveraging Superlinked's capabilities without the burden of infrastructure management, from initial prototype to full-scale production.


### [Direct link to heading](https://docs.superlinked.com/getting-started/why-superlinked\#how-does-it-fit-in-the-big-picture)    How does it fit in the big picture?

![](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-8786801e4dcc10a1409a9ae161e8013f8385f337%252Fsl_diagram.png%3Falt%3Dmedia&width=768&dpr=4&quality=100&sign=cf92e257&sv=2)

Superlinked framework diagram

[PreviousWelcome](https://docs.superlinked.com/) [NextSetup Superlinked](https://docs.superlinked.com/getting-started/installation)

Last updated 4 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject