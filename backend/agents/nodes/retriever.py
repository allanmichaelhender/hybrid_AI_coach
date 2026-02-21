# backend/agents/nodes/retriever.py
import re
from agents.state import AgentState
from api.services.embeddings import search_workouts_filtered

async def retriever_node(state: AgentState):
    """
    Step 4: The Retriever Node.
    Parses the AI's 'thoughts' and fetches real workouts from pgvector.
    """
    # 1. Get the latest 'reasoning' block from the AI
    if not state["ai_reasoning"]:
        return {"calendar": state["calendar"]}
        
    last_thought = state["ai_reasoning"][-1]
    
    # 2. Regex to find the pattern [DAY]: MODALITY | FOCUS | QUERY
    pattern = r"\[(\d+)\]:\s*([^|]+)\|\s*([^|]+)\|\s*(.*)"
    matches = re.findall(pattern, last_thought)
    
    new_calendar = [day.copy() for day in state["calendar"]]
    
    for match in matches:
        day_idx = int(match[0])
        modality = match[1].strip()
        focus = match[2].strip()
        query = match[3].strip()
        
        # 3. CALL YOUR HYBRID SEARCH SERVICE
        # This returns a SINGLE Workout object (via .first())
        workout = await search_workouts_filtered(
            query=query, 
            modality=modality, 
            focus=focus, 
            limit=1
        )
        
        # FIX: Check if workout exists, then use it directly (no [0])
        if workout:
            new_calendar[day_idx].update({
                "workout_id": workout.id,
                "title": workout.title,
                "modality": workout.modality,
                "focus": workout.focus,
                # Ensure this matches your Workout model field name (tss)
                "tss": getattr(workout, 'tss', 0) 
            })

    return {"calendar": new_calendar}
