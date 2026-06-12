from fastapi import APIRouter, Depends

from app.controllers.dashboard_controller import DashboardController
from app.middleware.auth_middleware import get_current_user_id


router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])
controller = DashboardController()


@router.get("/stats", summary="Get dashboard statistics for the authenticated user")
async def stats(user_id: str = Depends(get_current_user_id)):
    return await controller.stats(user_id)
