from pydantic import BaseModel, EmailStr, PastDatetime, conint
from typing import Optional
from fastapi import File, UploadFile

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: int
    role_name: str
    
    class Config:
        orm_mode = True
    

class CreateUser(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    username: str
    


class UserLogin(BaseModel):
    username: str
    password: str

    
class Group(BaseModel):
    name: str


class GroupResponse(BaseModel):
    id: int
    name: str


class Permission(BaseModel):
    name: str
    group: int


class PermissionResponse(BaseModel):
    id: int
    name: str
    group: int

    class Config:
        orm_mode = True
