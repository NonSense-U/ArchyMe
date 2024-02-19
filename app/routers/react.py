from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List,Optional
from .. import schemas,database,models,ouath2
from ..database import get_db

router = APIRouter(prefix="/react")


@router.get("/",response_model=List[schemas.reaction])
def get_reactions(db : Session = Depends(get_db)):
    Ups = db.query(models.Ups).all()
    Downs = db.query(models.Downs).all()
    return Ups + Downs


@router.post("/{id}/Up",response_model=Optional[schemas.react])
def Up(id:int,db : Session = Depends(get_db),Token_info: schemas.token_data = Depends(ouath2.get_current_user)):
    up_query = db.query(models.Ups).filter(models.Ups.user_id==Token_info.user_id).filter(models.Ups.post_id==id)
    down_query = db.query(models.Downs).filter(models.Downs.user_id==Token_info.user_id).filter(models.Downs.post_id==id)

    
    reaction = models.Ups(user_id=Token_info.user_id,post_id = id)
    if up_query.first() != None:
        up_query.delete(synchronize_session=False)
        db.commit()
        return 

    if down_query.first() != None:
        down_query.delete(synchronize_session=False)


    db.add(reaction)
    db.commit()
    return reaction


@router.post("/{id}/Down",response_model=Optional[schemas.react])
def Up(id:int,db : Session = Depends(get_db),Token_info: schemas.token_data = Depends(ouath2.get_current_user)):

    up_query = db.query(models.Ups).filter(models.Ups.user_id==Token_info.user_id).filter(models.Ups.post_id==id)
    down_query = db.query(models.Downs).filter(models.Downs.user_id==Token_info.user_id).filter(models.Downs.post_id==id)


    reaction = models.Downs(user_id=Token_info.user_id,post_id = id)

    if down_query.first() != None:
        down_query.delete()
        db.commit()
        return

    if up_query.first() != None:
        up_query.delete()

    db.add(reaction)
    db.commit()
    return reaction


    
