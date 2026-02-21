from pydantic import BaseModel, Field
from typing import List, Optional, Any, Union
from uuid import UUID

class WorkoutStep(BaseModel):
    name: str
    duration_mins: int
    intensity_factor: float

class CalendarDay(BaseModel):
    day_index: int
    workout_id: Optional[Union[UUID, str]] = None 
    title: Optional[str] = None
    modality: Optional[str] = None
    focus: Optional[str] = None
    description: Optional[str] = None
    structure: Optional[List[Any]] = None
    tss: float = 0.0
    is_user_locked: bool = False

class CalendarRequest(BaseModel):
    # This tells Pydantic: "I expect a list of the Day objects we defined above"
    calendar: List[CalendarDay] 
    cycle_length: int = Field(default=7, ge=7, le=14)
    user_goal: str
    request_scope: str = "bulk"

class CalendarUpdateResponse(BaseModel):
    updated_calendar: List[CalendarDay]
    coach_reasoning: List[str]

class SavePlanRequest(BaseModel):
    plan_name: Optional[str] = "My Hybrid Block"
    user_goal: str
    calendar_data: List[CalendarDay] # 👈 This validates the 14-day block
    coach_reasoning: Optional[str] = None