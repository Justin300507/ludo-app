from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Move(Base):
    __tablename__ = "moves"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dice_value = Column(Integer, nullable=False)
    token_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False, server_default=func.now())

    game = relationship("Game" )
    player = relationship("User" )
    token = relationship("Token" )