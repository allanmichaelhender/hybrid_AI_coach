from fastapi import APIRouter, Depends, status, HTTPException
from agents.nodes.graph import app as agent_app
from typing import List, Optional
from schemas.calendar import CalendarRequest, CalendarUpdateResponse, SavePlanResponse  # 👈 NEW
from models.plan import UserPlan
from schemas.calendar import SavePlanRequest
from deps import get_current_user, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select, desc


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


@router.post("/save", status_code=status.HTTP_201_CREATED)
async def save_user_plan(
    plan_in: SavePlanRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user) # 👈 Protection
):
    """
    Persist a 14-day AI plan to Neon.
    The user_id is automatically pulled from the JWT.
    """


    try:
        # Convert Pydantic list of objects to a raw list of dicts for JSONB storage
        calendar_json = [day.model_dump(mode='json') for day in plan_in.calendar_data]
        
      


        new_plan = UserPlan(
            user_id=UUID(str(current_user.id)),
            plan_name=plan_in.plan_name,
            user_goal=plan_in.user_goal,
            calendar_data=calendar_json, # 🧠 Stored as high-performance JSONB
            coach_reasoning=plan_in.coach_reasoning
        )

        print("test")


        print(f"DEBUG: Saving plan for User ID: {current_user.id} (Type: {type(current_user.id)})")
        print(f"DEBUG: Calendar Data Length: {len(calendar_json)}")
        # Check the first day to see if it's clean JSON
        print(f"DEBUG: Sample Day 0: {calendar_json[0]}") 

        db.add(new_plan)
        await db.commit()
        await db.refresh(new_plan)

        return {
            "status": "success", 
            "message": "Plan synced to Neon Cloud",
            "plan_id": str(new_plan.id)
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database sync failed: {str(e)}"
        )
    

@router.get("/latest", response_model=Optional[SavePlanResponse])
async def get_latest_plan(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Fetch the most recently saved 14-day block for the user.
    """
    # 1. Construct the query
    query = (
        select(UserPlan)
        .where(UserPlan.user_id == current_user.id)
        .order_by(desc(UserPlan.created_at)) # 👈 Sort by newest
        .limit(1)
    )
    
    # 2. Execute
    result = await db.execute(query)
    
    # 3. Return the first result (or None)
    return result.scalar_one_or_none()