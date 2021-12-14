from datetime import datetime
from pydantic import BaseModel, EmailStr
from sqlalchemy.sql.sqltypes import String

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class Post(PostBase):
    pass
    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email: EmailStr
    password: str
    

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True