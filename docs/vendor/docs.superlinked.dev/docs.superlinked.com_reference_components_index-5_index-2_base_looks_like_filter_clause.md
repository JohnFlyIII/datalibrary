---
url: "https://docs.superlinked.com/reference/components/index-5/index-2/base_looks_like_filter_clause"
title: "Base Looks Like Filter Clause | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-5/index-2/base_looks_like_filter_clause\#classes)    Classes

`BaseLooksLikeFilterClause(value_param: superlinked.framework.dsl.query.typed_param.TypedParam | superlinked.framework.common.interface.evaluated.Evaluated[superlinked.framework.dsl.query.typed_param.TypedParam], schema_field: IdField)`
: BaseLooksLikeFilterClause(value\_param: Union\[superlinked.framework.dsl.query.typed\_param.TypedParam, superlinked.framework.common.interface.evaluated.Evaluated\[superlinked.framework.dsl.query.typed\_param.TypedParam\]\], schema\_field: 'IdField')

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Ancestors (in MRO)

* superlinked.framework.dsl.query.query_clause.query_clause.NLQCompatible
* superlinked.framework.dsl.query.query_clause.single_value_param_query_clause.SingleValueParamQueryClause
* superlinked.framework.dsl.query.query_clause.query_clause.QueryClause
* abc.ABC

### Descendants

* superlinked.framework.dsl.query.query_clause.looks_like_filter_clause.LooksLikeFilterClause
* superlinked.framework.dsl.query.query_clause.looks_like_filter_clause_weights_by_space.LooksLikeFilterClauseWeightBySpace

### Instance variables

`schema_field: superlinked.framework.common.schema.id_field.IdField`
:

### Methods

`get_altered_query_vector_params(self, query_vector_params: QueryVectorClauseParams, index_node_id: str, query_schema: IdSchemaObject, storage_manager: StorageManager) ‑> superlinked.framework.dsl.query.clause_params.QueryVectorClauseParams`
:
```

[PreviousLimit Clause](https://docs.superlinked.com/reference/components/index-5/index-2/limit_clause) [NextNlq Clause](https://docs.superlinked.com/reference/components/index-5/index-2/nlq_clause)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject