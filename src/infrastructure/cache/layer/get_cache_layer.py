from src.core.ports.base_layer import BaseLayer
from src.core.ports.base_cache import BaseCache
from src.core.entities.message_context import MessageContext

# Distance threshold: ChromaDB cosine distance – lower means more similar.
# 0.25 means "within 75% semantic similarity" → treat as a cache hit.
_CACHE_HIT_THRESHOLD = 0.25


class GetCacheLayer(BaseLayer):
    """
    First layer in the pipeline.
    Checks the vector cache for a semantically similar previous question.
    On a hit: populates context.cached_response and sets context.is_cached = True
              so downstream heavy layers (classifiers + LLM) can short-circuit.
    On a miss: passes context through unchanged.
    """

    def __init__(self, cache: BaseCache):
        self._cache = cache

    def handle(self, context: MessageContext) -> MessageContext:
        if not context.question:
            return context

        score = self._cache.similar_question_score(context.question)

        if score < _CACHE_HIT_THRESHOLD:
            cached_answer = self._cache.get_answer(context.question)
            context.cached_response = cached_answer
            context.response = cached_answer
            context.is_cached = True
            context.layer_outputs["cache"] = "HIT"
        else:
            context.layer_outputs["cache"] = "MISS"

        return context