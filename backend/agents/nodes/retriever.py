# backend/agents/nodes/retriever.py
import re
from agents.state import AgentState
from api.services.embeddings import search_workouts_filtered
from agents.utils.synthetic import generate_synthetic_workout


async def retriever_node(state: AgentState):
    # 1. Get the latest reasoning block
    if not state["ai_reasoning"]:
        return {"calendar": state["calendar"]}

    last_thought = state["ai_reasoning"][-1]

    # 2. UPDATED REGEX: Handles "0:", "[0]:", or "0."
    # Pattern: Digit -> optional punctuation -> space -> Modality | Focus | Query
    pattern = r"\[(\d+)\]:\s*([^|]+)\|\s*([^|]+)\|\s*(.*)"

    # Use re.MULTILINE to catch every line in the block
    matches = re.findall(pattern, last_thought, re.MULTILINE)

    # Create a deep copy of the calendar to ensure React sees the update
    new_calendar = [day.copy() for day in state["calendar"]]


    for match in matches:
        day_idx = int(match[0])
        modality, focus, query = match[1].strip(), match[2].strip(), match[3].strip()

        if day_idx < 0 or day_idx >= len(new_calendar):
            print(f"⚠️ AI suggested Day {day_idx}, but cycle only has {len(new_calendar)} days. Skipping.")
            continue

        # 1. ATTEMPT: Search the Database (RAG)
        workout = await search_workouts_filtered(
            query=query, modality=modality, focus=focus, limit=1
        )

        if workout:
            # ✅ FOUND IN DB
            new_calendar[day_idx].update(
                {
                    "workout_id": str(workout.id),
                    "title": workout.title,
                    "description": workout.description,
                    "structure": workout.structure,
                    "modality": workout.modality,
                    "tss": float(workout.calculated_tss),
                }
            )
            print(f"DEBUG: ✅ Day {day_idx} matched DB: {workout.title}")
        else:
            # ⚠️ NOT FOUND: Generate a Custom Workout (Synthetic)
            print(f"DEBUG: 🪄 No DB match for Day {day_idx}. Generating Synthetic...")

            synthetic = await generate_synthetic_workout(modality, focus, query)

            new_calendar[day_idx].update(
                {
                    "workout_id": "synthetic",  # Flags this for the Frontend
                    "title": synthetic["title"],
                    "description": synthetic["description"],
                    "structure": synthetic["structure"],
                    "modality": modality,
                    "tss": synthetic["tss"],
                }
            )
            print(f"DEBUG: 🪄 Day {day_idx} synthesized: {synthetic['title']}")

    return {"calendar": new_calendar}
