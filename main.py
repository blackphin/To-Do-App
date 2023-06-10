from typing import List

from fastapi import FastAPI, Depends, Response, status, HTTPException
from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db
from config import settings
from routers import users, todo

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(todo.router)

models.Base.metadata.create_all(bind=engine)
# db: Session = Depends(get_db)


@app.get("/", status_code=status.HTTP_200_OK)
def hello():
    return {"message": "Hello World"}
