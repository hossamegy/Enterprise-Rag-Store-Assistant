from functools import lru_cache
import torch
from pydantic_settings import BaseSettings


class VectorDBSettings(BaseSettings):
    persist_directory: str = "./src/_db"
    collection_name: str = "online_store_collection"
    embedding_model_id: str = "src/core/models/embedding_model/all-MiniLM-L6-v2"

    cache_collection_name: str = "online_store_cache_collection"
    cache_persist_directory: str = "./src/_db_cache"
    cache_embedding_model_id: str = "src/core/models/embedding_model/all-MiniLM-L6-v2"
    device: str = "cpu"

    class Config:
        env_file = ".env"
        env_prefix = "VECTOR_"


class NLPSettings(BaseSettings):
    tokenizer_path: str = "src/core/models/tokenizer"

    device: str = "cuda" if torch.cuda.is_available() else "cpu"

    intent_bert_model_path: str = "src/core/models/intent_model/intent_bert"
    intent_model_path: str = "src/core/models/intent_model/intent_model.pth"
    intent_label_encoder_path: str = "src/core/models/intent_model/intent_classes.pkl"
    intent_num_classes: int = 10

    question_complexity_bert_model_path: str = "src/core/models/complexity_model/complexity_bert"
    question_complexity_model_path: str = "src/core/models/complexity_model/complexity_model.pth"
    question_complexity_label_encoder_path: str = "src/core/models/complexity_model/complexity_classes.pkl"
    question_complexity_num_classes: int = 2
    
    LLM_id: str = "src/core/models/Qwen2.5-1.5B-Instruct"
    LLM_max_token: int = 256
    confidence_threshold: float = 0.75

    class Config:
        env_file = ".env"
        env_prefix = "NLP_"


@lru_cache(maxsize=1)
def get_vector_settings() -> VectorDBSettings:
    return VectorDBSettings()


@lru_cache(maxsize=1)
def get_nlp_settings() -> NLPSettings:
    return NLPSettings()