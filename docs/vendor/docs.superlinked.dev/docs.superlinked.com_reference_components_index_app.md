---
url: "https://docs.superlinked.com/reference/components/index/app"
title: "App | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index/app\#classes)    Classes

`App(sources: Sequence[~SourceT], indices: Sequence[superlinked.framework.dsl.index.index.Index], vector_database: superlinked.framework.dsl.storage.vector_database.VectorDatabase, context: superlinked.framework.common.dag.context.ExecutionContext, init_search_indices: bool)` : Abstract base class for an App, a running executor that can, for example, do queries or ingest data.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
Initialize the App.
Args:
    sources (list[SourceT]): The list of sources.
    indices (list[Index]): The list of indices.
    vector_database (VectorDatabase): The vector database which the executor will use.
    context (Mapping[str, Mapping[str, Any]]): The context mapping.

### Ancestors (in MRO)

* abc.ABC
* typing.Generic

### Descendants

* superlinked.framework.dsl.app.online.online_app.OnlineApp

### Instance variables

`storage_manager: superlinked.framework.common.storage_manager.storage_manager.StorageManager`
:   Get the storage manager.
    Returns:
        StorageManager: The storage manager instance.
```

[PreviousApp](https://docs.superlinked.com/reference/components/index) [NextIn Memory](https://docs.superlinked.com/reference/components/index/index)

Last updated 7 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject