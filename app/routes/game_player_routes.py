from fastapi import APIRouter, Depends, HTTPException, Query, Path, Response
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.game_players import GamePlayer
from app.schemas.game_player import GamePlayerCreate, GamePlayerRead, GamePlayerUpdate
from app.utils.auth import get_current_user

# Authentication scheme (public token endpoint defined elsewhere)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Router variable must be named exactly as required
game_player_router = APIRouter()

# ---------------------------------------------------------------------------
# List game players with optional game_id filter and pagination
# ---------------------------------------------------------------------------
@game_player_router.get("/game_players", response_model=dict)
def list_game_players(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    game_id: Optional[int] = Query(None, ge=1),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    query = db.query(GamePlayer)
    if game_id is not None:
        query = query.filter(GamePlayer.game_id == game_id)
    total = query.count()
    items = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )
    return {"items": items, "total": total}

# ---------------------------------------------------------------------------
# Retrieve a specific game player by ID
# ---------------------------------------------------------------------------
@game_player_router.get("/game_players/{player_id}", response_model=GamePlayerRead)
def get_game_player(
    player_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    player = db.query(GamePlayer).filter(GamePlayer.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Not found")
    return player

# ---------------------------------------------------------------------------
# Add a player (user or guest) to a game lobby
# ---------------------------------------------------------------------------
@game_player_router.post("/game_players", response_model=GamePlayerRead, status_code=201)
def create_game_player(
    player_in: GamePlayerCreate,
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    # Ensure at least one of user_id or guest_name is provided
    if not player_in.user_id and not player_in.guest_name:
        raise HTTPException(status_code=400, detail="Either user_id or guest_name must be provided")
    new_player = GamePlayer(**player_in.model_dump())
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player

# ---------------------------------------------------------------------------
# Update player order, readiness, or token positions
# ---------------------------------------------------------------------------
@game_player_router.put("/game_players/{player_id}", response_model=GamePlayerRead)
def update_game_player(
    player_in: GamePlayerUpdate,
    player_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    player = db.query(GamePlayer).filter(GamePlayer.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Not found")
    update_data = player_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(player, field, value)
    db.commit()
    db.refresh(player)
    return player

# ---------------------------------------------------------------------------
# Remove a player from a game lobby
# ---------------------------------------------------------------------------
@game_player_router.delete("/game_players/{player_id}")
def delete_game_player(
    player_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    player = db.query(GamePlayer).filter(GamePlayer.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(player)
    db.commit()
    return Response(status_code=204)
