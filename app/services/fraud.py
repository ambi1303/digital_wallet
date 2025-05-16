from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import transaction as txn_model
from app.models import user as user_model
from app.database import SessionLocal
from app.utils.email import send_mock_email_alert

def flag_suspicious_transactions(db: Session, sender_id: int, new_txn: txn_model.Transaction):
    flagged = False
    reasons = []

    # 1. Large withdrawal
    if new_txn.type == "withdraw" and new_txn.amount > 1000:
        flagged = True
        reasons.append("Large withdrawal")

    # 2. Rapid multiple transfers
    if new_txn.type == "transfer":
        one_min_ago = datetime.utcnow() - timedelta(minutes=1)
        recent_transfers = db.query(txn_model.Transaction).filter(
            txn_model.Transaction.sender_id == sender_id,
            txn_model.Transaction.type == "transfer",
            txn_model.Transaction.timestamp >= one_min_ago
        ).count()
        if recent_transfers > 3:
            flagged = True
            reasons.append("Multiple rapid transfers")

    # Flag the transaction and send alert
    if flagged:
        new_txn.is_flagged = True
        new_txn.flag_reason = ", ".join(reasons)
        db.add(new_txn)
        db.commit()

        receiver = db.query(user_model.User).filter(user_model.User.id == sender_id).first()
        if receiver:
            send_mock_email_alert(
                to=receiver.email,
                subject="🚨 Suspicious Transaction Detected",
                content=f"Transaction ID {new_txn.id} flagged: {new_txn.flag_reason}"
            )

def daily_fraud_scan():
    db = SessionLocal()
    try:
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_txns = db.query(txn_model.Transaction).filter(
            txn_model.Transaction.timestamp >= yesterday,
            txn_model.Transaction.is_flagged == False,
            txn_model.Transaction.type.in_(["withdraw", "transfer"])
        ).all()

        for txn in recent_txns:
            flagged = False
            reasons = []

            # Large withdrawal threshold
            if txn.type == "withdraw" and txn.amount > 1000:
                flagged = True
                reasons.append("Large withdrawal")

            # Rapid transfers check
            if txn.type == "transfer":
                one_min_ago = txn.timestamp - timedelta(minutes=1)
                count = db.query(txn_model.Transaction).filter(
                    txn_model.Transaction.sender_id == txn.sender_id,
                    txn_model.Transaction.type == "transfer",
                    txn_model.Transaction.timestamp >= one_min_ago,
                    txn_model.Transaction.id != txn.id
                ).count()
                if count > 3:
                    flagged = True
                    reasons.append("Multiple rapid transfers")

            if flagged:
                txn.is_flagged = True
                txn.flag_reason = ", ".join(reasons)
                db.add(txn)

        db.commit()
    finally:
        db.close()
