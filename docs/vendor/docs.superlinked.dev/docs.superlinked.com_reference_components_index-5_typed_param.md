---
url: "https://docs.superlinked.com/reference/components/index-5/typed_param"
title: "Typed Param | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-5/typed_param\#classes)    Classes

`SchemaFieldToStrConverter()`
: Abstract base class for generic types.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
A generic type is typically declared by inheriting from
this class parameterized with one or more type variables.
For example, a generic mapping type might be defined as::

  class Mapping(Generic[KT, VT]):
      def __getitem__(self, key: KT) -> VT:
          ...
      # Etc.

This class can then be used as follows::

  def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
      try:
          return mapping[key]
      except KeyError:
          return default

### Ancestors (in MRO)

* superlinked.framework.common.interface.type_converter.TypeConverter
* typing.Generic
* abc.ABC

### Methods

`convert(self, base: SchemaField) ‑> str`
:
```

`TypedParam(param: Param, valid_param_value_types: Sequence[TypeDescriptor])`
: TypedParam(param: 'Param', valid\_param\_value\_types: 'Sequence\[TypeDescriptor\]')

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Static methods

`from_unchecked_types(param: Param, valid_param_value_types: Sequence[type]) ‑> superlinked.framework.dsl.query.typed_param.TypedParam`
:

`init_default(valid_param_value_types: Sequence[type], default: ParamInputType | None = None) ‑> superlinked.framework.dsl.query.typed_param.TypedParam`
:

`init_evaluated(valid_param_value_types: Sequence[type], value: Any) ‑> superlinked.framework.common.interface.evaluated.Evaluated[superlinked.framework.dsl.query.typed_param.TypedParam]`
:

### Instance variables

`param: superlinked.framework.dsl.query.param.Param`
:

`valid_param_value_types: Sequence[superlinked.framework.common.type_descriptor.TypeDescriptor]`
:

### Methods

`evaluate(self, value: Any) ‑> superlinked.framework.common.interface.evaluated.Evaluated[superlinked.framework.dsl.query.typed_param.TypedParam]`
:
```

[PreviousQuery Filters](https://docs.superlinked.com/reference/components/index-5/query_filters) [NextQuery Param Information](https://docs.superlinked.com/reference/components/index-5/query_param_information)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject