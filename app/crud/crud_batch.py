from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.batch import Batch
from app.schemas.batch import BatchCreate


class CRUDBatch(CRUDBase[Batch, BatchCreate]):
    def get_by_company(self, db: Session, *, company_id: str) -> list[Batch]:
        return db.query(Batch).filter(Batch.company_id == company_id).all()

    def create(self, db: Session, *, company_id: int, submitter_id: int) -> Batch:
        batch_creation_obj = {
            "submitter_id": submitter_id,
            "company_id": company_id,
        }
        db_obj = Batch(**batch_creation_obj)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


batch = CRUDBatch(Batch)