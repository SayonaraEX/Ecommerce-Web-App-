# backend/app/schemas/order_item.py
from pydantic import BaseModel, Field
from decimal import Decimal
from .product import Product

class OrderItemBase(BaseModel):
    order_id: int = Field(..., description="Foreign key to the orders table")
    product_id: int = Field(..., description="Foreign key to the products table")
    quantity: int = Field(..., ge=1, description="Quantity of the product in this order item")
    price_at_purchase: Decimal = Field(..., ge=0, decimal_places=2, description="Price of the product at the time of purchase")

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    order_item_id: int
    product: Product 

    class Config:
        from_attributes = True