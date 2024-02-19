from typing import Optional
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
    Ups : int
    Downs : int
    created_at : datetime
    publiched : bool


class create_post(BaseModel):
    title : str
    content : str
    publiched : bool


class Post(create_post):
    id : int
    owner : Public_UserInfo
    pass


class post_out(BaseModel):
    post : Post
    Ups : Optional[int] = None
    Downs : Optional[int] = None

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




    ##! Follow system



class followers_out(BaseModel):
    follower : Public_UserInfo


class followings_out(BaseModel):
    followed : Public_UserInfo



    ##! Reactions system


class reaction(BaseModel):
    user_id : int
    user : Public_UserInfo
    post_id : int
    post : Post


class react(BaseModel):
    user : Public_UserInfo
    post : Post