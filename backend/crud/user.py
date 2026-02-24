from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core import security
from models.user import User
from schemas.user import UserCreate
import uuid

# function to find all user info by username
async def get_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()


async def create(db: AsyncSession, *, obj_in: UserCreate):
    db_obj = User(
        username=obj_in.username,
        hashed_password=security.get_password_hash(obj_in.password),
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

# Function to authentica a user on login, it returns the user object
async def authenticate(db: AsyncSession, *, username: str, password: str):
    user = await get_by_username(db, username=username)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user

# function to find all user info by id (uuid)
async def get_user_by_id(db: AsyncSession, id: uuid.UUID):

    result = await db.execute(select(User).filter(User.id == id))
    return result.scalars().first()
