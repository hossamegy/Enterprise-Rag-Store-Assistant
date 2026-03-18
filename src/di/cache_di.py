from functools import lru_cache

from src.config.settings import get_vector_settings
from src.infrastructure.vector_store.embedding_function import EmbeddingFunction
from src.infrastructure.vector_store.chroma_db import ChromaDb
from src.infrastructure.cache.cache import Cache
from src.infrastructure.cache.layer.save_cache_layer import SaveCacheLayer
from src.infrastructure.cache.layer.get_cache_layer import GetCacheLayer


@lru_cache(maxsize=1)
def build_cache_embedding_function() -> EmbeddingFunction:
    settings = get_vector_settings()
    return EmbeddingFunction(
        model_id=settings.cache_embedding_model_id,
        device=settings.device,
    )


@lru_cache(maxsize=1)
def build_cache_chroma_db() -> ChromaDb:
    settings = get_vector_settings()
    return ChromaDb(
        collection_name=settings.cache_collection_name,
        persist_directory=settings.cache_persist_directory,
        embedding_function=build_cache_embedding_function(),
    )


@lru_cache(maxsize=1)
def build_cache() -> Cache:
    return Cache(vector_store=build_cache_chroma_db())


@lru_cache(maxsize=1)
def build_get_cache_layer() -> GetCacheLayer:
    return GetCacheLayer(cache=build_cache())


@lru_cache(maxsize=1)
def build_save_cache_layer() -> SaveCacheLayer:
    return SaveCacheLayer(cache=build_cache())
