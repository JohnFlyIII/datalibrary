---
url: "https://docs.superlinked.com/reference/components/parser/dataframe_parser"
title: "Dataframe Parser | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/parser/dataframe_parser\#classes)    Classes

`DataFrameParser(schema: IdSchemaObjectT, mapping: Mapping[SchemaField, str] | None = None)` : DataFrameParser gets a `pd.DataFrame` and using column-string mapping it transforms the `DataFrame` to a desired schema.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
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

* superlinked.framework.common.parser.data_parser.DataParser
* abc.ABC
* typing.Generic

### Methods

`unmarshal(self, data: pd.DataFrame) ‑> list[superlinked.framework.common.parser.parsed_schema.ParsedSchema]`
:   Parses the given DataFrame into a list of ParsedSchema objects according to the defined schema and mapping.
    Args:
        data (pd.DataFrame): Pandas DataFrame input.
    Returns:
        list[ParsedSchema]: A list of ParsedSchema objects that will be processed by the spaces.
```

[PreviousJson Parser](https://docs.superlinked.com/reference/components/parser/json_parser) [NextData Parser](https://docs.superlinked.com/reference/components/parser/data_parser)

Last updated 8 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject