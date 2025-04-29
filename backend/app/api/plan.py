from fastapi import APIRouter
from app.agents.trip_planner_autogen import create_trip_plan
from datetime import datetime

router = APIRouter()

@router.post("/plan")
async def generate_trip_plan():
    user_input = ("I want to visit Munich for three days, "
                  "I like coffee shops and outdoor activities, "
                  "medium budget, prefer walking over taking transportation")
    plan = create_trip_plan(user_input, start_date=datetime(2025, 5, 2))
    return plan

# from pydantic import BaseModel
# from fastapi import APIRouter
# from app.agents.trip_planner_autogen import create_trip_plan
# from datetime import datetime

# router = APIRouter()

# class PlanRequest(BaseModel):
#     user_input: str
#     start_date: str  # yyyy-mm-dd

# @router.post("/plan")
# async def generate_trip_plan(request: PlanRequest):
#     start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
#     plan = create_trip_plan(request.user_input, start_date=start_date)
#     return plan
