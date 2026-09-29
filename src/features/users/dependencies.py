from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.core.security import decode_token
from src.db.session import get_db
from src.features.users.models import User



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/signin")



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_token(token)

    if payload is None or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    return user


