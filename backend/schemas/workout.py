from enum import Enum
from typing import List, Optional, Any
from pydantic import BaseModel, Field, model_validator
from api.services.tss_calc import calculate_complex_tss
import uuid

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
    id: uuid.UUID # Changed from str to uuid.UUID to match our models
    calculated_tss: float

    @model_validator(mode='before')
    @classmethod
    def compute_tss(cls, data: Any) -> Any:
        """
        If the data coming from the DB/API doesn't have a TSS, 
        or if we want to verify it, we calculate it here.
        """
        # When coming from SQLAlchemy 'from_attributes', 'data' might be an object
        structure = getattr(data, "structure", None) or data.get("structure")
        modality = getattr(data, "modality", None) or data.get("modality")

        if structure and modality:
            # We use our shared service logic
            computed = calculate_complex_tss(structure, modality)
            
            # If the data is a dict (from API input)
            if isinstance(data, dict):
                data["calculated_tss"] = computed
            # If it's an object (from DB) we just ensure the field matches
            else:
                setattr(data, "calculated_tss", computed)
                
        return data

    class Config:
        from_attributes = True
