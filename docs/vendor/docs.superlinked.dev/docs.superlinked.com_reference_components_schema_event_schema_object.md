---
url: "https://docs.superlinked.com/reference/components/schema/event_schema_object"
title: "Event Schema Object | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/schema/event_schema_object\#classes)    Classes

`CreatedAtField(schema_obj: SchemaObjectT, created_at_field_name: str)` : A class representing creation time. A unix timestamp field in a schema object.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Ancestors (in MRO)

* superlinked.framework.common.schema.schema_object.SchemaField
* superlinked.framework.common.interface.comparison_operand.ComparisonOperand
* abc.ABC
* typing.Generic

### Instance variables

`supported_comparison_operation_types: Sequence[ComparisonOperationType]`
:

### Methods

`as_type(self, value: Any) ‑> int`
:
```

`EventSchemaObject(base_cls: type, id_field_name: str, created_at_field_name: str)` : Custom decorated event schema class. Event schemas can be used to reference other schema and to define interactions between schemas.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Ancestors (in MRO)

* superlinked.framework.common.schema.id_schema_object.IdSchemaObject
* superlinked.framework.common.schema.schema_object.SchemaObject
* abc.ABC

### Descendants

* superlinked.framework.common.schema.event_schema.EventSchema

### Static methods

`get_schema_field_type() ‑> types.UnionType`
:

### Instance variables

`created_at: CreatedAtField`
:
```

`MultipliedSchemaReference(schema_reference: SchemaReference[RST], multiplier: float = 1.0)` : Helper class that provides a standard way to create an ABC using inheritance.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Ancestors (in MRO)

* superlinked.framework.common.interface.has_multiplier.HasMultiplier
* abc.ABC
* typing.Generic
```

`SchemaReference(name: str, schema_obj: EventSchemaObject, referenced_schema: type[RST])` : Schema reference used within an `EventSchema` to reference other schemas.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Ancestors (in MRO)

* superlinked.framework.common.schema.schema_object.SchemaField
* superlinked.framework.common.interface.comparison_operand.ComparisonOperand
* superlinked.framework.common.interface.has_multiplier.HasMultiplier
* abc.ABC
* typing.Generic

### Instance variables

`supported_comparison_operation_types: Sequence[ComparisonOperationType]`
:
```

[PreviousId Schema Object](https://docs.superlinked.com/reference/components/schema/id_schema_object) [NextParser](https://docs.superlinked.com/reference/components/parser)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject