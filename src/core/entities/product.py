from pydantic import BaseModel

class Product(BaseModel):
    ProductId: int
    ProductName: str
    Brand: str
    CategoryName: str
    Price: float
    Description: str
    IsAvailable: bool
    StockQuantity: int
    ImageUrl: list[str]