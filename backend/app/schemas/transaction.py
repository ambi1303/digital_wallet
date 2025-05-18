from typing import Optional
from datetime import datetime
from pydantic import BaseModel, confloat
from app.core.models import TransactionType

class TransactionBase(BaseModel):
    amount: confloat(gt=0)
    currency: str
    transaction_type: TransactionType
    description: Optional[str] = None
    recipient_id: Optional[int] = None

class TransactionCreate(TransactionBase):
    user_id: int
    wallet_id: int

class TransactionUpdate(BaseModel):
    is_flagged: bool

class TransactionInDBBase(TransactionBase):
    id: int
    user_id: int
    wallet_id: int
    is_flagged: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Transaction(TransactionInDBBase):
    pass

class TransactionInDB(TransactionInDBBase):
    pass 