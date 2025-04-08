from fastapi import FastAPI,Response,status,HTTPException
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
from random import  randrange

app= FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published:bool=True
    rating: Optional[int] =None

my_post=[
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "published": True,
        'id': 1
    },
    {
        "title": "title of post 2",
        "content": "content of post 2",
        "published": False,
        'id': 2
    }
]

def get_post_by_id(id):
    for p in my_post:
        if p['id']==id:
            return p
    return None



@app.get("/")
def root():
    return {"message": "Hello World back"}

@app.get("/posts")
def get_posts():
    return {"data": my_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    print(f"response is: {response}")
    post=get_post_by_id(id)
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    # if not post:
    #     response.status_code=status.HTTP_404_NOT_FOUND
    #     return {"message": f"Post with id {id} not found"}
    return {"The post you're looking for is": post}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    print(post)
    print(post.dict())
    post_dict= post.dict()
    post_dict['id']= randrange(0, 1000000)
    my_post.append(post_dict)
    return {"data": post_dict}