from fastapi import FastAPI,APIRouter
from . import schemas,utils
from .database import get_db


app = FastAPI()

@app.get("/")
def Test():
    return {"data":"success!"}