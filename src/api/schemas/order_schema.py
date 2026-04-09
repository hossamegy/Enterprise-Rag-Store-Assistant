from pydantic import BaseModel
from typing import List
from enum import Enum
from .product_schema import ProductDTO

class OrderStatusDTO(str, Enum):
    Pending = 'Pending'
    Processing = 'Processing'
    Shipped = 'Shipped'
    Delivered = 'Delivered'
    Cancelled = 'Cancelled'

class OrderDTO(BaseModel):
    OrderID: int
    TotalAmount: float
    OrderNumber: int
    OrderStatus: OrderStatusDTO
    UserID: int
    ProductItems: List[ProductDTO]