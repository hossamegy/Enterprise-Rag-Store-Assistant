import asyncio
import time
from fastapi import APIRouter, Depends
from src.api.schemas import ChatRequestDTO, ChatResponseDTO
from src.core.entities.message_context import MessageContext
from src.application.services.pipeline_service import PipelineService
from src.di.nlp_di import build_nlp_pipeline
from src.config.logger import logger

chat_router = APIRouter(prefix='/chat', tags=['chat'])

@chat_router.post('/', summary='Send a message to the chatbot pipeline', response_model=ChatResponseDTO)
async def chat_endpoint(request: ChatRequestDTO, pipeline: PipelineService=Depends(build_nlp_pipeline)):
    logger.info(f'Chat request received: {request.message[:50]}...')
    start_time = time.time()
    context = MessageContext(question=request.message)
    processed_context = await asyncio.to_thread(pipeline.run, context)
    end_time = time.time()
    generation_time = end_time - start_time
    logger.info(f'Response generated in {generation_time:.2f}s')
    input_tokens_est = max(1, len(request.message) // 4)
    return ChatResponseDTO(response=processed_context.response or 'No response generated.', intent=processed_context.question_intent or 'Unknown', complexity=processed_context.question_complexity or 'Unknown', is_cached=processed_context.is_cached, layer_outputs=processed_context.layer_outputs, context=processed_context.retrieved_context, generation_time=round(generation_time, 2), input_tokens_est=input_tokens_est)

@chat_router.delete('/clear_cache', summary='Remove the semantic cache directory')
async def clear_cache():
    import shutil
    import os
    cache_dir = 'src/_db_cache'
    if os.path.exists(cache_dir):
        try:
            shutil.rmtree(cache_dir, ignore_errors=True)
            return {'status': 'Cache deleted'}
        except Exception as e:
            return {'status': 'Error', 'detail': str(e)}
    return {'status': 'Cache directory not found'}