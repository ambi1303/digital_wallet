from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.core.models import TransactionType

class TransactionCreate(BaseModel):
    type: str  # deposit, withdraw, transfer
    amount: float
    receiver_username: Optional[str] = None
    currency: Optional[str] = "USD"

class TransactionOut(BaseModel):
    id: int
    type: str
    amount: float
    currency: str
    timestamp: datetime
    sender_id: Optional[int]
    receiver_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)

class TransactionFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    transaction_type: Optional[TransactionType] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    is_flagged: Optional[bool] = None

