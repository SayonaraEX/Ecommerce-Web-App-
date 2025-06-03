# backend/app/schemas/category.py
from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=255, description="Name of the category")

class CategoryCreate(CategoryBase):
    pass 

class Category(CategoryBase):
    category_id: int


    class Config:
        from_attributes = True 