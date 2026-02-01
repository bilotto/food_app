from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os

from pathlib import Path

# Database configuration
# Use YAZIO_DB_PATH environment variable or fallback to ./data/yazio.db
DB_PATH = Path(os.getenv("YAZIO_DB_PATH", "data/yazio.db")).resolve()

# Ensure the directory for the database exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Use absolute path for SQLite to avoid "unable to open database file" issues
if os.name == 'nt':
    # SQLAlchemy on Windows likes sqlite:///C:\path\to\db
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
else:
    # On Unix, sqlite:////path/to/database.db
    SQLALCHEMY_DATABASE_URL = f"sqlite:////{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
