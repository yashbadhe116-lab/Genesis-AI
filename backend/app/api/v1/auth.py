from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError

from app.core.config import settings
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token, UserLogin
from app.services import user_service, auth_service
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

DbSession = Depends(get_db)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = DbSession):
    if user_service.get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(db, user_data)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = DbSession):
    user = user_service.get_user_by_email(db, form_data.username) # Using username as email here
    if not user or not auth_service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = auth_service.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = DbSession):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    user = user_service.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
