from abc import ABC, abstractmethod


class LocalLLM(ABC):

    @abstractmethod
    def load(self) -> tuple:
        pass

    @abstractmethod
    def rag_answer(self, question_intent: str, processed_question: str, retrieved_context: str) -> str:
        pass

    @abstractmethod
    def generate(self, messages: list[dict]) -> str:
        pass