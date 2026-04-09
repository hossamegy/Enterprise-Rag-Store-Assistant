from functools import lru_cache
import os
from src.infrastructure.nlp.llm.gemini_llm import GeminiLLmImpl
from src.di.vector_store_di import build_chroma_db
from src.infrastructure.nlp.classfiers.classfierModel import ClassfierModel
from src.infrastructure.nlp.layers.complexity_classifier_layer import ComplexityClassifierLayer
from src.infrastructure.nlp.layers.intent_classifier_layer import IntentClassifierLayer
from src.infrastructure.nlp.layers.preprocessing_layer import PreprocessingLayer
from src.infrastructure.nlp.layers.retrieve_context_layer import RetrieveContextLayer
from src.infrastructure.nlp.layers.local_llm_layer import LocalLLMLayer
from src.infrastructure.nlp.layers.gemini_llm_layer import GeminiLLMLayer

from src.infrastructure.nlp.llm.local_llm import LocalLLmImpl
from src.config.settings import get_nlp_settings
from src.application.services.pipeline_service import PipelineService
from src.di.cache_di import build_get_cache_layer, build_save_cache_layer
from src.application.services.context_formatter import ContextFormatter

@lru_cache(maxsize=1)
def build_intent_model() -> ClassfierModel:
    settings = get_nlp_settings()
    return ClassfierModel(
        bert_model_path=settings.intent_bert_model_path, 
        model_path=settings.intent_model_path, 
        tokenizer_path=settings.tokenizer_path, 
        classes_path=settings.intent_label_encoder_path, 
        num_classes=settings.intent_num_classes, 
        device=settings.device
    )

@lru_cache(maxsize=1)
def build_complexity_model() -> ClassfierModel:
    settings = get_nlp_settings()
    return ClassfierModel(
        bert_model_path=settings.question_complexity_bert_model_path, 
        model_path=settings.question_complexity_model_path, 
        tokenizer_path=settings.tokenizer_path, 
        classes_path=settings.question_complexity_label_encoder_path, 
        num_classes=settings.question_complexity_num_classes, 
        device=settings.device
    )

@lru_cache(maxsize=1)
def build_local_llm_rag() -> LocalLLmImpl:
    settings = get_nlp_settings()
    return LocalLLmImpl(
        model_id=settings.LLM_id, 
        device=settings.device, 
        llm_max_token=settings.LLM_max_token
    )

@lru_cache(maxsize=1)
def build_gemini_llm_rag() -> LocalLLmImpl:
    settings = get_nlp_settings()
    return GeminiLLmImpl(
        model_id=settings.gemini_llm_id,     
        api_key=settings.google_api_key
    )

@lru_cache(maxsize=1)
def build_context_formatter() -> ContextFormatter:
    return ContextFormatter()

@lru_cache(maxsize=1)
def build_nlp_pipeline() -> PipelineService:
    settings = get_nlp_settings()
    intent_model = build_intent_model()
    complexity_model = build_complexity_model()
    local_llm = build_local_llm_rag()
    gemini_llm = build_gemini_llm_rag()

    return PipelineService(
        layers=[
        build_get_cache_layer(), 
        PreprocessingLayer(), 
        ComplexityClassifierLayer(model=complexity_model, confidence_threshold=settings.confidence_threshold), 
        IntentClassifierLayer(model=intent_model, confidence_threshold=settings.confidence_threshold), 
        RetrieveContextLayer(vector_db=build_chroma_db(), formatter=build_context_formatter()), 
        LocalLLMLayer(model=local_llm), 
        GeminiLLMLayer(model=gemini_llm),
        build_save_cache_layer()],

    )