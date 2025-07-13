---
url: "https://docs.superlinked.com/reference/components/index-5/index/nlq_compatible_clause_handler"
title: "Nlq Compatible Clause Handler | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-5/index/nlq_compatible_clause_handler\#classes)    Classes

`NLQCompatibleClauseHandler(clause: QueryClause)`
: NLQCompatibleClauseHandler(clause: 'QueryClause')

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Ancestors (in MRO)

* superlinked.framework.dsl.query.query_clause.query_clause.NLQCompatible
* abc.ABC

### Static methods

`from_clauses(clauses: Sequence[QueryClause]) ‑> list[superlinked.framework.dsl.query.nlq.nlq_compatible_clause_handler.NLQCompatibleClauseHandler]`
:

### Instance variables

`annotation_by_space_annotation: dict[str, str]`
:

`clause: superlinked.framework.dsl.query.query_clause.query_clause.QueryClause`
:

`is_type_mandatory_in_nlq: bool`
:

`nlq_annotations: list[NLQAnnotation]`
:

`nlq_compatible_clause: NLQCompatible`
:

### Methods

`get_allowed_values(self, param: TypedParam | Evaluated[TypedParam]) ‑> set[collections.abc.Sequence[str] | collections.abc.Sequence[float] | PIL.Image.Image | str | int | float | bool | tuple[str | None, str | None] | None]`
:
```

[PreviousNlq](https://docs.superlinked.com/reference/components/index-5/index) [NextNlq Handler](https://docs.superlinked.com/reference/components/index-5/index/nlq_handler)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject