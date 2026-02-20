from datetime import timedelta
import token
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core import security
from core.config import settings
from crud import user as user_crud
import deps
from schemas import user as user_schema
from schemas import token as token_schema

import jwt


router = APIRouter()

@router.post("/register", response_model=user_schema.UserOut)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: user_schema.UserCreate
) -> Any:
    """Register a new user."""
    user = user_crud.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    return user_crud.create(db, obj_in=user_in)

@router.post("/login/access-token", response_model=token_schema.Token)
def login_access_token(db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_crud.authenticate(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {
        "access_token": security.create_access_token(subject=user.id),
        "refresh_token": security.create_refresh_token(subject=user.id),
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=token_schema.Token)
def refresh_token(refresh_token: str, db: Session = Depends(deps.get_db)):
    try:
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
