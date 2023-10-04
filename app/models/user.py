from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from app.enums import Role

from ..db.session import Base

if TYPE_CHECKING:
    from .company import Company
    from .batch import Batch


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime)
    company_id = Column(Integer, ForeignKey("companies.id"))
    role = Column(Enum(Role), nullable=False, default=Role.user)

    company = relationship("Company", back_populates="users")
    batches = relationship("Batch", back_populates="submitter")
