import jwt
from uuid import UUID # 👈 Import UUID
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.config import settings
from models.user import User
from schemas.token import TokenPayload # Ensure this matches your schema file
from crud.user import get_user_by_id # Ensure this points to your user service
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
        # 1. Decode using PyJWT
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        # 2. THE FIX: Cast the 'sub' to a UUID object, not an int
        user_id = UUID(token_data.sub) 
        
    except (jwt.PyJWTError, ValueError): # Catch JWT errors and UUID format errors
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Could not validate credentials"
        )
    
    # 3. Use the UUID object to fetch the user
    user = await get_user_by_id(db, id=user_id) 
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
        
    return user