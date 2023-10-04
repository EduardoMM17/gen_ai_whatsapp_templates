from pydantic import BaseModel, EmailStr
from app.enums import Role

# Shared properties
class UserBase(BaseModel):
    email: EmailStr | None = None
    company_id: str | None = None
    role: Role | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    company: str | None
    password: str
    role: str | None


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
