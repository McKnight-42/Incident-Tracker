import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = os.getenv("DATABASE_URL")

# Detect if we're in Docker (use 'db' hostname) or local dev
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./dev.db"
elif "db:" not in DATABASE_URL and DATABASE_URL.startswith("postgres"):
    # Local Postgres (non-Docker)
    pass  # Keep DATABASE_URL as-is


engine = create_engine(
    DATABASE_URL,
    connect_args=(
        {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    ),
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Provide a transactional scope for database access."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
