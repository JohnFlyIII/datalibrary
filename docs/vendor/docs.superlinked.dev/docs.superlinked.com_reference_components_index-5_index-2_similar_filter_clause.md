---
url: "https://docs.superlinked.com/reference/components/index-5/index-2/similar_filter_clause"
title: "Similar Filter Clause | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-5/index-2/similar_filter_clause\#classes)    Classes

`SimilarFilterClause(value_param: superlinked.framework.dsl.query.typed_param.TypedParam | superlinked.framework.common.interface.evaluated.Evaluated[superlinked.framework.dsl.query.typed_param.TypedParam], weight_param: TypedParam | Evaluated[TypedParam], field_set: SpaceFieldSet)`
: SimilarFilterClause(value\_param: Union\[superlinked.framework.dsl.query.typed\_param.TypedParam, superlinked.framework.common.interface.evaluated.Evaluated\[superlinked.framework.dsl.query.typed\_param.TypedParam\]\], weight\_param: 'TypedParam \| Evaluated\[TypedParam\]', field\_set: 'SpaceFieldSet')

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Ancestors (in MRO)

* superlinked.framework.dsl.query.query_clause.single_value_param_query_clause.SingleValueParamQueryClause
* superlinked.framework.dsl.query.query_clause.query_clause.QueryClause
* superlinked.framework.dsl.query.query_clause.query_clause.NLQCompatible
* abc.ABC

### Static methods

`from_param(spaces: Sequence[Space], field_set: SpaceFieldSet, param: ParamType, weight: NumericParamType) ‑> superlinked.framework.dsl.query.query_clause.similar_filter_clause.SimilarFilterClause`
:

### Instance variables

`annotation_by_space_annotation: dict[str, str]`
:

`field_set: superlinked.framework.dsl.space.space_field_set.SpaceFieldSet`
:

`params: Sequence[TypedParam | Evaluated[TypedParam]]`
:

`weight_param: superlinked.framework.dsl.query.typed_param.TypedParam | superlinked.framework.common.interface.evaluated.Evaluated[superlinked.framework.dsl.query.typed_param.TypedParam]`
:

### Methods

`get_allowed_values(self, param: TypedParam | Evaluated[TypedParam]) ‑> set[collections.abc.Sequence[str] | collections.abc.Sequence[float] | PIL.Image.Image | str | int | float | bool | tuple[str | None, str | None] | None]`
:

`get_altered_query_vector_params(self, query_vector_params: QueryVectorClauseParams, index_node_id: str, query_schema: IdSchemaObject, storage_manager: StorageManager) ‑> superlinked.framework.dsl.query.clause_params.QueryVectorClauseParams`
:

`get_default_value_by_param_name(self) ‑> dict[str, typing.Any]`
:

`get_weight_param_name_by_space(self) ‑> dict[superlinked.framework.dsl.space.space.Space | None, str]`
:
```

[PreviousSelect Clause](https://docs.superlinked.com/reference/components/index-5/index-2/select_clause) [NextLooks Like Filter Clause Weights By Space](https://docs.superlinked.com/reference/components/index-5/index-2/looks_like_filter_clause_weights_by_space)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject