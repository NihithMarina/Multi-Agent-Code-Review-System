from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str | None = None
    role: str | None = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12)
    full_name: str | None = None
    organization_id: int | None = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
    role: str
    organization_id: int | None = None
    is_active: bool

    model_config = {"from_attributes": True}
