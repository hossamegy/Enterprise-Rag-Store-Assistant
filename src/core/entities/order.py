from pydantic import BaseModel
from enum import Enum
from src.core.entities.product import Product

class OrderStatus(str, Enum):
    Pending = 'Pending'
    Processing = 'Processing'
    Shipped = 'Shipped'
    Delivered = 'Delivered'
    Cancelled = 'Cancelled'

class Order(BaseModel):
    OrderID: int
    TotalAmount: float
    OrderNumber: int
    OrderStatus: OrderStatus
    UserID: int
    ProductItems: list[Product]