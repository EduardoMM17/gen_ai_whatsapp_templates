from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

from ..db.session import Base

if TYPE_CHECKING:
    from .user import User
    from .company import Company


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.now())
    processed = Column(Boolean, default=False)
    submitter_id = Column(Integer, ForeignKey("users.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))

    submitter = relationship("User", back_populates="batches")
    company = relationship("Company", back_populates="batches")
