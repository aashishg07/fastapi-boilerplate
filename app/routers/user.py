from app import utils
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from typing import Optional,List
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix = "/users",
)


@router.post("/sign-up/", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateUserResponse, tags=["User"])
def create_user(create_user: schemas.CreateUser, db: Session = Depends(get_db)):
    """Create a new user and save the file path to the database."""
    existing_email = db.query(models.User).filter(models.User.email == create_user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    existing_username = db.query(models.User).filter(models.User.username == create_user.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    hashed_password = utils.hash(create_user.password)

    new_user = models.User(
        email=create_user.email,
        password=hashed_password,
        first_name=create_user.first_name,
        last_name=create_user.last_name,
        username=create_user.username,
        role_id=create_user.role_id,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
            

# Retrieve specific users if filtered by id else retrieve all
@router.get("/", response_model=List[schemas.UserResponse], tags=["User"])
def get_users(db: Session = Depends(get_db), id: Optional[int] = None):
    query = db.query(models.User)   
    if id is not None:
        query = query.filter(models.User.id == id)

    users = query.all()
    
    user_responses = []
    for user in users:
        role = user.role
        role_name = role.name if role else None
        permissions = [perm.name for perm in role.permissions] if role and role.permissions else []

        user_responses.append({
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role_id": user.role_id,
            "role_name": role_name,
            "permissions": permissions,
        })
    
    return user_responses


@router.post("/login/", tags=["User"])
def login_user(user_creds: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_creds.username).first()

    if not user or not utils.validate_user(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
   
    # Generate access token
    access_token = utils.create_access_token(data={"id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.patch("/update/{id}/", tags=["User"], response_model = schemas.UpdateUser)
def update_user(update_user: schemas.UpdateUser, id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.email = update_user.email
    user.first_name = update_user.first_name
    user.last_name = update_user.last_name
    user.username = update_user.username
    user.role_id = update_user.role_id

    db.commit()
    db.refresh(user)

    return user

@router.get("/check-user/", tags=["User"])
def check_user(db: Session = Depends(get_db), token: str = Depends(utils.get_current_token)):
    # Decode token to extract user information
    token_data = utils.decode_token(token)
    id = token_data.get("id")

    if not id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token or user not found"
        )

    # Query user details
    user = (
        db.query(models.User).filter(models.User.id == id).first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Prepare response data
    role_name = user.role.name if user.role else None
    permissions = [perm.name for perm in user.role.permissions] if user.role and user.role.permissions else []

    response_data = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role_id": user.role_id,
        "role_name": role_name,
        "permissions": permissions,
        "created_at": user.created_at.date(),
        "email": user.email,
    }

    return response_data
    

@router.delete("/{id}", tags=["User"])
def delete_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    
    user.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/group/", tags=["Group"])
def create_group(group: schemas.CreateGroup, db: Session = Depends(get_db)):
    existing_group = db.query(models.Group).filter(models.Group.name == group.name).first()
    if existing_group:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Group already exists")
    groups = models.Group(name=group.name)
    db.add(groups)
    db.commit()
    db.refresh(groups)
    return groups


@router.get("/group/", tags=["Group"])
def get_groups(db: Session = Depends(get_db), id: Optional[int] = None):
    groups = db.query(models.Group)
    if id is not None:
        groups = groups.filter(models.Group.id == id)
    groups = groups.all()
    return groups


@router.patch("/group/{id}/", tags=["Group"])
def update_group(update_group: schemas.CreateGroup, id: int, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.id == id).first()

    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    group.name = update_group.name

    db.commit()
    db.refresh(group)

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
def get_permissions(db: Session = Depends(get_db), id: Optional[int] = None):
    query = db.query(models.Permission)

    if id is not None:
        query = query.filter(models.Permission.id == id)

    permissions = query.all()
    return permissions


@router.patch("/permission/{id}/", tags=["Permission"])
def update_permissions(update_permission: schemas.Permission, id: int, db: Session = Depends(get_db)):
    permission = db.query(models.Permission).filter(models.Permission.id == id).first()

    if not permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")

    permission.name = update_permission.name
    permission.group = update_permission.group

    db.commit()
    db.refresh(permission)

    return permission

@router.delete("/delete/{id}/", tags=["Permission"])
def delete_permission(id: int, db: Session = Depends(get_db)):
    permission = db.query(models.Permission).filter(models.Permission.id == id)
    
    if not permission.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Permission not found')
    
    permission.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# TODO: forgot password / reset password and nested permissions on group list