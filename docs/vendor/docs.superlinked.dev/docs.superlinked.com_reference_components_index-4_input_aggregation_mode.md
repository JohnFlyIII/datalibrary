---
url: "https://docs.superlinked.com/reference/components/index-4/input_aggregation_mode"
title: "Input Aggregation Mode | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-4/input_aggregation_mode\#classes)    Classes

`InputAggregationMode(*args, **kwds)` : Create a collection of name/value pairs.

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

`INPUT_AVERAGE`
:

`INPUT_MAXIMUM`
:

`INPUT_MINIMUM`
:
```

[PreviousException](https://docs.superlinked.com/reference/components/index-4/exception) [NextCustom Space](https://docs.superlinked.com/reference/components/index-4/custom_space)

Last updated 8 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject