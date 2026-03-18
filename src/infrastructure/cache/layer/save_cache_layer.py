from src.core.entities.message_context import MessageContext
from src.core.ports.base_layer import BaseLayer
from src.core.ports.base_cache import BaseCache


class SaveCacheLayer(BaseLayer):
    """
    Last layer in the pipeline.
    Persists the LLM-generated Q+A pair to the vector cache so subsequent
    semantically-similar questions can be answered instantly.
    Skips saving if the answer was already served from cache.
    """

    def __init__(self, cache: BaseCache):
        self._cache = cache

    def handle(self, context: MessageContext) -> MessageContext:
        # Only persist when: we have both a question, a fresh LLM response,
        # and this was NOT already a cache hit.
        if context.processed_question and context.response and not context.is_cached:
            self._cache.save(
                question=context.processed_question,
                answer=context.response,
                model_type="llm",
            )
            context.layer_outputs["save_cache"] = "SAVED"
        else:
            context.layer_outputs["save_cache"] = "SKIPPED"

        return context
