---
url: "https://docs.superlinked.com/reference/components/dag/period_time"
title: "Period Time | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/dag/period_time\#classes)    Classes

`PeriodTime(period_time: datetime.timedelta, weight: float = 1.0)`
: A class representing a period time parameter.
Attributes:
period\_time (timedelta): Oldest item the parameter will differentiate. Older items will have
0 or `negative_filter` recency\_score.
weight (float): Defaults to 1.0. Useful to tune different period\_times against each other.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
### Instance variables

`period_time: datetime.timedelta`
:

`weight: float`
:
```

[PreviousDag](https://docs.superlinked.com/reference/components/dag) [NextSchema](https://docs.superlinked.com/reference/components/schema)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject