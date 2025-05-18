 
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.config import SECRET_KEY, ALGORITHM
from app.database import SessionLocal
from app.models import user as models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        db = SessionLocal()
        db_user = db.query(models.User).filter(models.User.username == username).first()
        db.close()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
