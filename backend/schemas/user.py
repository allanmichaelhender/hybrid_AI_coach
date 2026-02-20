from pydantic import BaseModel
import uuid

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: uuid.UUID

    class Config:
        from_attributes = True 
