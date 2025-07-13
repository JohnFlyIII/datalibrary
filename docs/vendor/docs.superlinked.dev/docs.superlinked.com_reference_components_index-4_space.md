---
url: "https://docs.superlinked.com/reference/components/index-4/space"
title: "Space | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-4/space\#classes)    Classes

`Space(fields: Sequence[SchemaField], type_: type | TypeAlias)` : Abstract base class for a space.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
This class defines the interface for a space in the context of the application.

### Ancestors (in MRO)

* superlinked.framework.common.space.interface.has_transformation_config.HasTransformationConfig
* superlinked.framework.common.interface.has_length.HasLength
* typing.Generic
* abc.ABC

### Descendants

* superlinked.framework.dsl.space.categorical_similarity_space.CategoricalSimilaritySpace
* superlinked.framework.dsl.space.custom_space.CustomSpace
* superlinked.framework.dsl.space.image_space.ImageSpace
* superlinked.framework.dsl.space.number_space.NumberSpace
* superlinked.framework.dsl.space.recency_space.RecencySpace
* superlinked.framework.dsl.space.text_similarity_space.TextSimilaritySpace

### Instance variables

`allow_similar_clause: bool`
:

`annotation: str`
:

`length: int`
:
```

[PreviousNumber Space](https://docs.superlinked.com/reference/components/index-4/number_space) [NextImage Space](https://docs.superlinked.com/reference/components/index-4/image_space)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject