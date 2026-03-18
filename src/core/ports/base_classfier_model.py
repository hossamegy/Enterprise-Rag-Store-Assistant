from abc import ABC, abstractmethod
from src.core.models.classfier_model import Classifier


class BaseClassfierModel(ABC):
    def __init__(self, bert_model_path: str, model_path: str, tokenizer_path: str, classes_path: str, num_classes: int, device: str):
        self.bert_model_path = bert_model_path
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path
        self.classes_path = classes_path
        self.num_classes = num_classes
        self.device = device
        
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def predict(self, text: str) -> tuple[str, float]:
       pass