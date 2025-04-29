from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import trips, messages, plan

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Update to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trips.router, prefix="/api/trips", tags=["trips"])
app.include_router(messages.router, prefix="/api", tags=["messages"])
app.include_router(plan.router, prefix="/api", tags=["plan"])
