from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)
    
    # Relationships
    wallet = relationship("Wallet", back_populates="user", uselist=False)

    sent_transactions = relationship(
        "Transaction",
        back_populates="user",
        foreign_keys="Transaction.user_id"
    )

    received_transactions = relationship(
        "Transaction",
        back_populates="recipient",
        foreign_keys="Transaction.recipient_id"
    )

    def __repr__(self):
        return f"<User {self.username}>"

    
    def __repr__(self):
        return f"<User {self.username}>" 

