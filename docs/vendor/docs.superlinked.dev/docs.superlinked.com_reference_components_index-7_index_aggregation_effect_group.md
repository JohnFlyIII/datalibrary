---
url: "https://docs.superlinked.com/reference/components/index-7/index/aggregation_effect_group"
title: "Aggregation Effect Group | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-7/index/aggregation_effect_group\#classes)    Classes

`AggregationEffectGroup(space: Space[AggregationInputT, EmbeddingInputT], affected_schema: SchemaObject, effects: Sequence[EffectWithReferencedSchemaObject[AggregationInputT, EmbeddingInputT]])`
: Group of effects with the same space and affected schema.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Ancestors (in MRO)

* typing.Generic

### Static methods

`from_filtered_effects(filtered_effects: Sequence[EffectWithReferencedSchemaObject[AggregationInputT, EmbeddingInputT]]) ‑> superlinked.framework.dsl.index.util.aggregation_effect_group.AggregationEffectGroup[~AggregationInputT, ~EmbeddingInputT]`
:

### Instance variables

`affected_schema: superlinked.framework.common.schema.schema_object.SchemaObject`
:

`effects: Sequence[superlinked.framework.dsl.index.util.effect_with_referenced_schema_object.EffectWithReferencedSchemaObject[~AggregationInputT, ~EmbeddingInputT]]`
:

`space: superlinked.framework.dsl.space.space.Space[~AggregationInputT, ~EmbeddingInputT]`
:
```

[PreviousAggregation Node Util](https://docs.superlinked.com/reference/components/index-7/index/aggregation_node_util) [NextEvent Aggregation Effect Group](https://docs.superlinked.com/reference/components/index-7/index/event_aggregation_effect_group)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject