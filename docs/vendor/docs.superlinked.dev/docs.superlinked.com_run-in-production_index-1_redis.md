---
url: "https://docs.superlinked.com/run-in-production/index-1/redis"
title: "Redis | Superlinked Docs"
---

This document provides clear steps on how to use and integrate Redis with Superlinked.

## [Direct link to heading](https://docs.superlinked.com/run-in-production/index-1/redis\#configuring-your-existing-managed-redis)    Configuring your existing managed Redis

To use Superlinked with Redis, you will need several Redis modules. The simplest approach is to use the official Redis Stack, which includes all the necessary modules. Installation instructions for the Redis Stack can be found in the [Redis official documentation](https://redis.io/docs/latest/operate/oss_and_stack/install/install-stack/). Alternatively, you can start a managed instance provided by Redis (a free-tier is available). For detailed steps on initiating a managed instance, refer to the [Start a Managed Redis Instance](https://docs.superlinked.com/run-in-production/index-1/redis#start-a-managed-redis-instance) section below.

Once your Redis instance is up and running, ensure it is accessible from the server that will use it. Additionally, configure the necessary authentication settings as described below.

## [Direct link to heading](https://docs.superlinked.com/run-in-production/index-1/redis\#modifications-in-your-configuration)    Modifications in your configuration

To integrate Redis, you need to add the `RedisVectorDatabase` class and include it in the executor. Here’s how you can do it:

To configure your Redis, the following code will help you:

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
from superlinked import framework as sl

vector_database = sl.RedisVectorDatabase(
    "<your_redis_host>", # (Mandatory) This is your Redis' URL without any port or extra fields.
    12315, # (Mandatory) This is the port and it must be an integer.
    default_query_limit=10, # This optional parameter specifies the maximum number of query results returned. If not set, it defaults to 10.
    # These params must be in a form of kwarg params. Here you can specify anything that the official python client
    # enables. The params can be found here: https://redis.readthedocs.io/en/stable/connections.html. Below you can see a very basic user-pass authentication as an example.
    username="test",
    password="password"
)
```

Once you have configured the vector database just simply set it as your vector database.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
...
executor = sl.RestExecutor(
    sources=[source],
    indices=[index],
    queries=[sl.RestQuery(sl.RestDescriptor("query"), query)],
    vector_database=vector_database, # Or any variable that you assigned your `RedisVectorDatabase`
)
...
```

## [Direct link to heading](https://docs.superlinked.com/run-in-production/index-1/redis\#start-a-managed-redis-instance)    Start a Managed Redis Instance

To initiate a managed Redis instance, navigate to [Redis Labs](https://app.redislabs.com/), sign in, and click the "New Database" button. On the ensuing page, locate the `Type` selector, which offers two options: `Redis Stack` and `Memcached`. By default, `Redis Stack` is pre-selected, which is the correct choice. If it is not selected, ensure to choose `Redis Stack`. For basic usage, no further configuration is necessary. Redis already generated a user which is called `default` and a password that you can see below it. However, if you intend to use the instance for persistent data storage beyond sandbox purposes, consider configuring High Availability (HA), data persistence, and other relevant settings.

## [Direct link to heading](https://docs.superlinked.com/run-in-production/index-1/redis\#example-app-with-redis)    Example app with Redis

You can find an example that utilizes Redis [here](https://github.com/superlinked/superlinked/blob/main/docs/run-in-production/vdbs/redis/app_with_redis.py).

[PreviousSupported Vector Databases](https://docs.superlinked.com/run-in-production/index-1) [NextMongo DB](https://docs.superlinked.com/run-in-production/index-1/mongodb)

Last updated 5 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject