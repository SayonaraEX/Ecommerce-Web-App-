# backend/app/services/order_item.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from app.database import models
from app.schemas import order_item as schemas 
from app.services import product as product_services 

def get_order_item(db: Session, order_item_id: int):
    """
    Retrieves a single order item by its ID.
    """
    return db.execute(select(models.OrderItem).filter(models.OrderItem.order_item_id == order_item_id)).scalar_one_or_none()

def get_order_items_by_order(db: Session, order_id: int):
    """
    Retrieves all order items for a specific order.
    """
    return db.execute(select(models.OrderItem).filter(models.OrderItem.order_id == order_id)).scalars().all()

def create_order_item(db: Session, order_item: schemas.OrderItemCreate):
    """
    Creates a new order item and updates product stock.
    Raises HTTPException if product not found or stock is insufficient.
    """
    db_product = product_services.get_product(db, product_id=order_item.product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {order_item.product_id} not found")
    if db_product.stock_quantity < order_item.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insufficient stock for product {db_product.name}. Available: {db_product.stock_quantity}")

    db_product.stock_quantity -= order_item.quantity
    db.add(db_product)

    db_order_item = models.OrderItem(
        order_id=order_item.order_id,
        product_id=order_item.product_id,
        quantity=order_item.quantity,
        price_at_purchase=order_item.price_at_purchase 
    )
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)
    db.refresh(db_product)
    return db_order_item

def update_order_item(db: Session, order_item_id: int, order_item_update: schemas.OrderItemCreate):
    """
    Updates an existing order item. This is complex as it involves stock adjustments.
    For simplicity, we'll assume full replacement for now. More robust logic would calculate diff.
    """
    db_order_item = db.execute(select(models.OrderItem).filter(models.OrderItem.order_item_id == order_item_id)).scalar_one_or_none()
    if not db_order_item:
        return None

    original_quantity = db_order_item.quantity
    new_quantity = order_item_update.quantity
    product_id = db_order_item.product_id

    db_product = product_services.get_product(db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Associated product with ID {product_id} not found")

    quantity_difference = new_quantity - original_quantity

    if quantity_difference > 0:
        if db_product.stock_quantity < quantity_difference:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insufficient stock for product {db_product.name}. Need {quantity_difference}, available: {db_product.stock_quantity}")
        db_product.stock_quantity -= quantity_difference
    elif quantity_difference < 0: 
        db_product.stock_quantity -= quantity_difference

    db_order_item.quantity = new_quantity
    db_order_item.price_at_purchase = order_item_update.price_at_purchase

    db.add(db_product)
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)
    db.refresh(db_product)
    return db_order_item

def delete_order_item(db: Session, order_item_id: int):
    """
    Deletes an order item and returns its quantity to product stock.
    """
    db_order_item = db.execute(select(models.OrderItem).filter(models.OrderItem.order_item_id == order_item_id)).scalar_one_or_none()
    if not db_order_item:
        return False 

    db_product = product_services.get_product(db, product_id=db_order_item.product_id)
    if db_product:
        db_product.stock_quantity += db_order_item.quantity
        db.add(db_product)

    db.delete(db_order_item)
    db.commit()
    if db_product: 
        db.refresh(db_product)
    return True 