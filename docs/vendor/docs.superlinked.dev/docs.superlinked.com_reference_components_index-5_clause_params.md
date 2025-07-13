---
url: "https://docs.superlinked.com/reference/components/index-5/clause_params"
title: "Clause Params | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-5/clause_params\#classes)    Classes

`KNNSearchClauseParams(limit: int | None = None, filters: Sequence[ComparisonOperation[SchemaField]] = <factory>, schema_fields_to_return: Sequence[SchemaField] = <factory>, radius: float | None = None, should_return_index_vector: bool = False)`
: KNNSearchClauseParams(limit: 'int \| None' = None, filters: 'Sequence\[ComparisonOperation\[SchemaField\]\]' = , schema\_fields\_to\_return: 'Sequence\[SchemaField\]' = , radius: 'float \| None' = None, should\_return\_index\_vector: 'bool' = False)

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Instance variables

`filters: Sequence[superlinked.framework.common.interface.comparison_operand.ComparisonOperation[superlinked.framework.common.schema.schema_object.SchemaField]]`
:

`limit: int | None`
:

`radius: float | None`
:

`schema_fields_to_return: Sequence[superlinked.framework.common.schema.schema_object.SchemaField]`
:

`should_return_index_vector: bool`
:

### Methods

`set_params(self, **params: Any) ‑> superlinked.framework.dsl.query.clause_params.KNNSearchClauseParams`
:
```

`MetadataExtractionClauseParams(vector_part_ids: Sequence[str] = <factory>)`
: MetadataExtractionClauseParams(vector\_part\_ids: 'Sequence\[str\]' = )

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Instance variables

`vector_part_ids: Sequence[str]`
:
```

`NLQClauseParams(client_config: OpenAIClientConfig | None = None, natural_query: str | None = None, system_prompt: str | None = None)`
: NLQClauseParams(client\_config: 'OpenAIClientConfig \| None' = None, natural\_query: 'str \| None' = None, system\_prompt: 'str \| None' = None)

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Instance variables

`client_config: superlinked.framework.common.nlq.open_ai.OpenAIClientConfig | None`
:

`natural_query: str | None`
:

`system_prompt: str | None`
:
```

`QueryVectorClauseParams(weight_by_space: Mapping[Space, float] = <factory>, context_time: int | None = None, query_node_inputs_by_node_id: Mapping[str, list[QueryNodeInput]] = <factory>)`
: QueryVectorClauseParams(weight\_by\_space: 'Mapping\[Space, float\]' = , context\_time: 'int \| None' = None, query\_node\_inputs\_by\_node\_id: 'Mapping\[str, list\[QueryNodeInput\]\]' = )

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Instance variables

`context_time: int | None`
:

`query_node_inputs_by_node_id: Mapping[str, list[superlinked.framework.query.query_node_input.QueryNodeInput]]`
:

`weight_by_space: Mapping[superlinked.framework.dsl.space.space.Space, float]`
:

### Methods

`set_params(self, **params: Any) ‑> superlinked.framework.dsl.query.clause_params.QueryVectorClauseParams`
:
```

[PreviousQuery Weighting](https://docs.superlinked.com/reference/components/index-5/query_weighting) [NextNlq Pydantic Model Builder](https://docs.superlinked.com/reference/components/index-5/nlq_pydantic_model_builder)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject