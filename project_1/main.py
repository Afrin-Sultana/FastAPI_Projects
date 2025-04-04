from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
from typing import Optional

app= FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published:bool=True
    rating: Optional[int] =None

@app.get("/")
def root():
    return {"message": "Hello World back"}

@app.get("/posts")
def get_post():
    return {"data": "This is your post"}



@app.post("/createposts")
def create_post(new_post: Post):
    print(new_post)
    print(new_post.dict())
    return {"data": new_post}