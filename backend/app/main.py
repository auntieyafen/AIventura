from fastapi import FastAPI
from app.api import trips

app = FastAPI()

app.include_router(trips.router, prefix="/api/trips", tags=["trips"])




