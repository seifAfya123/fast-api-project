from fastapi import FastAPI, HTTPException, Response ,status
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor 
from pydantic import BaseModel
from termcolor import colored
from typing import Optional
import time

app = FastAPI()

class Post(BaseModel):
    title: str 
    content: str
    published:bool=True
    rating: Optional[int] = 3
    
    
    
while True:
    
    try:
        conn=psycopg2.connect(host="localhost",database="fastapidb",user="postgres",password="5432",cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print(colored("Data base connected successfully ... ","green"))
        break
    except Exception as error:
        print(colored("connection faild ...","red"))
        print("error: ",error)
        time.sleep(2)

@app.get("/posts")
async def index():
    cursor.execute("""SELECT * FROM public.posts""")
    dbposts= cursor.fetchall()
    return {"posts":dbposts}

@app.get("/post/{id}")
async def get_post(id: str):
    cursor.execute("""SELECT * FROM posts Where id = %s """,(str(id),))
    post=cursor.fetchone()
    if not post:
        print(colored("post not found","red"))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no post found with this id")
    print(colored("post found","cyan"))
    return {"post":post}

@app.post("/post", status_code=status.HTTP_201_CREATED)
async def create_post(post:Post):
    cursor.execute("""INSERT INTO posts (title,content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title,post.content,post.published))
    new_post=cursor.fetchone()
    conn.commit()
    return {"message":"post created sucessfully", "post":new_post}

@app.put("/post/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_post(id:int , post : Post):
    cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s where id= %s RETURNING *""",
                   (post.title,post.content,post.published,str(id),))
    updated_post=cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found with this id")
    else:
        return {"message":"post updated sucessfully"}
    
    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    deleted_post_reference = cursor.fetchone()
    conn.commit()

    if deleted_post_reference is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    print("Post deleted successfully")
    return {"message": "Post deleted successfully"}