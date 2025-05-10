from pydantic import BaseModel
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str
    published:bool=True


class User(BaseModel):
    username: str
    email: str
    password:str

class UserOut(User):
    created_at: datetime
