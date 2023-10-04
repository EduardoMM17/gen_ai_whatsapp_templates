from pydantic import BaseModel
from typing import Optional


class CompanyBase(BaseModel):
    name: str


class CompanyCreate(CompanyBase):
    pass


class CompanyInDB(CompanyBase):
    id: int | None = None

    class Config:
        from_attributes = True


class Company(CompanyInDB):
    pass
