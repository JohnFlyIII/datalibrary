---
url: "https://docs.superlinked.com/reference/components/index/index-3/interactive_app"
title: "Interactive App | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index/index-3/interactive_app\#classes)    Classes

`InteractiveApp(sources: Sequence[superlinked.framework.dsl.source.interactive_source.InteractiveSource], indices: Sequence[superlinked.framework.dsl.index.index.Index], vector_database: superlinked.framework.dsl.storage.vector_database.VectorDatabase, context: superlinked.framework.common.dag.context.ExecutionContext, init_search_indices: bool = True)` : Interactive implementation of the App class.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
Initialize the InteractiveApp from an InteractiveExecutor.
Args:
    sources (list[InteractiveSource]): List of interactive sources.
    indices (list[Index]): List of indices.
    vector_database (VectorDatabase | None): Vector database instance. Defaults to InMemory.
    context (Mapping[str, Mapping[str, Any]]): Context mapping.
    init_search_indices (bool): Decides if the search indices need to be created. Defaults to True.

### Ancestors (in MRO)

* superlinked.framework.dsl.app.online.online_app.OnlineApp
* superlinked.framework.dsl.app.app.App
* abc.ABC
* typing.Generic
* superlinked.framework.dsl.query.query_mixin.QueryMixin

### Descendants

* superlinked.framework.dsl.app.in_memory.in_memory_app.InMemoryApp
```

[PreviousInteractive](https://docs.superlinked.com/reference/components/index/index-3) [NextExecutor](https://docs.superlinked.com/reference/components/index-1)

Last updated 7 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject