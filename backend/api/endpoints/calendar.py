from fastapi import APIRouter, Depends, status, HTTPException
from agents.nodes.graph import app as agent_app
from schemas.calendar import CalendarRequest, CalendarUpdateResponse, SavePlanResponse
from models.plan import UserPlan
from schemas.calendar import SavePlanRequest
from deps import get_current_user, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select, desc

router = APIRouter()

# Our suggest endpoint to read in user input and current state to create the workout plan
@router.post("/suggest", response_model=CalendarUpdateResponse)
async def ai_suggest_plan(plan_data: CalendarRequest):

    # 1. Prepare the initial state for LangGraph, model_dump converts the Pydantic object into a regular dictionary
    initial_state = plan_data.model_dump()
    if "ai_reasoning" not in initial_state:
        initial_state["ai_reasoning"] = ""

    # 2. Run the agent
    final_state = await agent_app.ainvoke(initial_state)

    # 3. Return the updated calendar and the reasoning paragraph
    return {
        "updated_calendar": final_state["calendar"],
        "coach_reasoning": final_state["ai_reasoning"],
    }


# Endpoint for saving a user plan
@router.post("/save", status_code=status.HTTP_201_CREATED)
async def save_user_plan(
    saved_plan: SavePlanRequest,
    # Depends is a fastapi function which calls the arguement function, checks all is working and sends over the return value to be used in our function, Depends also performs a cleanup phase after the response is returned, in this case closing the db connection
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):

    try:
        # Convert Pydantic list of objects to a raw list of dicts for JSONB storage
        calendar_json = [
            day.model_dump(mode="json") for day in saved_plan.calendar_data
        ]

        # Creating our SQL Alchemy model object ready to be saved in the db
        new_plan = UserPlan(
            user_id=UUID(str(current_user.id)),
            plan_name=saved_plan.plan_name,
            user_goal=saved_plan.user_goal,
            calendar_data=calendar_json,
            coach_reasoning=saved_plan.coach_reasoning,
        )

        # Staging our new object
        db.add(new_plan)

        # Commit tp the datenase
        await db.commit()

        # Making sure any new fields added by the db are added onto our new_plan object, like id
        await db.refresh(new_plan)

        return {
            "status": "success",
            "message": "Plan synced to database",
            "plan_id": str(new_plan.id),
        }
    except Exception as e:
        # Rolls back to state when the session was opened in the case of an error
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database sync failed: {str(e)}",
        )


# Endpoint for retrieving a user's latest submission


# We specify the return value can be none
@router.get("/latest", response_model=SavePlanResponse | None)
async def get_latest_plan(
    db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    # Constructing the db query
    query = (
        select(UserPlan)
        .where(UserPlan.user_id == current_user.id)
        .order_by(desc(UserPlan.created_at))
        .limit(1)
    )

    # Execute query
    result = await db.execute(query)

    # Return the first result (or None), scalar_one_or_none changes the result object to a single UserPlan object, FastAPI returns the fields that match our response model
    return result.scalar_one_or_none()
