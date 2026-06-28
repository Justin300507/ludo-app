from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.games import Game
from app.schemas.game import GameCreate, GameUpdate
from app.utils.auth import get_current_user
import random
import string

game_router = APIRouter()

def _generate_lobby_code(length: int = 6) -> str:
    """Generate a random alphanumeric lobby code of given length."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

@game_router.get("/games", response_model=dict)
def list_games(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    lobby_code: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    """List games with optional filters and pagination."""
    query = db.query(Game)
    if lobby_code:
        query = query.filter(Game.lobby_code == lobby_code)
    if status:
        query = query.filter(Game.status == status)
    total = query.count()
    games = query.offset(offset).limit(limit).all()
    items = []
    for game in games:
        data = game.__dict__.copy()
        data.pop("_sa_instance_state", None)
        items.append(data)
    return {"items": items, "total": total}

@game_router.get("/games/{game_id}", response_model=dict)
def get_game(
    game_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    """Retrieve a single game by its ID."""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Not found")
    data = game.__dict__.copy()
    data.pop("_sa_instance_state", None)
    return data

@game_router.post("/games", status_code=201, response_model=dict)
def create_game(
    game_in: GameCreate,
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    """Create a new game lobby. Generates a unique lobby code automatically."""
    lobby_code = _generate_lobby_code()
    # Ensure the generated lobby code is unique
    while db.query(Game).filter(Game.lobby_code == lobby_code).first():
        lobby_code = _generate_lobby_code()
    new_game = Game(
        title=game_in.title,
        description=game_in.description,
        is_private=game_in.is_private,
        lobby_code=lobby_code,
        status="waiting",
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    data = new_game.__dict__.copy()
    data.pop("_sa_instance_state", None)
    return data

@game_router.put("/games/{game_id}", response_model=dict)
def update_game(
    game_in: GameUpdate,
    game_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    """Update mutable fields of a game lobby."""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Not found")
    if game_in.title is not None:
        game.title = game_in.title
    if game_in.description is not None:
        game.description = game_in.description
    if game_in.is_private is not None:
        game.is_private = game_in.is_private
    # Allow status updates if the schema provides it
    if hasattr(game_in, "status") and getattr(game_in, "status", None) is not None:
        game.status = game_in.status  # type: ignore
    db.commit()
    db.refresh(game)
    data = game.__dict__.copy()
    data.pop("_sa_instance_state", None)
    return data

@game_router.delete("/games/{game_id}", status_code=204)
def delete_game(
    game_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    """Delete a game lobby."""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(game)
    db.commit()
    return
