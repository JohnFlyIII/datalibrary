---
url: "https://docs.superlinked.com/reference/components/index-1/executor"
title: "Executor | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-1/executor\#classes)    Classes

`Executor(sources: ~SourceT | Sequence[~SourceT], indices: superlinked.framework.dsl.index.index.Index | typing.Annotated[Sequence[superlinked.framework.dsl.index.index.Index], beartype.vale.Is[TypeValidator.list_validator.validator]], vector_database: superlinked.framework.dsl.storage.vector_database.VectorDatabase, context: superlinked.framework.common.dag.context.ExecutionContext)` : Abstract base class for an executor.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
Initialize the Executor.
Args:
    sources (list[SourceT]): The list of sources.
    indices (list[Index]): The list of indices.
    vector_database (VectorDatabase): The vector database which the executor will use.
    context (Mapping[str, Mapping[str, Any]]): The context mapping.

### Ancestors (in MRO)

* abc.ABC
* typing.Generic

### Descendants

* superlinked.framework.dsl.executor.interactive.interactive_executor.InteractiveExecutor
* superlinked.framework.dsl.executor.rest.rest_executor.RestExecutor

### Methods

`run(self) ‑> superlinked.framework.dsl.app.app.App`
:   Abstract method to run the executor.
    Returns:
        App: An instance of App.
```

[PreviousException](https://docs.superlinked.com/reference/components/index-1/exception) [NextIn Memory](https://docs.superlinked.com/reference/components/index-1/index)

Last updated 7 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject