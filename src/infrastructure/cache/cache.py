from src.core.ports.base_cache import BaseCache
from src.core.ports.base_vector_store import BaseVectorStore

class Cache(BaseCache):

    def __init__(self, vector_store: BaseVectorStore):
        self.vector_store = vector_store

    def save(self, question: str, answer: str, model_type: str, related_ids: list) -> None:
        metadata = {'answer': answer, 'model_type': model_type}
        if related_ids:
            for rid in related_ids:
                metadata[f'rel_id_{rid}'] = True
        self.vector_store.add(documents=[question], metadatas=[metadata])

    def similar_question_score(self, question: str) -> float:
        result = self.vector_store.query(query_texts=[question], top_k=1)
        distances = result.get('distances', [[]])
        if distances and distances[0]:
            return distances[0][0]
        return float('inf')

    def get_answer(self, question: str) -> str:
        result = self.vector_store.query(query_texts=[question], top_k=1)
        metadatas = result.get('metadatas', [[]])
        if metadatas and metadatas[0]:
            return metadatas[0][0].get('answer', '')
        return ''

    def delete_cached_question(self, ids: list) -> None:
        for id_val in ids:
            self.vector_store.delete_by_metadata_filter({f'rel_id_{id_val}': True})