from typing import Optional, TypedDict, Literal
from pydantic import BaseModel


class WorkoutStep(BaseModel):
    name: str
    duration_mins: int
    intensity_factor: float


class WorkoutBlock(BaseModel):
    name: str
    repeat_count: int
    steps: list[WorkoutStep]


class WorkoutData(BaseModel):
    title: str
    description: str
    modality: str
    focus: str
    structure: list[WorkoutBlock]
    tss: float


class WorkoutBuilderState(TypedDict):
    # User inputs from the form
    user_inputs: dict  # Partial workout data: title, modality, focus, etc.
    natural_language_prompt: Optional[str]  # "I want a 45min tempo run"

    # RAG matching results
    matched_workout: Optional[dict]  # Best DB match if found
    match_confidence: Optional[float]  # Similarity score

    # Final output
    final_workout: Optional[WorkoutData]
    generation_mode: Literal["manual", "rag_match", "synthetic"]

    # Validation
    errors: list[str]
