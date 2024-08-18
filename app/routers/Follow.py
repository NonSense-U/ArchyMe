from fastapi import  APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, ouath2
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Follow"])

@router.get("/follow")
def get_follow(db: Session = Depends(get_db)):
    try:
        return db.query(models.Followings).all()
    except Exception as e:
        logger.error(f"Error getting follow data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/follow/{id}", status_code=status.HTTP_201_CREATED)
def follow(id: int, db: Session = Depends(get_db), Token_Info: schemas.Token_data = Depends(ouath2.get_current_user)):
    try:
        follow_exist = db.query(models.Followings).filter(models.Followings.follower_id == Token_Info.user_id).filter(models.Followings.followed_id == id).first()
        if follow_exist is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already following")
        follow = models.Followings(followed_id=id, follower_id=Token_Info.user_id)
        db.add(follow)
        db.commit()
        db.refresh(follow)
        return {"DATA": "Followed Successfully!"}
    except Exception as e:
        logger.error(f"Error in follow process: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")



@router.post("/unfollow/{id}")
def unfollow(id: int, db: Session = Depends(get_db), Token_Info: schemas.Token_data = Depends(ouath2.get_current_user)):
    try:
        unfollow_query = db.query(models.Followings).filter(models.Followings.follower_id == Token_Info.user_id).filter(models.Followings.followed_id == id)
        if unfollow_query.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not following")
        unfollow_query.delete()
        db.commit()
        return {"Data": "Unfollowed Successfully!"}
    except Exception as e:
        logger.error(f"Error in unfollow process: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")



@router.get("/followers/{id}", response_model=List[schemas.Followers_out])
def get_followers(id: int, db: Session = Depends(get_db), Token_Info: schemas.Token_data = Depends(ouath2.get_current_user)):
    try:
        followers_query = db.query(models.Followings).filter(models.Followings.followed_id == id)
        return followers_query.all()
    except Exception as e:
        logger.error(f"Error getting followers: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/followings/{id}", response_model=List[schemas.Followings_out])
def get_followings(id: int, db: Session = Depends(get_db), Token_Info: schemas.Token_data = Depends(ouath2.get_current_user)):
    try:
        followings_query = db.query(models.Followings).filter(models.Followings.follower_id == id)
        return followings_query.all()
    except Exception as e:
        logger.error(f"Error getting followings: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
