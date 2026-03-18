from src.core.ports.base_layer import BaseLayer
from src.core.entities.message_context import MessageContext


class PreprocessingLayer(BaseLayer):
    """
    Cleans and normalizes raw Arabic (and English) text.
    Responsibilities: strip punctuation, lowercase, deduplicate words.
    Skips processing entirely if the question was already served from cache.
    """
    import string
    import re

    EN_PUNCT = string.punctuation
    AR_PUNCT = "،؛؟٪«»…٭٬"
    ALL_PUNCT = EN_PUNCT + AR_PUNCT

    def handle(self, context: MessageContext) -> MessageContext:
        # Short-circuit: no need to preprocess if cache already answered
        if context.is_cached:
            return context

        if not context.question or not context.question.strip():
            context.processed_question = None
            return context

        import re
        text = context.question.strip().lower()
        text = text.translate(str.maketrans('', '', self.ALL_PUNCT))
        text = re.sub(r'\s+', ' ', text).strip()

        words = text.split()
        deduped_words = list(dict.fromkeys(words))

        context.processed_question = ' '.join(deduped_words)
        context.layer_outputs["preprocessing"] = context.processed_question
        return context
