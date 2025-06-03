# backend/app/services/order.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from decimal import Decimal

from app.database import models
from app.schemas import order as order_schemas
from app.schemas import order_item as order_item_schemas
from app.services import user as user_services
from app.services import product as product_services
from app.services import order_item as order_item_services

def get_order(db: Session, order_id: int):
    return db.execute(select(models.Order).filter(models.Order.order_id == order_id)).scalar_one_or_none()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.execute(select(models.Order).offset(skip).limit(limit)).scalars().all()

def create_order(db: Session, order: order_schemas.OrderCreate):
    db_user = user_services.get_user(db, user_id=order.user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {order.user_id} not found")

    db_order = models.Order(
        user_id=order.user_id,
        status=order.status,
        shipping_address=order.shipping_address,
        shipping_city=order.shipping_city,
        shipping_state=order.shipping_state,
        shipping_zip_code=order.shipping_zip_code,
        shipping_country=order.shipping_country,
        total_amount=Decimal('0.00')
    )
    db.add(db_order)
    db.flush()

    total_order_amount = Decimal('0.00')
    order_items_to_add = []

    if not order.order_items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order must contain at least one item.")

    for item_data in order.order_items:
        db_product = product_services.get_product(db, product_id=item_data.product_id)
        if not db_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {item_data.product_id} not found.")
        if db_product.stock_quantity < item_data.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insufficient stock for product '{db_product.name}'. Available: {db_product.stock_quantity}, requested: {item_data.quantity}")

        db_product.stock_quantity -= item_data.quantity
        db.add(db_product)

        price_at_purchase = db_product.price
        item_total = price_at_purchase * item_data.quantity
        total_order_amount += item_total

        db_order_item = models.OrderItem(
            order_id=db_order.order_id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            price_at_purchase=price_at_purchase
        )
        order_items_to_add.append(db_order_item)

    db_order.total_amount = total_order_amount
    db.add(db_order)
    db.add_all(order_items_to_add)

    db.commit()
    db.refresh(db_order)
    db.refresh(db_user)

    return db_order

def update_order(db: Session, order_id: int, order_update: order_schemas.OrderCreate):
    db_order = db.execute(select(models.Order).filter(models.Order.order_id == order_id)).scalar_one_or_none()
    if not db_order:
        return None

    update_data = order_update.model_dump(exclude_unset=True, exclude={'order_items'})
    for key, value in update_data.items():
        setattr(db_order, key, value)

    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = db.execute(select(models.Order).filter(models.Order.order_id == order_id)).scalar_one_or_none()
    if not db_order:
        return False

    order_items = order_item_services.get_order_items_by_order(db, order_id=order_id)

    for item in order_items:
        db_product = product_services.get_product(db, product_id=item.product_id)
        if db_product:
            db_product.stock_quantity += item.quantity
            db.add(db_product)

    db.delete(db_order)
    db.commit()

    if order_items:
        for item in order_items:
            product_services.get_product(db, product_id=item.product_id)

    return True
