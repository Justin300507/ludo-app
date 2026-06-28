from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    avatar_url = Column(String(255), nullable=True)
    role = Column(String(20), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    game_players = relationship("GamePlayer", cascade="all, delete-orphan")
    moves = relationship("Move", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", cascade="all, delete-orphan")
    leaderboard_entries = relationship("LeaderboardEntry", cascade="all, delete-orphan")

User = Users  # alias
