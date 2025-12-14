# Database connection and session management

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.config import settings
from app.models.customer import Base

# Create database enging
engine = create_engine(
    settings.database_url,
    echo = settings.debug,
    connect_args = {"check_same_thread": False}
)

# Create session factory
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def create_tables():
    Base.metadata.create_all(bind = engine)

def get_db() -> Generator[Session, None, None]:
    # FastAPI dependency injection to provide databases session

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()