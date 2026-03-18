from src.core.ports.base_vector_store import BaseVectorStore
from src.core.entities.product import Product
from src.core.entities.user import User
from src.core.entities.order import Order
from src.infrastructure.vector_store.mappers import (
    product_to_document,
    user_to_document,
    order_to_document,
)

class VectorDbService:
    """
    Application service for interacting with the vector store.
    """

    def __init__(self, db: BaseVectorStore):
        self._db = db

    def add_product(self, product: Product) -> None:
        self._db.add(
            documents=[product_to_document(product)],
            metadatas=[{"type": "product"}],
            ids=[str(product.ProductId)]
        )

    def update_product(self, product_id: int, product: Product) -> None:
        self._db.update(
            ids=[str(product_id)],
            documents=[product_to_document(product)],
            metadatas=[{"type": "product"}]
        )

    def add_order(self, order: Order) -> None:
        self._db.add(
            documents=[order_to_document(order)],
            metadatas=[{"type": "order"}],
            ids=[str(order.OrderID)]
        )

    def update_order(self, order_id: int, order: Order) -> None:
        self._db.update(
            ids=[str(order_id)],
            documents=[order_to_document(order)],
            metadatas=[{"type": "order"}]
        )

    def add_user(self, user: User) -> None:
        self._db.add(
            documents=[user_to_document(user)],
            metadatas=[{"type": "user"}],
            ids=[str(user.UserId)]
        )

    def update_user(self, user_id: int, user: User) -> None:
        self._db.update(
            ids=[str(user_id)],
            documents=[user_to_document(user)],
            metadatas=[{"type": "user"}]
        )

    def delete(self, ids: list) -> None:
        self._db.delete(ids=ids)

    def query(self, query_texts: list, top_k: int = 10) -> dict:
        return self._db.query(query_texts=query_texts, top_k=top_k)
