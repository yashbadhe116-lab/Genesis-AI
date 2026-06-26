import uuid
from datetime import datetime
from pydantic import BaseModel

class TransactionResponse(BaseModel):
    id: uuid.UUID
    amount: int
    description: str
    created_at: datetime

    class Config:
        from_attributes = True
