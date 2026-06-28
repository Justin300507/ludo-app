from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.leaderboard import Leaderboard
# Import the User model to ensure SQLAlchemy registers it for relationships
# The relationship in other models references the class name "User".
# Importing the module that defines this class resolves the mapper initialization error.
from app.models.user import User  # noqa: F401
from app.models.users import Users
from app.schemas.leaderboard import LeaderboardCreate, LeaderboardUpdate
from typing import Optional

leaderboard_router = APIRouter()

@leaderboard_router.get("/leaderboard")
def list_leaderboard(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    username: Optional[str] = Query(None, min_length=1),
    db: Session = Depends(get_db),
):
    query = db.query(Leaderboard).join(Users, Leaderboard.user_id == Users.id)
    if username:
        query = query.filter(Users.username.ilike(f"%{username}%"))
    total = query.count()
    items = query.offset(offset).limit(limit).all()
    return {"items": items, "total": total}

@leaderboard_router.get("/leaderboard/{user_id}")
def get_leaderboard_entry(
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    entry = db.query(Leaderboard).filter(Leaderboard.user_id == user_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    return entry

@leaderboard_router.post("/leaderboard", status_code=201)
def create_leaderboard_entry(
    payload: LeaderboardCreate,
    db: Session = Depends(get_db),
):
    entry = Leaderboard(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

@leaderboard_router.put("/leaderboard/{user_id}")
def update_leaderboard_entry(
    payload: LeaderboardUpdate,
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    entry = db.query(Leaderboard).filter(Leaderboard.user_id == user_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(entry, field, value)
    db.commit()
    db.refresh(entry)
    return entry

@leaderboard_router.delete("/leaderboard/{user_id}", status_code=204)
def delete_leaderboard_entry(
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    entry = db.query(Leaderboard).filter(Leaderboard.user_id == user_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(entry)
    db.commit()
    return
