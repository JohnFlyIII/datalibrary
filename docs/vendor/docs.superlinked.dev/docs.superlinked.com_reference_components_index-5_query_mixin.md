---
url: "https://docs.superlinked.com/reference/components/index-5/query_mixin"
title: "Query Mixin | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-5/query_mixin\#classes)    Classes

`QueryMixin()`
: A mixin class that provides query execution capabilities for classes that include it.
This class sets up the necessary infrastructure to execute queries on a set of indices
using a storage manager.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Descendants

* superlinked.framework.dsl.app.online.online_app.OnlineApp

### Methods

`async_query(self, query_descriptor: superlinked.framework.dsl.query.query_descriptor.QueryDescriptor, **params: Any) ‑> superlinked.framework.dsl.query.result.QueryResult`
:

`query(self, query_descriptor: superlinked.framework.dsl.query.query_descriptor.QueryDescriptor, **params: Any) ‑> superlinked.framework.dsl.query.result.QueryResult`
:   Execute a query using the provided QueryDescriptor and additional parameters.

    Args:
        query_descriptor (QueryDescriptor): The query object containing the query details.
        **params (Any): Additional parameters for the query execution.

    Returns:
        Result: The result of the query execution.

    Raises:
        QueryException: If the query index is not found among the executor's indices.

`setup_query_execution(self, indices: Sequence[superlinked.framework.dsl.index.index.Index]) ‑> None`
:   Set up the query execution environment by initializing a mapping between indices
    and their corresponding QueryVectorFactory instances.

    Args:
        indices (Sequence[Index]): A sequence of Index instances to be used for query execution.
        storage_manager (StorageManager): The storage manager instance to be used.

`setup_query_result_converter(self, query_result_converter: superlinked.framework.dsl.query.query_result_converter.query_result_converter.QueryResultConverter) ‑> None`
:   Set up the query result converter to be used for converting the query results.

    Args:
        query_result_converter (QueryResultConverter): The query result converter instance.
```

[PreviousResult](https://docs.superlinked.com/reference/components/index-5/result) [NextSpace Weight Param Info](https://docs.superlinked.com/reference/components/index-5/space_weight_param_info)

Last updated 15 days ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject