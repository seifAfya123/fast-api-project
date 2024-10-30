from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from termcolor import colored

import app
from app import schemas, models, utils
from app import oauth2
from ..database import get_db

router=APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponeModel)
def Create_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    
    # hash the password 
    user.password= utils.hash(user.password)
    
    new_user=models.Users(**user.model_dump())
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return new_user

@router.get("/{id}",response_model=schemas.UserResponeModel)
def get_user(id:int,db: Session=Depends(get_db),get_current_user:int= Depends(oauth2.get_current_user)):
    
    user=db.query(models.Users).filter(models.Users.id== id).first()
    print(colored(user.id,"red"))
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    
    return user


