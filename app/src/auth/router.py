import jwt

from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.schemas import Token, UserInDB
from src.auth.service import authenticate_user, create_access_token
from settings import settings
from logger import get_logger

router = APIRouter(prefix="/auth")

log = get_logger("API_AUTH")

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user: UserInDB | None = authenticate_user(form_data.username, form_data.password)
    if not user:
        log.warning(f"Access denied for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token: str = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.auth.expire_minutes)
    )
    log.info(f"Access token for user: {user.username} successfully created")
    return {"access_token": access_token, "token_type": "bearer"}