---
url: "https://docs.superlinked.com/reference/components/index-4/recency_space"
title: "Recency Space | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-4/recency_space\#classes)    Classes

`RecencySpace(timestamp: superlinked.framework.common.schema.schema_object.Timestamp | None | collections.abc.Sequence[superlinked.framework.common.schema.schema_object.Timestamp | None], time_period_hour_offset: datetime.timedelta = datetime.timedelta(0), period_time_list: list[superlinked.framework.common.dag.period_time.PeriodTime] | superlinked.framework.common.dag.period_time.PeriodTime | None = None, aggregation_mode: superlinked.framework.dsl.space.input_aggregation_mode.InputAggregationMode = InputAggregationMode.INPUT_AVERAGE, negative_filter: float = 0.0)` : Recency space encodes timestamp type data measured in seconds and in unix timestamp format. Recency space is utilized to encode how recent items are. Use period\_time\_list to mark the time periods of interest. Items older than the largest period\_time are going to have uniform recency score. (0 or negative\_filter if set) You can use multiple period\_times to give additional emphasis to sub time periods. Like using 2 days and 5 days gives extra emphasis to the first 2 days. The extent of which can be controlled with the respective weight parameters. Unit weights would give double emphasis on the first 2 days, 1 and 0.1 weights respectively would give tenfold importance to the first 2 days. All items older than 5 days would get 0 or `negative_filter` recency score. Negative\_filter is useful for effectively filtering out entities that are older than the oldest period time. You can think of the value of negative\_filter as it offsets that amount of similarity stemming from other spaces in the index. For example setting it -1 would offset any text similarity that has weight 1 - effectively filtering out all old items however similar they are in terms of their text.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
Attributes:
    timestamp (SpaceFieldSet): A set of Timestamp objects. The actual data is expected to be unix timestamps
        in seconds.
        It is a SchemaFieldObject not regular python ints or floats.
    time_period_hour_offset (timedelta): Starting period time will be set to this hour.
        Day will be the next day of context.now(). Defaults to timedelta(hours=0).
    period_time_list (list[PeriodTime] | None): A list of period time parameters.
        Weights default to 1. Period time to 14 days.
    aggregation_mode (InputAggregationMode): The  aggregation mode of the number embedding.
        Possible values are: maximum, minimum and average. Defaults to InputAggregationMode.INPUT_AVERAGE.
    negative_filter (float): The recency score of items that are older than the oldest period time. Defaults to 0.0.

Initialize the RecencySpace.

Args:
    timestamp (SpaceFieldSet): A set of Timestamp objects. The actual data is expected to be unix timestamps
        in seconds.
        It is a SchemaFieldObject not regular python ints or floats.
    time_period_hour_offset (timedelta): Starting period time will be set to this hour.
        Day will be the next day of context.now(). Defaults to timedelta(hours=0).
    period_time_list (list[PeriodTime] | None): A list of period time parameters.
        Weights default to 1. Period time to 14 days.
    aggregation_mode (InputAggregationMode): The  aggregation mode of the recency embedding.
        Possible values are: maximum, minimum and average. Defaults to InputAggregationMode.INPUT_AVERAGE.
    negative_filter (float): The recency score of items that are older than the oldest period time.
        Defaults to 0.0.

### Ancestors (in MRO)

* superlinked.framework.dsl.space.space.Space
* superlinked.framework.common.space.interface.has_transformation_config.HasTransformationConfig
* superlinked.framework.common.interface.has_length.HasLength
* typing.Generic
* superlinked.framework.dsl.space.has_space_field_set.HasSpaceFieldSet
* abc.ABC

### Instance variables

`allow_similar_clause: bool`
:

`space_field_set: superlinked.framework.dsl.space.space_field_set.SpaceFieldSet`
:

`transformation_config: superlinked.framework.common.space.config.transformation_config.TransformationConfig[int, int]`
:
```

[PreviousCategorical Similarity Space](https://docs.superlinked.com/reference/components/index-4/categorical_similarity_space) [NextSpace Field Set](https://docs.superlinked.com/reference/components/index-4/space_field_set)

Last updated 3 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject