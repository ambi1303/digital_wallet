from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.wallet import Wallet, WalletCreate, WalletUpdate
from app.services.wallet import WalletService

router = APIRouter()

@router.get("/", response_model=Wallet)
def get_wallet(
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
) -> Any:
    """
    Get current user's wallet.
    """
    wallet = WalletService.get_by_user_id(db, user_id=current_user.id)
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )
    return wallet

@router.post("/", response_model=Wallet)
def create_wallet(
    *,
    db: Session = Depends(get_db),
    wallet_in: WalletCreate,
    current_user: Any = Depends(get_current_user)
) -> Any:
    """
    Create new wallet.
    """
    if current_user.id != wallet_in.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    wallet = WalletService.get_by_user_id(db, user_id=wallet_in.user_id)
    if wallet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wallet already exists"
        )
    wallet = WalletService.create(db, obj_in=wallet_in)
    return wallet

@router.put("/{wallet_id}", response_model=Wallet)
def update_wallet(
    *,
    db: Session = Depends(get_db),
    wallet_id: int,
    wallet_in: WalletUpdate,
    current_user: Any = Depends(get_current_user)
) -> Any:
    """
    Update wallet.
    """
    wallet = WalletService.get(db, id=wallet_id)
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )
    if wallet.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    wallet = WalletService.update(db, db_obj=wallet, obj_in=wallet_in)
    return wallet 