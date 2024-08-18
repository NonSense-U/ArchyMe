from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemas,models,database,config
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

ouath2_scheme = OAuth2PasswordBearer(tokenUrl='Auth/login')

SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minutes

black_list = set()

def Create_Access_Token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def revoke_token(token : str = Depends(ouath2_scheme)):
    black_list.add(token)

    
def verify_access_token(token:str, credentials_exception):
    try:
        if token in black_list:
            raise credentials_exception 
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id : int = payload.get("user_id")
        name:str = payload.get("username")
        #! Not needed, automaticly done by jwt.decode
        # if name is None or id is None:
        #     raise credentials_exception
        token_data = schemas.Token_data(user_id= id ,username=name)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token : str = Depends(ouath2_scheme),db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,detail="Could Not Validate Credentials!",headers={"WWW.Authenticate":"Bearer"})
    return verify_access_token(token,credentials_exception) 
