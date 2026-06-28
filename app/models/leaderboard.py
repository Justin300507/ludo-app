from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class LeaderboardEntry(Base):
    __tablename__ = "leaderboard_entries"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    score = Column(Float, nullable=False)
    rank = Column(Integer, nullable=True)
    period = Column(String, nullable=False, default="all_time")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship to User; defined as string to avoid circular imports
    user = relationship("User", back_populates="leaderboard_entries")

    def __repr__(self) -> str:
        return (
            f"<LeaderboardEntry id={self.id} user_id={self.user_id} "
            f"score={self.score} rank={self.rank}>"
        )

# Alias to satisfy imports expecting a `Leaderboard` symbol
Leaderboard = LeaderboardEntry