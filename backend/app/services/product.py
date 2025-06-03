# backend/app/services/product.py
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from app.database import models
from app.schemas import product as schemas 

def get_product(db: Session, product_id: int):
    return db.execute(select(models.Product).filter(models.Product.product_id == product_id)).scalar_one_or_none()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.execute(select(models.Product).offset(skip).limit(limit)).scalars().all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump()) 
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: schemas.ProductCreate):
    db_product = db.execute(select(models.Product).filter(models.Product.product_id == product_id)).scalar_one_or_none()
    if db_product:
        for key, value in product_update.model_dump(exclude_unset=True).items(): 
            setattr(db_product, key, value)
        db.add(db_product) 
        db.commit()
        db.refresh(db_product)
        return db_product
    return None

def delete_product(db: Session, product_id: int):
    db_product = db.execute(select(models.Product).filter(models.Product.product_id == product_id)).scalar_one_or_none()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True 
    return False