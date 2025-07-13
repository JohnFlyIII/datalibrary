---
url: "https://docs.superlinked.com/reference/components/index-1/index/in_memory_executor"
title: "In Memory Executor | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-1/index/in_memory_executor\#classes)    Classes

`InMemoryExecutor(sources: InMemorySource | Sequence[InMemorySource], indices: Index | Sequence[Index], context_data: Mapping[str, Mapping[str, ContextValue]] | None = None)` : Initialize the InMemoryExecutor.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
The InMemoryExecutor provides an in-memory implementation for executing queries against indexed data.
It creates optimized vector spaces based on the provided indices
and allows querying data from in-memory sources.

Args:
    sources (InMemorySource | Sequence[InMemorySource]): One or more in-memory data sources to query against.
        Can be a single source or sequence of sources.
    indices (Index | Sequence[Index]): One or more indices that define the vector spaces.
        Can be a single index or sequence of indices.
    context_data (Mapping[str, Mapping[str, ContextValue]] | None, optional): Additional context data
        for execution. The outer mapping key represents the context name, inner mapping contains
        key-value pairs for that context. Defaults to None.

Initialize the InMemoryExecutor.

The InMemoryExecutor provides an in-memory implementation for executing queries against indexed data.
It creates optimized vector spaces based on the provided indices
and allows querying data from in-memory sources.

Args:
    sources (InMemorySource | Sequence[InMemorySource]): One or more in-memory data sources to query against.
        Can be a single source or sequence of sources.
    indices (Index | Sequence[Index]): One or more indices that define the vector spaces.
        Can be a single index or sequence of indices.
    context_data (Mapping[str, Mapping[str, ContextValue]] | None, optional): Additional context data
        for execution. The outer mapping key represents the context name, inner mapping contains
        key-value pairs for that context. Defaults to None.

### Ancestors (in MRO)

* superlinked.framework.dsl.executor.interactive.interactive_executor.InteractiveExecutor
* superlinked.framework.dsl.executor.executor.Executor
* abc.ABC
* typing.Generic

### Methods

`run(self) ‑> superlinked.framework.dsl.app.in_memory.in_memory_app.InMemoryApp`
:   Run the InMemoryExecutor. It returns an app that can accept queries.
    Returns:
        InMemoryApp: An instance of InMemoryApp.
```

[PreviousIn Memory](https://docs.superlinked.com/reference/components/index-1/index) [NextRest](https://docs.superlinked.com/reference/components/index-1/index-1)

Last updated 7 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject