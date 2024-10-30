from fastapi import status , Depends, HTTPException , APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import oauth2, utils, schemas
from app import models
from ..database import get_db
 
router=APIRouter(tags=["authentication"])

@router.post("/login", response_model=schemas.Token)
def login(user_cridintials: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email==user_cridintials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")

    if not utils.verify(user_cridintials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credintails")
    
    access_token=oauth2.create_access_token(data={"user_id":user.id})
    return schemas.Token (access_token=access_token, token_type="Bearer") 