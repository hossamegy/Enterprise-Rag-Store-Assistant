from src.core.ports.base_vector_store import BaseVectorStore
from src.core.exceptions.domain_exceptions import VectorStoreOperationException

class SearchService:

    def __init__(self, db: BaseVectorStore):
        self._db = db

    def search(self, query: str, top_k: int=10) -> dict:
        try:
            return self._db.query(query_texts=[query], top_k=top_k)
        except Exception as e:
            raise VectorStoreOperationException(message=f'Semantic search failed for query: {query}', detail=str(e))