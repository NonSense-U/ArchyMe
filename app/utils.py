from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)


def Check_Credentials(plane_password:str , hashed_password : str):
    return pwd_context.verify(plane_password,hashed_password)