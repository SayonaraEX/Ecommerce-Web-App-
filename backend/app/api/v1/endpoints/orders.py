# backend/app/api/v1/endpoints/orders.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.schemas import order as order_schemas
from app.schemas import order_item as order_item_schemas 
from app.services import order as order_services
from app.services import order_item as order_item_services

router = APIRouter()

@router.post("/", response_model=order_schemas.Order, status_code=status.HTTP_201_CREATED)
def create_order(
    order: order_schemas.OrderCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new order.
    Requires a list of order_items with product_id and quantity.
    """
    return order_services.create_order(db=db, order=order)

@router.get("/", response_model=List[order_schemas.Order])
def read_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of orders.
    """
    orders = order_services.get_orders(db, skip=skip, limit=limit)
    return orders

@router.get("/{order_id}", response_model=order_schemas.Order)
def read_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a single order by its ID.
    """
    db_order = order_services.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return db_order

@router.put("/{order_id}", response_model=order_schemas.Order)
def update_order(
    order_id: int,
    order_update: order_schemas.OrderBase, 
    db: Session = Depends(get_db)
):
    """
    Update an existing order's basic fields (e.g., status, shipping address).
    Note: Modifying order items is handled by separate endpoints or more complex logic.
    """
    db_order = order_services.update_order(db, order_id, order_update)
    if db_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found or update failed")
    return db_order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an order. This will also return associated product stock.
    """
    success = order_services.delete_order(db, order_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return {"message": "Order deleted successfully"}

@router.get("/{order_id}/items", response_model=List[order_item_schemas.OrderItem])
def read_order_items_for_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve all order items for a specific order.
    """
    db_order = order_services.get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    order_items = order_item_services.get_order_items_by_order(db, order_id=order_id)
    return order_items

