from src.core.ports.base_classfier_model import BaseClassfierModel
from src.core.ports.base_layer import BaseLayer
from src.core.entities.message_context import MessageContext


class ComplexityClassifierLayer(BaseLayer):

    def __init__(self, model: BaseClassfierModel, confidence_threshold: float):
        self._CONFIDENCE_THRESHOLD = confidence_threshold
        self._model = model

    def handle(self, context: MessageContext) -> MessageContext:
        # Short-circuit: skip expensive classifier call on cache hit
        if context.is_cached:
            return context

        pred_complexity, max_prob = self._model.predict(context.processed_question)

        if max_prob < self._CONFIDENCE_THRESHOLD:
            context.question_complexity = f"unknown (confidence: {max_prob:.2f})"
        else:
            context.question_complexity = pred_complexity

        context.layer_outputs["question_complexity"] = context.question_complexity
        return context
