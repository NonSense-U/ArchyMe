from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from..database import get_db
from.. import models,schemas,utils,ouath2
from typing import List


router = APIRouter(tags=["Follow"])


@router.get("/follow")
def get_follow(db: Session = Depends(get_db)):
    return db.query(models.Followings).all()



@router.post("/follow/{id}",status_code=status.HTTP_201_CREATED)
def follow(id : int ,db: Session = Depends(get_db),Token_Info : schemas.Token_data = Depends(ouath2.get_current_user)):
    follow_exist = db.query(models.Followings).filter(models.Followings.follower_id==Token_Info.user_id).filter(models.Followings.followed_id==id).first()
    if follow_exist!=None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    follow = models.Followings(followed_id=id,follower_id=Token_Info.user_id)
    db.add(follow)
    db.commit()
    db.refresh(follow)
    return{"DATA":"Followed Successfully!"}



@router.post("/unfollow/{id}")
def unfollow(id:int,db : Session = Depends(get_db),Token_Info : schemas.Token_data = Depends(ouath2.get_current_user)):
    unfollow_query = db.query(models.Followings).filter(models.Followings.follower_id==Token_Info.user_id).filter(models.Followings.followed_id==id)

    if unfollow_query.first() is None : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    unfollow_query.delete()
    db.commit()
    return{"Data":"Unfollowed Successfully!"}


@router.get("/followers/{id}",response_model=List[schemas.Followers_out])
def get_followers(id : int,db : Session = Depends(get_db),Token_Info : schemas.Token_data = Depends(ouath2.get_current_user)):
    followers_query = db.query(models.Followings).filter(models.Followings.followed_id==id)
    return followers_query.all()



@router.get("/followings/{id}",response_model=List[schemas.Followings_out])
def get_followings(id : int,db : Session = Depends(get_db),Token_Info : schemas.Token_data = Depends(ouath2.get_current_user)):
    followings_query = db.query(models.Followings).filter(models.Followings.follower_id==id)
    return followings_query.all()