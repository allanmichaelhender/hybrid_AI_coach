from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator

class Modality(str, Enum):
    RUNNING = "Running"
    CYCLING = "Cycling"
    SWIMMING = "Swimming"
    CONDITIONING = "Conditioning"
    STRENGTH = "Strength"
    HYPERTROPHY = "Hypertrophy"

class Focus(str, Enum):
    VO2_MAX = "VO2 Max"
    AEROBIC_HIGH = "Aerobic High"
    AEROBIC_LOW = "Aerobic Low"
    ANAEROBIC = "Anaerobic"
    HYPERTROPHY = "Hypertrophy"
    STRENGTH = "Strength"

class WorkoutStep(BaseModel):
    name: str
    duration_mins: int = Field(..., ge=1, le=60)
    intensity_factor: float = Field(..., ge=0.1, le=1.5)
    description: Optional[str] = None

class WorkoutBlock(BaseModel):
    name: str
    repeat_count: int = Field(default=1, ge=1)
    steps: List[WorkoutStep]

class HybridWorkoutBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    modality: Modality
    focus: Focus
    rpe: int = Field(..., ge=1, le=10)
    description: str
    structure: List[WorkoutBlock]

class HybridWorkoutCreate(HybridWorkoutBase):
    """Used when creating a workout (e.g. in your setup script)"""
    pass

class HybridWorkoutRead(HybridWorkoutBase):
    """Includes calculated fields for the Frontend"""
    id: str
    calculated_tss: float

    @model_validator(mode='before')
    @classmethod
    def compute_tss(cls, data: any):
        # Logic to be implemented in your tss_calc.py service
        # This allows the API to return the TSS dynamically
        return data

    class Config:
        from_attributes = True
