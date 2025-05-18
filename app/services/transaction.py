from typing import Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException, status
from app.models.transaction import Transaction, TransactionStatus, TransactionType
from app.models.wallet import Wallet
from app.services.fraud_detection import FraudDetectionService
from app.utils.email import send_email_alert
from decimal import Decimal, ROUND_DOWN
import logging

logger = logging.getLogger(__name__)

class TransactionService:
    def __init__(self, db: Session):
        self.db = db
        self.fraud_service = FraudDetectionService(db)

    def process_transaction(
        self,
        user_id: int,
        amount: Decimal,
        currency: str,
        transaction_type: TransactionType,
        description: Optional[str] = None,
        recipient_id: Optional[int] = None
    ) -> Tuple[Transaction, bool]:
        """
        Process a transaction with proper error handling and transaction isolation.
        Returns (transaction, is_suspicious)
        """
        try:
            # Start transaction
            self.db.begin_nested()

            # Get user's wallet
            wallet = self._get_wallet(user_id)
            if not wallet:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Wallet not found"
                )

            # Validate transaction
            self._validate_transaction(
                wallet, amount, transaction_type, recipient_id
            )

            # Check for fraud
            is_suspicious, reason = self.fraud_service.check_transaction(
                user_id, float(amount), transaction_type
            )

            # Create transaction record
            transaction = self._create_transaction(
                user_id, wallet.id, amount, currency,
                transaction_type, description, recipient_id,
                is_suspicious, reason
            )

            # Process the transaction
            self._update_balances(
                wallet, amount, transaction_type, recipient_id
            )

            # Commit the transaction
            self.db.commit()

            # Send notifications if needed
            self._send_notifications(transaction, is_suspicious)

            return transaction, is_suspicious

        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Database integrity error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid transaction data"
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred"
            )
        except Exception as e:
            self.db.rollback()
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred"
            )

    def _get_wallet(self, user_id: int) -> Optional[Wallet]:
        """Get user's wallet with proper locking"""
        return self.db.query(Wallet).filter(
            Wallet.user_id == user_id,
            Wallet.is_active == True
        ).with_for_update().first()

    def _validate_transaction(
        self,
        wallet: Wallet,
        amount: Decimal,
        transaction_type: TransactionType,
        recipient_id: Optional[int]
    ) -> None:
        """Validate transaction parameters"""
        if amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Amount must be positive"
            )

        if transaction_type == TransactionType.TRANSFER:
            if not recipient_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Recipient ID required for transfers"
                )
            if recipient_id == wallet.user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot transfer to self"
                )

        if transaction_type in [TransactionType.WITHDRAWAL, TransactionType.TRANSFER]:
            if wallet.balance < amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient funds"
                )

    def _create_transaction(
        self,
        user_id: int,
        wallet_id: int,
        amount: Decimal,
        currency: str,
        transaction_type: TransactionType,
        description: Optional[str],
        recipient_id: Optional[int],
        is_suspicious: bool,
        reason: Optional[str]
    ) -> Transaction:
        """Create transaction record"""
        transaction = Transaction(
            user_id=user_id,
            wallet_id=wallet_id,
            transaction_type=transaction_type,
            amount=float(amount),
            currency=currency,
            description=description,
            recipient_id=recipient_id,
            is_flagged=is_suspicious,
            flag_reason=reason,
            status=TransactionStatus.COMPLETED
        )
        self.db.add(transaction)
        return transaction

    def _update_balances(
        self,
        wallet: Wallet,
        amount: Decimal,
        transaction_type: TransactionType,
        recipient_id: Optional[int]
    ) -> None:
        """Update wallet balances"""
        if transaction_type == TransactionType.DEPOSIT:
            wallet.balance += amount
        elif transaction_type == TransactionType.WITHDRAWAL:
            wallet.balance -= amount
        elif transaction_type == TransactionType.TRANSFER:
            recipient_wallet = self._get_wallet(recipient_id)
            if not recipient_wallet:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Recipient wallet not found"
                )
            wallet.balance -= amount
            recipient_wallet.balance += amount

    def _send_notifications(self, transaction: Transaction, is_suspicious: bool) -> None:
        """Send notifications for the transaction"""
        if is_suspicious:
            send_email_alert(
                to_email=transaction.user.email,
                subject="Suspicious Transaction Alert",
                body=f"A transaction of {transaction.amount} {transaction.currency} "
                     f"has been flagged as suspicious. Reason: {transaction.flag_reason}"
            ) 