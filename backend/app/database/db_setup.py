# backend/app/database/db_setup.py
from app.database.session import engine, Base
from app.database import models 

def create_db_and_tables():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_db_and_tables()