from src.core.ports.base_vector_store import BaseVectorStore
from src.core.entities.product import Product
from src.application.mappers import product_to_document
from src.core.exceptions.domain_exceptions import VectorStoreOperationException

class ProductService:

    def __init__(self, db: BaseVectorStore):
        self._db = db

    def add_product(self, product: Product) -> None:
        try:
            self._db.add(documents=[product_to_document(product)], metadatas=[{'type': 'product'}], ids=[str(product.ProductId)])
        except Exception as e:
            raise VectorStoreOperationException(message=f'Failed to add product {product.ProductId} to vector store.', detail=str(e))

    def update_product(self, product_id: int, product: Product) -> None:
        try:
            self._db.update(ids=[str(product_id)], documents=[product_to_document(product)], metadatas=[{'type': 'product'}])
        except Exception as e:
            raise VectorStoreOperationException(message=f'Failed to update product {product_id} in vector store.', detail=str(e))

    def delete_product(self, product_id: int) -> None:
        try:
            self._db.delete(ids=[str(product_id)])
        except Exception as e:
            raise VectorStoreOperationException(message=f'Failed to delete product {product_id} from vector store.', detail=str(e))