from fastapi import FastAPI
from .routers import Follow, Reaction, Accounts,Posts,Auth
from fastapi.middleware.cors import CORSMiddleware

origins  = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Accounts.router)
app.include_router(Posts.router)
app.include_router(Auth.router)
app.include_router(Follow.router)
app.include_router(Reaction.router)


@app.get("/")
def Test():
    return {"data":"success!"}