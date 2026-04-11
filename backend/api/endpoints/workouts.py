from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from agents.nodes.workout_builder import workout_builder_app, WorkoutBuilderState
from deps import get_current_user_optional

router = APIRouter()


class WorkoutStepInput(BaseModel):
    name: str
    duration_mins: int = Field(gt=0)
    intensity_factor: float = Field(ge=0.3, le=1.2)


class WorkoutBlockInput(BaseModel):
    name: str
    repeat_count: int = Field(default=1, ge=1)
    steps: List[WorkoutStepInput]


class BuildWorkoutRequest(BaseModel):
    user_inputs: Dict[str, Any] = Field(default_factory=dict)
    natural_language_prompt: Optional[str] = None


class BuildWorkoutResponse(BaseModel):
    workout: Optional[Dict[str, Any]]
    generation_mode: Literal["manual", "rag_match", "synthetic"]
    match_confidence: Optional[float]
    errors: List[str]


@router.post("/build", response_model=BuildWorkoutResponse)
async def build_workout(
    request: BuildWorkoutRequest, current_user=Depends(get_current_user_optional)
):
    """
    Build a workout from user inputs and/or natural language.

    Supports three modes:
    - manual: User provides complete workout structure
    - rag_match: Finds best matching workout from DB using semantic search
    - synthetic: Generates new workout using LLM
    """
    try:
        # Prepare initial state
        initial_state: WorkoutBuilderState = {
            "user_inputs": request.user_inputs,
            "natural_language_prompt": request.natural_language_prompt,
            "matched_workout": None,
            "match_confidence": None,
            "final_workout": None,
            "generation_mode": "manual",
            "errors": [],
        }

        # Run the workout builder graph
        final_state = await workout_builder_app.ainvoke(initial_state)

        # Extract results
        final_workout = final_state.get("final_workout")

        return BuildWorkoutResponse(
            workout=final_workout.model_dump() if final_workout else None,
            generation_mode=final_state.get("generation_mode", "manual"),
            match_confidence=final_state.get("match_confidence"),
            errors=final_state.get("errors", []),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Workout building failed: {str(e)}"
        )
