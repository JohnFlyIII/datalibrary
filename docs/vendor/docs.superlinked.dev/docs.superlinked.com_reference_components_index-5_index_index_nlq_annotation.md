---
url: "https://docs.superlinked.com/reference/components/index-5/index/index/nlq_annotation"
title: "Nlq Annotation | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-5/index/index/nlq_annotation\#classes)    Classes

`NLQAnnotation(annotation: str, annotation_type: superlinked.framework.dsl.query.nlq.param_filler.nlq_annotation.NLQAnnotationType)`
: NLQAnnotation(annotation: str, annotation\_type: superlinked.framework.dsl.query.nlq.param\_filler.nlq\_annotation.NLQAnnotationType)

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Instance variables

`annotation: str`
:

`annotation_type: superlinked.framework.dsl.query.nlq.param_filler.nlq_annotation.NLQAnnotationType`
:
```

`NLQAnnotationType(*args, **kwds)`
: Create a collection of name/value pairs.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
Example enumeration:

>>> class Color(Enum):
...     RED = 1
...     BLUE = 2
...     GREEN = 3

Access them by:

- attribute access::

>>> Color.RED
<Color.RED: 1>

- value lookup:

>>> Color(1)
<Color.RED: 1>

- name lookup:

>>> Color['RED']
<Color.RED: 1>

Enumerations can be iterated over, and know how many members they have:

>>> len(Color)
3

>>> list(Color)
[<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]

Methods can be added to enumerations, and members can have their own
attributes -- see the documentation for details.

### Ancestors (in MRO)

* enum.Enum

### Class variables

`EXACT_VALUE_REQUIRED`
:

`SPACE_AFFECTING`
:
```

[PreviousQuery Param Model Validator Info](https://docs.superlinked.com/reference/components/index-5/index/index/query_param_model_validator_info) [NextQuery Param Model Validator](https://docs.superlinked.com/reference/components/index-5/index/index/query_param_model_validator)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject