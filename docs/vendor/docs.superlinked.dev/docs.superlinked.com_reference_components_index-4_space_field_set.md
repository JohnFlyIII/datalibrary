---
url: "https://docs.superlinked.com/reference/components/index-4/space_field_set"
title: "Space Field Set | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-4/space_field_set\#classes)    Classes

`SpaceFieldSet(space: superlinked.framework.dsl.space.space.Space, fields: set[superlinked.framework.common.schema.schema_object.SchemaField], allowed_param_types: collections.abc.Sequence[type] | None = None)`
: A class representing a set of fields in a space.
Attributes:
space (Space): The space.
fields (set\[SchemaField\]): The set of fields.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Ancestors (in MRO)

* typing.Generic

### Descendants

* superlinked.framework.dsl.space.image_space_field_set.ImageDescriptionSpaceFieldSet
* superlinked.framework.dsl.space.image_space_field_set.ImageSpaceFieldSet

### Instance variables

`allowed_param_types: collections.abc.Sequence[type] | None`
:

`field_names_text: Sequence[str]`
:

`fields: set[superlinked.framework.common.schema.schema_object.SchemaField]`
:

`fields_id: str`
:

`input_type: type[~SIT]`
:

`space: superlinked.framework.dsl.space.space.Space`
:

`validated_allowed_param_types: Sequence[type]`
:

### Methods

`get_field_for_schema(self, schema_: Any) ‑> superlinked.framework.common.schema.schema_object.SchemaField | None`
:
```

[PreviousRecency Space](https://docs.superlinked.com/reference/components/index-4/recency_space) [NextQuery](https://docs.superlinked.com/reference/components/index-5)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject