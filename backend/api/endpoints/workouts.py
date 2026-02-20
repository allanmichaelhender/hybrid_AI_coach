from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from deps import get_db 
from models.workout import Workout
from schemas.workout import HybridWorkoutRead

router = APIRouter()

@router.get("/", response_model=List[HybridWorkoutRead])
async def list_workouts(
    db: AsyncSession = Depends(get_db), 
    limit: int = 20
):
    """
    Returns the library of 60-minute workouts.
    Use this to verify your 10 seeded workouts are live!
    """
    result = await db.execute(select(Workout).limit(limit))
    return result.scalars().all()

