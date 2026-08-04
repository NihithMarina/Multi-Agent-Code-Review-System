from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import Token, UserCreate


class AuthService:
    def __init__(self, db: Session, settings: Settings) -> None:
        self.db = db
        self.settings = settings

    def register_user(self, user_in: UserCreate) -> User:
        existing = self.db.query(User).filter(User.email == user_in.email).one_or_none()
        if existing is not None:
            raise ValueError("User already exists")
        user = User(
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=hash_password(user_in.password),
            organization_id=user_in.organization_id,
            role="admin" if user_in.organization_id is None else "member",
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate(self, email: str, password: str) -> Token | None:
        user = self.db.query(User).filter(User.email == email).one_or_none()
        if user is None or user.hashed_password is None or not verify_password(password, user.hashed_password):
            return None
        token = create_access_token(user.email, self.settings, claims={"role": user.role})
        return Token(access_token=token)
