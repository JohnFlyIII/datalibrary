---
url: "https://docs.superlinked.com/reference/components/index-1/index-1/rest_executor"
title: "Rest Executor | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-1/index-1/rest_executor\#classes)    Classes

`RestExecutor(sources: Sequence[RestSource | DataLoaderSource], indices: Sequence[Index], queries: Sequence[RestQuery], vector_database: VectorDatabase, endpoint_configuration: RestEndpointConfiguration | None = None, context_data: Mapping[str, Mapping[str, ContextValue]] | None = None, blob_handler_config: BlobHandlerConfig | None = None)` : The RestExecutor is a specialized subclass of the Executor base class designed to handle REST applications. It encapsulates all necessary parameters for configuring and running a REST-based application.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
Initialize the RestExecutor with the provided parameters.

Args:
    sources (Sequence[RestSource | DataLoaderSource]): Sources, either RestSource or DataLoaderSource.
    indices (Sequence[Index]): Indices for the RestExecutor.
    queries (Sequence[RestQuery]): Queries to execute.
    vector_database (VectorDatabase): Vector database instance.
    endpoint_configuration (RestEndpointConfiguration | None): REST endpoint configuration. Defaults to None.
    context_data (Mapping[str, Mapping[str, ContextValue]] | None):
        Context data for execution. Defaults to None.

### Ancestors (in MRO)

* superlinked.framework.dsl.executor.executor.Executor
* abc.ABC
* typing.Generic

### Methods

`run(self) ‑> superlinked.framework.dsl.app.rest.rest_app.RestApp`
:   Run the RestExecutor. It returns an app that will create rest endpoints.

    Returns:
        RestApp: An instance of RestApp.
```

[PreviousRest](https://docs.superlinked.com/reference/components/index-1/index-1) [NextRest Descriptor](https://docs.superlinked.com/reference/components/index-1/index-1/rest_descriptor)

Last updated 5 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject