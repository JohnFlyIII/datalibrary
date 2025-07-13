---
url: "https://docs.superlinked.com/getting-started/installation"
title: "Setup Superlinked | Superlinked Docs"
---

### [Direct link to heading](https://docs.superlinked.com/getting-started/installation\#in-a-notebook)    In a notebook

Install the superlinked library:

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
%pip install superlinked
```

### [Direct link to heading](https://docs.superlinked.com/getting-started/installation\#as-a-script)    As a script

Ensure your python version is at least `3.10.x` but not newer than `3.12.x`.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
$> python -V
Python 3.10.9
```

If your python version is not `>=3.10` and `<=3.12` you might use [pyenv](https://github.com/pyenv/pyenv) to install it.

Upgrade pip and install the superlinked library.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
$> python -m pip install --upgrade pip
$> python -m pip install superlinked
```

### [Direct link to heading](https://docs.superlinked.com/getting-started/installation\#run-the-example)    Run the example

First run will take slightly longer as it has to download the embedding model.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
import json
import os

from superlinked import framework as sl

class Product(sl.Schema):
    id: sl.IdField
    description: sl.String
    rating: sl.Integer

product = Product()

description_space = sl.TextSimilaritySpace(
    text=product.description, model="Alibaba-NLP/gte-large-en-v1.5"
)
rating_space = sl.NumberSpace(
    number=product.rating, min_value=1, max_value=5, mode=sl.Mode.MAXIMUM
)
index = sl.Index([description_space, rating_space], fields=[product.rating])

# Define your query and parameters to set them directly at query-time
# or let an LLM fill them in for you using the `natural_language_query` param.
# Don't forget to set your OpenAI API key to unlock this feature.
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

# Run the app in-memory (server & Apache Spark executors available too!).
source = sl.InMemorySource(product)
executor = sl.InMemoryExecutor(sources=[source], indices=[index])
app = executor.run()

# Ingest data into the system - index updates and other processing happens automatically.
source.put([\
    {\
        "id": 1,\
        "description": "Budget toothbrush in black color. Just what you need.",\
        "rating": 1,\
    },\
    {\
        "id": 2,\
        "description": "High-end toothbrush created with no compromises.",\
        "rating": 5,\
    },\
    {\
        "id": 3,\
        "description": "A toothbrush created for the smart 21st century man.",\
        "rating": 3,\
    },\
])

result = app.query(query, natural_query="best toothbrushes", limit=1)

# Examine the extracted parameters from your query
print(json.dumps(result.metadata, indent=2))

# The result is the 5-star rated product.
sl.PandasConverter.to_pandas(result)
```

[PreviousWhy Superlinked?](https://docs.superlinked.com/getting-started/why-superlinked) [NextBasic Building Blocks](https://docs.superlinked.com/getting-started/basic-building-blocks)

Last updated 4 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject