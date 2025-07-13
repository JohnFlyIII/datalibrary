---
url: "https://docs.superlinked.com/reference/components/index-4/image_space"
title: "Image Space | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-4/image_space\#classes)    Classes

`ImageSpace(image: superlinked.framework.common.schema.schema_object.Blob | superlinked.framework.common.schema.schema_object.DescribedBlob | None | collections.abc.Sequence[superlinked.framework.common.schema.schema_object.Blob | superlinked.framework.common.schema.schema_object.DescribedBlob | None], model: str = 'clip-ViT-B-32', model_handler: superlinked.framework.common.space.embedding.model_based.model_handler.ModelHandler = ModelHandler.SENTENCE_TRANSFORMERS, model_cache_dir: pathlib.Path | None = None, embedding_engine_config: superlinked.framework.common.space.embedding.model_based.engine.embedding_engine_config.EmbeddingEngineConfig | None = None)`
: Initialize the ImageSpace instance for generating vector representations
from images, supporting models from the OpenCLIP project.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
Args:
    image (Blob | DescribedBlob | Sequence[Blob | DescribedBlob]):
        The image content as a Blob or DescribedBlob (write image+description), or a sequence of them.
    model (str, optional): The model identifier for generating image embeddings.
        Defaults to "clip-ViT-B-32".
    model_handler (ModelHandler, optional): The handler for the model,
        defaults to ModelHandler.SENTENCE_TRANSFORMERS.
    model_cache_dir (Path | None, optional): Directory to cache downloaded models.
        If None, uses the default cache directory. Defaults to None.
    embedding_engine_config (EmbeddingEngineConfig, optional): Configuration for the embedding engine.
        Defaults to EmbeddingEngineConfig().

Raises:
    InvalidSpaceParamException: If the image and description fields are not
        from the same schema.

Initialize the ImageSpace instance for generating vector representations
from images, supporting models from the OpenCLIP project.

Args:
    image (Blob | DescribedBlob | Sequence[Blob | DescribedBlob]):
        The image content as a Blob or DescribedBlob (write image+description), or a sequence of them.
    model (str, optional): The model identifier for generating image embeddings.
        Defaults to "clip-ViT-B-32".
    model_handler (ModelHandler, optional): The handler for the model,
        defaults to ModelHandler.SENTENCE_TRANSFORMERS.
    model_cache_dir (Path | None, optional): Directory to cache downloaded models.
        If None, uses the default cache directory. Defaults to None.
    embedding_engine_config (EmbeddingEngineConfig, optional): Configuration for the embedding engine.
        Defaults to EmbeddingEngineConfig().

Raises:
    InvalidSpaceParamException: If the image and description fields are not
        from the same schema.

### Ancestors (in MRO)

* superlinked.framework.dsl.space.space.Space
* superlinked.framework.common.space.interface.has_transformation_config.HasTransformationConfig
* superlinked.framework.common.interface.has_length.HasLength
* typing.Generic
* abc.ABC

### Instance variables

`transformation_config: superlinked.framework.common.space.config.transformation_config.TransformationConfig[superlinked.framework.common.data_types.Vector, superlinked.framework.common.schema.image_data.ImageData]`
:
```

[PreviousSpace](https://docs.superlinked.com/reference/components/index-4/space) [NextException](https://docs.superlinked.com/reference/components/index-4/exception)

Last updated 16 days ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject