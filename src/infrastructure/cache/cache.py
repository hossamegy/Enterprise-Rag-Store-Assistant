from src.core.ports.base_cache import BaseCache
from src.core.ports.base_vector_store import BaseVectorStore


class Cache(BaseCache):
    def __init__(self, vector_store: BaseVectorStore):
        self.vector_store = vector_store

    def save(self, question: str, answer: str, model_type: str) -> None:
        self.vector_store.add(
            documents=[question],
            metadatas=[{"answer": answer, "model_type": model_type}],
        )

    def similar_question_score(self, question: str) -> float:
        result = self.vector_store.query(query_texts=[question], top_k=1)
        distances = result.get("distances", [[]])
        if distances and distances[0]:
            return distances[0][0]
        return float("inf")  # no cache entry → treat as miss

    def get_answer(self, question: str) -> str:
        result = self.vector_store.query(query_texts=[question], top_k=1)
        metadatas = result.get("metadatas", [[]])
        if metadatas and metadatas[0]:
            return metadatas[0][0].get("answer", "")
        return ""