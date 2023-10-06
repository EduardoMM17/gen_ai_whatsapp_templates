from pydantic import BaseModel, EmailStr
from app.enums import Role


# Shared properties
class UserBase(BaseModel):
    email: EmailStr | None = None
    company_id: str | None = None
    role: Role | None = None
    is_active: bool | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    company: str | None = None
    password: str
    role: str | None = Role.user
    is_active: bool = True


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: str | None = None
    company_id: str | None = None


class UserInDBBase(UserBase):
    id: int | None = None
    company_id: int | None = None

    class Cofig:
        from_attributes = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
