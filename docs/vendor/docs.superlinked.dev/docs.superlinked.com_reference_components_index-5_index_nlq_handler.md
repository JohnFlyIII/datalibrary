---
url: "https://docs.superlinked.com/reference/components/index-5/index/nlq_handler"
title: "Nlq Handler | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-5/index/nlq_handler\#classes)    Classes

`NLQHandler(client_config: superlinked.framework.common.nlq.open_ai.OpenAIClientConfig)` :

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Methods

`fill_params(self, natural_query: str, clauses: Sequence[superlinked.framework.dsl.query.query_clause.query_clause.QueryClause], space_weight_param_info: superlinked.framework.dsl.query.space_weight_param_info.SpaceWeightParamInfo, system_prompt: str | None = None) ‑> dict[str, typing.Any]`
:

`suggest_improvements(self, clauses: Sequence[superlinked.framework.dsl.query.query_clause.query_clause.QueryClause], space_weight_param_info: superlinked.framework.dsl.query.space_weight_param_info.SpaceWeightParamInfo, natural_query: str | None, feedback: str | None, system_prompt: str | None = None) ‑> superlinked.framework.dsl.query.nlq.suggestion.query_suggestion_model.QuerySuggestionsModel`
:
```

[PreviousNlq Compatible Clause Handler](https://docs.superlinked.com/reference/components/index-5/index/nlq_compatible_clause_handler) [NextException](https://docs.superlinked.com/reference/components/index-5/index/exception)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject