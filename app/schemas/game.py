from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class GameCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    is_private: bool = False


class GameUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)
    status: Optional[str] = None
    is_private: Optional[bool] = None


class GameResponse(BaseModel):
    id: int
    title: str
    description: str
    lobby_code: Optional[str] = None
    status: Optional[str] = None
    is_private: bool
    owner_id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
