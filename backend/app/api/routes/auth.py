from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.api.deps import db_session
from app.core.config import get_settings
from app.schemas.auth import Token, UserCreate, UserRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/register", response_model=UserRead)
def register_user(payload: UserCreate, db: Session = Depends(db_session)) -> UserRead:
    service = AuthService(db, get_settings())
    try:
        return UserRead.model_validate(service.register_user(payload))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.post("/login", response_model=Token)
def login_user(payload: LoginRequest, db: Session = Depends(db_session)) -> Token:
    service = AuthService(db, get_settings())
    token = service.authenticate(payload.email, payload.password)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return token
