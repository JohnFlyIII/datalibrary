---
url: "https://docs.superlinked.com/reference/components/index-4/text_similarity_space"
title: "Text Similarity Space | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-4/text_similarity_space\#functions)    Functions

`chunk(text: superlinked.framework.common.schema.schema_object.String, chunk_size: int | None = None, chunk_overlap: int | None = None, split_chars_keep: list[str] | None = None, split_chars_remove: list[str] | None = None) ‑> superlinked.framework.common.dag.chunking_node.ChunkingNode`
: Create smaller chunks from the given text, a String SchemaFieldObject. It is helpful when you search
for more granular information in your text corpus. It is recommended to try different chunk\_sizes to
find what fits best your use-case. Chunking respects word boundaries.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
    Args:
        text (String): The String field the text of which is to be chunked.
        chunk_size (int | None, optional): The maximum size of each chunk in characters. Defaults to None, which means
        effectively using 250.
        chunk_overlap (int | None, optional): The maximum overlap between chunks in characters. Defaults to None, which
        means effectively using {}.
        split_chars_keep: Characters to split at, but also keep in the text. Should be characters that can signal
        meaningful breakpoints in the text. Effectively defaults to ["!", "?", "."].
        split_chars_remove: Characters to split at and remove from the text. Should be characters that can signal
        meaningful breakpoints in the text. Effectively defaults to ["\
"].

    Returns:
        ChunkingNode: The chunking node.
```

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-4/text_similarity_space\#classes)    Classes

`TextSimilaritySpace(text: superlinked.framework.common.schema.schema_object.String | superlinked.framework.common.dag.chunking_node.ChunkingNode | None | collections.abc.Sequence[superlinked.framework.common.schema.schema_object.String | superlinked.framework.common.dag.chunking_node.ChunkingNode | None], model: str, cache_size: int = 10000, model_cache_dir: pathlib.Path | None = None, model_handler: superlinked.framework.common.space.embedding.model_based.model_handler.TextModelHandler = TextModelHandler.SENTENCE_TRANSFORMERS, embedding_engine_config: superlinked.framework.common.space.embedding.model_based.engine.embedding_engine_config.EmbeddingEngineConfig | None = None)`
: A text similarity space is used to create vectors from documents in order to search in them
later on. We only support (SentenceTransformers)\[https://www.sbert.net/\] models as they have
finetuned pooling to encode longer text sequences most efficiently.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
Initialize the TextSimilaritySpace.

Args:
    text (TextInput | list[TextInput]): The Text input or a list of Text inputs.
        It is a SchemaFieldObject (String), not a regular python string.
    model (str): The model used for text similarity.
    cache_size (int): The number of embeddings to be stored in an inmemory LRU cache.
        Set it to 0, to disable caching. Defaults to 10000.
    model_cache_dir (Path | None, optional): Directory to cache downloaded models.
        If None, uses the default cache directory. Defaults to None.
    model_handler (TextModelHandler, optional): The handler for the model,
        Defaults to ModelHandler.SENTENCE_TRANSFORMERS.
    embedding_engine_config (EmbeddingEngineConfig, optional): Configuration for the embedding engine.
        Defaults to EmbeddingEngineConfig().

### Ancestors (in MRO)

* superlinked.framework.dsl.space.space.Space
* superlinked.framework.common.space.interface.has_transformation_config.HasTransformationConfig
* superlinked.framework.common.interface.has_length.HasLength
* typing.Generic
* superlinked.framework.dsl.space.has_space_field_set.HasSpaceFieldSet
* abc.ABC

### Instance variables

`space_field_set: superlinked.framework.dsl.space.space_field_set.SpaceFieldSet`
:

`transformation_config: superlinked.framework.common.space.config.transformation_config.TransformationConfig[superlinked.framework.common.data_types.Vector, str]`
:
```

[PreviousImage Space Field Set](https://docs.superlinked.com/reference/components/index-4/image_space_field_set) [NextNumber Space](https://docs.superlinked.com/reference/components/index-4/number_space)

Last updated 16 days ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject