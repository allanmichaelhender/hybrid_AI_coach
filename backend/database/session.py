from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import settings
from database.base import Base

engine = create_async_engine(str(settings.DATABASE_URL), pool_pre_ping=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    autocommit=False, 
    autoflush=False, 
    expire_on_commit=False
)