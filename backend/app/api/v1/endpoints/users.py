# backend/app/v1/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.schemas import user as user_schemas
from app.services import user as user_services

router = APIRouter()

@router.post("/", response_model=user_schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(
    user: user_schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    Email and username must be unique.
    """
    db_user_email = user_services.get_user_by_email(db, email=user.email)
    if db_user_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    db_user_username = user_services.get_user_by_username(db, username=user.username)
    if db_user_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    return user_services.create_user(db=db, user=user)

@router.get("/", response_model=List[user_schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of users. (Admin access typically required)
    """
    users = user_services.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=user_schemas.User)
def read_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a single user by their ID.
    """
    db_user = user_services.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=user_schemas.User)
def update_user(
    user_id: int,
    user_update: user_schemas.UserBase, 
    db: Session = Depends(get_db)
):
    """
    Update an existing user.
    Note: Password update should be handled separately for security.
    """
    db_user = user_services.update_user(db, user_id, user_update)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or update failed")
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a user. (Admin access typically required)
    """
    success = user_services.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "User deleted successfully"}