---
url: "https://docs.superlinked.com/reference/components/index-5/index-1/binary_predicate"
title: "Binary Predicate | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-5/index-1/binary_predicate\#classes)    Classes

`LooksLikePredicate(left_param: superlinked.framework.common.schema.schema_object.SchemaField, right_param: collections.abc.Sequence[str] | collections.abc.Sequence[float] | PIL.Image.Image | str | int | float | bool | None | tuple[str | None, str | None] | superlinked.framework.dsl.query.param.Param, weight: float | int | superlinked.framework.dsl.query.param.Param)` : QueryPredicate(op: ~OPT, params: list\[superlinked.framework.common.schema.schema\_object.SchemaField \| superlinked.framework.dsl.query.param.Param \| collections.abc.Sequence\[str\] \| collections.abc.Sequence\[float\] \| PIL.Image.Image \| str \| int \| float \| None \| tuple\[str \| None, str \| None\]\], weight\_param: float \| int \| superlinked.framework.dsl.query.param.Param)

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Ancestors (in MRO)

* superlinked.framework.dsl.query.predicate.binary_predicate.BinaryPredicate
* superlinked.framework.dsl.query.predicate.query_predicate.QueryPredicate
* typing.Generic
```

`SimilarPredicate(left_param: superlinked.framework.common.schema.schema_object.SchemaField, right_param: collections.abc.Sequence[str] | collections.abc.Sequence[float] | PIL.Image.Image | str | int | float | bool | None | tuple[str | None, str | None] | superlinked.framework.dsl.query.param.Param, weight: float | int | superlinked.framework.dsl.query.param.Param, left_param_node: superlinked.framework.common.dag.node.Node)` : QueryPredicate(op: ~OPT, params: list\[superlinked.framework.common.schema.schema\_object.SchemaField \| superlinked.framework.dsl.query.param.Param \| collections.abc.Sequence\[str\] \| collections.abc.Sequence\[float\] \| PIL.Image.Image \| str \| int \| float \| None \| tuple\[str \| None, str \| None\]\], weight\_param: float \| int \| superlinked.framework.dsl.query.param.Param)

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Ancestors (in MRO)

* superlinked.framework.dsl.query.predicate.binary_predicate.BinaryPredicate
* superlinked.framework.dsl.query.predicate.query_predicate.QueryPredicate
* typing.Generic
```

[PreviousPredicate](https://docs.superlinked.com/reference/components/index-5/index-1) [NextQuery Predicate](https://docs.superlinked.com/reference/components/index-5/index-1/query_predicate)

Last updated 7 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject