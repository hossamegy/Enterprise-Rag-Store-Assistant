from src.core.entities.message_context import MessageContext
from src.core.ports.base_layer import BaseLayer
from src.core.ports.base_vector_store import BaseVectorStore
from src.application.services.context_formatter import ContextFormatter

class RetrieveContextLayer(BaseLayer):

    def __init__(self, vector_db: BaseVectorStore, formatter: ContextFormatter):
        self._vector_db = vector_db
        self._formatter = formatter

    def handle(self, context: MessageContext) -> MessageContext:
        if not context.processed_question:
            context.layer_outputs['retrieve_context'] = 'SKIPPED (no processed question)'
            return context
        results = self._vector_db.query(query_texts=[context.processed_question], top_k=3)
        context.retrieved_doc_ids = results.get('ids', [[]])[0]
        context.retrieved_context = self._formatter.format(results)
        context.layer_outputs['retrieve_context'] = context.retrieved_context
        return context