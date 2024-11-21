from fastapi import FastAPI, Response
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

from .routers import user 


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# models.Base.metadata.create_all(bind=engine) 

app = FastAPI(
    title="Boilerplate API",
    description="A boilerplate for a FastAPI project",
    docs_url="/"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)


