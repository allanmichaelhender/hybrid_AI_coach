from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, computed_field, ConfigDict
from api.services.tss_calc import calculate_complex_tss
import uuid

# Using enum forces the fixed choices listed
class Modality(str, Enum):
    RUNNING = "Running"
    CYCLING = "Cycling"
    SWIMMING = "Swimming"
    CONDITIONING = "Conditioning"
    STRENGTH = "Strength"
    REST = "Rest"

class Focus(str, Enum):
    VO2_MAX = "VO2 Max"
    AEROBIC_HIGH = "Aerobic High"
    AEROBIC_LOW = "Aerobic Low"
    ANAEROBIC = "Anaerobic"
    HYPERTROPHY = "Hypertrophy"
    STRENGTH = "Strength"
    REST = "Rest"

# We use field to add restrictions to the data, remember ... means required
class WorkoutStep(BaseModel):
    name: str
    duration_mins: int = Field(..., ge=1, le=60)
    intensity_factor: float = Field(..., ge=0, le=1.5)
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
    pass

class HybridWorkoutRead(HybridWorkoutBase):
    id: uuid.UUID 

    # Adding our computed tss value as a field, we have the required attributes because of how the classes are inherited
    @computed_field
    @property
    def calculated_tss(self) -> float:
        return calculate_complex_tss(self.structure, self.modality)

    # Allows pydantic to look into object attributes to find the entries it requires, allows pydantic to understand objects
    model_config = ConfigDict(from_attributes=True)
