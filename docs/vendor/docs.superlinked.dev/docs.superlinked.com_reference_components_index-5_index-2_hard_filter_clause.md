---
url: "https://docs.superlinked.com/reference/components/index-5/index-2/hard_filter_clause"
title: "Hard Filter Clause | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-5/index-2/hard_filter_clause\#classes)    Classes

`HardFilterClause(value_param: superlinked.framework.dsl.query.typed_param.TypedParam | superlinked.framework.common.interface.evaluated.Evaluated[superlinked.framework.dsl.query.typed_param.TypedParam], op: ComparisonOperationType, operand: SchemaField, group_key: int | None)`
: HardFilterClause(value\_param: Union\[superlinked.framework.dsl.query.typed\_param.TypedParam, superlinked.framework.common.interface.evaluated.Evaluated\[superlinked.framework.dsl.query.typed\_param.TypedParam\]\], op: 'ComparisonOperationType', operand: 'SchemaField', group\_key: 'int \| None')

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Ancestors (in MRO)

* superlinked.framework.dsl.query.query_clause.single_value_param_query_clause.SingleValueParamQueryClause
* superlinked.framework.dsl.query.query_clause.query_clause.QueryClause
* superlinked.framework.dsl.query.query_clause.query_clause.NLQCompatible
* abc.ABC

### Static methods

`from_param(operation: ComparisonOperation[SchemaField]) ‑> superlinked.framework.dsl.query.query_clause.hard_filter_clause.HardFilterClause`
:

### Instance variables

`group_key: int | None`
:

`is_type_mandatory_in_nlq: bool`
:

`nlq_annotations: list[NLQAnnotation]`
:

`op: superlinked.framework.common.interface.comparison_operation_type.ComparisonOperationType`
:

`operand: superlinked.framework.common.schema.schema_object.SchemaField`
:

### Methods

`get_altered_knn_search_params(self, knn_search_clause_params: KNNSearchClauseParams) ‑> superlinked.framework.dsl.query.clause_params.KNNSearchClauseParams`
:
```

[PreviousRadius Clause](https://docs.superlinked.com/reference/components/index-5/index-2/radius_clause) [NextOverriden Now Clause](https://docs.superlinked.com/reference/components/index-5/index-2/overriden_now_clause)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject