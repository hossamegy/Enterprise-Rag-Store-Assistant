from src.core.ports.base_vector_store import BaseVectorStore
from src.core.entities.order import Order
from src.application.mappers import order_to_document
from src.core.exceptions.domain_exceptions import VectorStoreOperationException

class OrderService:

    def __init__(self, db: BaseVectorStore):
        self._db = db

    def add_order(self, order: Order) -> None:
        try:
            self._db.add(documents=[order_to_document(order)], metadatas=[{'type': 'order'}], ids=[str(order.OrderID)])
        except Exception as e:
            raise VectorStoreOperationException(message=f'Failed to add order {order.OrderID} to vector store.', detail=str(e))

    def update_order(self, order_id: int, order: Order) -> None:
        try:
            self._db.update(ids=[str(order_id)], documents=[order_to_document(order)], metadatas=[{'type': 'order'}])
        except Exception as e:
            raise VectorStoreOperationException(message=f'Failed to update order {order_id} in vector store.', detail=str(e))

    def delete_order(self, order_id: int) -> None:
        try:
            self._db.delete(ids=[str(order_id)])
        except Exception as e:
            raise VectorStoreOperationException(message=f'Failed to delete order {order_id} from vector store.', detail=str(e))