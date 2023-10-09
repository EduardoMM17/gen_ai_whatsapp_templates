from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.company import Company
from app.schemas.company import CompanyCreate


class CRUDCompany(CRUDBase[Company, CompanyCreate]):
    def get_by_name(self, db: Session, *, name: str) -> Company | None:
        return db.query(Company).filter(Company.name == name).first()

    def create(self, db: Session, *, obj_in: CompanyCreate) -> Company:
        db_obj = Company(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


company = CRUDCompany(Company)
