from pydantic import BaseModel, EmailStr
from typing import List
from typing import Optional


class PermissionResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class GroupResponse(BaseModel):
    id: int
    name: str
    permissions: List[PermissionResponse] 

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    role_id: Optional[int]
    role_name: Optional[str]
    permissions: List[str]
    
    class Config:
        orm_mode = True
    

class CreateUser(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    username: str
    role_id: int


class UpdateUser(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    username: str
    role_id: int
    
    class Config:
        orm_mode = True

class CreateUserResponse(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    role_id: int

class UserLogin(BaseModel):
    username: str
    password: str

    
class CreateGroup(BaseModel):
    name: str


class GroupResponse(BaseModel):
    id: int
    name: str


class Permission(BaseModel):
    name: str
    group: int


class CheckUserResponse(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    role_id: int
    role_name: str
    permissions: List[str]
    created_at: str
    email: str

    class Config:
        orm_mode = True