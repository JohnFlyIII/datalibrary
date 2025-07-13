---
url: "https://docs.superlinked.com/reference/components/index/index/in_memory_app"
title: "In Memory App | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index/index/in_memory_app\#classes)    Classes

`InMemoryApp(sources: Sequence[superlinked.framework.dsl.source.in_memory_source.InMemorySource], indices: Sequence[superlinked.framework.dsl.index.index.Index], vector_database: superlinked.framework.dsl.storage.vector_database.VectorDatabase | None, context: superlinked.framework.common.dag.context.ExecutionContext)` : In-memory implementation of the App class.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
Initialize the InMemoryApp from an InMemoryExecutor.
Args:
    sources (list[InMemorySource]): List of in-memory sources.
    indices (list[Index]): List of indices.
    vector_database (VectorDatabase | None): Vector database instance. Defaults to InMemory.
    context (Mapping[str, Mapping[str, Any]]): Context mapping.

### Ancestors (in MRO)

* superlinked.framework.dsl.app.interactive.interactive_app.InteractiveApp
* superlinked.framework.dsl.app.online.online_app.OnlineApp
* superlinked.framework.dsl.app.app.App
* abc.ABC
* typing.Generic
* superlinked.framework.dsl.query.query_mixin.QueryMixin
```

[PreviousIn Memory](https://docs.superlinked.com/reference/components/index/index) [NextRest](https://docs.superlinked.com/reference/components/index/index-1)

Last updated 7 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject