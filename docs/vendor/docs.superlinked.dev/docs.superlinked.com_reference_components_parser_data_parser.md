---
url: "https://docs.superlinked.com/reference/components/parser/data_parser"
title: "Data Parser | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/parser/data_parser\#classes)    Classes

`DataParser(schema: IdSchemaObjectT, mapping: Mapping[SchemaField, str] | None = None)` : A DataParser describes the interface to get a source data to the format of a defined schema with mapping support.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
Attributes:
    mapping (Mapping[SchemaField, str], optional): Source to SchemaField mapping rules
        as `SchemaField`-`str` pairs such as `{movie_schema.title: "movie_title"}`.

Initialize DataParser

Get the desired output schema and initialize a default mapping
that can be extended by DataParser realizations.

Args:
    schema (IdSchemaObjectT): SchemaObject describing the desired output.
    mapping (Mapping[SchemaField, str], optional): Realizations can use the `SchemaField` to `str` mapping
        to define their custom mapping logic.

Raises:
    InitializationException: Parameter `schema` is of invalid type.

### Ancestors (in MRO)

* abc.ABC
* typing.Generic

### Descendants

* superlinked.framework.common.parser.dataframe_parser.DataFrameParser
* superlinked.framework.common.parser.json_parser.JsonParser

### Instance variables

`allow_bytes_input: bool`
:

`blob_loader: BlobLoader`
:

### Methods

`marshal(self, parsed_schemas: ParsedSchema | list[ParsedSchema]) ‑> list[~SourceTypeT]`
:   Get a previously parsed data and return it to it's input format.

    Args:
        parsed_schemas: Previously parsed data that follows the schema of the `DataParser`.

    Returns:
        list[SourceTypeT]: A list of the original source data format after marshalling the parsed data.

`set_allow_bytes_input(self, value: bool) ‑> None`
:

`unmarshal(self, data: SourceTypeT) ‑> list[superlinked.framework.common.parser.parsed_schema.ParsedSchema]`
:   Get the source data and parse it to the desired Schema with the defined mapping.

    Args:
        data (TSourceType): Source data that corresponds to the DataParser's type.

    Returns:
        list[ParsedSchema]: A list of ParsedSchema objects.
```

[PreviousDataframe Parser](https://docs.superlinked.com/reference/components/parser/dataframe_parser) [NextApp](https://docs.superlinked.com/reference/components/index)

Last updated 8 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject