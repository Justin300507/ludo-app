from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class UserCreate(BaseModel):
    email: str = Field(min_length=1)
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)
    display_name: str = Field(min_length=1)

class UserUpdate(BaseModel):
    email: Optional[str] = Field(default=None, min_length=1)
    username: Optional[str] = Field(default=None, min_length=1)
    display_name: Optional[str] = Field(default=None, min_length=1)
    avatar_url: Optional[str] = None
    role: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

