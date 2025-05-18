 
from pydantic import BaseModel,ConfigDict
from typing import Optional
from datetime import datetime

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

