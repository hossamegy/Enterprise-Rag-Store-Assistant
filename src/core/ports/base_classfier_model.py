from abc import ABC, abstractmethod
from src.core.models.classfier_model import Classifier

class BaseClassfierModel(ABC):

    @abstractmethod
    def predict(self, text: str) -> tuple[str, float]:
        pass

    @abstractmethod
    def predict(self, text: str) -> tuple[str, float]:
        pass