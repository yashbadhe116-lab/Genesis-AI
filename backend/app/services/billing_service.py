import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.models.transaction import Transaction

def deduct_credits(db: Session, user_id: uuid.UUID, amount: int, description: str):
    # Atomic deduction using row-level locking (FOR UPDATE)
    user = db.execute(
        select(User).where(User.id == user_id).with_for_update()
    ).scalar_one()

    if user.credits < amount:
        raise ValueError("Insufficient credits")

    user.credits -= amount
    
    transaction = Transaction(
        user_id=user_id,
        amount=-amount,
        description=description
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(user)
    return user

def get_transaction_history(db: Session, user_id: uuid.UUID):
    return db.execute(
        select(Transaction).where(Transaction.user_id == user_id).order_by(Transaction.created_at.desc())
    ).scalars().all()
