---
url: "https://docs.superlinked.com/reference/components/index-4/custom_space"
title: "Custom Space | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-4/custom_space\#classes)    Classes

`CustomSpace(vector: superlinked.framework.common.schema.schema_object.FloatList | None | collections.abc.Sequence[superlinked.framework.common.schema.schema_object.FloatList | None], length: int, description: str | None = None)` : CustomSpace is the instrument of ingesting your own vectors into Superlinked. This way you can use your own vectors right away. What you need to know: (you can use numbering too) - vectors need to have the same length - vectors will be L2Norm normalized to ensure weighting makes sense - weighting can be performed (query-time) - you are going to need an FloatList typed SchemaField to supply your data - the FloatList field will be able to parse any Sequence\[float \| int\]

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
Initializes a CustomSpace for vector storage and manipulation within Superlinked.

This constructor sets up a space designed for custom vector ingestion, allowing users to specify how these
vectors are aggregated and normalized.

Args:
    vector (FloatList | list[FloatList]): The input vector(s) to be stored in the space.
      This can be a single FloatList SchemaField or a list of those.
    length (int): The fixed length that all vectors in this space must have. This ensures uniformity and
      consistency in vector operations.

### Ancestors (in MRO)

* superlinked.framework.dsl.space.space.Space
* superlinked.framework.common.space.interface.has_transformation_config.HasTransformationConfig
* superlinked.framework.common.interface.has_length.HasLength
* typing.Generic
* superlinked.framework.dsl.space.has_space_field_set.HasSpaceFieldSet
* abc.ABC

### Instance variables

`space_field_set: superlinked.framework.dsl.space.space_field_set.SpaceFieldSet`
:

`transformation_config: superlinked.framework.common.space.config.transformation_config.TransformationConfig[superlinked.framework.common.data_types.Vector, superlinked.framework.common.data_types.Vector]`
:
```

[PreviousInput Aggregation Mode](https://docs.superlinked.com/reference/components/index-4/input_aggregation_mode) [NextCategorical Similarity Space](https://docs.superlinked.com/reference/components/index-4/categorical_similarity_space)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject