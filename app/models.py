from .database import Base
from sqlalchemy import ForeignKey,String,Column,Integer,Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text


class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(255),unique=True,nullable=False,index=True)
    email = Column(String(255),unique=True,nullable=False,index=True)
    password = Column(String(255),nullable=False)
    is_active = Column(Boolean,server_default=("False"))
    is_superuser = Column(Boolean,server_default=("False"))
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'))

class Post(Base):    
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255),nullable=False)
    content = Column(String(255),nullable=False)
    published = Column(Boolean, server_default=("True"))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey('users.id',ondelete=("CASCADE")))
    owner = relationship("User")


class Followings(Base):
    __tablename__ = "followings"
    follower_id = Column(Integer, ForeignKey('users.id',ondelete=("CASCADE")),primary_key=True)
    followed_id = Column(Integer, ForeignKey('users.id',ondelete=("CASCADE")),primary_key=True)
    follower = relationship("User",foreign_keys=[follower_id])
    followed = relationship("User",foreign_keys=[followed_id])


class Ups(Base):
    __tablename__ = "Ups"
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False,primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"))
    user = relationship("User",foreign_keys=[user_id])
    post = relationship("Post",foreign_keys=[post_id])


class Downs(Base):
    __tablename__ = "Downs"
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False,primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),nullable=False,primary_key=True)
    user = relationship("User",foreign_keys=[user_id])
    post = relationship("Post",foreign_keys=[post_id])


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    read = Column(Boolean)