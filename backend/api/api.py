from fastapi import APIRouter
from api.endpoints.calendar import router as calendar_router

api_router = APIRouter()

# Routing to our calendar endpoints, we use the tag to group endpoints for out fastapi docs
api_router.include_router(calendar_router, prefix="/calendar", tags=["Planner"])

