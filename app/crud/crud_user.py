from sqlalchemy.orm import Session


from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate
from app.crud.crud_company import company
from app.enums import Role


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

        if obj_in.role:
            user_creation_obj.update({"role": obj_in.role})

        db_obj = User(**user_creation_obj)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, *, email: str, password: str) -> User | None:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_admin(self, user: User) -> bool:
        return user.role == Role.admin


user = CRUDUser(User)
