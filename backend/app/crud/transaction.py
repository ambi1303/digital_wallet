from sqlalchemy.orm import Session
from app.crud.user import get_user_balances
from app.models import transaction as models, user as user_model
from app.schemas import transaction as schemas
from fastapi import HTTPException
from app.services import fraud

def create_transaction(db: Session, sender: user_model.User, data: schemas.TransactionCreate):
    balances = get_user_balances(db, sender.id)
    currency = data.currency.upper()

    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    if data.type == "deposit":
        txn = models.Transaction(
            type="deposit",
            amount=data.amount,
            receiver_id=sender.id,
            currency=currency
        )

    elif data.type == "withdraw":
        if balances.get(currency, 0) < data.amount:
            raise HTTPException(status_code=400, detail=f"Insufficient {currency} balance")
        txn = models.Transaction(
            type="withdraw",
            amount=data.amount,
            sender_id=sender.id,
            currency=currency
        )

    elif data.type == "transfer":
        receiver = db.query(user_model.User).filter(
            user_model.User.username == data.receiver_username,
            user_model.User.is_deleted == False
        ).first()
        if not receiver:
            raise HTTPException(status_code=404, detail="Receiver not found")
        if receiver.id == sender.id:
            raise HTTPException(status_code=400, detail="Cannot transfer to self")
        if balances.get(currency, 0) < data.amount:
            raise HTTPException(status_code=400, detail=f"Insufficient {currency} balance for transfer")

        txn = models.Transaction(
            type="transfer",
            amount=data.amount,
            sender_id=sender.id,
            receiver_id=receiver.id,
            currency=currency
        )

    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    db.add(txn)
    db.commit()
    db.refresh(txn)

    # Run fraud detection
    fraud.flag_suspicious_transactions(db, sender.id, txn)

    return txn
