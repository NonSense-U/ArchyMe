from fastapi import FastAPI,APIRouter,Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas
from typing import List


router = APIRouter(prefix="/posts",tags=["posts"])

@router.get("/",response_model=List[schemas.raw_post_info])
def get_post(db : Session = Depends(get_db)):
    query = db.query(models.Post)
    return query.all()



@router.post("/",response_model=schemas.post_out)
def create_post(post_info : schemas.create_post,db : Session = Depends(get_db)):
    new_post = models.Post(**post_info.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post