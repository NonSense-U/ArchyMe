from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas,ouath2
from..utils import Count_Ups,Count_Downs
from typing import List


router = APIRouter(prefix="/posts",tags=["posts"])

@router.get("/",response_model=List[schemas.Post_out])
def get_post(db : Session = Depends(get_db)):
    
    posts = db.query(models.Post, func.count(models.Ups.post_id).label("Ups"), func.count(models.Downs.post_id).label("Downs")).outerjoin(models.Ups, models.Post.id == models.Ups.post_id).outerjoin(models.Downs, models.Post.id == models.Downs.post_id).group_by(models.Post.id).all()
    res_posts = []
    for post,Up,Down in posts:
        res_posts.append({
            "post": post,
            "Ups" : Up,
            "Downs": Down
        })
    return res_posts

@router.get('/{id}',response_model=schemas.Post_out)
def get_post_by_id(id : int,db : Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id==id)
    post = query.first()
    if post is None or post.publiched is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    result = {"post":post,"Ups":Count_Ups(id,db),"Downs" : Count_Downs(id,db)}
    return result


@router.post("/",response_model=schemas.Post_out)
def create_post(post_info : schemas.Create_post,db : Session = Depends(get_db),Token_Info : schemas.Token_data = Depends(ouath2.get_current_user)):
    new_post = models.Post(**post_info.model_dump())
    new_post.owner_id  = Token_Info.user_id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    res = {"post":new_post,"Ups":0,"Downs":0}
    return res



@router.put('/{id}',response_model=schemas.Post_update)
def update_post(id : int,upodate_info : schemas.Post_update,db : Session = Depends(get_db),Token_Info : schemas.Token_data = Depends(ouath2.get_current_user)):
    update_query = db.query(models.Post).filter(models.Post.id==id)
    post_to_update = update_query.first()
    if post_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if post_to_update.owner_id != Token_Info.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    for key in upodate_info.model_dump().keys():
        if upodate_info.model_dump()[key]!=None:
            setattr(post_to_update,key,upodate_info.model_dump()[key])
    db.commit()
    db.refresh(post_to_update)
    return post_to_update
    

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db : Session = Depends(get_db),Token_Info : schemas.Token_data = Depends(ouath2.get_current_user)):
    delete_query = db.query(models.Post).filter(models.Post.id==id)
    post_to_delete = delete_query.first()
    if post_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if post_to_delete.owner_id != Token_Info.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    delete_query.delete(synchronize_session=False)
    db.commit()
    return None


    