from typing import List, Optional
import uuid
from pydantic import BaseModel
from datetime import date
class UserCreate(BaseModel):
    email: Optional[str] = None
    name: str
    password: str
    is_active: Optional[bool] = True

class UserResponse(BaseModel):
    name: str
    email: str
    is_active: bool

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: uuid.UUID
    username: str
    email: str

    class Config:
        orm_mode = True

# Model for user authentication
class UserAuth(BaseModel):
    username: str
    password: str

# Model for token schema
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None





class SystemUser(UserOut):
    password: str

#Story


class StoryCreate(BaseModel):
    title: str
    content: str


class StoryResponse(BaseModel):
    id : uuid.UUID
    title: str
    content: str
    created_at: date
    user_id: uuid.UUID

    class Config:
        orm_mode = True