from typing import Dict

from fastapi import UploadFile

from app.services.prediction_service import PredictionService
from app.utils.response_handler import success_response


class PredictionController:
    def __init__(self) -> None:
        self.service = PredictionService()

    async def predict(self, user_id: str, file: UploadFile) -> Dict:
        return success_response(await self.service.predict(user_id, file), "Prediction completed successfully")

    async def history(self, user_id: str, limit: int, skip: int) -> Dict:
        return success_response(await self.service.history(user_id, limit, skip), "Prediction history fetched successfully")

    async def get_prediction(self, prediction_id: str, user_id: str) -> Dict:
        return success_response(await self.service.get_prediction(prediction_id, user_id), "Prediction fetched successfully")

    async def delete_prediction(self, prediction_id: str, user_id: str) -> Dict:
        await self.service.delete_prediction(prediction_id, user_id)
        return success_response(message="Prediction deleted successfully")
