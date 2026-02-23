from agents.state import AgentState
from api.services.embeddings import search_workouts_filtered
from agents.utils.synthetic import generate_synthetic_workout


async def retriever_node(state: AgentState):
    planned_list = state.get("planned_workouts", [])
    if not planned_list:
        return {"calendar": state["calendar"]}

    print(planned_list)

    new_calendar = [day.copy() for day in state["calendar"]]

    for plan in planned_list:
        day_idx = plan["day_index"]
        modality = plan["modality"]
        focus = plan["focus"]
        vector_query = plan["vector_query"]

        if new_calendar[day_idx].get("is_user_locked"):
            continue

        # Search The Database
        workout = await search_workouts_filtered(
            query=vector_query, modality=modality, focus=focus
        )

        if workout:
            new_calendar[day_idx].update(
                {
                    "workout_id": str(workout.id),
                    "title": workout.title,
                    "modality": workout.modality,
                    "focus": workout.focus,
                    "tss": float(workout.calculated_tss),
                    "structure": workout.structure,
                    "description": workout.description,
                }
            )
            print(f"✅ Day {day_idx} matched DB: {workout.title}")
        else:
            # If not found, generate a custom workout
            print(f"DEBUG: 🪄 No DB match for Day {day_idx}. Generating Synthetic...")

            synthetic = await generate_synthetic_workout(modality, focus, vector_query)

            new_calendar[day_idx].update(
                {
                    "workout_id": "synthetic",
                    "title": synthetic["title"],
                    "description": synthetic["description"],
                    "structure": synthetic["structure"],
                    "modality": modality,
                    "focus": focus,
                    "tss": synthetic["tss"],
                }
            )
            print(f"DEBUG: 🪄 Day {day_idx} synthesized: {synthetic['title']}")

    return {"calendar": new_calendar}
