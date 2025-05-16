 
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime,Boolean,Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    amount = Column(Float)
    type = Column(String)  # "deposit", "withdraw", "transfer"
    timestamp = Column(DateTime, default=datetime.utcnow)
    currency = Column(String, default="USD")

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
    is_flagged = Column(Boolean, default=False)
    flag_reason = Column(Text, nullable=True)
    is_deleted = Column(Boolean, default=False)

