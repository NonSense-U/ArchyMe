from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, ouath2
from ..utils import Count_Ups, Count_Downs
from typing import List
import logging

# Create a logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=List[schemas.Post_out])
def get_post(skip: int = 0, limit: int | None = None ,db: Session = Depends(get_db)):
    
    try:
        posts = db.query(models.Post, func.count(models.Ups.post_id).label("Ups"), func.count(models.Downs.post_id).label("Downs")).outerjoin(models.Ups, models.Post.id == models.Ups.post_id).outerjoin(models.Downs, models.Post.id == models.Downs.post_id).group_by(models.Post.id).offset(skip).limit(limit).all()
        res_posts = []
        for post, Up, Down in posts:
            res_posts.append({
                "post": post,
                "Ups": Up,
                "Downs": Down
            })
        return res_posts
    except Exception as e:
        logger.error(f"Error getting posts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get('/{id}', response_model=schemas.Post_out)
def get_post_by_id(id: int, db: Session = Depends(get_db)):

    try:
        query = db.query(models.Post).filter(models.Post.id == id)
        post = query.first()
        if post is None or post.publiched is False:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        result = {"post": post, "Ups": Count_Ups(id, db), "Downs": Count_Downs(id, db)}
        return result
    except Exception as e:
        logger.error(f"Error getting post by id: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/", response_model=schemas.Post_out)
def create_post(post_info: schemas.Create_post, db: Session = Depends(get_db), Token_Info: schemas.Token_data = Depends(ouath2.get_current_user)):

    try:
        new_post = models.Post(**post_info.model_dump())
        new_post.owner_id = Token_Info.user_id
        db.add(new_post)
        
        res = {"post": new_post, "Ups": 0, "Downs": 0}
        followers = db.query(models.Followings).filter(models.Followings.followed_id==Token_Info.user_id).all()
        for follower in followers:
            notification = models.Notification(user_id = follower.follower_id, message = f"{Token_Info.username} has made a post!")
            db.add(notification)

        db.commit()
        db.refresh(new_post)
        return res
    
    except Exception as e:
        logger.error(f"Error creating post: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put('/{id}', response_model=schemas.Post_update)
def update_post(id: int, update_info: schemas.Post_update, db: Session = Depends(get_db), Token_Info: schemas.Token_data = Depends(ouath2.get_current_user)):
    
    try:
        update_query = db.query(models.Post).filter(models.Post.id == id)
        post_to_update = update_query.first()
        if post_to_update is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if post_to_update.owner_id != Token_Info.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        for key in update_info.model_dump().keys():
            if update_info.model_dump()[key] is not None:
                setattr(post_to_update, key, update_info.model_dump()[key])
        db.commit()
        db.refresh(post_to_update)
        return post_to_update
    except Exception as e:
        logger.error(f"Error updating post: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), Token_Info: schemas.Token_data = Depends(ouath2.get_current_user)):
    
    try:
        delete_query = db.query(models.Post).filter(models.Post.id == id)
        post_to_delete = delete_query.first()
        if post_to_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if post_to_delete.owner_id != Token_Info.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        delete_query.delete(synchronize_session=False)
        db.commit()
        return None
    except Exception as e:
        logger.error(f"Error deleting post: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
