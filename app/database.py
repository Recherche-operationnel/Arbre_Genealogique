import sqlite3
from pathlib import Path
from contextlib import contextmanager

DATABASE_PATH = "family_graph.db"

def init_db():
    """Initialize the database with the schema"""
    with get_connection() as conn:
        with open("schema.sql") as f:
            conn.executescript(f.read())
        conn.commit()

@contextmanager
def get_connection():
    """Context manager for database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def get_cursor():
    """Context manager for database cursor"""
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./family_graph.db"

# Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Make sure Base is exported
__all__ = ["Base", "engine", "SessionLocal", "get_db"]