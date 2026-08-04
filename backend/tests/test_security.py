from datetime import timedelta

from app.core.config import get_settings
from app.core.security import create_access_token, hash_password, verify_password


def test_password_hash_roundtrip() -> None:
    hashed = hash_password("super-secret-password")
    assert verify_password("super-secret-password", hashed)


def test_create_access_token_contains_subject() -> None:
    settings = get_settings()
    token = create_access_token("test@example.com", settings, expires_delta=timedelta(minutes=5))
    assert token
