from fastapi import APIRouter

#Creates the router for auth
router = APIRouter(prefix="/auth", tags=["Authentication"])
