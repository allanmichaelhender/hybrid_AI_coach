from sqlalchemy.orm import Session
from core import security
from models.user import User
from schemas.user import UserCreate

def get_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create(db: Session, *, obj_in: UserCreate):
    db_obj = User(
        username=obj_in.username,
        hashed_password=security.get_password_hash(obj_in.password)
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def authenticate(db: Session, *, username: str, password: str):
    user = get_by_username(db, username=username)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user


def get(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()