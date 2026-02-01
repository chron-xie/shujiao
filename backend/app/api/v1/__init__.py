from fastapi import APIRouter
from app.api.v1.endpoints import parameters, templates, consultations, users

api_router = APIRouter()

api_router.include_router(parameters.router, prefix="/parameters", tags=["parameters"])
api_router.include_router(templates.router, prefix="/templates", tags=["templates"])
api_router.include_router(consultations.router, prefix="/consultations", tags=["consultations"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
