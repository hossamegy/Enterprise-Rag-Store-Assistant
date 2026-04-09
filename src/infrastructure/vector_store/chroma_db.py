import chromadb
from chromadb import Collection
from src.core.ports.base_vector_store import BaseVectorStore
from src.infrastructure.vector_store.embedding_function import EmbeddingFunction

class ChromaDb(BaseVectorStore):

    def __init__(self, collection_name: str, persist_directory: str, embedding_function: EmbeddingFunction):
        self._collection: Collection = self._resolve_collection(collection_name=collection_name, persist_directory=persist_directory, embedding_function=embedding_function)

    @staticmethod
    def _resolve_collection(collection_name: str, persist_directory: str, embedding_function: EmbeddingFunction) -> Collection:
        client = chromadb.PersistentClient(path=persist_directory)
        existing = [col.name for col in client.list_collections()]
        if collection_name in existing:
            return client.get_collection(name=collection_name, embedding_function=embedding_function)
        return client.create_collection(name=collection_name, embedding_function=embedding_function)

    def add(self, documents: list, metadatas: list=None, ids: list=None) -> None:
        if ids is None:
            import uuid
            ids = [str(uuid.uuid4()) for _ in range(len(documents))]
        self._collection.add(documents=documents, metadatas=metadatas, ids=ids)

    def query(self, query_texts: list, top_k: int=5) -> dict:
        count = self._collection.count()
        if count == 0:
            return {'documents': [[]], 'metadatas': [[]], 'distances': [[]]}
        n_res = min(top_k, count)
        return self._collection.query(query_texts=query_texts, n_results=n_res)

    def delete(self, ids: list) -> None:
        self._collection.delete(ids=ids)

    def update(self, ids: list, documents: list=None, metadatas: list=None) -> None:
        self._collection.update(ids=ids, documents=documents, metadatas=metadatas)

    def delete_by_metadata_filter(self, filter_dict: dict) -> None:
        results = self._collection.get(where=filter_dict)
        ids_to_delete = results.get('ids', [])
        if ids_to_delete:
            self.delete(ids=ids_to_delete)