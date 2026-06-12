from typing import Dict

from app.services.dashboard_service import DashboardService
from app.utils.response_handler import success_response


class DashboardController:
    def __init__(self) -> None:
        self.service = DashboardService()

    async def stats(self, user_id: str) -> Dict:
        return success_response(await self.service.stats(user_id), "Dashboard stats fetched successfully")
