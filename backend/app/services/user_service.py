from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth_service import get_password_hash
import uuid

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.execute(select(User).where(User.email == email)).scalar_one_or_none()

def get_user_by_id(db: Session, user_id: uuid.UUID) -> Optional[User]:
    return db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()

def create_user(db: Session, user_create: UserCreate) -> User:
    hashed_password = get_password_hash(user_create.password)
    user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
