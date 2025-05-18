from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, get_current_active_admin
from app.schemas.user import User, UserCreate, UserUpdate
from app.services.user import UserService

router = APIRouter()

@router.get("/me", response_model=User)
def read_user_me(
    current_user: Any = Depends(get_current_user)
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.put("/me", response_model=User)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: Any = Depends(get_current_user)
) -> Any:
    """
    Update current user.
    """
    user = UserService.update(db, db_obj=current_user, obj_in=user_in)
    return user

@router.get("/{user_id}", response_model=User)
def read_user_by_id(
    user_id: int,
    current_user: Any = Depends(get_current_active_admin),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = UserService.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get("/", response_model=List[User])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(get_current_active_admin),
) -> Any:
    """
    Retrieve users.
    """
    users = UserService.get_multi(db, skip=skip, limit=limit)
    return users

@router.delete("/{user_id}", response_model=User)
def delete_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    current_user: Any = Depends(get_current_active_admin),
) -> Any:
    """
    Delete a user.
    """
    user = UserService.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user = UserService.delete(db, id=user_id)
    return user 