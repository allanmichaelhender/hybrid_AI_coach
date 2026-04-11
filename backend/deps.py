import jwt
from uuid import UUID
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.config import settings
from models.user import User
from schemas.token import TokenPayload
from crud.user import get_user_by_id
from fastapi.security import OAuth2PasswordBearer
from database.session import AsyncSessionLocal


# Opening up a new database session
async def get_db():
    async with AsyncSessionLocal() as session:
        # We use yield to keep the session open until the endpoint tells us to close, remember we pair with Depends to do this
        yield session


# Code to grab the access token from the authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/access-token")


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        # Data validation step
        token_data = TokenPayload(**payload)

        user_id = UUID(token_data.sub)

    except (jwt.PyJWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    user = await get_user_by_id(db, id=user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


async def get_current_user_optional(
    db: Session = Depends(get_db),
    token: str = Depends(
        OAuth2PasswordBearer(tokenUrl="/auth/login/access-token", auto_error=False)
    ),
) -> User | None:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        # Data validation step
        token_data = TokenPayload(**payload)

        user_id = UUID(token_data.sub)

    except (jwt.PyJWTError, ValueError):
        return None

    user = await get_user_by_id(db, id=user_id)

    if not user:
        return None

    return user
