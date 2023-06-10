from typing import List

from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from fastapi.params import Body

from pydantic import BaseModel

from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

router = APIRouter(
    prefix="/todo",
)


@router.post("/get", status_code=status.HTTP_200_OK, response_model=List[schemas.TodoDetails])
def getTodo(payLoad: schemas.GetTodo, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(
        models.Todo.todo_id == payLoad.user_id).all()
    user_data = db.query(models.Users).filter(
        models.Users.user_id == payLoad.user_id,
        models.Todo.category == payLoad.category,
        models.Todo.status == payLoad.status)
    if (todo is None or user_data is None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Todos Found")
    elif (user_data.first() is not None):
        return todo
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No Account Found")


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=schemas.TodoDetails)
def addAddress(payLoad: schemas.AddTodo, db: Session = Depends(get_db)):
    user_data = db.query(models.Users).filter(
        models.Users.user_id == payLoad.user_id)
    if (user_data.first() is not None and user_data.first().email == payLoad.email):
        new_todo = models.Todo(user_id=payLoad.user_id, email=payLoad.email, category=payLoad.category,
                               title=payLoad.title, status=payLoad.status, description=payLoad.description)
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User Account not Found")


@router.put("/update", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.TodoDetails)
def updateAddress(payLoad: schemas.UpdateTodo, db: Session = Depends(get_db)):
    todo_data = db.query(models.Todo).filter(
        models.Todo.todo_id == payLoad.todo_id)

    user_data = db.query(models.Users).filter(
        models.Users.user_id == payLoad.user_id)

    if (todo_data.first() is None or user_data.first() is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Todo Doesn't Exist")

    elif (payLoad.todo_id == str(todo_data.first().todo_id) and payLoad.user_id == str(todo_data.first().user_id)):
        payload_dict = payLoad.dict()
        todo_data.update(payload_dict, synchronize_session=False)
        db.commit()
        return todo_data.first()

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="No Account Found")


@router.delete("/delete", status_code=status.HTTP_404_NOT_FOUND)
def deleteAddress(payLoad: schemas.DelTodo, db: Session = Depends(get_db)):
    user_data = db.query(models.Users).filter(
        models.Users.user_id == payLoad.user_id)

    todo_data = db.query(models.Todo).filter(
        models.Todo.todo_id == payLoad.todo_id)

    if user_data.first() is None or todo_data.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Account Doesn't Exist")

    elif (payLoad.todo_id == str(todo_data.first().todo_id) and payLoad.user_id == str(todo_data.first().user_id)):
        todo_data.delete(synchronize_session=False)
        db.commit()
        return {"message": "Todo Deleted"}

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Todo Doesn't Exist")
