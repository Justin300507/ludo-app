from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class GamePlayer(Base):
    __tablename__ = "game_players"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    player_order = Column(Integer, nullable=False)
    token_positions = Column(Text)
    is_ready = Column(Boolean, nullable=False)

    game = relationship("Game" )
    user = relationship("User" )