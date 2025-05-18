from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.transaction import Transaction, TransactionStatus
from app.config import (
    SUSPICIOUS_TRANSACTION_THRESHOLD,
    RAPID_TRANSACTION_WINDOW,
    MAX_RAPID_TRANSACTIONS,
    MAX_TRANSACTION_AMOUNT,
    DAILY_TRANSACTION_LIMIT
)

class FraudDetectionService:
    def __init__(self, db: Session):
        self.db = db

    def check_transaction(self, user_id: int, amount: float, transaction_type: str) -> tuple[bool, str]:
        """
        Check if a transaction is suspicious
        Returns: (is_suspicious: bool, reason: str)
        """
        # Check amount threshold
        if amount > MAX_TRANSACTION_AMOUNT:
            return True, f"Transaction amount {amount} exceeds maximum allowed {MAX_TRANSACTION_AMOUNT}"

        # Check for rapid transactions
        recent_transactions = self._get_recent_transactions(user_id)
        if len(recent_transactions) >= MAX_RAPID_TRANSACTIONS:
            return True, f"Too many transactions in short period: {len(recent_transactions)}"

        # Check daily limit
        daily_total = self._get_daily_total(user_id)
        if daily_total + amount > DAILY_TRANSACTION_LIMIT:
            return True, f"Daily transaction limit exceeded: {daily_total + amount}"

        # Check for suspicious amount
        if amount > SUSPICIOUS_TRANSACTION_THRESHOLD:
            return True, f"Large transaction amount: {amount}"

        return False, ""

    def _get_recent_transactions(self, user_id: int) -> list[Transaction]:
        """Get transactions within the rapid transaction window"""
        window_start = datetime.utcnow() - timedelta(seconds=RAPID_TRANSACTION_WINDOW)
        return self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.created_at >= window_start,
            Transaction.status == TransactionStatus.COMPLETED
        ).all()

    def _get_daily_total(self, user_id: int) -> float:
        """Calculate total transaction amount for today"""
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        transactions = self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.created_at >= today_start,
            Transaction.status == TransactionStatus.COMPLETED
        ).all()
        return sum(t.amount for t in transactions)

    def calculate_fraud_score(self, transaction: Transaction) -> float:
        """Calculate a fraud score for a transaction"""
        score = 0.0
        
        # Amount-based scoring
        if transaction.amount > SUSPICIOUS_TRANSACTION_THRESHOLD:
            score += 0.3
        
        # Time-based scoring
        recent_transactions = self._get_recent_transactions(transaction.user_id)
        if len(recent_transactions) > 3:
            score += 0.2
        
        # Pattern-based scoring
        if transaction.transaction_type == "TRANSFER":
            # Check if recipient has been involved in flagged transactions
            recipient_flagged = self.db.query(Transaction).filter(
                Transaction.recipient_id == transaction.recipient_id,
                Transaction.is_flagged == True
            ).count()
            if recipient_flagged > 0:
                score += 0.2
        
        return min(score, 1.0)  # Cap score at 1.0 