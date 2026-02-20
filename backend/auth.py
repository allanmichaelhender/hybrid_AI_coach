from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession # NEW: Use AsyncSession

from core import security
from core.config import settings
from crud import user as user_crud
import deps
from schemas import user as user_schema
from schemas import token as token_schema

from jose import jwt # Use python-jose for consistency

router = APIRouter()

@router.post("/register", response_model=user_schema.UserOut)
async def register_user( # ADD: async
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: user_schema.UserCreate
) -> Any:
    """Register a new user."""
    # ADD: await
    user = await user_crud.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    # ADD: await
    return await user_crud.create(db, obj_in=user_in)

@router.post("/login/access-token", response_model=token_schema.Token)
async def login_access_token( # ADD: async
    db: AsyncSession = Depends(deps.get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    # ADD: await
    user = await user_crud.authenticate(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # Subject is now a UUID, but create_access_token usually expects a string
    return {
        "access_token": security.create_access_token(subject=str(user.id)),
        "refresh_token": security.create_refresh_token(subject=str(user.id)),
        "token_type": "bearer",
    }

@router.post("/refresh", response_model=token_schema.Token)
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(deps.get_db)):
    try:
        # Use jose.jwt
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    return {
        "access_token": security.create_access_token(user_id),
        "token_type": "bearer",
    }
