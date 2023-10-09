from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status, Form
from typing_extensions import Annotated
from sqlalchemy.orm import Session
from typing import Any

from app import crud, models, schemas
from app.api import dependencies
from app.core.config import settings
from app.services.file_services import process_zip_file


router = APIRouter()


@router.post("/upload")
async def upload_batch(
    *,
    file: UploadFile,
    company: Annotated[str, Form()] = None,
    current_user: models.User = Depends(dependencies.get_current_active_user),
    db=Depends(dependencies.get_db)
):
    if file.filename.endswith(".zip"):
        zip_bytes = await file.read()
        process_zip_file(zip_bytes)
        if company:
            company_obj = crud.company.get_by_name(db=db, name=company)
        else:
            company_obj = crud.company.get(db=db, id=current_user.company_id)

        crud.batch.create(
            db=db, company_id=company_obj.id, submitter_id=current_user.id
        )
        return {
            "msg": "Batch uploaded successfully. A CSV file will be send to your email in max 1 hour"
        }
    else:
        return {"msg": "File format not supported"}
