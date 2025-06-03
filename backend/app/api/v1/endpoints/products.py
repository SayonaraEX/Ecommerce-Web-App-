# backend/app/api/v1/endpoints/products.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.schemas import product as product_schemas
from app.services import product as product_services 

router = APIRouter()

@router.post("/", response_model=product_schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product: product_schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new product.
    """
    return product_services.create_product(db=db, product=product)

@router.get("/", response_model=List[product_schemas.Product])
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of products.
    """
    products = product_services.get_products(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=product_schemas.Product)
def read_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a single product by its ID.
    """
    db_product = product_services.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=product_schemas.Product)
def update_product(
    product_id: int,
    product_update: product_schemas.ProductCreate, 
    db: Session = Depends(get_db)
):
    """
    Update an existing product.
    """
    db_product = product_services.update_product(db, product_id, product_update)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or update failed")
    return db_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a product.
    """
    success = product_services.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return {"message": "Product deleted successfully"}