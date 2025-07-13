---
url: "https://docs.superlinked.com/reference/components/index-5/index-2/looks_like_filter_clause_weights_by_space"
title: "Looks Like Filter Clause Weights By Space | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-5/index-2/looks_like_filter_clause_weights_by_space\#classes)    Classes

`LooksLikeFilterClauseWeightBySpace(value_param: superlinked.framework.dsl.query.typed_param.TypedParam | superlinked.framework.common.interface.evaluated.Evaluated[superlinked.framework.dsl.query.typed_param.TypedParam], schema_field: IdField, space_weight_map: SpaceWeightMap = <factory>)`
: LooksLikeFilterClauseWeightBySpace(value\_param: Union\[superlinked.framework.dsl.query.typed\_param.TypedParam, superlinked.framework.common.interface.evaluated.Evaluated\[superlinked.framework.dsl.query.typed\_param.TypedParam\]\], schema\_field: 'IdField', space\_weight\_map: 'SpaceWeightMap' = )

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Ancestors (in MRO)

* superlinked.framework.dsl.query.query_clause.base_looks_like_filter_clause.BaseLooksLikeFilterClause
* superlinked.framework.dsl.query.query_clause.query_clause.NLQCompatible
* superlinked.framework.dsl.query.query_clause.single_value_param_query_clause.SingleValueParamQueryClause
* superlinked.framework.dsl.query.query_clause.query_clause.QueryClause
* abc.ABC

### Static methods

`from_param(id_: IdField, id_param: StringParamType, weight: Mapping[Space, NumericParamType]) ‑> superlinked.framework.dsl.query.query_clause.looks_like_filter_clause_weights_by_space.LooksLikeFilterClauseWeightBySpace`
:

### Instance variables

`nlq_annotations: list[NLQAnnotation]`
:

`params: Sequence[TypedParam | Evaluated[TypedParam]]`
:

`space_weight_map: superlinked.framework.dsl.query.query_clause.space_weight_map.SpaceWeightMap`
:

### Methods

`get_default_value_by_param_name(self) ‑> dict[str, typing.Any]`
:

`get_weight_param_name_by_space(self) ‑> dict[superlinked.framework.dsl.space.space.Space | None, str]`
:

`set_defaults_for_nlq(self) ‑> Self`
:
```

[PreviousSimilar Filter Clause](https://docs.superlinked.com/reference/components/index-5/index-2/similar_filter_clause) [NextSpace Weight Map](https://docs.superlinked.com/reference/components/index-5/index-2/space_weight_map)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject