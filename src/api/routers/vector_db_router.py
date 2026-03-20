from fastapi import APIRouter, Depends
import asyncio

from src.di.vector_store_di import build_vector_db_service
from src.core.entities.product import Product
from src.core.entities.user import User
from src.core.entities.order import Order
from src.application.services.vector_db_service import VectorDbService
from src.api.schemas import ProductDTO, UserDTO, OrderDTO


router = APIRouter(prefix="/vector", tags=["vector"])


# ── Products ─────────────────────────────────────────────────────────────────

@router.post("/products", summary="Index a product into the vector store")
async def add_product(
    product_dto: ProductDTO,
    service: VectorDbService = Depends(build_vector_db_service),
):
    product = Product(**product_dto.model_dump())
    await asyncio.to_thread(service.add_product, product)
    return {"status": "added", "id": product.ProductId}


@router.put("/products/{product_id}", summary="Update a product in the vector store")
async def update_product(
    product_id: int,
    product_dto: ProductDTO,
    service: VectorDbService = Depends(build_vector_db_service),
):
    product = Product(**product_dto.model_dump())
    await asyncio.to_thread(service.update_product, product_id, product)
    return {"status": "updated", "id": product_id}


@router.delete("/products/{product_id}", summary="Remove a product from the vector store")
async def delete_product(
    product_id: int,
    service: VectorDbService = Depends(build_vector_db_service),
):
    await asyncio.to_thread(service.delete, ids=[str(product_id)])
    return {"status": "deleted", "id": product_id}


# ── Orders ────────────────────────────────────────────────────────────────────

@router.post("/orders", summary="Index an order into the vector store")
async def add_order(
    order_dto: OrderDTO,
    service: VectorDbService = Depends(build_vector_db_service),
):
    order = Order(**order_dto.model_dump())
    await asyncio.to_thread(service.add_order, order)
    return {"status": "added", "id": order.OrderID}


@router.put("/orders/{order_id}", summary="Update an order in the vector store")
async def update_order(
    order_id: int,
    order_dto: OrderDTO,
    service: VectorDbService = Depends(build_vector_db_service),
):
    order = Order(**order_dto.model_dump())
    await asyncio.to_thread(service.update_order, order_id, order)
    return {"status": "updated", "id": order_id}


@router.delete("/orders/{order_id}", summary="Remove an order from the vector store")
async def delete_order(
    order_id: int,
    service: VectorDbService = Depends(build_vector_db_service),
):
    await asyncio.to_thread(service.delete, ids=[str(order_id)])
    return {"status": "deleted", "id": order_id}


# ── Users ─────────────────────────────────────────────────────────────────────

@router.post("/users", summary="Index a user into the vector store")
async def add_user(
    user_dto: UserDTO,
    service: VectorDbService = Depends(build_vector_db_service),
):
    user = User(**user_dto.model_dump())
    await asyncio.to_thread(service.add_user, user)
    return {"status": "added", "id": user.UserId}


@router.put("/users/{user_id}", summary="Update a user in the vector store")
async def update_user(
    user_id: int,
    user_dto: UserDTO,
    service: VectorDbService = Depends(build_vector_db_service),
):
    user = User(**user_dto.model_dump())
    await asyncio.to_thread(service.update_user, user_id, user)
    return {"status": "updated", "id": user_id}


@router.delete("/users/{user_id}", summary="Remove a user from the vector store")
async def delete_user(
    user_id: int,
    service: VectorDbService = Depends(build_vector_db_service),
):
    await asyncio.to_thread(service.delete, ids=[str(user_id)])
    return {"status": "deleted", "id": user_id}


# ── Search ────────────────────────────────────────────────────────────────────

@router.get("/search", summary="Semantic search across all indexed documents")
async def search(
    q: str,
    top_k: int = 10,
    service: VectorDbService = Depends(build_vector_db_service),
):
    return await asyncio.to_thread(service.query, query_texts=[q], top_k=top_k)
