from abc import ABC, abstractmethod

class BaseVectorStore(ABC):

    @abstractmethod
    def add(self, documents: list, metadatas: list=None, ids: list=None) -> None:
        pass

    @abstractmethod
    def query(self, query_texts: list, top_k: int=5) -> dict:
        pass

    @abstractmethod
    def delete(self, ids: list) -> None:
        pass

    @abstractmethod
    def update(self, ids: list, documents: list=None, metadatas: list=None) -> None:
        pass

    @abstractmethod
    def delete_by_metadata_filter(self, filter_dict: dict) -> None:
        pass