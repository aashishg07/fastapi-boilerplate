from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from typing import Optional,List

from fastapi.responses import JSONResponse
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import engine, get_db


router = APIRouter(
    prefix = "/users",
    tags=['Users'] 
)

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    get_all_users = db.query(models.User).all()
    return get_all_users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserResponse)
def create_User(create_user: schemas.CreateUser, db:Session = Depends(get_db)):
    # Create a new user and save the file path to the database
    existing_email = db.query(models.User).filter(models.User.email == create_user.email).first()
    if existing_email:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Email already exists"}
        )

    # Check if the username already exists
    existing_username = db.query(models.User).filter(models.User.username == create_user.username).first()
    if existing_username:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Username already exists"}
        )
    db_user = models.User(
        email=create_user.email,
        password=create_user.password,  # Remember to hash the password in a real app
        first_name=create_user.first_name,
        last_name=create_user.last_name,
        username=create_user.username,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    if db_user:
        return db_user
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND, detail='User not created')

@router.get("/{id}", response_model=schemas.GetUser)
def get_one_user(id:int, db:Session = Depends(get_db)):
    get_single = db.query(models.User).filter(models.User.id == id).first()
    
    if not get_single:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return get_single







    
    
   
    