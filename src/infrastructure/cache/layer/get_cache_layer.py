from src.config.settings import get_nlp_settings
from src.core.ports.base_layer import BaseLayer
from src.core.ports.base_cache import BaseCache
from src.core.entities.message_context import MessageContext

class GetCacheLayer(BaseLayer):

    def __init__(self, cache: BaseCache):
        self._cache = cache
         
    def handle(self, context: MessageContext) -> MessageContext:
        if not context.question:
            return context
        score = self._cache.similar_question_score(context.question)
        if score < get_nlp_settings().confidence_threshold:
            cached_answer = self._cache.get_answer(context.question)
            context.cached_response = cached_answer
            context.response = cached_answer
            context.is_cached = True
            context.layer_outputs['cache'] = 'HIT'
        else:
            context.layer_outputs['cache'] = 'MISS'
        return context