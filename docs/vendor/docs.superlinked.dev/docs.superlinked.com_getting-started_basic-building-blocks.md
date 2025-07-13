---
url: "https://docs.superlinked.com/getting-started/basic-building-blocks"
title: "Basic Building Blocks | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/getting-started/basic-building-blocks\#intro)    Intro

Superlinked's framework is built on key components: [@schema](https://docs.superlinked.com/reference/components/schema/schema), [Source](https://docs.superlinked.com/reference/components/index-2), [Spaces](https://docs.superlinked.com/reference/components/index-4), [Index](https://docs.superlinked.com/reference/components/index-7), [Query](https://docs.superlinked.com/reference/components/index-5), and [Executor](https://docs.superlinked.com/reference/components/index-1). These building blocks allow you to create a modular system tailored to your specific use cases.

You begin by defining your desired endpoints - how you want your embeddings to represent your data. This guides your system setup, allowing you to **customize your modules before running queries**. You can adjust query weights for different scenarios, such as a user's interests or recent items.

This modular approach **separates query description from execution**, enabling you to run the same query across different environments without reimplementation. You build your Query using descriptive elements like @schema, Source, Spaces, Index, or Event, which can be **reused with different Executors**.

Superlinked's focus on connectors facilitates easy transitions between deployments, from in-memory to batch or real-time data pipelines. This flexibility allows for rapid experimentation in embedding and retrieval while maximizing control over index creation.

Let's explore these building blocks in more detail.

**Follow along in this Colab.**

[![Logo](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2Fssl.gstatic.com%2Fcolaboratory-static%2Fcommon%2F817b2046193605d71a233a8db91ae991%2Fimg%2Ffavicon.ico&width=20&dpr=4&quality=100&sign=de642489&sv=2)Google Colab](https://colab.research.google.com/github/superlinked/superlinked/blob/main/notebook/feature/basic_building_blocks.ipynb)

## [Direct link to heading](https://docs.superlinked.com/getting-started/basic-building-blocks\#turning-classes-into-schemas)    Turning classes into Schemas

Once you’ve parsed data into your notebook via JSON or a pandas dataframe, it’s time to create a Schema describing your data.

To do this, you **use the Schema decorator to annotate your class as a schema** representing your structured data. Schemas translate to searchable entities in the embedding space. To get started, type @schema, and then define the field types to match the different types of data you’ve imported.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
class ParagraphSchema(sl.Schema):
    body: sl.String
    id: sl.IdField
```

With your Schemas created, you are ready to move on to embedding and querying, which is where Superlinked’s building blocks approach really empowers you. The Superlinked framework is based on the intuition that people doing semantic search can better satisfy the requirements of their use case/s if they can customize how their system handles data and queries.

## [Direct link to heading](https://docs.superlinked.com/getting-started/basic-building-blocks\#declaring-how-to-embed-your-data-using-spaces)    Declaring how to embed your data using Spaces

**Spaces** is a declarative class developed with this in mind. The Space module encapsulates the vector creation logic that will be used at ingestion time, and again at query time.

Spaces lets you tailor how you embed different attributes of your data and can be categorized along 2 key dimensions:

1. what input types the Space permits - e.g., text, timestamp, numeric, categorical

2. whether the Space represents similarity (e.g, TextSimilaritySpace) or scale (e.g., numeric space)


Which Space/s fit your use case depends on both these dimensions - your input type and what you need to represent about your data. You can find a list of spaces in Superlinked [here](https://docs.superlinked.com/reference/components/index-4).

You use different Spaces for different data types. For example, [TextSimilaritySpace](https://docs.superlinked.com/reference/components/index-4/text_similarity_space) and [CategoricalSimilaritySpace](https://docs.superlinked.com/reference/components/index-4/categorical_similarity_space) can take String as an input, [RecencySpace](https://docs.superlinked.com/reference/components/index-4/recency_space) can take Timestamp, [NumberSpace](https://docs.superlinked.com/reference/components/index-4/number_space) can take Int/Float, and so on. Each Space captures a different, relevant piece of information (e.g., title, review count, etc.) about an entity. This lets you weight each Space according to which attributes are relevant to your use case - before you concatenate all your Spaces into a single multimodal vector among others in the queryable vector space.

By prioritizing the creation of smarter vectors up front - and only then creating the index - we can achieve better quality retrieval, without costly and time-consuming reranking and general post-processing work.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
relevance_space = sl.TextSimilaritySpace(text=paragraph.body, model="Snowflake/snowflake-arctic-embed-s")
```

## [Direct link to heading](https://docs.superlinked.com/getting-started/basic-building-blocks\#indexing)    Indexing

Superlinked’s Index module components enable you to group Spaces into indices that make your queries more efficient.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
paragraph_index = sl.Index(relevance_space)
```

## [Direct link to heading](https://docs.superlinked.com/getting-started/basic-building-blocks\#executing-your-query-to-your-chosen-endpoints)    Executing your query to your chosen endpoints

Before running your code, you need to structure your query using the following arguments:

- `Query`: defines the index you want it to search, and you can add Params here (details in our [notebook](https://github.com/superlinked/superlinked/blob/main/notebook/feature/dynamic_parameters.ipynb))

- `.find`: tells it what to look for

- `.similar`: tells it how to identify relevant results (details in [notebook](https://github.com/superlinked/superlinked/blob/main/notebook/feature/basic_building_blocks.ipynb))

- `.select_all`: returns all the stored fields, without this clause, it will only return the id(s) (details in [notebook](https://github.com/superlinked/superlinked/blob/main/notebook/feature/query_result.ipynb))


Note that you can wait to fill out the specific Params until later. (You can also add a `.with_vector` to search with an embedded vector of a specific element of your data (see details in [notebook](https://github.com/superlinked/superlinked/blob/main/notebook/feature/query_by_object.ipynb))).

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
query = (
    sl.Query(paragraph_index)
    .find(paragraph)
    .similar(relevance_space.text, Param("query_text"))
    .select_all()
)
```

Once you’ve defined your schema and built out the structure of your Index and Query, it’s time to connect everything.

Use **Source** to connect your data to the schema.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
source: sl.InMemorySource = sl.InMemorySource(paragraph)
```

Now that you’ve connected data with schema, you use the **Executor** to prepare your code to run. The Executor connects the source data with the index, which describes how each part of the data should be treated within Spaces.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
executor = sl.InMemoryExecutor(sources=[source], indices=[paragraph_index])
app = executor.run()
```

## [Direct link to heading](https://docs.superlinked.com/getting-started/basic-building-blocks\#experimenting-with-some-sample-data)    Experimenting with some sample data

Now we can insert some sample data...

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
source.put([{"id": "happy_dog", "body": "That is a happy dog"}])
source.put([{"id": "happy_person", "body": "That is a very happy person"}])
source.put([{"id": "sunny_day", "body": "Today is a sunny day"}])
```

...and query it to see what it produces.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
result = app.query(query, query_text="This is a happy person")
sl.PandasConverter.to_pandas(result)
```

Here's our result.

body

id

0

That is a very happy person

happy\_person

1

That is a happy dog

happy\_dog

2

Today is a sunny day

sunny\_day

Changing the query text further demonstrates how our system produces results that are relevant to each query.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
result = app.query(query, query_text="This is a happy dog")
sl.PandasConverter.to_pandas(result)
```

body

id

0

That is a happy dog

happy\_dog

1

That is a very happy person

happy\_person

2

Today is a sunny day

sunny\_day

## [Direct link to heading](https://docs.superlinked.com/getting-started/basic-building-blocks\#in-sum)    In sum

In sum, the Superlinked framework empowers you to create and tailor a modular system that fits your use case/s, repurposable for different deployments, saving you from resource- and time-consuming reimplementation, reranking, and postprocessing.

Now for the fun part - try it out yourself! The notebook is [here](https://github.com/superlinked/superlinked/blob/main/notebook/feature/basic_building_blocks.ipynb). Experiment with your own sample data and query inputs, and give us a star!

[PreviousSetup Superlinked](https://docs.superlinked.com/getting-started/installation) [NextOverview](https://docs.superlinked.com/run-in-production/overview)

Last updated 1 month ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject