from dataclasses import dataclass

@dataclass
class CacheData:
    question: str
    answer: str
    model_type: str