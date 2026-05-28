from logging.config import fileConfig
import os
from pathlib import Path

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from dotenv import load_dotenv

from alembic import context

# Alembic Config object
config = context.config

# Configure Python logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Load .env from the project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env", override=True)

# Read database credentials from .env
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Your local PostgreSQL is mapped to localhost:5433
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")

if not DB_USER or not DB_PASSWORD or not DB_NAME:
    raise RuntimeError(
        "Missing DB_USER, DB_PASSWORD, or DB_NAME in .env file. "
        "Please check your .env configuration."
    )

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("ALEMBIC DATABASE URL =", DATABASE_URL)

# Tell Alembic to use this URL
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# No SQLAlchemy models yet, so keep this as None.
# Later, if you create ORM models, this can point to Base.metadata.
target_metadata = None


def run_migrations_offline() -> None:
    """
    Run migrations without opening a live DB connection.
    This is less common for local development.
    """
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations against a live PostgreSQL database connection.
    This is what you will normally use locally.
    """
    configuration = config.get_section(config.config_ini_section)

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
