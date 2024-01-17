from fastapi import FastAPI,APIRouter
from . import schemas,utils
from .database import get_db
from .routers import accounts
app = FastAPI()


app.include_router(accounts.router)



@app.get("/")
def Test():
    return {"data":"success!"}