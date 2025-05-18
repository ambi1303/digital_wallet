from typing import Optional
from sqlalchemy.orm import Session
from app.core.models import User
from app.core.security import verify_password, get_password_hash
from app.schemas.user import UserCreate

class AuthService:
    @staticmethod
    def authenticate(db: Session, *, email: str, password: str) -> Optional[User]:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def get_password_hash(password: str) -> str:
        return get_password_hash(password)

    @staticmethod
    def create_user(db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            is_active=obj_in.is_active,
            is_admin=obj_in.is_admin,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj 