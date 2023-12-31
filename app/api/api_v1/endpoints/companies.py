from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any

from app import crud, models, schemas
from app.api import dependencies
from app.core.config import settings

router = APIRouter()


# to do
# modify so only super users can create companies
@router.post("/", response_model=schemas.Company)
def create_company(
    *, db: Session = Depends(dependencies.get_db), company_in: schemas.CompanyCreate
):
    """Create new company"""
    company = crud.company.get_by_name(db=db, name=company_in.name)
    if company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The company {company_in.name} already exists",
        )
    return crud.company.create(db=db, obj_in=company_in)
