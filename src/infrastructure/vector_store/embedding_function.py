from chromadb import EmbeddingFunction as ChromaEmbeddingFunction
from sentence_transformers import SentenceTransformer

class EmbeddingFunction(ChromaEmbeddingFunction):

    def __init__(self, model_id: str, device: str):
        self._model = SentenceTransformer(model_id, device=device)

    def __call__(self, input: list) -> list:
        return self._model.encode(input).tolist()