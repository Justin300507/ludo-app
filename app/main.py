from app.models.user import User
from fastapi import FastAPI

from app.database import Base, engine

# import models
from app.models.games import *  # noqa: F401
from app.models.chat_messages import *  # noqa: F401
from app.models.users import *  # noqa: F401
from app.models.moves import *  # noqa: F401
from app.models.game_players import *  # noqa: F401
from app.models.leaderboard_entries import *  # noqa: F401

# import routers
from app.routes.stats_routes import stats_router
from app.routes.user_routes import user_router
from app.routes.game_player_routes import game_player_router
from app.routes.game_routes import game_router
from app.routes.seed_routes import seed_router
from app.routes.leaderboard_routes import leaderboard_router
from app.routes.chat_message_routes import chat_message_router

app = FastAPI()

# CORS (required for frontend access)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health endpoint (required for deployment health checks)
@app.get("/health")
def health():
    return {"status": "ok"}

# Create tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(stats_router)
app.include_router(user_router)
app.include_router(game_player_router)
app.include_router(game_router)
app.include_router(seed_router)
app.include_router(leaderboard_router)
app.include_router(chat_message_router)
