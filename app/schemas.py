from pydantic import BaseModel,EmailStr
from datetime import datetime


class Private_UserInfo(BaseModel):
    id : int
    username : str
    email : str
    created_at : datetime
    is_active : bool
    is_superuser : bool

class Public_UserInfo(BaseModel):
    username : str
    email : EmailStr
    created_at : datetime

class UserCreate(BaseModel):
    email : EmailStr
    username : str
    password : str

class UserUpdate(UserCreate):
    pass
