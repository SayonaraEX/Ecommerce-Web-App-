# backend/app/services/category.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import models
from app.schemas import category as schemas 

def get_category(db: Session, category_id: int):
    """
    Retrieves a single category by its ID.
    """
    return db.execute(select(models.Category).filter(models.Category.category_id == category_id)).scalar_one_or_none()

def get_category_by_name(db: Session, name: str):
    """
    Retrieves a single category by its name.
    """
    return db.execute(select(models.Category).filter(models.Category.name == name)).scalar_one_or_none()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieves a list of categories.
    """
    return db.execute(select(models.Category).offset(skip).limit(limit)).scalars().all()

def create_category(db: Session, category: schemas.CategoryCreate):
    """
    Creates a new category in the database.
    """
    db_category = models.Category(name=category.name) 
    db.add(db_category)
    db.commit()
    db.refresh(db_category) 
    return db_category

def update_category(db: Session, category_id: int, category_update: schemas.CategoryCreate):
    """
    Updates an existing category.
    """
    db_category = db.execute(select(models.Category).filter(models.Category.category_id == category_id)).scalar_one_or_none()
    if db_category:
        for key, value in category_update.model_dump(exclude_unset=True).items():
            setattr(db_category, key, value)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    return None

def delete_category(db: Session, category_id: int):
    """
    Deletes a category from the database.
    """
    db_category = db.execute(select(models.Category).filter(models.Category.category_id == category_id)).scalar_one_or_none()
    if db_category:
        db.delete(db_category)
        db.commit()
        return True 
    return False 