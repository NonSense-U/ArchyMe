from fastapi import Depends,FastAPI,status,APIRouter,HTTPException
from sqlalchemy.orm import Session
from ...database import get_db
from ...ouath2 import get_current_user
from typing import List
from ... import schemas,models
import logging


logger = logging.getLogger(__name__)

router = APIRouter(tags=["notifications"],prefix='/profile')

@router.get('/notifications',status_code=status.HTTP_200_OK,response_model=List[schemas.Notification_out])
def get_notifications(Token_Info : schemas.Token_data = Depends(get_current_user),db : Session = Depends(get_db)):
    try:
        notifications_query = db.query(models.Notification).filter(models.Notification.user_id == Token_Info.user_id)
        return notifications_query.all()
    except Exception as e :
        logger.error(f"Error Getting Notifications : {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.put('/notifications/{id}',status_code=status.HTTP_202_ACCEPTED)
def mark_as_read(id : int = id,Token_Info : schemas.Token_data = Depends(get_current_user),db : Session = Depends(get_db)):
    try:
        notification = db.query(models.Notification).filter(models.Notification.id == id).first()
        notification.read = True
        db.commit()
        db.refresh(notification)
        return notification
    except Exception as e : 
        logger.error(f"Error marking notification {id} as read!")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)