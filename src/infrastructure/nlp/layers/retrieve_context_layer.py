from src.core.entities.message_context import MessageContext
from src.core.ports.base_layer import BaseLayer
from src.application.services.vector_db_service import VectorDbService

class RetrieveContextLayer(BaseLayer):
    """
    Retrieves relevant documents from the vector store based on the user's question.
    Requires: context.processed_question to be set.
    """

    def __init__(self, vector_db_service: VectorDbService):
        self._vector_db_service = vector_db_service

    def handle(self, context: MessageContext) -> MessageContext:
        if not context.processed_question:
            context.layer_outputs["retrieve_context"] = "SKIPPED (no processed question)"
            return context

        # Retrieve top 5 similar documents
        results = self._vector_db_service.query(
            query_texts=[context.processed_question],
            top_k=5,
        )

        # Format retrieved documents as context
        context.retrieved_context = self._format_retrieved_context(results)
        context.layer_outputs["retrieve_context"] = context.retrieved_context
        return context

    def _format_retrieved_context(self, results: dict) -> str:
        """Format retrieved documents into a context string for the LLM."""
        if not results or not results.get("documents") or not results["documents"][0]:
            return "No relevant documents found."

        context_parts = []
        distances = results.get("distances", [[]])[0]
        for i, (doc, distance) in enumerate(zip(results["documents"][0], distances)):
            context_parts.append(f"Document {i+1} (distance: {distance:.4f}):\n{doc}")

        return "\n\n".join(context_parts)