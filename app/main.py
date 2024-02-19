from fastapi import FastAPI,APIRouter
from . import schemas,utils
from .database import get_db
from .routers import Follow, Reaction, Accounts,Posts,Auth

app = FastAPI()


app.include_router(Accounts.router)
app.include_router(Posts.router)
app.include_router(Auth.router)
app.include_router(Follow.router)
app.include_router(Reaction.router)

@app.get("/")
def Test():
    return {"data":"success!"}