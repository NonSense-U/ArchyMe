from fastapi import FastAPI,APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas,utils,ouath2
from typing import List


router = APIRouter(prefix="/accounts",tags=["Accounts"])


@router.get("/",response_model=List[schemas.Private_UserInfo])
def get_users(db:Session = Depends(get_db)):
    return db.query(models.User).all()


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Public_UserInfo)
def create_account(user:schemas.UserCreate,db:Session = Depends(get_db)):
    exist=db.query(models.User).filter(models.User.email==user.email).first()
    if exist!=None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    user.password = utils.hash_password(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.get("/{id}",response_model=schemas.Private_UserInfo)
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED,response_model=schemas.Public_UserInfo)
def update_user(id:int,user:schemas.UserUpdate,db:Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.id==id)
    user_to_update = query.first()
    if user_to_update==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    for key in user.model_dump().keys():
        if user.model_dump()[key]!=None:
            if key=="password":
                user.password = utils.hash_password(user.password)
                setattr(user_to_update,key,user.model_dump()[key])
            else:
                setattr(user_to_update,key,user.model_dump()[key])
    db.commit()
    db.refresh(user_to_update)
    return user_to_update   



@router.delete("/{id}",status_code=status.HTTP_202_ACCEPTED)
def delete_user(id:int,db:Session = Depends(get_db),Token_Info : schemas.token_data = Depends(ouath2.get_current_user)):
    delete_query = db.query(models.User).filter(models.User.id==id)
    user_to_delete = delete_query.first()

    if user_to_delete==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if user_to_delete.id != Token_Info.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    delete_query.delete()
    db.commit()
    return{"data":"success!"}