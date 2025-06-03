# backend/app/schemas/order.py
from pydantic import BaseModel, Field
from typing import Optional, Literal, List 
from datetime import datetime
from decimal import Decimal

from .user import User
from .order_item import OrderItem, OrderItemCreate 

class OrderBase(BaseModel):
    user_id: int = Field(..., description="Foreign key to the users table")
    total_amount: Decimal = Field(Decimal('0.00'), ge=0, decimal_places=2, description="Total amount of the order") # Default to 0, backend calculates
    status: Literal['pending', 'processing', 'shipped', 'delivered', 'cancelled'] = Field('pending', description="Current status of the order") # Define literal for enum
    shipping_address: Optional[str] = Field(None, max_length=255)
    shipping_city: Optional[str] = Field(None, max_length=255)
    shipping_state: Optional[str] = Field(None, max_length=255)
    shipping_zip_code: Optional[str] = Field(None, max_length=20)
    shipping_country: Optional[str] = Field(None, max_length=255)

class OrderCreate(BaseModel):
    user_id: int = Field(..., description="Foreign key to the users table")
    shipping_address: Optional[str] = Field(None, max_length=255)
    shipping_city: Optional[str] = Field(None, max_length=255)
    shipping_state: Optional[str] = Field(None, max_length=255)
    shipping_zip_code: Optional[str] = Field(None, max_length=20)
    shipping_country: Optional[str] = Field(None, max_length=255)
    order_items: List[OrderItemCreate] = Field(..., min_length=1, description="List of items in the order")

class Order(OrderBase):
    order_id: int
    order_date: datetime
    user: User 
    order_items: List[OrderItem] = [] 

    class Config:
        from_attributes = True