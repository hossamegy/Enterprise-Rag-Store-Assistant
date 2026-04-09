import asyncio
from fastapi import APIRouter, Depends

from src.config.logger import logger
from src.di.vector_store_di import build_product_service, build_order_service, build_search_service
from src.core.entities.product import Product
from src.core.entities.order import Order
from src.application.services.product_service import ProductService
from src.application.services.order_service import OrderService
from src.application.services.search_service import SearchService
from src.api.schemas import ProductDTO, OrderDTO
from src.infrastructure.cache.cache import Cache
from src.di.cache_di import build_cache

router = APIRouter(prefix='/vector', tags=['vector'])

@router.post('/products', summary='Index a product into the vector store')
async def add_product(product_dto: ProductDTO, service: ProductService=Depends(build_product_service)):
    logger.info(f'Adding product: {product_dto.ProductName}')
    product = Product(**product_dto.model_dump())
    await asyncio.to_thread(service.add_product, product)
    return {'status': 'added', 'id': product.ProductId}

@router.put('/products/{product_id}', summary='Update a product in the vector store')
async def update_product(product_id: int, product_dto: ProductDTO, service: ProductService=Depends(build_product_service), cache: Cache=Depends(build_cache)):
    product = Product(**product_dto.model_dump())
    await asyncio.to_thread(service.update_product, product_id, product)
    await asyncio.to_thread(cache.delete_cached_question, [str(product_id)])
    return {'status': 'updated', 'id': product_id}

@router.delete('/products/{product_id}', summary='Remove a product from the vector store')
async def delete_product(product_id: int, service: ProductService=Depends(build_product_service), cache: Cache=Depends(build_cache)):
    await asyncio.to_thread(service.delete_product, product_id)
    await asyncio.to_thread(cache.delete_cached_question, [str(product_id)])
    return {'status': 'deleted', 'id': product_id}

@router.post('/orders', summary='Index an order into the vector store')
async def add_order(order_dto: OrderDTO, service: OrderService=Depends(build_order_service)):
    order = Order(**order_dto.model_dump())
    await asyncio.to_thread(service.add_order, order)
    return {'status': 'added', 'id': order.OrderID}

@router.put('/orders/{order_id}', summary='Update an order in the vector store')
async def update_order(order_id: int, order_dto: OrderDTO, service: OrderService=Depends(build_order_service), cache: Cache=Depends(build_cache)):
    order = Order(**order_dto.model_dump())
    await asyncio.to_thread(service.update_order, order_id, order)
    await asyncio.to_thread(cache.delete_cached_question, [str(order_id)])
    return {'status': 'updated', 'id': order_id}

@router.delete('/orders/{order_id}', summary='Remove an order from the vector store')
async def delete_order(order_id: int, service: OrderService=Depends(build_order_service), cache: Cache=Depends(build_cache)):
    await asyncio.to_thread(service.delete_order, order_id)
    await asyncio.to_thread(cache.delete_cached_question, [str(order_id)])
    return {'status': 'deleted', 'id': order_id}

@router.get('/search', summary='Semantic search across all indexed documents')
async def search(q: str, top_k: int=10, service: SearchService=Depends(build_search_service)):
    return await asyncio.to_thread(service.search, q, top_k=top_k)