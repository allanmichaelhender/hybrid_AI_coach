from typing import List, Optional, Annotated
from typing_extensions import TypedDict
import uuid
from pydantic import BaseModel, Field
from typing import List, Literal

#Defining some schemas for the model to better understand what it's output should include
class PlannedWorkout(BaseModel):
    day_index: int
    modality: Literal["Running", "Cycling", "Swiming", "Strength", "Conditioning", "Hypertrophy", "Rest"]
    focus: Literal["Aerobic Low", "Aerobic High", "VO2 Max", "Anaerobic", "Hypertrophy", "Strength", "Rest"]
    vector_query: str

class PlanAnalysis(BaseModel):
    planned_workouts: List[PlannedWorkout]
    ai_reasoning: str = Field("Step-by-step logic for the plan")



def replace_list(left: list, right: list) -> list:
    return right

# Laying out our CalendarDay Format and data types
class CalendarDay(TypedDict):
    day_index: int
    workout_id: Optional[uuid.UUID]
    title: Optional[str]
    modality: Optional[str]
    focus: Optional[str]
    tss: float
    is_user_locked: bool  

#Defining the state of our AI Agent
class AgentState(TypedDict):
    calendar: Annotated[List[CalendarDay], replace_list]
    
    # Configuration
    cycle_length: int
         
    # Context
    user_goal: str   
    ai_reasoning: List[str] 
    errors: List[str]  # Any safety violations (e.g., TSS too high)
    planned_workouts: List[PlannedWorkout] 

