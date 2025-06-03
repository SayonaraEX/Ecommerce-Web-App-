# backend/app/services/user.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext 
from app.database import models
from app.schemas import user as schemas 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db: Session, user_id: int):
    """
    Retrieves a single user by their ID.
    """
    return db.execute(select(models.User).filter(models.User.user_id == user_id)).scalar_one_or_none()

def get_user_by_email(db: Session, email: str):
    """
    Retrieves a single user by their email address.
    """
    return db.execute(select(models.User).filter(models.User.email == email)).scalar_one_or_none()

def get_user_by_username(db: Session, username: str):
    """
    Retrieves a single user by their username.
    """
    return db.execute(select(models.User).filter(models.User.username == username)).scalar_one_or_none()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieves a list of users.
    """
    return db.execute(select(models.User).offset(skip).limit(limit)).scalars().all()

def create_user(db: Session, user: schemas.UserCreate):
    """
    Creates a new user in the database, hashing the password.
    """
    hashed_password = get_password_hash(user.password) 
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password, 
        first_name=user.first_name,
        last_name=user.last_name,
        address=user.address,
        city=user.city,
        state=user.state,
        zip_code=user.zip_code,
        country=user.country,
        phone_number=user.phone_number,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserBase):
    """
    Updates an existing user. Note: This function does NOT handle password updates directly.
    A separate function would be needed for secure password changes.
    """
    db_user = db.execute(select(models.User).filter(models.User.user_id == user_id)).scalar_one_or_none()
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key != "password_hash": 
                setattr(db_user, key, value)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def delete_user(db: Session, user_id: int):
    """
    Deletes a user from the database.
    """
    db_user = db.execute(select(models.User).filter(models.User.user_id == user_id)).scalar_one_or_none()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False 