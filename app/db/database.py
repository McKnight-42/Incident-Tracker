import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

# Detect Docker environment
if DATABASE_URL and "db:" in DATABASE_URL:
    # Docker environment
    pass
else:
    # Local fallback
    DATABASE_URL = DATABASE_URL or "sqlite:///./dev.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
