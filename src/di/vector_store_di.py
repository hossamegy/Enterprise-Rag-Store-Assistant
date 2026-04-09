from functools import lru_cache
from src.config.settings import get_vector_settings
from src.infrastructure.vector_store.embedding_function import EmbeddingFunction
from src.infrastructure.vector_store.chroma_db import ChromaDb

@lru_cache(maxsize=1)
def build_embedding_function() -> EmbeddingFunction:
    settings = get_vector_settings()
    return EmbeddingFunction(model_id=settings.embedding_model_id, device=settings.device)

@lru_cache(maxsize=1)
def build_chroma_db() -> ChromaDb:
    settings = get_vector_settings()
    return ChromaDb(collection_name=settings.collection_name, persist_directory=settings.persist_directory, embedding_function=build_embedding_function())
from src.application.services.product_service import ProductService
from src.application.services.order_service import OrderService
from src.application.services.search_service import SearchService

@lru_cache(maxsize=1)
def build_product_service() -> ProductService:
    return ProductService(db=build_chroma_db())

@lru_cache(maxsize=1)
def build_order_service() -> OrderService:
    return OrderService(db=build_chroma_db())

@lru_cache(maxsize=1)
def build_search_service() -> SearchService:
    return SearchService(db=build_chroma_db())