from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core import security
from models.user import User
from schemas.user import UserCreate
import uuid

async def get_by_username(db: AsyncSession, username: str):
    # Modern SQLAlchemy 2.0 Async Select
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()

async def create(db: AsyncSession, *, obj_in: UserCreate):
    db_obj = User(
        username=obj_in.username,
        hashed_password=security.get_password_hash(obj_in.password)
    )
    db.add(db_obj)
    await db.commit()      # MUST BE AWAITED
    await db.refresh(db_obj) # MUST BE AWAITED
    return db_obj

async def authenticate(db: AsyncSession, *, username: str, password: str):
    user = await get_by_username(db, username=username) # Await the helper
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user

async def get_user_by_id(db: AsyncSession, id: uuid.UUID):
    # Updated to UUID since we fixed the ID issue
    result = await db.execute(select(User).filter(User.id == id))
    return result.scalars().first()
