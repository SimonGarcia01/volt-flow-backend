from fastapi import APIRouter

from app.auth.router import router as auth_router
from app.charging.router import router as charging_router

#This is the general API router for version 1 of the app
#It includes the routers for auth and charging
api_router = APIRouter(prefix="/api/v1", tags=["API v1"])
api_router.include_router(auth_router)
api_router.include_router(charging_router)