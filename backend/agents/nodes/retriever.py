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
    last_thought = state["ai_reasoning"][-1]
    
    # 2. Regex to find the pattern [DAY]: MODALITY | FOCUS | QUERY
    # Example: [2]: Swimming | Aerobic Low | Easy drills
    pattern = r"\[(\d+)\]:\s*([^|]+)\|\s*([^|]+)\|\s*(.*)"
    matches = re.findall(pattern, last_thought)
    
    new_calendar = state["calendar"].copy()
    
    for match in matches:
        day_idx = int(match[0])
        modality = match[1].strip()
        focus = match[2].strip()
        query = match[3].strip()
        
        # 3. CALL YOUR HYBRID SEARCH SERVICE
        # This hits pgvector + Postgres filters
        results = await search_workouts_filtered(
            query=query, 
            modality=modality, 
            focus=focus, 
            limit=1
        )
        
        if results:
            workout = results[0]
            # 4. Update the 'State' with the real Database object
            new_calendar[day_idx].update({
                "workout_id": workout.id,
                "title": workout.title,
                "modality": workout.modality,
                "focus": workout.focus,
                "tss": workout.calculated_tss
            })

    return {"calendar": new_calendar}
