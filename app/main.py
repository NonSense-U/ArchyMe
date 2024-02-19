from fastapi import FastAPI,APIRouter
from . import schemas,utils
from .database import get_db
from .routers import accounts,posts,auth,follow_unfollow,react
app = FastAPI()


app.include_router(accounts.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(follow_unfollow.router)
app.include_router(react.router)

@app.get("/")
def Test():
    return {"data":"success!"}