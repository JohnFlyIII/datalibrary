---
url: "https://docs.superlinked.com/concepts/overview"
title: "Overview | Superlinked Docs"
---

1. Describe your data using Python classes with the [@schema](https://docs.superlinked.com/reference/components/schema/schema) decorator.

2. Describe your vector embeddings from building blocks with [Spaces](https://docs.superlinked.com/reference/components/index-4).

3. Combine your embeddings into a queryable [Index](https://docs.superlinked.com/reference/components/index-7).

4. Define your search with dynamic parameters and weights as a [Query](https://docs.superlinked.com/reference/components/index-5/query).

5. Load your data using a [Source](https://docs.superlinked.com/reference/components/index-2).

6. Define your transformations with a [Parser](https://docs.superlinked.com/reference/components/parser) (e.g.: from [`pd.DataFrame`](https://docs.superlinked.com/reference/components/parser/dataframe_parser)).

7. Run your configuration with an [Executor](https://docs.superlinked.com/reference/components/index-1/index/in_memory_executor).


## [Direct link to heading](https://docs.superlinked.com/concepts/overview\#colab-notebooks-explaining-the-concepts)    Colab notebooks explaining the concepts

![Cover](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-c3143e31a51b14f0c21d9fea2799e7f6f006589f%252Faccess-vector-parts.png%3Falt%3Dmedia&width=245&dpr=4&quality=100&sign=ab6beb7&sv=2)

**Accessing stored vector parts**

Use query interface to return vector-parts based on our needs

![Cover](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-731085501e10dd1be6f59e1d59cdf257d0b9311f%252FCategorical%2520Embeddings.png%3Falt%3Dmedia&width=245&dpr=4&quality=100&sign=e5da8b29&sv=2)

**Categorical Embeddings**

Efficiently represent and compare categorical data in vector space for similarity searches.

![Cover](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-dc019e722b3babeb1ba310bb2ceb341fd8b7f051%252FCombine%2520Multiple%2520Embeddings.png%3Falt%3Dmedia&width=245&dpr=4&quality=100&sign=2a69d249&sv=2)

**Combine Multiple Embeddings**

Merge different types of embeddings to create a unified representation for complex objects.

![Cover](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-9d9bc72611aa27bdab82b57d924142d67a96a596%252FCustom%2520Spaces.png%3Falt%3Dmedia&width=245&dpr=4&quality=100&sign=8f60c252&sv=2)

**Custom Spaces**

Create and manage custom vector spaces for specialized similarity searches.

![Cover](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-a4f87468ff456834d5e2ee8cc3207822c1f9e67f%252FDynamic%2520Parameters.png%3Falt%3Dmedia&width=245&dpr=4&quality=100&sign=543bb4e8&sv=2)

**Dynamic Parameters**

Adjust query parameters dynamically to fine-tune search results.

![Cover](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-8d3da9a56e561332974f54f63346d3c41d3db10f%252FEvent%2520Effects.png%3Falt%3Dmedia&width=245&dpr=4&quality=100&sign=e7728f38&sv=2)

**Event Effects**

Model and apply the impact of events on vector representations over time.

![Cover](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-f24e11cbc56353b3be7b351a25ce3602fb0be433%252FHard%2520Filtering.png%3Falt%3Dmedia&width=245&dpr=4&quality=100&sign=77761d6c&sv=2)

**Hard Filtering**

Apply strict criteria to narrow down search results before similarity ranking.

![Cover](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-cda625f79a7323d3d2297e54741b50bdef636157%252FImage%2520Embedding.png%3Falt%3Dmedia&width=245&dpr=4&quality=100&sign=99b7396&sv=2)

**Image Embedding**

Embed text or images into a multi-modal vector space.

![Cover](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-33211f629371a85f544ad815acb5a39d8f5086c3%252FNatural%2520Language%2520Querying.png%3Falt%3Dmedia&width=245&dpr=4&quality=100&sign=6801d665&sv=2)

**Natural Language Querying**

Perform similarity searches using natural language queries instead of vector representations.

![Cover](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-abaaa2a0ea1581c8d8e7b9806cd88dfb351712aa%252FNumber%2520Embedding%2520Minmax.png%3Falt%3Dmedia&width=245&dpr=4&quality=100&sign=6765dff&sv=2)

**Number Embedding Minmax**

Embed numerical values within a specified range for effective similarity comparisons.

![Cover](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-44dc241b7869af06532b1cd8b027049df4b05d4d%252FNumber%2520Embedding%2520Similar.png%3Falt%3Dmedia&width=245&dpr=4&quality=100&sign=99458a68&sv=2)

**Number Embedding Similar**

Embed numbers to find similar values based on relative closeness rather than exact matches.

![Cover](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-340fc2e0553cb63e618cb5a457d0916db828a67c%252Foptional-schema-fields.png%3Falt%3Dmedia&width=245&dpr=4&quality=100&sign=21ed1a9&sv=2)

**Optional Schema Fields**

Define optional fields in your schema.

![Cover](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-d3f4f7ac6634c290c5e7adbc02bbe0fcdb2ead43%252Fquery-result.png%3Falt%3Dmedia&width=245&dpr=4&quality=100&sign=9df60bc7&sv=2)

**Query Result**

Customize the result object for your queries.

![Cover](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-879b12a947fe6f1cf9dc14cf4f64fe9a77299650%252FQuery%2520Time%2520Weights.png%3Falt%3Dmedia&width=245&dpr=4&quality=100&sign=82cd15ae&sv=2)

**Query Time Weights**

Adjust the importance of different embedding components during query execution.

![Cover](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-2fbe157dad3a932a96010eaeca8190fe398a9f41%252FQuerying%2520Options.png%3Falt%3Dmedia&width=245&dpr=4&quality=100&sign=b5fd5099&sv=2)

**Querying Options**

Customize search behavior with various querying options for refined results.

![Cover](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-b8866db5c217538f0f1922e7b1568f81bea76931%252FRecency%2520Embedding.png%3Falt%3Dmedia&width=245&dpr=4&quality=100&sign=7aae2d05&sv=2)

**Recency Embedding**

Incorporate time-based relevance into vector representations for up-to-date search results.

![Cover](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-626c1451dc027cabfb7a66b18c3dcede69eda576%252FText%2520Embedding.png%3Falt%3Dmedia&width=245&dpr=4&quality=100&sign=6a512ced&sv=2)

**Text Embedding**

Convert text data into vector representations for semantic similarity searches.

![Cover](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2F1191462896-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxPeYN5u4abP5ihDZHRrM%252Fuploads%252Fgit-blob-7d1a4dafd9b0d02197156fc004d2e6a544a30404%252FVector%2520Sampling.png%3Falt%3Dmedia&width=245&dpr=4&quality=100&sign=2179c314&sv=2)

**Vector Sampler**

Generate diverse vector samples to explore and understand the embedding space.

[PreviousQdrant](https://docs.superlinked.com/run-in-production/index-1/qdrant) [NextCombining Multiple Embeddings for Better Retrieval Outcomes](https://docs.superlinked.com/concepts/multiple-embeddings)

Last updated 1 month ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject