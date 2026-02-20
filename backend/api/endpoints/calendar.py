from fastapi import APIRouter, Depends
from agents.nodes.graph import app as agent_app
from schemas.workout import HybridWorkoutRead # For response validation
from typing import List, Any
import uuid

router = APIRouter()

@router.post("/suggest")
async def ai_suggest_plan(
    # We use a dict here for the test, but later we'll use a strict Pydantic model
    plan_data: dict 
):
    """
    The 'AI Suggest' endpoint. 
    Pass a 7 or 14-day array, and the LangGraph Agent will fill the nulls.
    """
    # 1. Prepare the initial state for LangGraph
    initial_state = {
        "calendar": plan_data.get("calendar", []),
        "cycle_length": plan_data.get("cycle_length", 7),
        "user_goal": plan_data.get("user_goal", "Maintain fitness"),
        "request_scope": plan_data.get("request_scope", "bulk"),
        "ai_reasoning": []
    }

    # 2. RUN THE AGENT (The 'Thinking' phase)
    final_state = await agent_app.ainvoke(initial_state)

    # 3. Return the updated calendar and the AI's 'thoughts'
    return {
        "updated_calendar": final_state["calendar"],
        "coach_reasoning": final_state["ai_reasoning"]
    }
