from fastapi import APIRouter
from app.api.api_v1.endpoints import batches, companies, auth


api_router = APIRouter()
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(batches.router, prefix="/batches", tags=["batches"])
