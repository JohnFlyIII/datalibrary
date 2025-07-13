---
url: "https://docs.superlinked.com/reference/components/index-5/query"
title: "Query | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-5/query\#classes)    Classes

`Query(index: superlinked.framework.dsl.index.index.Index, weights: collections.abc.Mapping[superlinked.framework.dsl.space.space.Space, float | int | superlinked.framework.dsl.query.param.Param] | None = None)` : A class representing a query. Build queries using Params as placeholders for weights or query text, and supply their value later on when executing a query.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
Attributes:
    index (Index): The index to be used for the query.
    weights (Mapping[Space, NumericParamType] | None, optional): The mapping of spaces to weights.
        Defaults to None, which is equal weight for each space.

Initialize the Query.

Args:
    index (Index): The index to be used for the query.
    weights (Mapping[Space, NumericParamType] | None, optional): The mapping of spaces to weights.
        Defaults to None, which is equal weight for each space.

### Methods

`find(self, schema: superlinked.framework.common.schema.id_schema_object.IdSchemaObject) ‑> superlinked.framework.dsl.query.query_descriptor.QueryDescriptor`
:   Find a schema in the query.

    Args:
        schema (IdSchemaObject): The schema to find.

    Returns:
        QueryDescriptor: The QueryDescriptor object.

    Raises:
        QueryException: If the index does not have the queried schema.
```

[PreviousQuery Vector Factory](https://docs.superlinked.com/reference/components/index-5/query_vector_factory) [NextQuery Param Value Setter](https://docs.superlinked.com/reference/components/index-5/query_param_value_setter)

Last updated 8 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject