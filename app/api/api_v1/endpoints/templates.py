from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any

from app import crud, models, schemas
from app.api import dependencies
from app.core.config import settings
from app.utils.file_handler import process_zip_file

router = APIRouter()


@router.post("/upload-batch")
async def upload_batch(file: UploadFile):
    if file.filename.endswith(".zip"):
        zip_bytes = await file.read()
        process_zip_file(zip_bytes)
    return {
        "msg": "Batch uploaded successfully. A CSV file will be send to your email in max 1 hour"
    }
