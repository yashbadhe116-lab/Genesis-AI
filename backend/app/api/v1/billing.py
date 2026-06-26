from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.schemas.transaction import TransactionResponse
from app.services import billing_service
from typing import List

router = APIRouter(prefix="/billing", tags=["billing"])

@router.get("/transactions", response_model=List[TransactionResponse])
def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return billing_service.get_transaction_history(db, current_user.id)
