from typing import Optional
from datetime import datetime
from pydantic import BaseModel, confloat

class WalletBase(BaseModel):
    balance: confloat(ge=0)
    currency: str

class WalletCreate(WalletBase):
    user_id: int

class WalletUpdate(WalletBase):
    pass

class WalletInDBBase(WalletBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Wallet(WalletInDBBase):
    pass

class WalletInDB(WalletInDBBase):
    pass 