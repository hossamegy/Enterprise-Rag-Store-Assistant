import logging
from src.core.entities.message_context import MessageContext
from src.core.ports.base_layer import BaseLayer
from src.core.ports.local_llm import LocalLLM
from src.infrastructure.nlp.llm.gemini_llm import LLMUnavailableError

logger = logging.getLogger(__name__)

class GeminiLLMLayer(BaseLayer):

    def __init__(self, model: LocalLLM):
        self._model = model

    def handle(self, context: MessageContext) -> MessageContext:
        if context.is_cached:
            context.layer_outputs['Gemini'] = 'SKIPPED (cache hit)'
            return context
        if context.question_complexity != 'simple':
            try:
                context.response = self._model.rag_answer(
                    question_intent=context.question_intent, 
                    processed_question=context.processed_question, 
                    retrieved_context=context.retrieved_context or ''
                )
                context.layer_outputs['llm'] = context.response
            except LLMUnavailableError as e:
                logger.error(f"Gemini API fallback triggered: {e}")
                context.response = "عذراً، أواجه حالياً ضغطاً كبيراً في الطلبات. يرجى المحاولة مرة أخرى بعد قليل."
                context.layer_outputs['llm'] = context.response
            
        return context