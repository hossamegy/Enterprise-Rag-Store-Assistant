from src.core.ports.base_classfier_model import BaseClassfierModel
from src.core.ports.base_layer import BaseLayer
from src.core.entities.message_context import MessageContext

class IntentClassifierLayer(BaseLayer):

    def __init__(self, model: BaseClassfierModel, confidence_threshold: float):
        self._CONFIDENCE_THRESHOLD = confidence_threshold
        self._model = model

    def handle(self, context: MessageContext) -> MessageContext:
        if context.is_cached:
            return context
        pred_intent, max_prob = self._model.predict(context.processed_question)
        if max_prob < self._CONFIDENCE_THRESHOLD:
            context.question_intent = f'unknown (confidence: {max_prob:.2f})'
        else:
            context.question_intent = pred_intent
        context.layer_outputs['question_intent'] = context.question_intent
        return context