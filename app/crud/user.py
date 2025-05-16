from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import user as models
from app.models import transaction as txn_model
from app.schemas import user as schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username,
        models.User.is_deleted == False
    ).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user_balances(db: Session, user_id: int):
    balances = {}

    currencies = db.query(txn_model.Transaction.currency).distinct().all()
    for (currency,) in currencies:
        credit = db.query(func.coalesce(func.sum(txn_model.Transaction.amount), 0)).filter(
            txn_model.Transaction.receiver_id == user_id,
            txn_model.Transaction.currency == currency,
            txn_model.Transaction.type.in_(["deposit", "transfer"]),
            txn_model.Transaction.is_deleted == False
        ).scalar()

        debit = db.query(func.coalesce(func.sum(txn_model.Transaction.amount), 0)).filter(
            txn_model.Transaction.sender_id == user_id,
            txn_model.Transaction.currency == currency,
            txn_model.Transaction.type.in_(["withdraw", "transfer"]),
            txn_model.Transaction.is_deleted == False
        ).scalar()

        balances[currency] = round(credit - debit, 2)

    return balances
