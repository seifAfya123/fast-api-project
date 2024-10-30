from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app import models, schemas,database
from sqlalchemy.orm import Session
from .config import settings
outh2_schema=OAuth2PasswordBearer(tokenUrl='login')


# SECRET_KEY= "89ycrp98yw3rp9yp9qy9pryqp98werywer9p8y9pq8erpy2p98r"
SECRET_KEY= settings.secret_Key
ALGORITH=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=settings.access_token_exp_time

def create_access_token(data: dict):
    to_encode=data.copy()
    expire =datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITH)
    return encoded_jwt

def verify_access_token(token: str, creadintial_exception):
    """gives me the information stored in the token :: here like user id"""
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITH])
        id:str = payload.get("user_id")
        if id is None:
            raise creadintial_exception
        token_data =schemas.TokenData(id=str(id))
    except JWTError:
        raise creadintial_exception
    
    return token_data
    
def get_current_user(token : str=Depends(outh2_schema), db : Session=Depends(database.get_db)):
    credintials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="n0t valid creadintials", headers={"www-Authenticate":"Bearer"})
    tokenoo = verify_access_token(token,credintials_exception)
    user = db.query(models.Users).filter(models.Users.id==tokenoo.id).first()
    return user