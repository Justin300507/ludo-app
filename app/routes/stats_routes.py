from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import time

from app.database import get_db
from app.models.games import Game
from app.models.users import Users
from app.models.chat_messages import ChatMessage
from app.models.moves import Move
from app.models.game_players import GamePlayer

stats_router = APIRouter()

# Simple in‑memory cache for the summary endpoint (TTL = 30 seconds)
_STATS_CACHE = {"data": None, "timestamp": 0}
_CACHE_TTL = 30  # seconds

@stats_router.get("/stats/summary")
def get_stats_summary(db: Session = Depends(get_db)):
    """Return aggregate counts and key metrics for the dashboard.
    The result is cached for a short period to avoid heavy aggregation on every call.
    """
    now = time.time()
    if _STATS_CACHE["data"] is not None and now - _STATS_CACHE["timestamp"] < _CACHE_TTL:
        return _STATS_CACHE["data"]

    total_users = db.query(Users).count()
    total_games = db.query(Game).count()
    total_chat_messages = db.query(ChatMessage).count()
    total_moves = db.query(Move).count()
    total_game_players = db.query(GamePlayer).count()

    # Example additional metric - number of games created today (placeholder 0)
    active_today = 0

    data = {
        "total_users": total_users,
        "total_games": total_games,
        "total_chat_messages": total_chat_messages,
        "total_moves": total_moves,
        "total_game_players": total_game_players,
        "active_today": active_today,
    }

    _STATS_CACHE["data"] = data
    _STATS_CACHE["timestamp"] = now
    return data
