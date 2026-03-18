from src.core.entities.message_context import MessageContext
from src.core.ports.base_layer import BaseLayer
from src.core.ports.local_llm import LocalLLM


class LocalLLMLayer(BaseLayer):
    """
    Calls the locally-hosted LLM (Qwen2.5) to generate a RAG answer.
    Only executes when the request was NOT served by the cache.
    Requires: context.question_intent and context.retrieved_context to be set.
    """

    def __init__(self, model: LocalLLM):
        self._model = model

    def handle(self, context: MessageContext) -> MessageContext:
        # Short-circuit: cache already provided the answer
        if context.is_cached:
            context.layer_outputs["llm"] = "SKIPPED (cache hit)"
            return context

        context.response = self._model.rag_answer(
            question_intent=context.question_intent,
            processed_question=context.processed_question,
            retrieved_context=context.retrieved_context or "",
        )
        context.layer_outputs["llm"] = context.response
        return context
