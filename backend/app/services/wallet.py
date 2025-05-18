from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.models import Wallet
from app.schemas.wallet import WalletCreate, WalletUpdate

class WalletService:
    @staticmethod
    def get(db: Session, id: int) -> Optional[Wallet]:
        return db.query(Wallet).filter(Wallet.id == id).first()

    @staticmethod
    def get_by_user_id(db: Session, user_id: int) -> Optional[Wallet]:
        return db.query(Wallet).filter(Wallet.user_id == user_id).first()

    @staticmethod
    def get_multi(db: Session, *, skip: int = 0, limit: int = 100) -> List[Wallet]:
        return db.query(Wallet).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, *, obj_in: WalletCreate) -> Wallet:
        db_obj = Wallet(
            user_id=obj_in.user_id,
            balance=obj_in.balance,
            currency=obj_in.currency,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update(db: Session, *, db_obj: Wallet, obj_in: WalletUpdate) -> Wallet:
        update_data = obj_in.dict(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete(db: Session, *, id: int) -> Wallet:
        obj = db.query(Wallet).get(id)
        db.delete(obj)
        db.commit()
        return obj

    @staticmethod
    def update_balance(db: Session, *, wallet_id: int, amount: float) -> Wallet:
        wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
        if not wallet:
            return None
        wallet.balance += amount
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
        return wallet 