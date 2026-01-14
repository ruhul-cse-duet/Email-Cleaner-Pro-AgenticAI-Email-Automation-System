from fastapi import APIRouter

from app.services.stats_service import StatsService

router = APIRouter()


@router.get("/stats")
def get_stats() -> dict:
    return StatsService().get_stats()
