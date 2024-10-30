from datetime import datetime
from pydantic import BaseModel,EmailStr, conint
from typing import Optional






# ? ________________________________________________
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponeModel(BaseModel):
    id : int
    email: EmailStr
    # password:str
    
    class Config:
        orm_mode=True
        
        
class UserLogin(BaseModel):
    email:EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id:str = None
    


# ? ________________________________________________



class PostBase(BaseModel):
    title: str 
    content: str
    published:bool=True


class CreatePost(PostBase):
    pass


class UpdatePost(PostBase):
    pass


# hena a3rf a3ml controle 3ala 4kl el response el rag3
class Post(BaseModel):
    id: int
    created_at: datetime
    owner_id:int
    owner:UserResponeModel

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
        
# New response model
class CreatePostResponse(BaseModel):
    message: str
    post: Post
    
# ? ________________________________________________
class Vote(BaseModel):
    post_id:int
    dir: conint(ge=0,le=1)  # type: ignore