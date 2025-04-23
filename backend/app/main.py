from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import trips, messages

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: 改成前端網址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trips.router, prefix="/api/trips", tags=["trips"])
app.include_router(messages.router, prefix="/api", tags=["messages"])
