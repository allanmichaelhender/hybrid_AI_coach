from fastapi import APIRouter, Depends
from agents.nodes.graph import app as agent_app
from typing import List
from schemas.calendar import CalendarRequest, CalendarUpdateResponse  # 👈 NEW

router = APIRouter()


@router.post(
    "/suggest", response_model=CalendarUpdateResponse
)  # 👈 Add response validation
async def ai_suggest_plan(
    plan_data: CalendarRequest,  # 👈 Use strict Pydantic model instead of dict
):
    """
    The 'AI Suggest' endpoint.
    Pass a 7 or 14-day array, and the LangGraph Agent will fill the nulls.
    """
    # 1. Prepare the initial state for LangGraph
    # plan_data.model_dump() converts the Pydantic object to a clean dict for the Agent
    initial_state = plan_data.model_dump()
    if "ai_reasoning" not in initial_state:
        initial_state["ai_reasoning"] = []

    # 2. RUN THE AGENT (The 'Thinking' phase)
    final_state = await agent_app.ainvoke(initial_state)

    if final_state.get("ai_reasoning"):
        print("\n--- 🧠 AI COACH REASONING ---")
        print(final_state["ai_reasoning"][-1])
        print("-----------------------------\n")

    # 3. Return the updated calendar and the AI's 'thoughts'
    return {
        "updated_calendar": final_state["calendar"],
        "coach_reasoning": final_state["ai_reasoning"],
    }
