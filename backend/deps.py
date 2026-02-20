from typing import Generator
from db.session import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from core.config import settings
from crud.user import get as get_user
import models
from schemas.token import TokenPayload
from models.user import User

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/access-token")

def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, jwt.exceptions.PyJWTError):
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    user = get_user(db, id=int(token_data.sub)) 
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user