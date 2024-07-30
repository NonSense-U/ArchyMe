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

class Raw_post_info(BaseModel):
    id : int
    title : str
    content : str
    Ups : int
    Downs : int
    created_at : datetime
    published : bool

class Post_base(BaseModel):
    title : str
    content : str
    published : bool


class Create_post(Post_base):
    pass


class Post(Post_base):
    id : int
    owner : Public_UserInfo
    pass
    created_at : datetime


class Post_out(BaseModel):
    post : Post
    Ups : int
    Downs : int



class Post_update(Create_post):
    title : str = None
    content : str = None
    published : bool = None



#! Auth scemas

class User_login_credentials(BaseModel):
    email : EmailStr
    password : str


class Token_data(BaseModel):
    username : str 
    user_id : int




    ##! Follow system



class Followers_out(BaseModel):
    follower : Public_UserInfo


class Followings_out(BaseModel):
    followed : Public_UserInfo



    ##! Reactions system


class Reaction(BaseModel):
    user_id : int
    user : Public_UserInfo
    post_id : int
    post : Post


class Reaction_out(BaseModel):
    user : Public_UserInfo
    post : Post

    ##! Notifications
class Notification_out(BaseModel):
    message  : str