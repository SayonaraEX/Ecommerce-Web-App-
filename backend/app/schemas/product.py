# backend/app/schemas/product.py
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime

from .category import Category

class ProductBase(BaseModel):
    name: str = Field(..., max_length=255, description="Name of the product")
    description: Optional[str] = Field(None, description="Detailed description of the product")
    price: Decimal = Field(..., ge=0, decimal_places=2, description="Price of the product")
    stock_quantity: int = Field(0, ge=0, description="Current stock level of the product")
    image_url: Optional[str] = Field(None, max_length=255, description="URL to the product image")
    category_id: int = Field(..., description="Foreign key to the categories table")

class ProductCreate(ProductBase):
    pass 

class Product(ProductBase):
    product_id: int
    created_at: datetime
    updated_at: datetime
    category: Category 

    class Config:
        from_attributes = True