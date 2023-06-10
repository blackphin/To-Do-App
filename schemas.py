from pydantic import BaseModel, EmailStr
from datetime import datetime


# Request Schemas


# Users


class CreateAccount(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str


class Login(BaseModel):
    email: EmailStr
    password: str


# Todo


class GetTodo(BaseModel):
    todo_id: str
    user_id: str
    category: str
    status: str


class DelTodo(BaseModel):
    todo_id: str
    user_id: str


class AddTodo(BaseModel):
    user_id: str
    email: str
    category: str
    status: str
    title: str
    description: str


class UpdateTodo(BaseModel):
    todo_id: str
    user_id: str
    category: str
    status: str
    title: str
    description: str


# Response Schemas


# Users


class AccountDetails(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    created_at: datetime

    class Config:
        orm_mode = True


# Todo


class TodoDetails(BaseModel):
    todo_id: str
    user_id: str
    email: EmailStr
    category: str
    status: str
    title: str
    description: str

    class Config:
        orm_mode = True
