---
url: "https://docs.superlinked.com/reference/components/index-2/in_memory_source"
title: "In Memory Source | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-2/in_memory_source\#classes)    Classes

`InMemorySource(schema: ~IdSchemaObjectT, parser: superlinked.framework.common.parser.data_parser.DataParser[~IdSchemaObjectT, ~SourceTypeT] | None = None)` : InMemorySource represents a source of data, where you can put your data. This will supply the index with the data it needs to index and search in.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
Initialize the InteractiveSource.

Args:
    schema (IdSchemaObject): The schema object.
    parser (DataParser | None, optional): The data parser. Defaults to JsonParser if None is supplied.

Raises:
    InitializationException: If the schema is not an instance of SchemaObject.

### Ancestors (in MRO)

* superlinked.framework.dsl.source.interactive_source.InteractiveSource
* superlinked.framework.online.source.online_source.OnlineSource
* superlinked.framework.common.observable.TransformerPublisher
* superlinked.framework.common.source.source.Source
* typing.Generic
```

[PreviousSource](https://docs.superlinked.com/reference/components/index-2/source) [NextData Loader Source](https://docs.superlinked.com/reference/components/index-2/data_loader_source)

Last updated 7 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject