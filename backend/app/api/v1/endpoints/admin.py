from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_admin
from app.schemas.transaction import Transaction, TransactionUpdate
from app.schemas.user import User
from app.services.transaction import TransactionService
from app.services.user import UserService

router = APIRouter()

@router.get("/users", response_model=List[User])
def get_all_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(get_current_active_admin),
) -> Any:
    """
    Get all users (admin only).
    """
    users = UserService.get_multi(db, skip=skip, limit=limit)
    return users

@router.get("/transactions", response_model=List[Transaction])
def get_all_transactions(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(get_current_active_admin),
) -> Any:
    """
    Get all transactions (admin only).
    """
    transactions = TransactionService.get_multi(db, skip=skip, limit=limit)
    return transactions

@router.put("/transactions/{transaction_id}", response_model=Transaction)
def update_transaction(
    *,
    db: Session = Depends(get_db),
    transaction_id: int,
    transaction_in: TransactionUpdate,
    current_user: Any = Depends(get_current_active_admin),
) -> Any:
    """
    Update transaction (admin only).
    """
    transaction = TransactionService.get(db, id=transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    transaction = TransactionService.update(db, db_obj=transaction, obj_in=transaction_in)
    return transaction

@router.get("/flagged-transactions", response_model=List[Transaction])
def get_flagged_transactions(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(get_current_active_admin),
) -> Any:
    """
    Get all flagged transactions (admin only).
    """
    transactions = db.query(Transaction).filter(
        Transaction.is_flagged == True
    ).offset(skip).limit(limit).all()
    return transactions 