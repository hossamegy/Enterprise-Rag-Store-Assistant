from pydantic import BaseModel
from typing import List

class ProductDTO(BaseModel):
    ProductId: int
    ProductName: str
    Brand: str
    CategoryName: str
    Price: float
    Description: str
    IsAvailable: bool
    StockQuantity: int
    ImageUrl: List[str]
