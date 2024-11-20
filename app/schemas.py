from pydantic import BaseModel, EmailStr, PastDatetime, conint
from typing import Optional
from fastapi import File, UploadFile

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    
    
    class Config:
        orm_mode = True
    

# USER SCHEMAS DEFINED BELOW
class CreateUser(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    username: str
    

class GetUser(BaseModel):
    email: str
    created_at: PastDatetime
