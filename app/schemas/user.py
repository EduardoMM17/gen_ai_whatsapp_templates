from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: EmailStr | None = None
    company_id: str | None = None
    role: str | None = None


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
