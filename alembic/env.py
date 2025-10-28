import os
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context

# -----------------------------------------------------------------------------
# Alembic Config object
# -----------------------------------------------------------------------------
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -----------------------------------------------------------------------------
# Try to import DATABASE_URL and Base from your app
# -----------------------------------------------------------------------------
DATABASE_URL = None
Base = None

try:
    from app.db.database import Base, DATABASE_URL
except Exception:
    try:
        # Fallback: import Base directly from models
        from app.db.models import Base
    except ImportError:
        Base = None

    # Fallback: use environment variable or alembic.ini value
    DATABASE_URL = (
        os.getenv("DATABASE_URL")
        or config.get_main_option("sqlalchemy.url")
        or "sqlite:///./dev.db"
    )

if not DATABASE_URL:
    raise RuntimeError(
        "❌ DATABASE_URL could not be determined for Alembic migrations."
    )

if Base is None:
    raise RuntimeError(
        "❌ SQLAlchemy Base could not be imported for Alembic migrations."
    )

target_metadata = Base.metadata

print(f"✅ Using DATABASE_URL: {DATABASE_URL}")


# -----------------------------------------------------------------------------
# Migration functions
# -----------------------------------------------------------------------------
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
