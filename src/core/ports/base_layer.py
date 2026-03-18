from abc import ABC, abstractmethod
from src.core.entities.message_context import MessageContext


class BaseLayer(ABC):

    @abstractmethod
    def handle(self, context: MessageContext) -> MessageContext:
        pass
