---
url: "https://docs.superlinked.com/reference/components/index-7/index/effect_with_referenced_schema_object"
title: "Effect With Referenced Schema Object | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-7/index/effect_with_referenced_schema_object\#classes)    Classes

`EffectWithReferencedSchemaObject(base_effect: Effect[AggregationInputT, EmbeddingInputT], resolved_affected_schema_reference: ResolvedSchemaReference, resolved_affecting_schema_reference: ResolvedSchemaReference, event_schema: EventSchemaObject)`
: EffectWithReferencedSchemaObject(base\_effect: 'Effect\[AggregationInputT, EmbeddingInputT\]', resolved\_affected\_schema\_reference: 'ResolvedSchemaReference', resolved\_affecting\_schema\_reference: 'ResolvedSchemaReference', event\_schema: 'EventSchemaObject')

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Ancestors (in MRO)

* typing.Generic

### Static methods

`from_base_effect(base_effect: Effect, schemas: set[SchemaObject]) ‑> superlinked.framework.dsl.index.util.effect_with_referenced_schema_object.EffectWithReferencedSchemaObject`
:

### Instance variables

`base_effect: superlinked.framework.dsl.index.effect.Effect[~AggregationInputT, ~EmbeddingInputT]`
:

`dag_effect: DagEffect`
:

`event_schema: superlinked.framework.common.schema.event_schema_object.EventSchemaObject`
:

`resolved_affected_schema_reference: superlinked.framework.common.dag.resolved_schema_reference.ResolvedSchemaReference`
:

`resolved_affecting_schema_reference: superlinked.framework.common.dag.resolved_schema_reference.ResolvedSchemaReference`
:
```

[PreviousUtil](https://docs.superlinked.com/reference/components/index-7/index) [NextEvent Aggregation Node Util](https://docs.superlinked.com/reference/components/index-7/index/event_aggregation_node_util)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject