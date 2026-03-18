from src.core.entities.product import Product
from src.core.entities.user import User
from src.core.entities.order import Order


def product_to_document(product: Product) -> str:
    return " ".join(f"{k}: {v}" for k, v in product.model_dump().items() if k != "ProductId")


def user_to_document(user: User) -> str:
    exclude = {"UserId"}
    return " ".join(f"{k}: {v}" for k, v in user.model_dump().items() if k not in exclude)


def order_to_document(order: Order) -> str:
    exclude = {"OrderID", "UserID", "ProductItems"}
    base = " ".join(f"{k}: {v}" for k, v in order.model_dump().items() if k not in exclude)
    products = " ".join(product_to_document(p) for p in order.ProductItems)
    return f"{base} {products}"
