from typing import List
from src.core.ports.base_layer import BaseLayer
from src.core.entities.message_context import MessageContext
from src.config.logger import logger
from src.core.exceptions.domain_exceptions import InferenceException

class PipelineService:

    def __init__(self, layers: List[BaseLayer]):
        self._layers = layers

    def run(self, context: MessageContext) -> MessageContext:
        logger.info(f'Starting pipeline execution for question: {context.question[:50]}...')
        for layer in self._layers:
            layer_name = layer.__class__.__name__
            try:
                logger.info(f'Executing layer: {layer_name}')
                context = layer.handle(context)
            except Exception as e:
                logger.error(f'Critical failure in pipeline layer {layer_name}: {str(e)}', exc_info=True)
                raise InferenceException(message=f'An error occurred during the {layer_name} stage of processing.', detail=str(e))
        logger.info('Pipeline execution completed.')
        return context