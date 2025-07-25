---
url: "https://docs.superlinked.com/reference/components/index-1/index-1/rest_configuration"
title: "Rest Configuration | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-1/index-1/rest_configuration\#classes)    Classes

`RestEndpointConfiguration(**data: Any)`
: !!! abstract "Usage Documentation" [Models](https://github.com/superlinked/superlinked/blob/main/docs/reference/dsl/executor/concepts/models.md)

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
A base class for creating Pydantic models.

Attributes:
    __class_vars__: The names of the class variables defined on the model.
    __private_attributes__: Metadata about the private attributes of the model.
    __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.

    __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
    __pydantic_core_schema__: The core schema of the model.
    __pydantic_custom_init__: Whether the model has a custom `__init__` function.
    __pydantic_decorators__: Metadata containing the decorators defined on the model.
        This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
    __pydantic_generic_metadata__: Metadata for generic models; contains data used for a similar purpose to
        __args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these.
    __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
    __pydantic_post_init__: The name of the post-init method for the model, if defined.
    __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
    __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
    __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.

    __pydantic_fields__: A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
    __pydantic_computed_fields__: A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.

    __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
        is set to `'allow'`.
    __pydantic_fields_set__: The names of fields explicitly set during instantiation.
    __pydantic_private__: Values of private attributes set on the model instance.

Create a new model by parsing and validating input data from keyword arguments.

Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
validated to form a valid model.

`self` is explicitly positional-only to allow `self` as a field name.

### Ancestors (in MRO)

* superlinked.framework.common.util.immutable_model.ImmutableBaseModel
* pydantic.main.BaseModel

### Class variables

`api_root_path: str`
:

`ingest_path_prefix: str`
:

`model_config`
:

`query_path_prefix: str`
:

### Static methods

`add_slash_to_api_root_path(values: dict) ‑> dict`
:
```

`RestQuery(rest_descriptor: superlinked.framework.dsl.executor.rest.rest_descriptor.RestDescriptor, query_descriptor: superlinked.framework.dsl.query.query_descriptor.QueryDescriptor)`
: RestQuery(rest\_descriptor: superlinked.framework.dsl.executor.rest.rest\_descriptor.RestDescriptor, query\_descriptor: superlinked.framework.dsl.query.query\_descriptor.QueryDescriptor)

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Instance variables

`path: str | None`
:

`query_descriptor: superlinked.framework.dsl.query.query_descriptor.QueryDescriptor`
:

`rest_descriptor: superlinked.framework.dsl.executor.rest.rest_descriptor.RestDescriptor`
:
```

[PreviousRest Handler](https://docs.superlinked.com/reference/components/index-1/index-1/rest_handler) [NextQuery](https://docs.superlinked.com/reference/components/index-1/index-2)

Last updated 2 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject