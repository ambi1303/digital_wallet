from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class TransactionType(enum.Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER = "TRANSFER"

class TransactionStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    FLAGGED = "FLAGGED"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    wallet_id = Column(Integer, ForeignKey("wallets.id"))
    transaction_type = Column(Enum(TransactionType))
    amount = Column(Float)
    currency = Column(String)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    description = Column(String, nullable=True)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Fraud detection flags
    is_flagged = Column(Boolean, default=False)
    flag_reason = Column(String, nullable=True)
    fraud_score = Column(Float, default=0.0)
    
    # Relationships
    user = relationship("User", back_populates="transactions", foreign_keys=[user_id])
    wallet = relationship("Wallet", back_populates="transactions")
    recipient = relationship("User", foreign_keys=[recipient_id])

    def __repr__(self):
        return f"<Transaction {self.id} - {self.transaction_type.value}>"

