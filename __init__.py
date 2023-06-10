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
from routers import todo, users, activity, orders, points

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
app.include_router(activity.router)
app.include_router(orders.router)
app.include_router(points.router)

models.Base.metadata.create_all(bind=engine)
# db: Session = Depends(get_db)


@app.get("/", status_code=status.HTTP_200_OK)
def hello():
    return {"message": "Hello World"}


@app.post("/all", status_code=status.HTTP_200_OK)
def all_data(payLoad: schemas.AllAccounts, db: Session = Depends(get_db)):
    if payLoad.type == "3":
        return db.query(models.Users.first_name, models.Users.last_name, models.Users.points).all()
    elif payLoad.password == settings.database_master_password:
        if payLoad.type == "0":
            return db.query(models.Users).all()
        elif payLoad.type == "1":
            return db.query(models.Activity).all()
        elif payLoad.type == "2":
            return db.query(models.Orders).all()
        elif payLoad.type == "4":
            return db.query(models.Addresses).all()

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
