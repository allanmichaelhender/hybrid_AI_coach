# backend/agents/state.py
from typing import List, Optional, Annotated
from typing_extensions import TypedDict
import operator
import uuid

def replace_list(left: list, right: list) -> list:
    return right


class CalendarDay(TypedDict):
    """Represents a single slot in the 7 or 14 day cycle."""
    day_index: int
    workout_id: Optional[uuid.UUID]
    title: Optional[str]
    modality: Optional[str]
    focus: Optional[str]
    tss: float
    is_user_locked: bool  # If True, the AI must NOT change this day

class AgentState(TypedDict):
    """The shared memory of our LangGraph Agent."""
    # Annotated with operator.setitem tells LangGraph to replace 
    # the list when a node returns a new version
    calendar: Annotated[List[CalendarDay], replace_list]
    
    # Configuration
    cycle_length: int  # 7 or 14
    request_scope: str # "single" or "bulk"
    target_day: Optional[int] # The specific day index if scope is "single"
    
    # Context
    user_goal: str     # e.g., "I want to improve my 5k run time"
    ai_reasoning: List[str] # A log of 'thoughts' the AI had
    errors: List[str]  # Any safety violations (e.g., TSS too high)
