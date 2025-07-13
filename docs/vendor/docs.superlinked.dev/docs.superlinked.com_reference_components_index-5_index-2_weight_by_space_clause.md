---
url: "https://docs.superlinked.com/reference/components/index-5/index-2/weight_by_space_clause"
title: "Weight By Space Clause | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-5/index-2/weight_by_space_clause\#classes)    Classes

`WeightBySpaceClause(space_weight_map: SpaceWeightMap = <factory>)`
: WeightBySpaceClause(space\_weight\_map: 'SpaceWeightMap' = )

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Ancestors (in MRO)

* superlinked.framework.dsl.query.query_clause.query_clause.QueryClause
* superlinked.framework.dsl.query.query_clause.query_clause.NLQCompatible
* abc.ABC

### Static methods

`from_params(weight_param_by_space: Mapping[Space, NumericParamType], all_space: Sequence[Space]) ‑> superlinked.framework.dsl.query.query_clause.weight_by_space_clause.WeightBySpaceClause`
:

### Instance variables

`annotation_by_space_annotation: dict[str, str]`
:

`params: Sequence[TypedParam | Evaluated[TypedParam]]`
:

`space_weight_map: superlinked.framework.dsl.query.query_clause.space_weight_map.SpaceWeightMap`
:

### Methods

`add_missing_space_weight_params(self, all_space: Sequence[Space]) ‑> Self`
:

`extend(self, weight_param_by_space: Mapping[Space, NumericParamType], all_space: Sequence[Space]) ‑> Self`
:

`get_altered_query_vector_params(self, query_vector_params: QueryVectorClauseParams, index_node_id: str, query_schema: IdSchemaObject, storage_manager: StorageManager) ‑> superlinked.framework.dsl.query.clause_params.QueryVectorClauseParams`
:

`get_space_weight_param_name_by_space(self) ‑> dict[superlinked.framework.dsl.space.space.Space, str]`
:
```

[PreviousNlq Clause](https://docs.superlinked.com/reference/components/index-5/index-2/nlq_clause) [NextRadius Clause](https://docs.superlinked.com/reference/components/index-5/index-2/radius_clause)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject