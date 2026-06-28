import os
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator

# Database URL – default to a local SQLite file if not provided
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Engine creation – sync engine as required by the project contract
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    future=True,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

# Base class for all models
Base = declarative_base()

def get_db() -> Generator:
    """FastAPI dependency that provides a database session and ensures it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
