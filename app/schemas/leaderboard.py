from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class LeaderboardCreate(BaseModel):
    """Schema for creating a leaderboard entry."""
    username: str = Field(min_length=1)
    score: int = Field(ge=0)

class LeaderboardUpdate(BaseModel):
    """Schema for updating a leaderboard entry."""
    username: Optional[str] = Field(default=None, min_length=1)
    score: Optional[int] = Field(default=None, ge=0)
    rank: Optional[int] = None

class LeaderboardResponse(BaseModel):
    """Schema for returning leaderboard data."""
    id: int
    user_id: int
    username: str
    score: int
    rank: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
