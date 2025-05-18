from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.transaction import Transaction, TransactionStatus
from app.services.fraud_detection import FraudDetectionService
from app.utils.email import send_email_alert

def run_daily_fraud_scan(db: Session):
    """
    Run daily fraud scan on all transactions from the last 24 hours
    """
    # Get transactions from last 24 hours
    yesterday = datetime.utcnow() - timedelta(days=1)
    transactions = db.query(Transaction).filter(
        Transaction.created_at >= yesterday,
        Transaction.status == TransactionStatus.COMPLETED,
        Transaction.is_flagged == False
    ).all()

    fraud_service = FraudDetectionService(db)
    flagged_transactions = []

    for transaction in transactions:
        # Recalculate fraud score
        fraud_score = fraud_service.calculate_fraud_score(transaction)
        
        if fraud_score > 0.7:  # High risk threshold
            transaction.is_flagged = True
            transaction.fraud_score = fraud_score
            transaction.flag_reason = f"High fraud score detected: {fraud_score}"
            flagged_transactions.append(transaction)
            
            # Send email alert
            send_email_alert(
                to_email=transaction.user.email,
                subject="Suspicious Transaction Alert",
                body=f"A transaction of {transaction.amount} {transaction.currency} has been flagged as suspicious."
            )

    # Commit changes
    db.commit()

    return {
        "scanned_transactions": len(transactions),
        "flagged_transactions": len(flagged_transactions),
        "scan_time": datetime.utcnow()
    } 