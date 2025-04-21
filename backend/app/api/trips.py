from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_trips():
    return [{"trip_name": "Test Munich Trip"}]
