---
url: "https://docs.superlinked.com/reference/components/index-5/index-2/select_clause"
title: "Select Clause | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-5/index-2/select_clause\#classes)    Classes

`SelectClause(value_param: superlinked.framework.dsl.query.typed_param.TypedParam | superlinked.framework.common.interface.evaluated.Evaluated[superlinked.framework.dsl.query.typed_param.TypedParam], schema: IdSchemaObject, vector_parts: Sequence[Space])`
: SelectClause(value\_param: Union\[superlinked.framework.dsl.query.typed\_param.TypedParam, superlinked.framework.common.interface.evaluated.Evaluated\[superlinked.framework.dsl.query.typed\_param.TypedParam\]\], schema: 'IdSchemaObject', vector\_parts: 'Sequence\[Space\]')

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Ancestors (in MRO)

* superlinked.framework.dsl.query.query_clause.single_value_param_query_clause.SingleValueParamQueryClause
* superlinked.framework.dsl.query.query_clause.query_clause.QueryClause
* abc.ABC

### Static methods

`from_param(schema: IdSchemaObject, fields: Param | Sequence[str], vector_parts: Sequence[Space]) ‑> superlinked.framework.dsl.query.query_clause.select_clause.SelectClause`
:

### Instance variables

`schema: superlinked.framework.common.schema.id_schema_object.IdSchemaObject`
:

`vector_parts: Sequence[superlinked.framework.dsl.space.space.Space]`
:

### Methods

`get_altered_knn_search_params(self, knn_search_clause_params: KNNSearchClauseParams) ‑> superlinked.framework.dsl.query.clause_params.KNNSearchClauseParams`
:

`get_altered_metadata_extraction_params(self, metadata_extraction_params: MetadataExtractionClauseParams) ‑> superlinked.framework.dsl.query.clause_params.MetadataExtractionClauseParams`
:
```

[PreviousLooks Like Filter Clause](https://docs.superlinked.com/reference/components/index-5/index-2/looks_like_filter_clause) [NextSimilar Filter Clause](https://docs.superlinked.com/reference/components/index-5/index-2/similar_filter_clause)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject