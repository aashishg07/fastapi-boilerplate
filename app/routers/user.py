from app import utils
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from typing import Optional,List

from fastapi.responses import JSONResponse
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import engine, get_db
from passlib.context import CryptContext



router = APIRouter(
    prefix = "/users",
)


@router.post("/sign-up/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserResponse, tags=["User"])
def create_User(create_user: schemas.CreateUser, db:Session = Depends(get_db)):
    # Create a new user and save the file path to the database
    hashed_password = utils.hash(create_user.password)
    # Check if email already exists
    existing_email = db.query(models.User).filter(models.User.email == create_user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    # Check if the username already exists
    existing_username = db.query(models.User).filter(models.User.username == create_user.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    db_user = models.User(
        email=create_user.email,
        password=hashed_password,
        first_name=create_user.first_name,
        last_name=create_user.last_name,
        username=create_user.username,
    )
    db.add(db_user) # Adds the new user to the database.
    db.commit() # Commits the changes to the database
    db.refresh(db_user) # Reloads the user from the database to include any auto-generated fields (like id and created_at).

    if db_user:
        return db_user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not created"
        )
            

# List all user
@router.get("/", response_model=List[schemas.UserResponse], tags=["User"])
def get_users(db: Session = Depends(get_db)):
    get_all_users = db.query(models.User).all()
    return get_all_users


# Retrieve a single user by ID
@router.get("/{id}", response_model=schemas.UserResponse, tags=["User"])
def get_one_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user


@router.post("/login/", tags=["User"])
def login_user(user_creds: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_creds.username).first()

    if not user or not utils.validate_user(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
   
    # Generate access token
    access_token = utils.create_access_token(data={"username": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}
    

@router.delete("/{id}", tags=["User"])
def delete_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    
    user.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/group/", tags=["Group"])
def create_group(group: schemas.Group, db: Session = Depends(get_db)):
    existing_group = db.query(models.Group).filter(models.Group.id == group.id).first()
    if existing_group:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Group already exists")
    groups = models.Group(name=group.name)
    db.add(groups)
    db.commit()
    db.refresh(groups)
    return groups


@router.get("/group/", tags=["Group"])
def get_groups(db: Session = Depends(get_db)):
    groups = db.query(models.Group).all()
    return groups


@router.get("/group/{id}/", tags=["Group"])
def retrieve_group(id: int, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.id == id).first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return group


@router.delete("/group/{id}/", tags=["Group"])
def delete_group(id: int, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.id == id)
    
    if not group.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Group not found')
    
    group.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/permission/", tags=["Permission"])
def create_permission(permission: schemas.Permission, db: Session = Depends(get_db)):
    existing_permission = db.query(models.Permission).filter(models.Permission.name == permission.name).first()
    if existing_permission:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission already exists")
    
    if not db.query(models.Group).filter(models.Group.id == permission.group).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    permissions = models.Permission(name=permission.name, group=permission.group)
    db.add(permissions)
    db.commit()
    db.refresh(permissions)
    return permissions


@router.get("/permission/", tags=["Permission"])
def get_permissions(db: Session = Depends(get_db)):
    permissions = db.query(models.Permission).all()
    return permissions


@router.get("/permission/{id}/", tags=["Permission"])
def retrieve_permission(id: int, db: Session = Depends(get_db)):
    permission = db.query(models.Permission).filter(models.Permission.id == id).first()
    if not permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")

    response = schemas.PermissionResponse(
        id=permission.id,
        name=permission.name,
        group=permission.group.name 
    )
    return response


@router.delete("/delete/{id}/", tags=["Permission"])
def delete_permission(id: int, db: Session = Depends(get_db)):
    permission = db.query(models.Permission).filter(models.Permission.id == id)
    
    if not permission.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Permission not found')
    
    permission.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)