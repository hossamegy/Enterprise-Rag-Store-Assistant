from functools import lru_cache

from src.config.settings import get_vector_settings
from src.infrastructure.vector_store.embedding_function import EmbeddingFunction
from src.infrastructure.vector_store.chroma_db import ChromaDb
from src.application.services.vector_db_service import VectorDbService

@lru_cache(maxsize=1)
def build_embedding_function() -> EmbeddingFunction:
    settings = get_vector_settings()
    return EmbeddingFunction(
        model_id=settings.embedding_model_id,
        device=settings.device,
    )


@lru_cache(maxsize=1)
def build_chroma_db() -> ChromaDb:
    settings = get_vector_settings()
    return ChromaDb(
        collection_name=settings.collection_name,
        persist_directory=settings.persist_directory,
        embedding_function=build_embedding_function(),
    )


@lru_cache(maxsize=1)
def build_vector_db_service() -> VectorDbService:
    return VectorDbService(db=build_chroma_db())
