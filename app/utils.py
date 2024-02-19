from passlib.context import CryptContext
from fastapi import Depends
from sqlalchemy.orm  import Session
from . import models,schemas
from .database import get_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)


def Check_Credentials(plane_password:str , hashed_password : str):
    return pwd_context.verify(plane_password,hashed_password)



def Count_Ups(post_id : int ,db:Session):
    Ups = db.query(models.Ups).filter(models.Ups.post_id==post_id).count()
    return Ups

def Count_Downs (post_id : int ,db:Session):
    Downs = db.query(models.Downs).filter(models.Downs.post_id==post_id).count()
    return Downs