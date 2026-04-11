from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from core.config import settings
from api.services.embeddings import search_workouts_filtered
from api.services.tss_calc import calculate_complex_tss, MODALITY_MULTIPLIERS
from .state import WorkoutBuilderState, WorkoutData, WorkoutBlock, WorkoutStep
from .prompts import WORKOUT_BUILDER_SYNTHEtic_PROMPT
import json

llm = ChatGroq(
    temperature=0.2, model_name="llama-3.3-70b-versatile", api_key=settings.GROQ_API_KEY
)


async def intake_node(state: WorkoutBuilderState) -> dict:
    """Parse user inputs and determine generation mode."""
    user_inputs = state.get("user_inputs", {})
    prompt = state.get("natural_language_prompt", "")

    # Check if we have complete manual structure
    has_complete_structure = (
        user_inputs.get("title")
        and user_inputs.get("modality")
        and user_inputs.get("focus")
        and user_inputs.get("structure")
    )

    if has_complete_structure:
        return {"generation_mode": "manual"}

    # If we have a natural language prompt, we need RAG or synthetic
    if prompt:
        # Extract modality and focus from inputs or infer from prompt
        modality = user_inputs.get("modality")
        focus = user_inputs.get("focus")

        return {
            "generation_mode": "rag_match" if not has_complete_structure else "manual",
            "user_inputs": {
                **user_inputs,
                "modality": modality,
                "focus": focus,
            },
        }

    # Default to manual if no prompt and incomplete
    return {"generation_mode": "manual"}


async def matcher_node(state: WorkoutBuilderState) -> dict:
    """Run RAG search if natural language prompt is present."""
    prompt = state.get("natural_language_prompt", "")
    user_inputs = state.get("user_inputs", {})

    if not prompt:
        return {"matched_workout": None, "match_confidence": None}

    modality = user_inputs.get("modality")
    focus = user_inputs.get("focus")

    # Perform RAG search
    workout = await search_workouts_filtered(
        query=prompt, modality=modality, focus=focus
    )

    if workout:
        return {
            "matched_workout": {
                "id": str(workout.id),
                "title": workout.title,
                "modality": workout.modality,
                "focus": workout.focus,
                "description": workout.description,
                "structure": workout.structure,
                "tss": workout.calculated_tss,
            },
            "match_confidence": 0.85,  # Could calculate actual similarity
            "generation_mode": "rag_match",
        }

    # No match found - will fall back to synthetic
    return {
        "matched_workout": None,
        "match_confidence": None,
        "generation_mode": "synthetic",
    }


async def builder_node(state: WorkoutBuilderState) -> dict:
    """Build the final workout based on generation mode."""
    mode = state.get("generation_mode", "manual")
    user_inputs = state.get("user_inputs", {})
    matched_workout = state.get("matched_workout")
    prompt = state.get("natural_language_prompt", "")

    if mode == "manual":
        # Use user-provided structure directly
        structure = user_inputs.get("structure", [])
        modality = user_inputs.get("modality", "Conditioning")

        workout_data = WorkoutData(
            title=user_inputs.get("title", "Custom Workout"),
            description=user_inputs.get("description", ""),
            modality=modality,
            focus=user_inputs.get("focus", "Aerobic Low"),
            structure=[WorkoutBlock(**block) for block in structure]
            if structure
            else [],
            tss=0.0,  # Will be calculated in validator
        )
        return {"final_workout": workout_data}

    elif mode == "rag_match" and matched_workout:
        # Use the matched workout from DB
        structure = matched_workout.get("structure", [])
        workout_data = WorkoutData(
            title=matched_workout.get("title", ""),
            description=matched_workout.get("description", ""),
            modality=matched_workout.get("modality", ""),
            focus=matched_workout.get("focus", ""),
            structure=[WorkoutBlock(**block) for block in structure]
            if structure
            else [],
            tss=matched_workout.get("tss", 0.0),
        )
        return {"final_workout": workout_data}

    else:
        # Generate synthetic workout using LLM
        modality = user_inputs.get("modality", "Running")
        focus = user_inputs.get("focus", "Aerobic Low")

        structured_llm = llm

        prompt_template = ChatPromptTemplate.from_template(
            WORKOUT_BUILDER_SYNTHEtic_PROMPT
        )
        chain = prompt_template | structured_llm

        response = await chain.ainvoke(
            {"user_prompt": prompt, "modality": modality, "focus": focus}
        )

        try:
            # Parse the JSON response
            content = response.content.replace("```json", "").replace("```", "").strip()
            data = json.loads(content)

            structure = data.get("structure", [])
            validated_modality = (
                modality if modality in MODALITY_MULTIPLIERS else "Conditioning"
            )

            # Calculate TSS
            tss = calculate_complex_tss(structure, validated_modality)

            workout_data = WorkoutData(
                title=data.get("title", f"Custom {modality} Session"),
                description=data.get("description", ""),
                modality=validated_modality,
                focus=focus,
                structure=[WorkoutBlock(**block) for block in structure],
                tss=tss,
            )
            return {"final_workout": workout_data}

        except Exception as e:
            print(f"Synthetic generation error: {e}")
            # Fallback to basic workout
            workout_data = WorkoutData(
                title=f"Custom {modality} Session",
                description="AI-generated session",
                modality=modality,
                focus=focus,
                structure=[
                    WorkoutBlock(
                        name="Main",
                        repeat_count=1,
                        steps=[
                            WorkoutStep(
                                name="Steady State",
                                duration_mins=45,
                                intensity_factor=0.6,
                            )
                        ],
                    )
                ],
                tss=45.0,
            )
            return {"final_workout": workout_data}


async def validator_node(state: WorkoutBuilderState) -> dict:
    """Validate the workout and calculate TSS if needed."""
    workout = state.get("final_workout")
    errors = []

    if not workout:
        return {"errors": ["No workout generated"]}

    # Calculate total duration
    total_mins = 0
    for block in workout.structure:
        for step in block.steps:
            total_mins += step.duration_mins * block.repeat_count

    # Validate duration
    if workout.modality == "Rest":
        if total_mins > 30:
            errors.append(f"Rest day exceeds 30 minutes ({total_mins} mins)")
    else:
        if total_mins > 60:
            errors.append(f"Workout exceeds 60 minutes ({total_mins} mins)")

    # Calculate TSS if not set or zero
    if workout.tss == 0.0 and workout.structure:
        workout.tss = calculate_complex_tss(
            [block.model_dump() for block in workout.structure], workout.modality
        )

    return {"errors": errors}
