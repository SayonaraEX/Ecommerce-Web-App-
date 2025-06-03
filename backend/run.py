# backend/run.py 
import uvicorn
from app.api import app
from app.database.db_setup import create_db_and_tables 

if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)