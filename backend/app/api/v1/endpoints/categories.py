# backend/app/api/v1/endpoints/categories.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.schemas import category as category_schemas
from app.services import category as category_services

router = APIRouter()

@router.post("/", response_model=category_schemas.Category, status_code=status.HTTP_201_CREATED)
def create_category(
    category: category_schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new product category.
    """
    db_category = category_services.get_category_by_name(db, name=category.name)
    if db_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category with this name already exists")
    return category_services.create_category(db=db, category=category)

@router.get("/", response_model=List[category_schemas.Category])
def read_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of product categories.
    """
    categories = category_services.get_categories(db, skip=skip, limit=limit)
    return categories

@router.get("/{category_id}", response_model=category_schemas.Category)
def read_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a single category by its ID.
    """
    db_category = category_services.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return db_category

@router.put("/{category_id}", response_model=category_schemas.Category)
def update_category(
    category_id: int,
    category_update: category_schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    """
    Update an existing category.
    """
    existing_category_with_name = category_services.get_category_by_name(db, name=category_update.name)
    if existing_category_with_name and existing_category_with_name.category_id != category_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Another category with this name already exists")

    db_category = category_services.update_category(db, category_id, category_update)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found or update failed")
    return db_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a category.
    """
    success = category_services.delete_category(db, category_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return {"message": "Category deleted successfully"}