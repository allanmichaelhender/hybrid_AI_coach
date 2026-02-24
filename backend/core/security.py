import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from core.config import settings

# Password hashing function
def get_password_hash(password: str) -> str:
    # Convert password to bytes
    pwd_bytes = password.encode('utf-8')
    # Generate salt to add on end of password
    salt = bcrypt.gensalt()

    # Hash the password 
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    
    # Return as string for DB storage
    return hashed_password.decode('utf-8')

# Function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # We use bcypt's checkpw function, this takes the encoded passwords, and checks them against each other, returning true if the same
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False

def create_access_token(user_id: str |Any) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # First we create a dict for jose to use
    to_encode = {"exp": expire, "sub": str(user_id), "type": "access"}

    # We encode using our secret key and our algorith from env/settings
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(user_id: Union[str, Any]) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode = {"exp": expire, "sub": str(user_id), "type": "refresh"}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
