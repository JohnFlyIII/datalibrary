---
url: "https://docs.superlinked.com/reference/components/index-2/interactive_source"
title: "Interactive Source | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-2/interactive_source\#classes)    Classes

`InteractiveSource(schema: ~IdSchemaObjectT, parser: superlinked.framework.common.parser.data_parser.DataParser[~IdSchemaObjectT, ~SourceTypeT] | None = None)` : InteractiveSource represents a source of data, where you can put your data. This will supply the index with the data it needs to index and search in.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
Initialize the InteractiveSource.

Args:
    schema (IdSchemaObject): The schema object.
    parser (DataParser | None, optional): The data parser. Defaults to JsonParser if None is supplied.

Raises:
    InitializationException: If the schema is not an instance of SchemaObject.

### Ancestors (in MRO)

* superlinked.framework.online.source.online_source.OnlineSource
* superlinked.framework.common.observable.TransformerPublisher
* superlinked.framework.common.source.source.Source
* typing.Generic

### Descendants

* superlinked.framework.dsl.source.in_memory_source.InMemorySource

### Methods

`allow_data_ingestion(self) ‑> None`
:

`put(self, data: SourceTypeT | Sequence[SourceTypeT]) ‑> None`
:   Put data into the InteractiveSource. This operation can take time as the vectorization
    of your data happens here.

    Args:
        data (SourceTypeT | list[SourceTypeT]): The data to put.
```

[PreviousSource](https://docs.superlinked.com/reference/components/index-2) [NextTypes](https://docs.superlinked.com/reference/components/index-2/types)

Last updated 7 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject