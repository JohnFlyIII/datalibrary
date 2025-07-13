---
url: "https://docs.superlinked.com/reference/components/index-1/index-2/query_executor"
title: "Query Executor | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-1/index-2/query_executor\#classes)    Classes

`QueryExecutor(app: superlinked.framework.dsl.app.app.App, query_descriptor: superlinked.framework.dsl.query.query_descriptor.QueryDescriptor, query_vector_factory: superlinked.framework.dsl.query.query_vector_factory.QueryVectorFactory)`
: QueryExecutor provides an interface to execute predefined queries with query time parameters.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
Initializes the QueryExecutor.

Args:
    app: An instance of the App class.
    query_descriptor: An instance of the QueryDescriptor class representing the query to be executed.
    query_vector_factory: An instance of the QueryVectorFactory class used to produce query vectors.

### Methods

`query(self, **params: collections.abc.Sequence[str] | collections.abc.Sequence[float] | PIL.Image.Image | str | int | float | bool | tuple[str | None, str | None] | None) ‑> superlinked.framework.dsl.query.result.QueryResult`
:   Execute a query with keyword parameters.

    Args:
        **params: Arbitrary arguments with keys corresponding to the `name` attribute of the `Param` instance.

    Returns:
        Result: The result of the query execution that can be inspected and post-processed.

    Raises:
        QueryException: If the query index is not amongst the executor's indices.
```

[PreviousQuery](https://docs.superlinked.com/reference/components/index-1/index-2) [NextInteractive](https://docs.superlinked.com/reference/components/index-1/index-3)

Last updated 1 month ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject