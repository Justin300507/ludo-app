from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String(200), nullable=False)
    sent_at = Column(DateTime, server_default=func.now(), nullable=False)

    game = relationship("Game" )
    sender = relationship("User" )
