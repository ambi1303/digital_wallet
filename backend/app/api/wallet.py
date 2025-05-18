from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.transaction import TransactionCreate, TransactionOut, TransactionFilter
from app.schemas.wallet import Wallet, WalletCreate
from app.services.wallet import WalletService
from app.services.fraud_detection import FraudDetectionService
from app.models.transaction import Transaction, TransactionStatus
from app.models.wallet import Wallet
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/transactions", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new transaction.
    
    - **amount**: Transaction amount (must be positive)
    - **currency**: Currency code (e.g., USD)
    - **transaction_type**: Type of transaction (DEPOSIT/WITHDRAWAL/TRANSFER)
    - **description**: Optional transaction description
    - **recipient_id**: Required for transfers
    
    Returns the created transaction with status and fraud detection results.
    """
    try:
        # Get user's wallet
        wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")

        # Validate transaction
        if transaction.transaction_type == "TRANSFER" and not transaction.recipient_id:
            raise HTTPException(status_code=400, detail="Recipient ID required for transfers")

        # Check fraud detection
        fraud_service = FraudDetectionService(db)
        is_suspicious, reason = fraud_service.check_transaction(
            current_user.id,
            transaction.amount,
            transaction.transaction_type
        )

        # Create transaction
        db_transaction = Transaction(
            user_id=current_user.id,
            wallet_id=wallet.id,
            transaction_type=transaction.transaction_type,
            amount=transaction.amount,
            currency=transaction.currency,
            description=transaction.description,
            recipient_id=transaction.recipient_id,
            is_flagged=is_suspicious,
            flag_reason=reason if is_suspicious else None
        )

        # Process transaction
        if transaction.transaction_type == "DEPOSIT":
            wallet.balance += transaction.amount
        elif transaction.transaction_type == "WITHDRAWAL":
            if wallet.balance < transaction.amount:
                raise HTTPException(status_code=400, detail="Insufficient funds")
            wallet.balance -= transaction.amount
        elif transaction.transaction_type == "TRANSFER":
            if wallet.balance < transaction.amount:
                raise HTTPException(status_code=400, detail="Insufficient funds")
            recipient_wallet = db.query(Wallet).filter(Wallet.user_id == transaction.recipient_id).first()
            if not recipient_wallet:
                raise HTTPException(status_code=404, detail="Recipient wallet not found")
            wallet.balance -= transaction.amount
            recipient_wallet.balance += transaction.amount

        db_transaction.status = TransactionStatus.COMPLETED
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)

        return db_transaction

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")

@router.get("/transactions", response_model=List[TransactionOut])
async def get_transactions(
    filters: TransactionFilter = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's transactions with optional filtering.
    
    - **start_date**: Filter transactions after this date
    - **end_date**: Filter transactions before this date
    - **transaction_type**: Filter by transaction type
    - **min_amount**: Filter transactions above this amount
    - **max_amount**: Filter transactions below this amount
    - **is_flagged**: Filter flagged transactions
    """
    query = db.query(Transaction).filter(Transaction.user_id == current_user.id)

    if filters.start_date:
        query = query.filter(Transaction.created_at >= filters.start_date)
    if filters.end_date:
        query = query.filter(Transaction.created_at <= filters.end_date)
    if filters.transaction_type:
        query = query.filter(Transaction.transaction_type == filters.transaction_type)
    if filters.min_amount:
        query = query.filter(Transaction.amount >= filters.min_amount)
    if filters.max_amount:
        query = query.filter(Transaction.amount <= filters.max_amount)
    if filters.is_flagged is not None:
        query = query.filter(Transaction.is_flagged == filters.is_flagged)

    return query.order_by(Transaction.created_at.desc()).all()

@router.get("/balance")
async def get_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's current wallet balance.
    """
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    return {
        "balance": wallet.balance,
        "currency": wallet.currency.value,
        "last_updated": wallet.updated_at
    }
