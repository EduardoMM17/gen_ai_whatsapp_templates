from fastapi import APIRouter
from app.api.api_v1.endpoints import companies, auth


api_router = APIRouter()
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
