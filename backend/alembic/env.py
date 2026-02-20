import os
import sys
import asyncio # NEW: Required for async migrations
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config # NEW: Async engine
from alembic import context
import selectors

# Ensure the root project dir is in path
sys.path.insert(0, os.getcwd())

from core.config import settings
from database.base_class import Base
# Importing models ensures they are registered on Base.metadata
from models.user import User 
from models.plan import UserPlan
from models.workout import Workout

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Dynamically set the URL from our Pydantic settings
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))
target_metadata = Base.metadata

def include_object(object, name, type_, reflected, compare_to):
    """NEW: Prevents Alembic from trying to drop internal PG tables."""
    if type_ == "table" and name == "spatial_ref_sys":
        return False
    return True

def do_run_migrations(connection):
    """Helper to run the actual migration logic on a connection."""
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        compare_type=True,
        include_object=include_object # NEW: Use the filter
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode using an Async Engine."""
    # Build configuration with our DATABASE_URL
    configuration = config.get_section(config.config_ini_section, {})
    
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # We use run_sync because Alembic's core is still synchronous
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object
    )
    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    # THE WINDOWS FIX: 
    # Force the SelectorEventLoop which Psycopg requires
    loop = asyncio.SelectorEventLoop(selectors.SelectSelector())
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_migrations_online())
    finally:
        loop.close()
