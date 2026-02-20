# backend/api/api.py
from fastapi import APIRouter
from api.endpoints import calendar, workouts  # Import your new endpoints

api_router = APIRouter()

# Register the AI Planner
api_router.include_router(calendar.router, prefix="/calendar", tags=["Planner"])
# Register the Library search/viewing
api_router.include_router(workouts.router, prefix="/workouts", tags=["Workouts"])
