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


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/access-token")

async def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        user_id = UUID(token_data.sub) 
        
    except (jwt.PyJWTError, ValueError): 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Could not validate credentials"
        )
    
    user = await get_user_by_id(db, id=user_id) 
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
        
    return user