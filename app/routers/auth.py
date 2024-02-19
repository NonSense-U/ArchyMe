from fastapi import FastAPI,APIRouter,status,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import database,schemas,models,utils,ouath2




router = APIRouter(prefix="/login",tags=["Auth"])


@router.get("/",status_code=status.HTTP_200_OK)

def login(user_credentials : schemas.User_login_credentials,db : Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email==user_credentials.email).first()  

    if user == None or not utils.Check_Credentials(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credentials! Try again")
    

    Access_Token = ouath2.Create_Access_Token(data={"user_id":user.id,"username":user.username})


    return {"access_token":Access_Token,"token_type":"bearer"}