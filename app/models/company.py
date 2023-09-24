from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

from ..db.session import Base

if TYPE_CHECKING:
    from .user import User
    from .batch import Batch


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())

    users = relationship("User", back_populates="company")
    batches = relationship("Batch", back_populates="submitter")
