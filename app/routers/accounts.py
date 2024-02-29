from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, ouath2
from typing import List
import logging
# Use a logger for debugging and tracking

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/accounts", tags=["Accounts"])


#? Getting Users
@router.get("/", response_model=List[schemas.Private_UserInfo])
def get_users(db: Session = Depends(get_db)):

    try:
        return db.query(models.User).all()
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


#? creating Users
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Public_UserInfo)
def create_account(user: schemas.UserCreate, db: Session = Depends(get_db)):

    try:
        exist = db.query(models.User).filter(models.User.email == user.email).first()
        if exist is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)
        user.password = utils.hash_password(user.password)
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        logger.error(f"Error creating account: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


#? Getting User By id
    
@router.get("/{id}", response_model=schemas.Private_UserInfo)
def get_user(id: int, db: Session = Depends(get_db)):

    try:
        user = db.query(models.User).filter(models.User.id == id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


#? Updating a User
    
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Public_UserInfo)
def update_user(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db), Token_info: schemas.Token_data = Depends(ouath2.get_current_user)):

    try:
        if id != Token_info.user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        query = db.query(models.User).filter(models.User.id == id)
        user_to_update = query.first()
        if user_to_update is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        for key in user.model_dump().keys():
            if user.model_dump()[key] is not None:
                if key == "password":
                    user.password = utils.hash_password(user.password)
                    setattr(user_to_update, key, user.model_dump()[key])
                else:
                    setattr(user_to_update, key, user.model_dump()[key])
        db.commit()
        db.refresh(user_to_update)
        return user_to_update
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


#? Deleting Users
@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_user(id: int, db: Session = Depends(get_db), Token_Info: schemas.Token_data = Depends(ouath2.get_current_user)):

    try:
        delete_query = db.query(models.User).filter(models.User.id == id)
        user_to_delete = delete_query.first()
        if user_to_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if user_to_delete.id != Token_Info.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        delete_query.delete()
        db.commit()
        return {"data": "success!"}
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    

#? Getting Users Notifications
    
@router.get("/notifications/mynotifications",response_model=List[schemas.Notification_out])
def get_notifications(db : Session = Depends(get_db),Token_info : schemas.Token_data = Depends(ouath2.get_current_user)):
    try:
        notifications_query = db.query(models.Notification).filter(models.Notification.user_id==Token_info.user_id)
        return notifications_query.all()
    except Exception as e :
        logger.error(f"Error Getting Notifications : {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

