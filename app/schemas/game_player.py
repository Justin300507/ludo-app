from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class GamePlayerCreate(BaseModel):
    game_id: int = Field(..., ge=1)
    user_id: Optional[int] = None
    guest_name: Optional[str] = None
    order: Optional[int] = None
    ready: Optional[bool] = None
    token_position: Optional[int] = None

class GamePlayerUpdate(BaseModel):
    game_id: Optional[int] = None
    user_id: Optional[int] = None
    guest_name: Optional[str] = None
    order: Optional[int] = None
    ready: Optional[bool] = None
    token_position: Optional[int] = None

class GamePlayerResponse(BaseModel):
    id: int
    game_id: int
    user_id: Optional[int] = None
    guest_name: Optional[str] = None
    order: Optional[int] = None
    ready: Optional[bool] = None
    token_position: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class GamePlayerRead(GamePlayerResponse):
    """Schema for reading a game player, identical to response."""
    pass