from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.transaction import Transaction, TransactionCreate
from app.services.transaction import TransactionService
from app.models.transaction import TransactionType

router = APIRouter()

@router.post("/deposit", response_model=Transaction)
def deposit(
    *,
    db: Session = Depends(get_db),
    amount: float,
    currency: str,
    current_user: Any = Depends(get_current_user)
) -> Any:
    """
    Deposit funds into the user's wallet.
    """
    transaction_service = TransactionService(db)
    transaction, is_suspicious = transaction_service.process_transaction(
        user_id=current_user.id,
        amount=amount,
        currency=currency,
        transaction_type=TransactionType.DEPOSIT
    )
    return transaction

@router.post("/withdraw", response_model=Transaction)
def withdraw(
    *,
    db: Session = Depends(get_db),
    amount: float,
    currency: str,
    current_user: Any = Depends(get_current_user)
) -> Any:
    """
    Withdraw funds from the user's wallet.
    """
    transaction_service = TransactionService(db)
    transaction, is_suspicious = transaction_service.process_transaction(
        user_id=current_user.id,
        amount=amount,
        currency=currency,
        transaction_type=TransactionType.WITHDRAWAL
    )
    return transaction

@router.post("/transfer", response_model=Transaction)
def transfer(
    *,
    db: Session = Depends(get_db),
    amount: float,
    currency: str,
    recipient_id: int,
    current_user: Any = Depends(get_current_user)
) -> Any:
    """
    Transfer funds to another user.
    """
    transaction_service = TransactionService(db)
    transaction, is_suspicious = transaction_service.process_transaction(
        user_id=current_user.id,
        amount=amount,
        currency=currency,
        transaction_type=TransactionType.TRANSFER,
        recipient_id=recipient_id
    )
    return transaction

@router.get("/history", response_model=List[Transaction])
def get_transaction_history(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(get_current_user)
) -> Any:
    """
    Get transaction history for the current user.
    """
    transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id
    ).order_by(
        Transaction.created_at.desc()
    ).offset(skip).limit(limit).all()
    return transactions 