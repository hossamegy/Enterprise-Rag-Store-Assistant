from src.core.entities.message_context import MessageContext
from src.core.ports.base_layer import BaseLayer
from src.core.ports.base_cache import BaseCache

class SaveCacheLayer(BaseLayer):

    def __init__(self, cache: BaseCache):
        self._cache = cache

    def handle(self, context: MessageContext) -> MessageContext:
        if context.processed_question and context.response and (not context.is_cached):
            self._cache.save(question=context.processed_question, answer=context.response, model_type='llm', related_ids=context.retrieved_doc_ids)
            context.layer_outputs['save_cache'] = 'SAVED'
        else:
            context.layer_outputs['save_cache'] = 'SKIPPED'
        return context