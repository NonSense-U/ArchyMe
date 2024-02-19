from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List,Optional
from .. import schemas,database,models,ouath2
from ..database import get_db

router = APIRouter(prefix="/react",tags=["Reactions"])


@router.get("/",response_model=List[schemas.Reaction])
def get_reactions(db : Session = Depends(get_db)):
    Ups = db.query(models.Ups).all()
    Downs = db.query(models.Downs).all()
    return Ups + Downs


@router.post("/{id}/Up",status_code=status.HTTP_201_CREATED)
def Up( id : int , db : Session = Depends(get_db),  Token_info: schemas.Token_data = Depends(ouath2.get_current_user)):

    up_query = db.query(models.Ups).filter(models.Ups.user_id==Token_info.user_id,models.Ups.post_id==id)
    down_query = db.query(models.Downs).filter(models.Downs.user_id==Token_info.user_id,models.Downs.post_id==id)

    
    reaction = models.Ups(user_id=Token_info.user_id,post_id = id)

    if up_query.first() != None:
        up_query.delete(synchronize_session=False)
        db.commit()
        return {"DATA":"Successfully removed!"}

    if down_query.first() != None:
        down_query.delete(synchronize_session=False)


    db.add(reaction)
    db.commit()
    return {"DATA":"Successfully Created!"}


@router.post("/{id}/Down",status_code=status.HTTP_201_CREATED)
def Up(id:int,db : Session = Depends(get_db),Token_info: schemas.Token_data = Depends(ouath2.get_current_user)):

    up_query = db.query(models.Ups).filter(models.Ups.user_id==Token_info.user_id).filter(models.Ups.post_id==id)
    down_query = db.query(models.Downs).filter(models.Downs.user_id==Token_info.user_id).filter(models.Downs.post_id==id)


    reaction = models.Downs(user_id=Token_info.user_id,post_id = id)

    if down_query.first() != None:
        down_query.delete(synchronize_session=False)
        db.commit()
        return {"DATA":"Succesfully removed!"}

    if up_query.first() != None:
        up_query.delete(synchronize_session=False)

    db.add(reaction)
    db.commit()
    return {"DATA":"Succesfully Created!"}

    
