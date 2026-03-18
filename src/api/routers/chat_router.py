from fastapi import APIRouter, Depends
from src.api.schemas import ChatRequestDTO, ChatResponseDTO
from src.core.entities.message_context import MessageContext
from src.application.services.pipeline_service import PipelineService
from src.di.nlp_di import build_nlp_pipeline

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", summary="Send a message to the chatbot pipeline", response_model=ChatResponseDTO)
def chat_endpoint(
    request: ChatRequestDTO,
    pipeline: PipelineService = Depends(build_nlp_pipeline),
):
    context = MessageContext(question=request.message)
    processed_context = pipeline.run(context)

    return ChatResponseDTO(
        response=processed_context.response or "No response generated.",
        intent=processed_context.question_intent or "Unknown",
        complexity=processed_context.question_complexity or "Unknown",
        is_cached=processed_context.is_cached,
        layer_outputs=processed_context.layer_outputs,
        context=processed_context.retrieved_context,
    )
