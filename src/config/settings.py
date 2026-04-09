from functools import lru_cache
import torch
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AliasChoices
from typing import Optional

class VectorDBSettings(BaseSettings):
    persist_directory: str = './src/_db'
    collection_name: str = 'online_store_collection'
    embedding_model_id: str = 'src/core/models/embedding_model/all-MiniLM-L6-v2'
    cache_collection_name: str = 'online_store_cache_collection'
    cache_persist_directory: str = './src/_db_cache'
    cache_embedding_model_id: str = 'src/core/models/embedding_model/all-MiniLM-L6-v2'
    device: str = 'cpu'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='VECTOR_',
        extra='ignore'
    )

class NLPSettings(BaseSettings):
    tokenizer_path: str = 'src/core/models/tokenizer'
    device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
    intent_bert_model_path: str = 'src/core/models/intent_model/intent_bert'
    intent_model_path: str = 'src/core/models/intent_model/intent_model.pth'
    intent_label_encoder_path: str = 'src/core/models/intent_model/intent_classes.pkl'
    intent_num_classes: int = 10
    question_complexity_bert_model_path: str = 'src/core/models/complexity_model/complexity_bert'
    question_complexity_model_path: str = 'src/core/models/complexity_model/complexity_model.pth'
    question_complexity_label_encoder_path: str = 'src/core/models/complexity_model/complexity_classes.pkl'
    question_complexity_num_classes: int = 2
    LLM_id: str = 'src/core/models/Qwen2.5-1.5B-Instruct'
    LLM_max_token: int = 256
    confidence_threshold: float = 0.75

    gemini_llm_id: str = "gemini-3.1-flash-lite-preview"
    google_api_key: Optional[str] = Field(default=None, validation_alias=AliasChoices('nlp_google_api_key', 'google_api_key', 'GOOGLE_API_KEY'))

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='NLP_',
        extra='ignore'
    )

@lru_cache(maxsize=1)
def get_vector_settings() -> VectorDBSettings:
    return VectorDBSettings()

@lru_cache(maxsize=1)
def get_nlp_settings() -> NLPSettings:
    return NLPSettings()
