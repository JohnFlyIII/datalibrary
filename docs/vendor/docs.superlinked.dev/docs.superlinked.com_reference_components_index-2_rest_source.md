---
url: "https://docs.superlinked.com/reference/components/index-2/rest_source"
title: "Rest Source | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-2/rest_source\#classes)    Classes

`RestSource(schema: ~IdSchemaObjectT, parser: superlinked.framework.common.parser.data_parser.DataParser | None = None, rest_descriptor: superlinked.framework.dsl.executor.rest.rest_descriptor.RestDescriptor | None = None)` : Abstract base class for generic types.

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

* superlinked.framework.online.source.online_source.OnlineSource
* superlinked.framework.common.observable.TransformerPublisher
* superlinked.framework.common.source.source.Source
* typing.Generic

### Instance variables

`path: str`
:
```

[PreviousData Loader Source](https://docs.superlinked.com/reference/components/index-2/data_loader_source) [NextRegistry](https://docs.superlinked.com/reference/components/index-3)

Last updated 8 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject