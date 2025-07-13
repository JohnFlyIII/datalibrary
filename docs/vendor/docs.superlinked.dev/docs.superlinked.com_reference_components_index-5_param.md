---
url: "https://docs.superlinked.com/reference/components/index-5/param"
title: "Param | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-5/param\#classes)    Classes

`Param(name: str, description: str | None = None, default: ParamInputType | None = None, options: Sequence[ParamInputType | None] | None = None)` : Class representing a parameter that will be provided during the execution of the query.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
Attributes:
    name (str): The unique name of the parameter.
    description (str, optional): Description of the parameter. Used for natural language query.
        Defaults to None.
    default (ParamInputType | None, optional): Value to use if not overridden by query parameter.
        Natural language query will use defaults. Defaults to None.
    options (list[ParamInputType] | set[ParamInputType] | None, optional): Allowed values for this parameter.
        If provided, only these values will be accepted. Defaults to None.

Initialize the Param.

Args:
    name (str): The unique name of the parameter.
    description (str, optional): Description of the parameter. Used for natural language query.
        Defaults to None.
    default (ParamInputType, | None optional): Value to use if not overridden by query parameter.
        Natural language query will use defaults. Defaults to None.
    options (list[ParamInputType] | set[ParamInputType] | None, optional): Allowed values for this parameter.
        If provided, only these values will be accepted. Defaults to None.

### Static methods

`init_default(default: ParamInputType | None = None) ‑> superlinked.framework.dsl.query.param.Param`
:
```

[PreviousQuery Filter Validator](https://docs.superlinked.com/reference/components/index-5/query_filter_validator) [NextQuery Filters](https://docs.superlinked.com/reference/components/index-5/query_filters)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject