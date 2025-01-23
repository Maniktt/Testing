from pydantic import BaseModel
from typing import Optional
from app.config import ORMConfig

class UserCreate(BaseModel):
    name: str
    age: int
    email: str
    password: str

#obj = UserCreate("python", "age", "email", "password")

class UserUpdate(BaseModel):
    name: str
    email: str
    age: int

class UserResponse(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None

class UserPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    description: Optional[str] = None

    class Config:
        from_attributes = ORMConfig.from_attributes

        """
        Pydantic doesn't directly allow us to use the Config class without defining it in each model, we can follow the pattern
        where UserResponse will inherit from BaseModel and we can use the orm_mode variable directly in the Config class of BaseModel.
        """