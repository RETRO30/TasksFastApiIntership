from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

from passlib.context import CryptContext
from src.auth.schemas import TokenData, User, UserInDB
from datetime import datetime, timedelta
from settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ONLY FOR EXAMPLE | TODO: ADD REAL DATABASE
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("1234"),
    },
    "executor1": {
        "username": "executor1",
        "hashed_password": pwd_context.hash("1234"),
    },
    "executor1": {
        "username": "executor1",
        "hashed_password": pwd_context.hash("1234"),
    },
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str) -> UserInDB | None:
    user = fake_users_db.get(username)
    if user:
        return UserInDB(**user)
    return None


def authenticate_user(username: str, password: str) -> UserInDB | None:
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.auth.expire_minutes)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.auth.secret_key, algorithm="HS256")
    return token



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.auth.secret_key, algorithms=["HS256"])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception

    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception

    return user