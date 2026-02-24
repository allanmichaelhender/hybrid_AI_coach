from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import settings

# Creating the connection engine, pool_pre_ping pings the db to confirm liveliness
engine = create_async_engine(str(settings.DATABASE_URL), pool_pre_ping=True)

# Code to create individual database sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    autocommit=False, 
    autoflush=False, 
    expire_on_commit=False
)