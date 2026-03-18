from abc import ABC, abstractmethod


class BaseCache(ABC):

    @abstractmethod
    def save(self, question: str, answer: str, model_type: str) -> None:
        pass

    @abstractmethod
    def similar_question_score(self, question: str) -> float:
        pass

    @abstractmethod
    def get_answer(self, question: str) -> str:
        pass
