# backend/database/session.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import settings
from database.base import Base

# WRAP THIS IN str()
engine = create_async_engine(str(settings.DATABASE_URL), pool_pre_ping=True)

# Also ensure you are using AsyncSessionLocal
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    autocommit=False, 
    autoflush=False, 
    expire_on_commit=False
)