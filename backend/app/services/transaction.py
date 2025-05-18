from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.models import Transaction, TransactionType, Wallet
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.services.wallet import WalletService

class TransactionService:
    @staticmethod
    def get(db: Session, id: int) -> Optional[Transaction]:
        return db.query(Transaction).filter(Transaction.id == id).first()

    @staticmethod
    def get_by_user_id(db: Session, user_id: int, *, skip: int = 0, limit: int = 100) -> List[Transaction]:
        return db.query(Transaction).filter(Transaction.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_multi(db: Session, *, skip: int = 0, limit: int = 100) -> List[Transaction]:
        return db.query(Transaction).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, *, obj_in: TransactionCreate) -> Transaction:
        db_obj = Transaction(
            user_id=obj_in.user_id,
            wallet_id=obj_in.wallet_id,
            amount=obj_in.amount,
            currency=obj_in.currency,
            transaction_type=obj_in.transaction_type,
            description=obj_in.description,
            recipient_id=obj_in.recipient_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update(db: Session, *, db_obj: Transaction, obj_in: TransactionUpdate) -> Transaction:
        update_data = obj_in.dict(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def process_transaction(db: Session, *, obj_in: TransactionCreate) -> Transaction:
        # Get source wallet
        source_wallet = WalletService.get(db, id=obj_in.wallet_id)
        if not source_wallet:
            raise ValueError("Source wallet not found")

        # Process based on transaction type
        if obj_in.transaction_type == TransactionType.DEPOSIT:
            WalletService.update_balance(db, wallet_id=source_wallet.id, amount=obj_in.amount)
        elif obj_in.transaction_type == TransactionType.WITHDRAWAL:
            if source_wallet.balance < obj_in.amount:
                raise ValueError("Insufficient funds")
            WalletService.update_balance(db, wallet_id=source_wallet.id, amount=-obj_in.amount)
        elif obj_in.transaction_type == TransactionType.TRANSFER:
            if not obj_in.recipient_id:
                raise ValueError("Recipient ID required for transfer")
            if source_wallet.balance < obj_in.amount:
                raise ValueError("Insufficient funds")
            
            # Get recipient wallet
            recipient_wallet = WalletService.get_by_user_id(db, user_id=obj_in.recipient_id)
            if not recipient_wallet:
                raise ValueError("Recipient wallet not found")

            # Update both wallets
            WalletService.update_balance(db, wallet_id=source_wallet.id, amount=-obj_in.amount)
            WalletService.update_balance(db, wallet_id=recipient_wallet.id, amount=obj_in.amount)

        # Create transaction record
        return TransactionService.create(db, obj_in=obj_in) 