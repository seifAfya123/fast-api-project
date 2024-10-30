import shutil
from typing import List, Optional
from fastapi import Depends, File, HTTPException, UploadFile, status, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import func
from sqlalchemy.orm import Session
from termcolor import colored
from app import oauth2
from .. import schemas, models, oauth2
from app.database import get_db
import os

router=APIRouter(prefix="/posts",tags=["posts"])


@router.get("/",response_model=List[schemas.PostOut],)
async def index(db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),
                limit:int =10,skip:int =0 ,search:Optional[str]=''):
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts=db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    return posts

@router.get("/{id}",response_model=schemas.PostOut)
async def get_post(id: int, db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post=db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    print(post)
    if not post:
        print(colored("post not found","red"))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no post found with this id")
    print(colored("post found","cyan"))
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.CreatePost, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user) ):
    print(current_user.email)
    print(post)
    
    new_post = models.Post(owner_id= current_user.id,**post.model_dump())
    db.add(new_post)
    try:
        db.commit()
        db.refresh(new_post)
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="somthing went wrong")
    # Here we return the new_post directly as a response, and it will be serialized correctly
    return new_post

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
async def update_post(id:int , post:schemas.UpdatePost , db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    query_post=db.query(models.Post).filter(models.Post.id == id,)
    dbpost=query_post.first()
    if dbpost is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found with this id")
    if dbpost.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="you are not allowed to do the action")
    query_post.update(post.model_dump(),synchronize_session=False)
    db.commit()
    updated_post = query_post.first()
    return updated_post
    
# ! _____________________________________________________________ FE MOSHKLA HENA 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    post=db.query(models.Post).filter(models.Post.id == id,).first()
    # print(post)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="you are not allowed to do the action")

    db.delete(post)
    db.commit()
    print(colored("post deleted","red"))
    # return 
    return JSONResponse(content={"Message":"Post deleted"})




@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    UPLOAD_DIRECTORY = "uploads"
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    
    # Save the file
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"info": f"File '{file.filename}' saved at '{file_location}'"}