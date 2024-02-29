from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, ouath2
from ..database import get_db
import logging  # Added logging for better debugging and tracking

# Create a logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/react", tags=["Reactions"])

@router.get("/", response_model=List[schemas.Reaction])
def get_reactions(db: Session = Depends(get_db)):

    try:
        Ups = db.query(models.Ups).all()
        Downs = db.query(models.Downs).all()
        return Ups + Downs
    except Exception as e:
        logger.error(f"Error getting reactions: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/{id}/Up", status_code=status.HTTP_201_CREATED)
def Up(id: int, db: Session = Depends(get_db), Token_info: schemas.Token_data = Depends(ouath2.get_current_user)):

    try:
        up_query = db.query(models.Ups).filter(models.Ups.user_id == Token_info.user_id, models.Ups.post_id == id)
        down_query = db.query(models.Downs).filter(models.Downs.user_id == Token_info.user_id, models.Downs.post_id == id)

        post = db.query(models.Post).filter(models.Post.id==id).first()
        reaction = models.Ups(user_id=Token_info.user_id, post_id=id)

        if up_query.first() is not None:
            up_query.delete(synchronize_session=False)
            db.commit()
            return {"DATA": "Successfully removed!"}

        if down_query.first() is not None:
            down_query.delete(synchronize_session=False)
        notification = models.Notification(user_id = post.owner_id,message = f"You got an upvote from {Token_info.username}!")
        db.add(notification)
        db.add(reaction)
        db.commit()
        return {"DATA": "Successfully Created!"}
    except Exception as e:
        logger.error(f"Error in Up process: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/{id}/Down", status_code=status.HTTP_201_CREATED)
def Down(id: int, db: Session = Depends(get_db), Token_info: schemas.Token_data = Depends(ouath2.get_current_user)):  # Changed function name to Down

    try:
        up_query = db.query(models.Ups).filter(models.Ups.user_id == Token_info.user_id).filter(models.Ups.post_id == id)
        down_query = db.query(models.Downs).filter(models.Downs.user_id == Token_info.user_id).filter(models.Downs.post_id == id)

        reaction = models.Downs(user_id=Token_info.user_id, post_id=id)

        if down_query.first() is not None:
            down_query.delete(synchronize_session=False)
            db.commit()
            return {"DATA": "Successfully removed!"}

        if up_query.first() is not None:
            up_query.delete(synchronize_session=False)

        db.add(reaction)
        db.commit()
        return {"DATA": "Successfully Created!"}
    except Exception as e:
        logger.error(f"Error in Down process: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
