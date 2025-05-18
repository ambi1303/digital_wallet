from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.middlewares.auth_middleware import get_current_user
from app.models import transaction as txn_model, user as user_model
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/flagged-transactions")
def get_flagged_transactions(db: Session = Depends(get_db)):
    flagged = db.query(txn_model.Transaction).filter(txn_model.Transaction.is_flagged == True).all()
    return flagged

@router.get("/total-balances")
def get_total_balances(db: Session = Depends(get_db)):
    # Sum balances of all users (calculated dynamically)
    users = db.query(user_model.User).all()
    total = 0
    for u in users:
        credit = db.query(func.coalesce(func.sum(txn_model.Transaction.amount), 0)).filter(
            (txn_model.Transaction.receiver_id == u.id) &
            (txn_model.Transaction.type.in_(["deposit", "transfer"]))
        ).scalar()
        debit = db.query(func.coalesce(func.sum(txn_model.Transaction.amount), 0)).filter(
            (txn_model.Transaction.sender_id == u.id) &
            (txn_model.Transaction.type.in_(["withdraw", "transfer"]))
        ).scalar()
        total += (credit - debit)
    return {"total_balance": total}

@router.get("/top-users")
def get_top_users(db: Session = Depends(get_db)):
    # Return users sorted by transaction volume (sum of amounts sent or received)
    users = db.query(user_model.User).all()
    user_volumes = []
    for u in users:
        volume = db.query(func.coalesce(func.sum(txn_model.Transaction.amount), 0)).filter(
            (txn_model.Transaction.receiver_id == u.id) | (txn_model.Transaction.sender_id == u.id)
        ).scalar()
        user_volumes.append({"user": u.username, "transaction_volume": volume})
    user_volumes.sort(key=lambda x: x["transaction_volume"], reverse=True)
    return user_volumes[:10]

@router.delete("/me")
def soft_delete_user(db: Session = Depends(get_db), user=Depends(get_current_user)):
    user.is_deleted = True
    db.commit()
    return {"msg": "User account soft-deleted"}
