from sqlalchemy.orm import Session


from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate
from app.crud.crud_company import company


class CRUDUser(CRUDBase[User, UserCreate]):
    def get_by_email(self, db: Session, *, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        user_creation_obj = {
            "email": obj_in.email,
            "hashed_password": get_password_hash(obj_in.password),
        }
        if obj_in.company:
            db_c = company.get_by_name(db=db, name=obj_in.company)
            user_creation_obj.update({"company_id": db_c.id})
            print(db_c)
            # find company

        if obj_in.role:
            user_creation_obj.update({"role": obj_in.role})

        print("USER CREATION OBJ:", user_creation_obj)

        db_obj = User(**user_creation_obj)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


user = CRUDUser(User)
