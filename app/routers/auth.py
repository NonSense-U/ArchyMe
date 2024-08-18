from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, ouath2
import logging

router = APIRouter(prefix="/Auth", tags=["Auth"])
logger = logging.getLogger(__name__)

@router.post("/login", status_code=status.HTTP_200_OK) 
def login(user_credentials: schemas.User_login_credentials, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

        if user is None or not utils.Check_Credentials(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials! Try again")

        Access_Token = ouath2.Create_Access_Token(data={"user_id": user.id, "username": user.username})

        return {"access_token": Access_Token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error in the login process: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error!")


@router.post("/logout",status_code=status.HTTP_202_ACCEPTED)
def sign_out(Token_info : schemas.Token_data = Depends(ouath2.revoke_token)):
    try:
        return("Token Revoked Successfully!")
    except Exception as e:
        logger.error(f"Error signing out: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal Server Error!")
