---
url: "https://docs.superlinked.com/reference/changelog"
title: "Changelog | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/changelog\#id-2025-05-25)    2025-05-25

- **Framework: v23.2.0 - v25.1.0**

- **Batch: v2.22.0 - v2.29.0**

- **Server: v1.25.0 - v1.26.0**


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#breaking-changes)    Breaking Changes

- **Framework (v24.0.0)**: Fixed embedding node `node_id` generation.

- **Framework (v25.0.0)**: Introduced full text field for Redis performance improvements.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#added)    Added

- **Boolean Field Type**: Introduced boolean field type to schema for both Framework and Batch.

- **Qdrant gRPC Config**: Added gRPC configurability for Qdrant.

- **Qdrant Search Algorithm Config**: Implemented search algorithm configuration for Qdrant vector search.

- **Query Result Weight Explanation**: Extended weight mechanics and explanation in query results.

- **Batch Data Sorting**: Added sorting of parsed data by ID in Batch.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#changed)    Changed

- **Redis Query Performance**: Improved Redis query performance by using `__schema__` as a tag.

- **Modal Embedding Latency**: Enhanced Modal embeddings with a minimum latency setting.

- **Concurrent Processing Optimization**: Optimized concurrent processing for blob loading, Hugging Face embeddings, and query DAG evaluation.

- **Log Argument Naming**: Updated argument naming in framwork logs for clarity.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#fixed)    Fixed

- **Embedding Node ID Generation**: Fixed embedding node with specific `node_id` generation.

- **Vector Operation Negative Filter**: Resolved negative filter handling in vector operations.

- **Batch GPU/CPU OOM**: Addressed batch GPU/CPU Out-Of-Memory issues.

- **Batch Negative Filter Indices**: Ensured no `None` value for `negative_filter_indices` in Batch.

- **Batch Node ID Calculation**: Adjusted batch to `node_id` calculation change.

- **Raw Schema Reading (Batch)**: Corrected raw schema reading in Batch.

- **Model Loading Memory Leak (Batch)**: Prevented memory leaks in model loading in Batch.

- **Parallel Download Connection Pooling (Batch)**: Ensured proper connection pooling for parallel downloads in Batch.


## [Direct link to heading](https://docs.superlinked.com/reference/changelog\#id-2025-05-09)    2025-05-09

- **Framework: v22.16.1 - v23.2.0**

- **Batch: v2.18.1 - v2.22.0**

- **Server: v1.24.2 - v1.25.0**


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#breaking-changes-1)    Breaking Changes

- **Framework (v23.0.0)**:



- Changed default of `SUPERLINKED_CONCURRENT_BLOB_LOADING` setting to `True`.

- Introduced new setting: `SUPERLINKED_CONCURRENT_EFFECT_EVALUATION` which enables concurrent event processing (defaults to `True`).


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#added-1)    Added

- **Concurrent Event Processing**: Introduced concurrent event processing for improved throughput.

- **Image Resizing**: Enabled resizing images for more flexible input handling.

- **Configurable Redis Search**: Added support for configurable search algorithm (FLAT or HNSW) for Redis.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#changed-1)    Changed

- **Modal Performance**: Improved modal performance.

- **Silver Dataset Efficiency**: Optimized silver dataset updates by using deltas instead of full recreation, improving efficiency.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#fixed-1)    Fixed

- **HuggingFace Error Handling**: Improved error handling by catching `HfHubHTTPError` when interfacing with HuggingFace.

- **Batch Metadata Storage**: Reworked metadata handling to enable storing (partial) node results in batch.


## [Direct link to heading](https://docs.superlinked.com/reference/changelog\#id-2025-04-25)    2025-04-25

- **Framework: v22.13.0 - v22.16.1**

- **Batch: v2.16.2 - v2.18.1**

- **Server: v1.23.0 - v1.24.2**


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#added-2)    Added

- **DescribedBlob Shorthand**: `DescribedBlob` can now be imported using `sl.DescribedBlob`.

- **Infinity Image Embedding**: Added support for image embedding with Infinity models.

- **Modal Handler**: Introduced modal handler capabilities.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#changed-2)    Changed

- **Result Loading Performance**: Optimized query result loading to happen only once per query.

- **Text Embedding Performance**: Optimized text embedding to process each unique text value only once.

- **Batch Job Timestamp Performance**: Improved `created_at` timestamp generation in batch jobs by using Spark metadata instead of file scanning.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#fixed-2)    Fixed

- **OnlineAggregationNode Traversal**: Improved parent traversal logic for `OnlineAggregationNode`.

- **Dataframe Nullable Support**: Added support for nullable fields and columns in the dataframe parser.

- **NumberSpace Default Weight**: Ensured `NumberSpace` `with_vector` queries default to the correct weight.

- **Server Blob Handling**: Fixed issue where blob file names were incorrectly treated as directories.

- **Batch Empty Message Bus Handling**: Prevented creation of dummy dataframes when the external message bus provides no data.


## [Direct link to heading](https://docs.superlinked.com/reference/changelog\#id-2025-04-08)    2025-04-08

- **Framework: v19.13.0 - v22.7.0**

- **Server: v1.5.0 - v1.19.1**

- **Batch: v1.59.1 - v2.9.0**


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#breaking-changes-2)    Breaking Changes

- **HuggingFace API Re-ingestion (v22.0.0)**: Using external HuggingFace API for `TextSimilaritySpace` requires re-ingestion. Internal logic revisited to minimize this need.

- **Select Syntax Change (v21.0.0)**: `.select(foo.bar, foo.baz)` syntax is deprecated. Use `.select([foo.bar, foo.baz])` to support additional parameters like metadata.

- **Non-deterministic Node ID Fix (v20.0.0)**: Resolved intermittent issue causing index reference problems with previously ingested data.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#added-3)    Added

- **Batch Settings**: Introduced configuration settings in `superlinked-batch`.

- **VDB Timeouts**: Added support for increasing timeouts for Redis and Qdrant.

- **FP16 Precision Support**: Enabled FP16 precision for VDBs ( `SUPERLINKED_DISABLE_HALF_PRECISION_EMBEDDING=false`), requiring data re-ingestion.

- **GCS Error Handling**: Improved error handling for GCS file loading.

- **FP16 Model Embedding**: Added support for FP16 precision in model embedding for performance.

- **Parallel Image Downloads**: Implemented parallel image downloading for faster embedding.

- **Cached Model Size Limit**: Added limit to cached model sizes to prevent out-of-memory errors in Spark.

- **Batch Cluster Configuration**: Added support for different cluster configurations (GPU/CPU, memory) per batch job stage.

- **Multi-worker Server**: Enabled server execution with multiple workers.

- **Redis Connection Persistence**: Prevented Redis connection drops during inactivity.

- **Sentence-Transformers Timeout Handling**: Added timeout catching for model downloads.

- **OR Operator in Hard-Filters**: Added support for `OR` operator.

- **Per-Space Weights with Vector**: Enabled per-space weights in `.with_vector(...)`.

- **Vector Parts Metadata**: Return vector parts as metadata for `CustomSpace` calculations.

- **Hard-Filters on ID Field**: Allowed hard-filters on `IdField` for retrieving single entries (e.g., for `CustomSpace` interactions).

- **Batch File Timestamps**: Use file creation time for `created_at` timestamp during batch ingestion.

- **Batched VDB Writes**: Improved VDB write performance through batching.

- **Datetime Input Support**: Added support for datetime input for `created_at` property.

- **Float/Int Ingestion**: Allowed ingestion of floats and ints with `FloatField` type.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#changed-3)    Changed

- **Image Loading Performance**: Improved image loading time in batch by 7.5x.

- **Image Pre-processing Performance**: Decreased image pre-processing time by 50% for image embeddings.

- **Framework Performance**: Enhanced framework performance through parallel execution.

- **Redis Client Update**: Switched to Redis' official Python client for improved security and maintainability.

- **VectorSampler Weights**: Removed weights from `VectorSampler`.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#fixed-3)    Fixed

- **Qdrant Input Sanitization**: Sanitized input data before Qdrant ingestion.

- **Qdrant Partial Ingestion**: Prevented partial result ingestion on errors with Qdrant.

- **Nullable Value Hard-Filters**: Fixed hard-filters for nullable values.

- **.with\_vector() with Qdrant**: Fixed `.with_vector()` functionality with Qdrant.

- **Batch Nullable Values**: Fixed support for nullable values in batch.

- **Categorical Space Uncategorized**: Fixed `CategoricalSpace` behavior with `uncategorized_as_category=True`.

- **Non-deterministic Node IDs**: Resolved non-deterministic node ID issues across the framework (See Breaking Changes v20.0.0).

- **Custom ID Fields**: Fixed support for custom ID fields.


## [Direct link to heading](https://docs.superlinked.com/reference/changelog\#id-2025-02-24)    2025-02-24

- **Framework: v17.8.0 - v19.13.0**

- **Server: v0.7.3 - v1.5.0**

- **Batch: v1.33.0 - v1.59.1**


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#breaking-changes-3)    Breaking Changes

- **Query Results Restructure (v19.0.0)**: Query results have been restructured to provide more detailed information, including partial scores per space. Check [this](https://github.com/superlinked/superlinked/blob/main/notebook/feature/query_result.ipynb) notebook for example query structure.

- **Text Similarity Space Updates (v18.0.0)**: TextSimilaritySpace now defaults to query mode for supported models.

- **Server Query Structure (v1.0.0)**: Updated to align with new framework query result structure from v18.0.0.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#added-4)    Added

- **Embedding Cache**: Implemented recalculation cache providing 30x speed-up on 1M datasets with optimized LLM usage.

- **Partial Scores**: Added per-space partial scores to query results for improved explainability.

- **Field Selection**: Introduced options to select specific return fields ( `select_all()`, `select(...)`, `select_fields=...`) for improved query latency.

- **Acceptance Testing**: Added internal tool for validating end-to-end user flows.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#changed-4)    Changed

- **Storage Optimization**: Removed unnecessary object storage in VDB to improve latency and storage efficiency.

- **Example Updates**: Updated all examples to use simplified superlinked imports.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#fixed-4)    Fixed

- Various improvements to the storage layer of the framework supporting pilot project requirements.


## [Direct link to heading](https://docs.superlinked.com/reference/changelog\#id-2024-12-20)    2024-12-20

- **Framework: v12.28.1 - v17.8.0**

- **Server: v14.7.1 - v0.7.3**

- **Batch: v1.17.0 - v1.33.0**


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#added-5)    Added

- **Simplified Server Startup**: Added support for single command server startup using `python -m superlinked.server`.

- **NLQ Prompt Suggestions**: Enhanced NLQ with suggestions for better prompting.

- **Debugging Feature Flag**: Added option to return debugging data for users.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#changed-5)    Changed

- **Event System Redesign**: Simplified and reshaped the event system across online and batch components.

- **Batch Index Creation**: Moved index creation to dedicated component instead of server instances.

- **Dynamic Model Cache**: Implemented dynamic cache directory setting for Hugging Face models.

- **Query Performance**: Improved query performance from O(n) to O(1) using transactional reading.

- **NLQ Refactor**: Restructured NLQ implementation for improved performance and quality.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#fixed-5)    Fixed

- **Parameter Validation**: Added exception throwing for invalid query parameters.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#misc)    Misc

- **Code Cleanup**: Removed obsolete server code from repository.


## [Direct link to heading](https://docs.superlinked.com/reference/changelog\#id-2024-11-20)    2024-11-20

- **Framework: v12.23.0 - v12.28.1**

- **Server: v12.23.0 - v14.7.1**

- **Batch: v1.15.2 - v1.17.0**


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#added-6)    Added

- **Query Arithmetics**: Completed foundation for multi-modal data representation in single vectors, enabling cohesive interaction between vectors, aggregations, and normalizations.

- **Qdrant Connector**: Added support for Qdrant as an alternative to MongoDB and Redis.

- **System Prompts in NLQ**: Added capability for users to customize NLQ translation prompts.

- **Contains All Filter**: Implemented new filter operation.

- **Query Vector Exposure**: Added ability to view query vectors in results for improved observability.

- **NLQ Parameter Constraints**: Added support to constrain Parameters to fixed lists.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#changed-6)    Changed

- **DSL Improvements**: Added support for single items where lists were previously required.

- **Parameter Validation**: Enhanced validation for space fields, schema references, and parameter names.

- **String Parameter Support**: Added support for string parameters in filter, contains, and in operators.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#fixed-6)    Fixed

- **Executor Validation**: Added guardrails for data ingestion without running executor.

- **User ID Validation**: Improved error handling for invalid user IDs.


## [Direct link to heading](https://docs.superlinked.com/reference/changelog\#id-2024-11-06)    2024-11-06

- **Framework: v12.2.0 - v12.23.0**

- **Server: v12.2.0 - v12.23.0**

- **Batch: v1.13.1 - v1.15.2**


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#added-7)    Added

- **Simplified Superlinked Imports**: Users can now import Superlinked using a single import statement `import superlinked as sl`, eliminating the need to remember the import path of each object.

- **Support for OpenCLIP Models**: Added support for OpenCLIP models in image embeddings, extending the supported models to include OpenCLIP and sentence-transformers supported vision encoders.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#fixed-7)    Fixed

- **File Discovery Issues**: Resolved file discovery issues experienced by Yassine.

- **Dynamic Cache Directory for Sentence-Transformers**: Made the sentence-transformers cache directory dynamic to ensure compatibility with batch operations.

- **Zero Division in Events**: Fixed an issue where events with virtually no age resulted in a division by zero error.

- **Storing Unreferenced Fields**: Corrected the storage of fields that were not referenced in the index.

- **Default Similarity Weights**: Adjusted similarity weights to default to one when a parameter is not provided.

- **StringLists Support in NLQ**: Added support for StringLists to be filled by NLQ.

- **Categorical Similarity Node Bug**: Fixed a bug affecting events in the categorical similarity node.

- **Error on Unknown ID**: Now throws an error if an unknown ID is used, instead of returning similarities for the given scenario.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#misc-1)    Misc

- **NLQ Feature Improvements**: Made further improvements to the NLQ feature.

- **New NLQ Examples**: Added new NLQ examples showcasing product search instead of product reviews.

- **Enhanced Logging**: Added further logging for the external message bus.

- **Test Performance Improvement**: Improved test performance, reducing execution time from 4.6 seconds to 0.6 seconds.


## [Direct link to heading](https://docs.superlinked.com/reference/changelog\#id-2024-10-23)    2024-10-23

- **Framework: v10.1.0 - v12.2.0**

- **Server: v10.1.0 - v12.2.0**

- **Batch: v1.11.1 - v1.13.1**


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#added-8)    Added

- **Stack Trace in JSON Logging**: Enhanced JSON logging by adding stack traces to facilitate debugging.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#fixed-8)    Fixed

- **Support SchemaA and SchemaB both affecting SchemaC**: Added support for scenarios where both SchemaA and SchemaB can affect SchemaC, such as users being influenced by paragraphs they read and comments they like.

- **Registry Bug**: Resolved an internal registry bug.


## [Direct link to heading](https://docs.superlinked.com/reference/changelog\#id-2024-10-9)    2024-10-9

- **Framework: v9.43.0 - v10.1.0**

- **Server: v9.42.1 - 10.1.0 (running with framework/v10.1.0)**

- **Batch: v1.8.0 - v1.11.1**


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#added-9)    Added

- **Optional Params in Query**: Params in Query are now optional. If not filled during a query, the clause will not affect the query results.

- **Support for VDBs in Notebooks**: Introduced the `InteractiveExecutor` to support connecting to different VDBs from a notebook environment.

- **Simplified Query Definition**: Users can now provide the space as a parameter when only one field is suitable, e.g., `.similar(number_space, 3)` instead of `.similar(number_space.number, 3)`.

- **Stacktrace in JSON Logs**: Added stacktrace to JSON logs for improved debugging.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#fixed-9)    Fixed

- **Plot Rendering in Notebooks**: Added support to render notebooks properly across different environments.

- **Redis Incorrect Results**: Fixed a naming issue that caused Redis to return incorrect results. Continuous testing of VDB integrations is planned to prevent such issues.

- **Constrain Category Choices in NLQ**: NLQ can no longer "hallucinate" categories that do not exist for a given query.


## [Direct link to heading](https://docs.superlinked.com/reference/changelog\#id-2024-09-25)    2024-09-25

- **Framework: v9.33.0 - v9.43.0**

- **Server: v9.33.0 - v9.42.1 (running with framework/v9.42.1)**

- **Batch: v1.4.0 - v1.8.0**


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#added-10)    Added

- **NLQ support for IN and NOT\_IN operators**: Added support for NLQ to translate natural language to IN and NOT\_IN operators.

- **Logging for superlinked components**: Logging was added for unified debugging and observability, led by Krisztian.

- **Basic caching for text-embeddings**: Implemented caching for 10k items to handle repeating inputs efficiently.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#fixed-10)    Fixed

- **Chunking with hard-filters**: Fixed an issue where chunking was breaking hard-filters.

- **Limit NLQ to respect given categories**: Ensured NLQ does not "hallucinate" categories not present in the application.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#changed-7)    Changed

- **Image embedding model update**: Replaced the image embedding model in the use-case notebook with the latest model.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#misc-2)    Misc

- **Batch infrastructure risk mitigation**: Verified that the GCP hosted solution works as intended.

- **Hard-filter compatibility with batch**: Ensured compatibility of IN, NOT\_IN, LT, LTE, GT, GTE operators with batch-encoded datasets.


## [Direct link to heading](https://docs.superlinked.com/reference/changelog\#id-2024-09-11)    2024-09-11

- **Framework: v9.22.1 - v9.33.0**

- **Server: v9.33.0 - v9.33.0 (running with framework/v9.33.0)**

- **Batch: v1.1.2 - v1.4.0**


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#added-11)    Added

- **Separated the user code into multiple files**: We have separated the previous app.py into dedicated index.py/query.py/api.py, which promotes reusability and explainability of the system behavior.

- **Added "or" and "contains" to the notebooks**: Added further examples to notebooks based on user feedback.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#fixed-11)    Fixed

- **Fixed skewed vectors, when recency was 0**: A known limitation of the system is that, if full zero vectors make it to the index or query as an output of a space, then the weighting logic.

- **Added NLQ support for in and not\_in operators**: Newly introduced hard-filters were not properly handled by NLQ before.

- **Fixed hard-filters with chunking**: Hard-filters were not tested with chunking, this is now fixed.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#changed-8)    Changed

- **Improved the system message at server startup**: Users were experiencing confusing when starting up server as the messages were not clear on the status.


## [Direct link to heading](https://docs.superlinked.com/reference/changelog\#id-2024-08-28)    2024-08-28

- **Framework: v9.12.1 - v9.22.1**

- **Server: v9.12.1 - v9.22.0 (running with framework/v9.12.1)**

- **Batch: v1.1.0 - v1.1.2**


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#added-12)    Added

- **Event support in batch**: Users can now batch calculate with events as well, rendering the online and batch systems in feature parity.

- **Support for more hard filter operations**: Added support for LT, LTE, GT, GTE, AND, OR, CONTAINS, NOT\_CONTAINS, IN, NOT\_IN, unlocking more tabular data heavy use-cases.

- **Optimized GPU usage**: Optimized GPU utilization for best performance, which below a certain size (~10k embeddings) is more optimal with CPU.

- **Integration tests of online executor with GPU**: Added tests to measure if the frameworks correctly recognize the underlying GPU, if any.

- **Added scores to example notebooks**: Expanded all notebooks to show how scores work, allowing users to better understand the underlying vector similarity scores.

- **Further NLQ support**: Extended NLQ features with filter support and temperature tuning based on feedback.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#fixed-12)    Fixed

- **Results were not ordered by score with Redis**: Fixed issue where results were not properly ordered by their scores in ascending order.

- **Long categorical embeddings were dominating the results**: Fixed an issue that resulted in all 0 vectors that skewed the results by breaking the normalization.

- **Source.put was behaving differently with different inputs**: Fixed to work as expected with arrays and data frames alike.

- **Index temperature was not accepting integers**: Fixed the index to accept integer temperatures.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#changed-9)    Changed

- **Added better formatted logs in tests**: Improved logging support for easier issue identification during development.

- **(breaking) Removed status endpoints for initial data loader**: Necessary step to allow the executor to be stateless, preparing it for high availability hosting.


## [Direct link to heading](https://docs.superlinked.com/reference/changelog\#id-2024-08-14)    2024-08-14

- **Framework: v9.7.0 - v9.12.1**

- **Server: v9.6.0 - v9.7.0 (running with v9.2.0)**

- **Batch: v1.0.2 - v1.1.0**


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#added-13)    Added

- **Return similarity scores**: Now returning similarity scores along with results, allowing clients to better understand the distribution.

- **Improved feature notebooks**: Extended with examples containing similarity scores, querying of recency space, and event parameters (max\_count, max\_age, temperature).

- **Code quality checks for server**: Added automations to ensure server testing and unified code format.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#fixed-13)    Fixed

- **Recency was not always using the same NOW from the context**: Fixed to use the correct reference point.


## [Direct link to heading](https://docs.superlinked.com/reference/changelog\#id-2024-08-07)    2024-08-07

- **Framework: v9.7.0**

- **Server: v9.6.0**

- **Batch: v1.0.2**


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#added-14)    Added

- **Bumped sentence-transformers to 3.0.1**: Allows experimentation with highest scoring models from mteb leaderboard.

- **Support for empty list embedding**: Enables ingestion of data with lists where not all rows have an item.

- **Default limits to vector database connectors**: Set default return of 10 items for both Redis and Mongo.

- **Natural Language Queries**: Users can describe parameters for prompting the underlying model.

- **Support logarithmic number embeddings**: Captures non-linear preferences with large values.


### [Direct link to heading](https://docs.superlinked.com/reference/changelog\#fixed-14)    Fixed

- **Negative weights boosting recommendations**: Fixed issues within the event handling system.

- **Negative weight now applied even for the first received event**: Addressed bug where negative weights only worked after a positively weighted event.


[PreviousOverview](https://docs.superlinked.com/reference/overview) [NextComponents](https://docs.superlinked.com/reference/components)

Last updated 1 month ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject