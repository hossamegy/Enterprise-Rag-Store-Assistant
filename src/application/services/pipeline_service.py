from typing import List

from src.core.ports.base_layer import BaseLayer
from src.core.entities.message_context import MessageContext


class PipelineService:


    def __init__(self, layers: List[BaseLayer]):
        self._layers = layers

    def run(self, context: MessageContext) -> MessageContext:
        for layer in self._layers:
            context = layer.handle(context)
            
        return context
