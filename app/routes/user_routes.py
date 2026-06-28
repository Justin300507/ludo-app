from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List, Dict

from app.database import get_db
from app.schemas.user import UserCreate, UserUpdate
from app.utils.auth import get_password_hash, get_current_user

# Router variable must be named exactly "user_router"
user_router = APIRouter()

# Lazy import to avoid duplicate model registration at import time
def _UserModel():
    from app.models.users import Users
    return Users

@user_router.get("/users", response_model=Dict)
def list_users(
    username: Optional[str] = Query(None, min_length=1),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: "Users" = Depends(get_current_user),
):
    """List users with optional username search and pagination.
    Returns a JSON object {"items": [...], "total": <int>}.
    """
    Users = _UserModel()
    base_query = db.query(Users)
    if username:
        base_query = base_query.filter(Users.username.ilike(f"%{username}%"))
    total = base_query.count()
    users = base_query.offset(offset).limit(limit).all()
    items = [
        {
            "id": u.id,
            "email": u.email,
            "username": u.username,
            "display_name": getattr(u, "display_name", None),
        }
        for u in users
    ]
    return {"items": items, "total": total}

@user_router.get("/users/{user_id}", response_model=Dict)
def get_user(
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: "Users" = Depends(get_current_user),
):
    """Retrieve a single user by ID."""
    Users = _UserModel()
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "display_name": getattr(user, "display_name", None),
    }

@user_router.post("/users", status_code=status.HTTP_201_CREATED, response_model=Dict)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    """Create a new user account (registration)."""
    Users = _UserModel()
    hashed_password = get_password_hash(user_in.password)
    new_user = Users(
        email=user_in.email,
        username=user_in.username,
        password_hash=hashed_password,
        display_name=user_in.display_name,
    )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User with given email or username already exists")
    return {
        "id": new_user.id,
        "email": new_user.email,
        "username": new_user.username,
        "display_name": getattr(new_user, "display_name", None),
    }

@user_router.put("/users/{user_id}", response_model=Dict)
def update_user(
    user_in: UserUpdate,
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: "Users" = Depends(get_current_user),
):
    """Update user profile data (e.g., avatar, username)."""
    Users = _UserModel()
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    # Only allow the user themselves or an admin to update
    if current_user.id != user.id and getattr(current_user, "role", None) != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    update_data = user_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "display_name": getattr(user, "display_name", None),
    }

@user_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: "Users" = Depends(get_current_user),
):
    """Delete a user account (admin only)."""
    Users = _UserModel()
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    if getattr(current_user, "role", None) != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    db.delete(user)
    db.commit()
    return None
