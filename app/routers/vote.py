from fastapi import FastAPI , Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.exc import IntegrityError
from termcolor import colored
from .. import  schemas, database, models, oauth2
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/vote", tags=["vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db:Session=Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post= db.query(models.Post).filter(models.Post.id == vote.post_id). first()
    if not post:
        raise HTTPException(status_code=404, detail="post does not exist")
    
    q_vote=db.query(models.Votes).filter(models.Votes.post_id==vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = q_vote.first()
    if(vote.dir ==1):
        if found_vote:
            raise HTTPException(status_code=409, detail="user has already voted on this post")
        new_vote = models.Votes(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message":"vote added"}
        # new_vote.commit()
    else:
        if not found_vote:
            raise HTTPException(status_code=404, detail="vote does not exist")
        q_vote.delete()
        db.commit()
        return {"message":"vote Deleted"}