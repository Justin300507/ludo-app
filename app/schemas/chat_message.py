from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ChatMessageCreate(BaseModel):
    """Schema for creating a new chat message."""

    game_id: int = Field(..., ge=1, description="Identifier of the game session")
    # The user is typically derived from the authenticated token; optional here.
    user_id: Optional[int] = Field(default=None, ge=1, description="Identifier of the author")
    content: str = Field(..., min_length=1, description="Message text")

    model_config = ConfigDict(from_attributes=True)


class ChatMessageUpdate(BaseModel):
    """Schema for updating an existing chat message (moderation)."""

    content: Optional[str] = Field(
        default=None,
        min_length=1,
        description="Updated message text",
    )

    model_config = ConfigDict(from_attributes=True)


class ChatMessageResponse(BaseModel):
    """Schema returned to clients for a chat message."""

    id: int
    game_id: int
    user_id: Optional[int] = None
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
