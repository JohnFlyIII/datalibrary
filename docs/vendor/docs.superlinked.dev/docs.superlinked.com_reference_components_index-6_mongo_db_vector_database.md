---
url: "https://docs.superlinked.com/reference/components/index-6/mongo_db_vector_database"
title: "Mongo Db Vector Database | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-6/mongo_db_vector_database\#classes)    Classes

`MongoDBVectorDatabase(host: str, db_name: str, cluster_name: str, project_id: str, admin_api_user: str, admin_api_password: str, default_query_limit: int = 10, **extra_params: Any)` : MongoDB implementation of the VectorDatabase.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
This class provides a MongoDB-based vector database connector.

Initialize the MongoDBVectorDatabase.

Args:
    host (str): The hostname of the MongoDB server.
    db_name (str): The name of the database.
    cluster_name (str): The name of the MongoDB cluster.
    project_id (str): The project ID for MongoDB.
    admin_api_user (str): The admin API username.
    admin_api_password (str): The admin API password.
    default_query_limit (int): Default vector search limit,
        MongoDB does not have a default for it so setting it to a reasonable number of 10.
    **extra_params (Any): Additional parameters for the MongoDB connection.

### Ancestors (in MRO)

* superlinked.framework.dsl.storage.vector_database.VectorDatabase
* abc.ABC
* typing.Generic
```

[PreviousRedis Vector Database](https://docs.superlinked.com/reference/components/index-6/redis_vector_database) [NextVector Database](https://docs.superlinked.com/reference/components/index-6/vector_database)

Last updated 8 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject