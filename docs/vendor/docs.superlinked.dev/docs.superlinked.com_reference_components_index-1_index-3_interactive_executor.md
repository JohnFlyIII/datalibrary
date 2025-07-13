---
url: "https://docs.superlinked.com/reference/components/index-1/index-3/interactive_executor"
title: "Interactive Executor | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-1/index-3/interactive_executor\#classes)    Classes

`InteractiveExecutor(sources: InteractiveSourceT | Sequence[InteractiveSourceT], indices: Index | Sequence[Index], vector_database: VectorDatabase | None = None, context_data: Mapping[str, Mapping[str, ContextValue]] | None = None)` : Interactive implementation of the Executor class. Supply it with the sources through which your data is received, the indices indicating the desired vector spaces, and optionally a vector database. The executor will create the spaces optimized for search.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
Initialize the InteractiveExecutor.
Args:
    sources (list[InteractiveSourceT]): List of interactive sources.
    indices (list[Index]): List of indices.
    vector_database: (VectorDatabase | None): Vector database instance. Defaults to InMemoryVectorDatabase.
    context_data (Mapping[str, Mapping[str, ContextValue]] | None):
        Context data for execution. Defaults to None.

### Ancestors (in MRO)

* superlinked.framework.dsl.executor.executor.Executor
* abc.ABC
* typing.Generic

### Descendants

* superlinked.framework.dsl.executor.in_memory.in_memory_executor.InMemoryExecutor

### Methods

`run(self) ‑> superlinked.framework.dsl.app.interactive.interactive_app.InteractiveApp`
:   Run the InteractiveExecutor. It returns an app that can accept queries.
    Returns:
        InteractiveApp: An instance of InteractiveApp.
```

[PreviousInteractive](https://docs.superlinked.com/reference/components/index-1/index-3) [NextSource](https://docs.superlinked.com/reference/components/index-2)

Last updated 7 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject