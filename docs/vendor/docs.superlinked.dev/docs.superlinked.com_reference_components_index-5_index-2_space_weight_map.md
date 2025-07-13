---
url: "https://docs.superlinked.com/reference/components/index-5/index-2/space_weight_map"
title: "Space Weight Map | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-5/index-2/space_weight_map\#classes)    Classes

`SpaceWeightMap(space_weights: Mapping[superlinked.framework.dsl.space.space.Space, superlinked.framework.dsl.query.typed_param.TypedParam | superlinked.framework.common.interface.evaluated.Evaluated[superlinked.framework.dsl.query.typed_param.TypedParam]] = <factory>)`
: SpaceWeightMap(space\_weights: collections.abc.Mapping\[superlinked.framework.dsl.space.space.Space, typing.Union\[superlinked.framework.dsl.query.typed\_param.TypedParam, superlinked.framework.common.interface.evaluated.Evaluated\[superlinked.framework.dsl.query.typed\_param.TypedParam\]\]\] = )

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Ancestors (in MRO)

* collections.abc.Mapping
* collections.abc.Collection
* collections.abc.Sized
* collections.abc.Iterable
* collections.abc.Container

### Instance variables

`params: Sequence[superlinked.framework.dsl.query.typed_param.TypedParam | superlinked.framework.common.interface.evaluated.Evaluated[superlinked.framework.dsl.query.typed_param.TypedParam]]`
:

`space_weights: Mapping[superlinked.framework.dsl.space.space.Space, superlinked.framework.dsl.query.typed_param.TypedParam | superlinked.framework.common.interface.evaluated.Evaluated[superlinked.framework.dsl.query.typed_param.TypedParam]]`
:

### Methods

`alter_param_values(self, param_values: Mapping[str, collections.abc.Sequence[str] | collections.abc.Sequence[float] | PIL.Image.Image | str | int | float | bool | tuple[str | None, str | None] | None], is_override_set: bool) ‑> Self | None`
:

`extend(self, weight_param_by_space: Mapping[superlinked.framework.dsl.space.space.Space, float | int | superlinked.framework.dsl.query.param.Param], all_space: Sequence[superlinked.framework.dsl.space.space.Space]) ‑> Self`
:

`set_param_name_if_unset(self, prefix: str) ‑> None`
:
```

[PreviousLooks Like Filter Clause Weights By Space](https://docs.superlinked.com/reference/components/index-5/index-2/looks_like_filter_clause_weights_by_space) [NextSingle Value Param Query Clause](https://docs.superlinked.com/reference/components/index-5/index-2/single_value_param_query_clause)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject