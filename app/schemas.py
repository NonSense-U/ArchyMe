from pydantic import BaseModel,EmailStr
from datetime import datetime


#! Users Schemas


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
    email : EmailStr = None
    username : str = None
    password : str = None


#! Posts Schemas

class raw_post_info(BaseModel):
    id : int
    title : str
    content : str
    created_at : datetime
    publiched : bool


class create_post(BaseModel):
    title : str
    content : str
    publiched : bool


class post_out(create_post):
    owner : Public_UserInfo
    pass

class post_update(create_post):
    title : str = None
    content : str = None
    publiched : bool = None



#! Auth scemas

class user_login_credentials(BaseModel):
    email : EmailStr
    password : str


class token_data(BaseModel):
    username : str
    user_id : int