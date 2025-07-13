---
url: "https://docs.superlinked.com/reference/components/index-7/index/event_aggregation_effect_group"
title: "Event Aggregation Effect Group | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-7/index/event_aggregation_effect_group\#classes)    Classes

`EventAggregationEffectGroup(key: GroupKey[AggregationInputT, EmbeddingInputT], effects: Sequence[EffectWithReferencedSchemaObject])`
: Group of effects with the same space, event schema, affected schema and affecting schema.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Ancestors (in MRO)

* typing.Generic

### Static methods

`group_by_event_and_affecting_schema(effects: Sequence[EffectWithReferencedSchemaObject[AggregationInputT, EmbeddingInputT]]) ‑> list[superlinked.framework.dsl.index.util.event_aggregation_effect_group.EventAggregationEffectGroup[~AggregationInputT, ~EmbeddingInputT]]`
:

### Instance variables

`effects: Sequence[superlinked.framework.dsl.index.util.effect_with_referenced_schema_object.EffectWithReferencedSchemaObject]`
:

`key: superlinked.framework.dsl.index.util.event_aggregation_effect_group.GroupKey[~AggregationInputT, ~EmbeddingInputT]`
:
```

`GroupKey(space: Space[AggregationInputT, EmbeddingInputT], event_schema: EventSchemaObject, resolved_affected_schema_reference: ResolvedSchemaReference, resolved_affecting_schema: IdSchemaObject, resolved_affecting_reference_field: SchemaReference)`
: GroupKey(space: 'Space\[AggregationInputT, EmbeddingInputT\]', event\_schema: 'EventSchemaObject', resolved\_affected\_schema\_reference: 'ResolvedSchemaReference', resolved\_affecting\_schema: 'IdSchemaObject', resolved\_affecting\_reference\_field: 'SchemaReference')

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Ancestors (in MRO)

* typing.Generic

### Instance variables

`event_schema: superlinked.framework.common.schema.event_schema_object.EventSchemaObject`
:

`resolved_affected_schema_reference: superlinked.framework.common.dag.resolved_schema_reference.ResolvedSchemaReference`
:

`resolved_affecting_reference_field: superlinked.framework.common.schema.event_schema_object.SchemaReference`
:

`resolved_affecting_schema: superlinked.framework.common.schema.id_schema_object.IdSchemaObject`
:

`space: superlinked.framework.dsl.space.space.Space[~AggregationInputT, ~EmbeddingInputT]`
:
```

[PreviousAggregation Effect Group](https://docs.superlinked.com/reference/components/index-7/index/aggregation_effect_group) [NextOverview](https://docs.superlinked.com/recipes/overview)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject