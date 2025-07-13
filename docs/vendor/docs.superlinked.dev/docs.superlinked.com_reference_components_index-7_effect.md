---
url: "https://docs.superlinked.com/reference/components/index-7/effect"
title: "Effect | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-7/effect\#classes)    Classes

`Effect(space: superlinked.framework.dsl.space.space.Space[~AggregationInputT, ~EmbeddingInputT], affected_schema_reference: superlinked.framework.common.schema.event_schema_object.SchemaReference, affecting_schema_reference: superlinked.framework.common.schema.event_schema_object.SchemaReference | superlinked.framework.common.schema.event_schema_object.MultipliedSchemaReference, filter_: superlinked.framework.common.interface.comparison_operand.ComparisonOperation[superlinked.framework.common.schema.schema_object.SchemaField])`
: An effect represents a conditional interaction within a `Space` where the `affecting_schema_reference` interacted with the `affected_schema_reference`.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
It allows you to real-time adjust embeddings based on interaction.
e.g.: A `User` schema interacts with a `Post` schema, if `event.type == 'like'.

### Ancestors (in MRO)

* typing.Generic

### Instance variables

`affected_schema_reference: superlinked.framework.common.schema.event_schema_object.SchemaReference`
:

`affecting_schema_reference: superlinked.framework.common.schema.event_schema_object.SchemaReference | superlinked.framework.common.schema.event_schema_object.MultipliedSchemaReference`
:

`filter_: superlinked.framework.common.interface.comparison_operand.ComparisonOperation[superlinked.framework.common.schema.schema_object.SchemaField]`
:

`space: superlinked.framework.dsl.space.space.Space[~AggregationInputT, ~EmbeddingInputT]`
:
```

[PreviousIndex](https://docs.superlinked.com/reference/components/index-7) [NextIndex](https://docs.superlinked.com/reference/components/index-7/index.m)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject