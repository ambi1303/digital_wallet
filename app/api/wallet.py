from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.transaction import TransactionCreate, TransactionOut
from app.crud import transaction as crud_txn
from app.crud import user as crud_user
from app.database import SessionLocal
from app.middlewares.auth_middleware import get_current_user
from app.models import transaction as txn_model

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=TransactionOut)
def perform_transaction(
    txn: TransactionCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return crud_txn.create_transaction(db, user, txn)


@router.get("/history", response_model=List[TransactionOut])
def get_transaction_history(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    transactions = db.query(txn_model.Transaction).filter(
        (
            (txn_model.Transaction.sender_id == user.id) |
            (txn_model.Transaction.receiver_id == user.id)
        ) &
        (txn_model.Transaction.is_deleted == False)
    ).order_by(txn_model.Transaction.timestamp.desc()).all()

    return transactions


@router.get("/balance")
def get_balance(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    balances = crud_user.get_user_balances(db, user.id)
    return {"balances": balances}
