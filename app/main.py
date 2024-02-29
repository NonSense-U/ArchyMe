from fastapi import FastAPI
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